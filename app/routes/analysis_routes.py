from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.api_history import APIHistory
router=APIRouter(); templates=Jinja2Templates(directory='templates')
@router.get('/analysis-dashboard/{id}')
def analysis_dashboard(request:Request,id:int,db:Session=Depends(get_db)):
    h=db.query(APIHistory).filter(APIHistory.id==id).first()
    if not h:return templates.TemplateResponse(request=request,name='error.html',context={'message':'API history not found'},status_code=404)
    return templates.TemplateResponse(request=request,name='analysis_dashboard.html',context={'request':request,'history':h,'ai_result':h.ai_recommendation})
