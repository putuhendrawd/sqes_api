# src/auth/routing.py
import logging # Import the standard logging library
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional # Keep Optional for BaseModel fields
from pydantic import BaseModel, EmailStr # Keep BaseModel and EmailStr
from firebase_admin import auth # Keep Firebase Admin Auth

# Import your custom dependencies and schemas
from src.auth.dependencies import get_current_firebase_user, admin_required
from src.auth.schemas import FirebaseUser 

# --- Logging Configuration ---
# It's generally best practice to configure logging once in your main.py or a dedicated config module.
# If this is the *only* place you're setting basicConfig, it's fine.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # Get a logger instance for this module

# Create an API router for authentication-related endpoints
router = APIRouter(tags=["Authentication"])


@router.get(
    "/me",
    response_model=FirebaseUser,
    summary="Get Current Authenticated User Info",
    description="Retrieves the profile information of the currently authenticated Firebase user. "
                "Requires a valid Firebase ID Token in the 'Authorization: Bearer' header."
)
async def read_current_user(
    current_user: Annotated[FirebaseUser, Depends(get_current_firebase_user)]
):
    """
    Endpoint to get details of the authenticated Firebase user.

    Args:
        current_user (FirebaseUser): The authenticated user object, provided by the
                                      `get_current_firebase_user` dependency.

    Returns:
        FirebaseUser: The profile information of the authenticated user.
    """
    # This log is good for production to track access to this sensitive endpoint
    logger.info(f"Accessed /api/auth/me. User UID: {current_user.uid}, Role: {current_user.role}, Email: {current_user.email}")
    return current_user

# Pydantic model for setting a user's role
class SetUserRoleRequest(BaseModel):
    uid: Optional[str] = None
    email: Optional[EmailStr] = None
    role: str 

    def check_identifier(self):
        if not self.uid and not self.email:
            raise ValueError("Either UID or email must be provided.")
        return self

# Endpoint to set a user's role custom claim
@router.post("/set-user-role", status_code=status.HTTP_200_OK)
async def set_user_role(
    request: SetUserRoleRequest,
    admin_user: Annotated[FirebaseUser, admin_required]
):
    """
    Sets the 'role' custom claim for a user identified by UID or email.
    Requires an authenticated admin user to call this endpoint.
    """
    request.check_identifier()

    try:
        user_id_to_update = None
        if request.uid:
            user_id_to_update = request.uid
        elif request.email:
            user_record = auth.get_user_by_email(request.email)
            user_id_to_update = user_record.uid
        
        current_claims = auth.get_user(user_id_to_update).custom_claims or {}
        new_claims = {**current_claims, "role": request.role}

        auth.set_custom_user_claims(user_id_to_update, new_claims)
        
        # Log success for auditing purposes
        logger.info(f"Role set to '{request.role}' for user {user_id_to_update} by admin {admin_user.uid} ({admin_user.email}).")
        return {"message": f"Role updated to '{request.role}' for user {user_id_to_update}. User needs to re-authenticate to get the new ID token."}
    
    except auth.UserNotFoundError:
        # Log a warning if the target user doesn't exist
        logger.warning(f"Attempted to set role for non-existent user: {request.uid or request.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found for the provided UID or email."
        )
    except Exception as e:
        # Log errors with traceback for debugging in production logs
        logger.error(f"Error setting user role for {request.uid or request.email}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to set user role: An unexpected server error occurred." # Generic message for client
        )