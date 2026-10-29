from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from app.models.user import User
from datetime import datetime, timezone

templates = Jinja2Templates(directory='templates')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def register_page(request):
    if request.session.get('user_id'):
        return RedirectResponse('/dashboard', status_code=303)
    return templates.TemplateResponse(request=request, name='auth/register.html', context={'error': None, 'name': '', 'email': ''})

def register_user(request, name, email, password, db):
    name = name.strip(); email = email.strip().lower()
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse(request=request, name='auth/register.html', context={'error': 'This email is already registered. Please login.', 'name': name, 'email': email}, status_code=409)
    db.add(User(name=name, email=email, password=pwd_context.hash(password)))
    db.commit()
    return RedirectResponse('/login', status_code=303)

def login_page(request):
    if request.session.get('user_id'):
        return RedirectResponse('/dashboard', status_code=303)
    return templates.TemplateResponse(request=request, name='auth/login.html', context={'error': None, 'email': ''})

def login_user(request, email, password, db):
    email = email.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password):
        return templates.TemplateResponse(request=request, name='auth/login.html', context={'error': 'Invalid email or password.', 'email': email}, status_code=401)

    # Replace any old session with the authenticated user's session.
    request.session.clear()
    request.session.update({
        'user_id': user.id,
        'user_name': user.name,
        'user_email': user.email,
        'login_at': datetime.now(timezone.utc).isoformat()
    })
    return RedirectResponse('/dashboard', status_code=303)

def logout(request):
    request.session.clear()
    return RedirectResponse('/login', status_code=303)
