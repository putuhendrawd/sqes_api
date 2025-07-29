# src/auth/dependencies.py
import logging
from datetime import datetime
from functools import lru_cache
from typing import Annotated, Dict, List, Optional
import pytz
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth, firestore
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError, UserDisabledError
from firebase_admin.exceptions import FirebaseError
from src.auth.schemas import FirebaseUser
from src.core.config import settings # Import the centralized settings

# --- Module-level logger ---
# Inherits configuration from main.py, so no basicConfig here.
logger = logging.getLogger(__name__)

# --- Reusable Security Scheme ---
bearer_scheme = HTTPBearer()

# --- Scope Definitions ---
# This is a good way to centralize scope definitions.
API_SCOPES = {
    "metadata:read": "Allows reading station metadata.",
    "metadata:write": "Allows writing/modifying station metadata.",
    "qc:read": "Allows reading Quality Control (QC) results.",
    "qc:write": "Allows writing/modifying Quality Control (QC) results.",
    "admin": "Grants full administrative access."
}

# --- Helper Functions for Cleaner Logic ---

def _create_debug_user() -> FirebaseUser:
    """Creates a mock admin user for development bypass. Controlled by settings."""
    logger.warning("!!! SECURITY WARNING: Using DEBUG_BYPASS_TOKEN !!!")
    return FirebaseUser(
        uid="debug_user_id",
        id="debug_user_id",
        email="debug@sqes.com",
        email_verified=True,
        display_name="Debug User",
        photo_url="",
        profilePicture="",
        disabled=False,
        role="user",
        username="debuguser",
        createdAt=datetime.now(pytz.utc), 
        updatedAt=datetime.now(pytz.utc), 
        is_admin=False,
        scopes=[scope for scope in API_SCOPES.keys() if scope != "admin"]
    )

@lru_cache(maxsize=128) # Cache Firestore lookups to reduce latency
def _get_user_details_from_firestore(uid: str) -> Dict:
    """Fetches and returns user data from the Firestore 'Users' collection."""
    try:
        db = firestore.client()
        user_doc_ref = db.collection('Users').document(uid)
        user_doc = user_doc_ref.get()

        if user_doc.exists:
            logger.debug(f"Fetched user details from Firestore for UID: {uid}")
            return user_doc.to_dict()
        else:
            logger.warning(f"Firestore document for user UID {uid} not found.")
            return {}
    except Exception as e:
        logger.error(f"Error fetching user details from Firestore for UID {uid}: {e}", exc_info=True)
        return {} # Return empty dict on error to prevent auth failure

def _determine_scopes_from_role(role: str) -> List[str]:
    """Determines the list of allowed scopes based on a user's role."""
    if role == "admin":
        return list(API_SCOPES.keys())
    if role == "manager":
        return ["metadata:read", "metadata:write", "qc:read", "qc:write"]
    if role == "user":
        return ["metadata:read", "qc:read"]
    return []


async def get_current_firebase_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]
) -> FirebaseUser:
    """
    Dependency to verify Firebase ID token and return a user model.
    Handles token verification, debug bypass, and enriching user data from Firestore.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials

    # --- Secure Debug Bypass Logic ---
    # This logic is now controlled by your environment settings.
    if settings.ENABLE_DEBUG_BYPASS_TOKEN and token == settings.DEBUG_BYPASS_TOKEN:
        return _create_debug_user()

    try:
        # 1. Verify the Firebase ID token
        logger.debug("Verifying Firebase ID token...")
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        logger.info(f"Successfully verified token for UID: {uid}")

        # 2. Get additional user details from Firestore (cached)
        firestore_data = _get_user_details_from_firestore(uid)

        # 3. Consolidate user role (custom token claim takes precedence)
        role = decoded_token.get('role') or firestore_data.get('role', 'user')

        # 4. Determine scopes based on the final role
        scopes = _determine_scopes_from_role(role)

        # 5. Construct the user model
        return FirebaseUser(
            uid=uid,
            email=decoded_token.get('email'),
            email_verified=decoded_token.get('email_verified', False),
            display_name=decoded_token.get('name'),
            photo_url=decoded_token.get('picture'),
            role=role,
            username=firestore_data.get('username') or decoded_token.get('username'),
            is_admin=(role == "admin"),
            scopes=scopes
        )

    except (InvalidIdTokenError, ExpiredIdTokenError, UserDisabledError) as e:
        error_map = {
            InvalidIdTokenError: ("invalid_token", "Invalid authentication token."),
            ExpiredIdTokenError: ("token_expired", "Authentication token has expired."),
            UserDisabledError: ("user_disabled", "User account has been disabled."),
        }
        error_code, detail = error_map.get(type(e), ("auth_error", "Firebase authentication failed."))
        logger.warning(f"Authentication failed: {detail} (Code: {error_code})")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": f"Bearer error=\"{error_code}\""},
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during user authentication: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred during authentication.",
        )


def require_scopes(required_scopes: List[str]):
    """
    A dependency factory that creates a dependency to check for required scopes.
    """
    def scope_checker(
        current_user: Annotated[FirebaseUser, Depends(get_current_firebase_user)]
    ) -> FirebaseUser:
        
        user_scopes = set(current_user.scopes)
        for scope in required_scopes:
            if scope not in user_scopes:
                logger.warning(f"Permission denied for user {current_user.uid}. Missing scope: {scope}.")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions. Requires scope: '{scope}'.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        logger.debug(f"Permission granted for user {current_user.uid} for scopes: {required_scopes}")
        return current_user

    return Depends(scope_checker)


# --- Pre-configured Dependencies for Common Use Cases ---
# Using the factory to create specific dependencies makes your endpoint code cleaner.
admin_required = require_scopes(["admin"])
metadata_write_required = require_scopes(["metadata:write"])
metadata_read_required = require_scopes(["metadata:read"])
qc_read_required = require_scopes(["qc:read"])
qc_write_required = require_scopes(["qc:write"])
