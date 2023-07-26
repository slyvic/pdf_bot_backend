from fastapi import APIRouter
from internal import chat
from pydantic import BaseModel
router = APIRouter()
class Context(BaseModel):
    text: str | None = None

@router.post('/upload')
async def index (data: Context):
  return {
    'msg': chat.extract_info(data.text)
  }

@router.post('/chat')
async def index (data: Context):
  return {
    'msg': chat.chat(data.text)
  }