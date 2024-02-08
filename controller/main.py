
from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from config import models
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from config.models import db_dependency
 
templates = Jinja2Templates(directory="templates")
 
app = FastAPI()
 
app.mount("/static", StaticFiles(directory="static"), name="static")
 
 
@app.get("/")
async def index(request: Request, db:db_dependency):
    users = db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "users": users})
 
@app.post("/add")
async def add(db:db_dependency,
              request: Request, 
              name: str = Form(...),
              email: str = Form(...),
              mobile: str = Form(...),
              age: str = Form(...)):
  
    users = models.User(name=name, email=email, mobile=mobile,age=age)
    db.add(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("index"), status_code=status.HTTP_303_SEE_OTHER)
 
@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})
 
@app.get("/edit/{user_id}")
async def edit(db:db_dependency,request: Request, user_id: int,):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})
 
@app.post("/update/{user_id}")
async def update(db:db_dependency, request: Request,
                 user_id: int, 
                 name: str = Form(...),
                 email: str = Form(...), 
                 mobile: str = Form(...),
                 age: str = Form(...)):
    
    users = db.query(models.User).filter(models.User.id == user_id).first()
    users.name = name
    users.mobile = mobile
    users.age = age
    db.commit()
    return RedirectResponse(url=app.url_path_for("index"), status_code=status.HTTP_303_SEE_OTHER)
 
@app.get("/delete/{user_id}")
async def delete(db:db_dependency,request: Request, user_id: int):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("index"), status_code=status.HTTP_303_SEE_OTHER)