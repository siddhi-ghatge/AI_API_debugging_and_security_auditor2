from fastapi import APIRouter,Request,Form,Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers.api_controller import analyzer_page,analyzer_result
router=APIRouter()
@router.get('/api-analyzer')
def api_page(request:Request): return analyzer_page(request)
@router.post('/api-analyzer')
def analyze(request:Request,url:str=Form(...),method:str=Form(...),db:Session=Depends(get_db)): return analyzer_result(request,url,method,db)
