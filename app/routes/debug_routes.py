from fastapi import APIRouter,Request,Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.api_history import APIHistory
from app.controllers.debug_controller import debug_page
router=APIRouter()
@router.get('/debugging/{id}')
def debugging(request:Request,id:int,db:Session=Depends(get_db)):
    h=db.query(APIHistory).filter(APIHistory.id==id).first()
    if not h:return {'error':'API history not found'}
    return debug_page(request,h)
