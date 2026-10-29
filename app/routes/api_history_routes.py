from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.api_history import APIHistory
router=APIRouter(); templates=Jinja2Templates(directory='templates')
@router.get('/history')
def history_page(request:Request,db:Session=Depends(get_db)):
    if 'user_id' not in request.session:return {'error':'Login required'}
    return templates.TemplateResponse(request=request,name='api_history.html',context={'request':request,'history':db.query(APIHistory).order_by(APIHistory.id.desc()).all(),'user':request.session.get('user_name')})
