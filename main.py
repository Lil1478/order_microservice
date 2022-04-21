import uvicorn
from fastapi import FastAPI
from order_module import order_controller

# from database import SessionLocal

app = FastAPI()
app.include_router(order_controller.router)

# db = SessionLocal()

if __name__ == '__main__':
    uvicorn.run(app, port=5000)
