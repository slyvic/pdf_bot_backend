from http.client import HTTPException

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from internal import chat
from internal import auth
from core.database import get_db
from sqlalchemy.orm import Session

from util.token_management import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

router = APIRouter()

class Context(BaseModel):
  text: str | None = None

class User(BaseModel):
  id: int = -1
  name: str | None = None
  email: str | None = None
  password: str | None = None
  token: str | None = None

@router.post('/create-user')
async def index (db: Session = Depends(get_db), data: User = None):
  return auth.create_user(db, data)
@router.post('/login')
async def index (db: Session = Depends(get_db), data: User = None):
  return auth.login(db, data)

@router.post('/upload')
async def index (data: Context, token: str = Depends(oauth2_scheme)):
  payload = decode_token(token)
  if payload is None:
      raise HTTPException(status_code=401, detail="Invalid token")
  return {
    'msg': chat.extract_info(data.text)
  }

@router.post('/chat')
async def index (data: Context, payload: dict = Depends(decode_token)):
  return {
    'msg': chat.chat(data.text)
  }