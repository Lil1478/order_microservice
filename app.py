import os

import uvicorn
from fastapi import FastAPI
from order_module import order_controller
from database import SessionLocal, Base, engine

app = FastAPI()
app.include_router(order_controller.router)

db = SessionLocal()

if __name__ == '__main__':
    # init_account_module()
    # server_port = os.environ.get('PORT', '8080')
    uvicorn.run(app, port=8081)
