from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import verify_token

bearer_scheme = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> int:
    """JWT 驗證 dependency，回傳 user_id。"""
    payload = verify_token(credentials.credentials, token_type="access")
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return user_id
