from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from chainlit.auth import create_jwt
from chainlit.user import User
from chainlit.utils import mount_chainlit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/custom-auth")
async def custom_auth():
    # TODO SSO 验签 防 token 盗用
    token = create_jwt(User(identifier="Test User"))
    return JSONResponse({"token": token})


mount_chainlit(app=app, target="cl_app.py", path="/chat")
