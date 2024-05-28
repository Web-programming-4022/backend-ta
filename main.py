from fastapi import FastAPI , Depends,HTTPException
from typing import Annotated, ClassVar,List
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models


app = FastAPI()

# Set up CORS
origins = [
    "http://localhost:*",
    "http://localhost:5173",
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username : str
    password : str

class UserModel(UserBase):
    pass
    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users")
async def getAllUsers(db : Session = Depends(get_db)):
    users = db.query(models.USER).all()
    return users


@app.post("/login")
async def login(user : UserBase, db: Session = Depends(get_db)):
    logged = db.query(models.USER).filter(models.USER.username == user.username).first()
    if logged:
         if(logged.password == user.password): 
            return  {
                    "message" : "با موفقیت وارد شدید",
                    "data" : logged
                    }
    return False

@app.post("/register")
async def register(user : UserBase ,  db: Session = Depends(get_db)):
    username = user.username
    isTaken = db.query(models.USER).filter(models.USER.username == username).first()
    db_users =  models.USER(**user.dict())
    db.add(db_users)
    db.commit()
    db.refresh(db_users)
    if(isTaken):
        raise HTTPException(status_code=404, detail="یوزر تکراری است..")
    return {
        "data" : db_users,
        "message" : "ثبت نام شما موفقیت آمیز بود."
    }

@app.delete("/user/{username}")
async def deleteUser(username : str , db: Session = Depends(get_db)):
    isLogged = db.query(models.USER).filter(models.USER.username == username).first()
    if not isLogged:
        raise HTTPException(status_code=404, detail="یوزر یافت نشد.")
    db.delete(isLogged)
    db.commit()
    return {"message": "یوزر با موفقیت حذف شد"}
    

    
