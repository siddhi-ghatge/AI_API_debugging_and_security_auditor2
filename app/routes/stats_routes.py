from fastapi import APIRouter,Request,Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.controllers.stats_controller import stats_page
router=APIRouter()
@router.get('/statistics')
def statistics(request:Request,db:Session=Depends(get_db)): return stats_page(request,db)
