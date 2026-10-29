import json
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.services.api_service import analyze_api
from app.services.ai_service import analyze_with_ai
from app.models.api_history import APIHistory

templates=Jinja2Templates(directory='templates')
def analyzer_page(request):
    if 'user_id' not in request.session: return RedirectResponse('/login',status_code=303)
    return templates.TemplateResponse(request=request,name='api/analyzer.html',context={'request':request,'user':request.session.get('user_name'),'result':None,'ai_result':None})
def analyzer_result(request,url,method,db):
    if 'user_id' not in request.session: return RedirectResponse('/login',status_code=303)
    result=analyze_api(url,method)
    if 'error' in result:
        return templates.TemplateResponse(request=request,name='api/analyzer.html',context={'request':request,'user':request.session.get('user_name'),'result':result,'ai_result':None})
    ai=analyze_with_ai(result)
    history=APIHistory(api_url=url,method=method.upper(),status_code=result.get('status'),response_time=result.get('time'),content_type=result.get('content_type'),response_headers=json.dumps(result.get('headers',{})),response_body=json.dumps(result.get('body',{})),security_score=result.get('security_score',0),present_security_headers=json.dumps(result.get('present_security_headers',[])),missing_security_headers=json.dumps(result.get('missing_security_headers',[])),missing_header_percentage=result.get('missing_header_percentage',0),ai_recommendation=ai)
    db.add(history); db.commit(); db.refresh(history)
    return RedirectResponse(f'/analysis-dashboard/{history.id}',status_code=303)
