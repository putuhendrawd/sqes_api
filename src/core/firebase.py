# src/core/firebase.py
import firebase_admin
from firebase_admin import credentials, auth
import os
import logging # Import logging

# Get a logger instance for this module
logger = logging.getLogger(__name__)

def initialize_firebase(service_account_key_path: str):
    """
    Initializes the Firebase Admin SDK.
    This function should be called once at application startup.

    Args:
        service_account_key_path (str): The file path to the Firebase service account key JSON.

    Raises:
        ValueError: If the service_account_key_path is not provided or empty.
        FileNotFoundError: If the service account key file does not exist at the given path.
        Exception: If Firebase Admin SDK initialization fails for any other reason.
    """
    if not service_account_key_path:
        logger.error("Firebase service account key path is missing. Firebase Admin SDK will not be initialized.")
        # Raising ValueError to explicitly prevent app startup if path is critical and missing
        raise ValueError("Firebase service account key path is required for initialization.")

    # Check if the file actually exists before attempting to load it
    if not os.path.exists(service_account_key_path):
        logger.error(f"Firebase service account key file not found at: '{service_account_key_path}'. Please verify the path in your configuration.")
        # Raising FileNotFoundError to explicitly prevent app startup if the file doesn't exist
        raise FileNotFoundError(f"Firebase service account key file not found: '{service_account_key_path}'.")

    # Check if Firebase app is already initialized to prevent re-initialization errors
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(service_account_key_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized successfully!")
        except Exception as e:
            # Use logger.exception to log the full traceback for critical errors
            logger.exception(f"Critical Error initializing Firebase Admin SDK: {e}")
            # Re-raise the exception to prevent the application from starting if initialization fails
            raise
    else:
        # This case is less common but handles redundant calls gracefully
        logger.info("Firebase Admin SDK already initialized. Skipping initialization.")