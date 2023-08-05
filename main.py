from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import api
from util.class_object import singleton
from core.config import configs

@singleton
class AppCreator:
    def __init__(self):
        # set app default
        self.app = FastAPI()
        # set cors
        if configs.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=["http://localhost:3000"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        # set routes
        @self.app.get("/")
        def root():
            return "service is working"

        self.app.include_router(api.router, prefix=configs.API_V1_STR)


app_creator = AppCreator()
app = app_creator.app