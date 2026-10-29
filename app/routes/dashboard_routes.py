from fastapi import APIRouter,Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
router=APIRouter(); templates=Jinja2Templates(directory='templates')
@router.get('/dashboard')
def dashboard(request:Request):
    if 'user_id' not in request.session:return RedirectResponse('/login',303)
    return templates.TemplateResponse(request=request,name='dashboard/dashboard.html',context={'request':request,'user':request.session['user_name']})
