from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import LoginRequest, TokenResponse
from auth import verify_password, create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Branch or Head Office login.

    Request body:
        { "branch_code": "ZKP", "password": "1234" }

    Returns:
        JWT access token + user info
    """
    # 1. Find user by branch code
    user = db.query(User).filter(
        User.branch_code == request.branch_code.upper()
    ).first()

    # 2. Check user exists and password is correct
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid branch code or password"
        )

    # 3. Create JWT token with branch_code as subject
    token = create_access_token(data={"sub": user.branch_code})

    return TokenResponse(
        access_token=token,
        branch_code=user.branch_code,
        branch_name=user.branch_name,
        role=user.role,
        branch=user.branch
    )


@router.post("/logout")
def logout():
    """
    Logout endpoint.
    Since we use JWT (stateless tokens), logout is handled on the frontend
    by deleting the stored token. This endpoint just confirms the action.
    """
    return {"message": "Logged out successfully. Please delete your token."}
