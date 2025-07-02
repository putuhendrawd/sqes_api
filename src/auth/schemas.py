# src/auth/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime 

class FirebaseUser(BaseModel):
    """
    Represents a user authenticated via Firebase Authentication, combining standard claims
    from their ID token with additional profile information fetched from Firestore.

    Attributes:
        uid (str): The user's unique ID from Firebase, aliased from 'id' in Firestore.
        email (Optional[EmailStr]): The user's email address.
        email_verified (bool): Indicates if the user's email has been verified.
        display_name (Optional[str]): The user's display name from Firebase Auth.
        photo_url (Optional[str]): The URL to the user's profile picture from Firebase Auth (aliased from 'profilePicture' in Firestore).
        disabled (bool): Indicates if the user account is disabled.

        role (str): The user's role (e.g., 'admin', 'manager', 'user'), prioritized from custom claims in the ID token.
        username (str): The user's username, prioritized from custom claims in the ID token.

        createdAt (Optional[datetime]): Timestamp when the user record was created in Firestore.
        updatedAt (Optional[datetime]): Timestamp when the user record was last updated in Firestore.

        is_admin (bool): Derived flag; True if the user's role is 'admin'.
        scopes (List[str]): List of API access scopes granted to the user based on their role.
    """
    # Standard fields from Firebase ID token payload (some mapped with alias for clarity)
    uid: str = Field(..., alias="id", description="The user's unique ID from Firebase (maps to 'id' from Firestore).")
    email: Optional[EmailStr] = Field(None, description="The user's email address, if available from Firebase Auth.")
    email_verified: bool = Field(False, description="True if the user's email address has been verified by Firebase Auth.")
    display_name: Optional[str] = Field(None, description="The user's display name from Firebase Auth, if available.")
    photo_url: Optional[str] = Field(None, alias="profilePicture", description="The URL to the user's profile picture (maps to 'profilePicture' from Firestore).")
    disabled: bool = Field(False, description="True if the user account is disabled in Firebase Auth.")
    
    # Custom profile fields, primarily fetched from Firestore, or set as custom claims
    role: str = Field(..., description="The user's role (e.g., 'admin', 'manager', 'user'), prioritized from custom claims in the ID token.")
    username: str = Field(..., description="The user's unique username, prioritized from custom claims in the ID token.")
    
    # Timestamps for user record creation/update, typically from Firestore
    createdAt: Optional[datetime] = Field(None, description="Timestamp when the user record was created in Firestore.")
    updatedAt: Optional[datetime] = Field(None, description="Timestamp when the user record was last updated in Firestore.")

    # Authorization-specific fields, derived internally by the API
    is_admin: bool = Field(False, description="Derived: True if the user has administrative privileges (based on 'role').")
    scopes: List[str] = Field([], description="Derived: List of API scopes granted to the user based on their role.")

    class Config:
        populate_by_name = True
        from_attributes = True 
