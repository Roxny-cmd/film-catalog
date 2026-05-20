from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from core.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")