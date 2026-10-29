from fastapi import APIRouter, Request, Form, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers.auth_controller import register_page,register_user,login_page,login_user,logout
router=APIRouter()
@router.get('/register')
def show_register(request:Request): return register_page(request)
@router.post('/register')
def create_user(request:Request,name:str=Form(...),email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)): return register_user(request,name,email,password,db)
@router.get('/login')
def show_login(request:Request): return login_page(request)
@router.post('/login')
def login(request:Request,email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)): return login_user(request,email,password,db)
@router.get('/logout')
def logout_user(request:Request): return logout(request)
