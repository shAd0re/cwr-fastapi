import uvicorn
from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users



app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8002)

