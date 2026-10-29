from sqlalchemy import func
from fastapi.templating import Jinja2Templates
from app.models.api_history import APIHistory

templates=Jinja2Templates(directory='templates')
def stats_page(request,db):
    total=db.query(APIHistory).count(); success=db.query(APIHistory).filter(APIHistory.status_code.between(200,299)).count(); failed=db.query(APIHistory).filter(APIHistory.status_code.between(400,599)).count(); avg=db.query(func.avg(APIHistory.response_time)).scalar() or 0
    return templates.TemplateResponse(request=request,name='stats/dashboard_stats.html',context={'request':request,'user':request.session.get('user_name'),'total':total,'success':success,'failed':failed,'avg_time':round(avg,2)})
