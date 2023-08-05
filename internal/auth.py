from passlib.context import CryptContext
from util.token_management import create_access_token
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

def verify_password (plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def get_user (db, email: str = ""):
  result = db.execute("SELECT * FROM user WHERE email='" + email + "'")
  return result.fetchone()


def create_user (db, user):
  temp_user = get_user(db, user.email)
  if temp_user:
    return {'code': 400, 'message': 'すでに使用中のメールです。'}
  hashed_password = pwd_context.hash(user.password)
  db.execute(
    'INSERT INTO user (name, email, password, token) VALUES ("' + user.name + '", "' + user.email + '", "' + hashed_password + '", "")')
  db.commit()
  return {'code': 200, 'message': 'ログイン成功。', 'user': user}


def login (db, user):
  temp_user = get_user(db, user.email)
  if not user or not verify_password(user.password, temp_user.password):
    return {'code': 400, 'message': 'ユーザーネームまたはパスワードが違います。'}
  access_token = create_access_token(data = {"sub": user.email})
  return {'code': 200, 'token': access_token, 'message': 'ログインに成功しました。'}
