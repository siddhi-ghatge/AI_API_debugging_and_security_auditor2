import json
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates(directory='templates')
def debug_page(request,history):
    try: body=json.dumps(json.loads(history.response_body or 'null'),indent=4)
    except Exception: body=history.response_body or ''
    try: headers=json.dumps(json.loads(history.response_headers or '{}'),indent=4)
    except Exception: headers=history.response_headers or ''
    debugging=[]
    if history.status_code == 200: debugging.append({'issue':'Success','message':'API is working correctly.'})
    elif history.status_code == 404: debugging.append({'issue':'404 Not Found','message':'Check API URL.'})
    elif history.status_code and history.status_code >= 500: debugging.append({'issue':'Server Error','message':'Internal server error.'})
    if history.response_time and history.response_time > 1000: debugging.append({'issue':'Slow Response','message':'API response is slow.'})
    return templates.TemplateResponse(request=request,name='debugging.html',context={'request':request,'history':history,'response_body':body,'response_headers':headers,'debugging':debugging})
