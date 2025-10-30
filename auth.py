import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict

# Public Key 읽기
with open('public.pem') as f:
    PUBLIC_KEY = f.read()

# HTTPBearer: Authorization 헤더에서 토큰 추출
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict:
    """
    JWT 토큰을 검증하고 사용자 정보를 반환합니다.
    
    Args:
        credentials: Authorization 헤더의 Bearer 토큰
    
    Returns:
        사용자 정보 (user_id)
    
    Raises:
        HTTPException: 토큰이 유효하지 않을 경우
    """
    token = credentials.credentials
    
    try:
        # Public Key로 토큰 검증
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"]  # RS256 알고리즘 명시
        )
        
        # 토큰에서 사용자 정보 추출
        return {
            "user_id": payload.get("user_id"),
            "username": payload.get("username"),
        }
    
    except jwt.ExpiredSignatureError as exc:
        # 토큰 만료
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다"
        ) from exc
    except jwt.InvalidTokenError as exc:
        # 토큰이 유효하지 않음
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다"
        ) from exc