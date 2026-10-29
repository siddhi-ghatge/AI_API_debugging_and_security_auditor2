# ============================================================
# AI API DEBUGING AND SECURITY AUDITOR
# Main Application File
# ============================================================

from os import getenv

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse


# ============================================================
# DATABASE
# ============================================================

from app.database.database import engine, Base

from app.models.user import User
from app.models.api_history import APIHistory


# ============================================================
# ROUTES
# ============================================================

from app.routes.auth_routes import router as auth_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.api_routes import router as api_router
from app.routes.stats_routes import router as stats_router
from app.routes.debug_routes import router as debug_router
from app.routes.analysis_routes import router as analysis_router
from app.routes.security_routes import router as security_router
from app.routes.vulnerability_routes import router as vulnerability_router
from app.routes.api_history_routes import router as history_router


# ============================================================
# DATABASE TABLE CREATION
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI API DEBUGING AND SECURITY AUDITOR",
    description="AI based API debugging and security auditing system",
    version="1.0"
)


# ============================================================
# SESSION CONFIGURATION
# ============================================================

SESSION_SECRET_KEY = getenv(
    "SESSION_SECRET_KEY",
    "dev-session-secret-change-this-key-123456789"
)

SESSION_HTTPS_ONLY = (
    getenv(
        "SESSION_HTTPS_ONLY",
        "false"
    ).lower() == "true"
)


# ============================================================
# SESSION MIDDLEWARE
# ============================================================

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
    max_age=60 * 60 * 8,
    same_site="lax",
    https_only=SESSION_HTTPS_ONLY
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)

app.include_router(dashboard_router)

app.include_router(api_router)

app.include_router(stats_router)

app.include_router(debug_router)

app.include_router(analysis_router)

app.include_router(security_router)

app.include_router(vulnerability_router)

app.include_router(history_router)


# ============================================================
# HOME PAGE
# ============================================================

@app.get("/")
async def home(request: Request):

    user_id = request.session.get("user_id")

    if user_id:

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    return RedirectResponse(
        url="/login",
        status_code=303
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "application": "AI API DEBUGING AND SECURITY AUDITOR",
        "version": "1.0"
    }


# ============================================================
# SESSION TEST
# ============================================================

@app.get("/session-test")
async def session_test(request: Request):

    user_id = request.session.get("user_id")

    return {
        "session_available": True,
        "user_id": user_id,
        "logged_in": bool(user_id)
    }