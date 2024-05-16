from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.controller import ChatController



chatController = ChatController()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"]
)



app.include_router(chatController.chat, prefix='/v1')