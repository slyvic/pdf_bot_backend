from fastapi import APIRouter
from internal import chat

router = APIRouter()
@router.get("/test/{message}")
def read_root (message):
  return chat.chat(message)
