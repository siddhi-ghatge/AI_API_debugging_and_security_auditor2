# ============================================================
# SECURITY CONTROLLER
# AI API DEBUGING AND SECURITY AUDITOR
# ============================================================

import json

from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# SECURITY HEADER DESCRIPTIONS
# ============================================================

DESCRIPTIONS = {

    "content-security-policy":
        "Controls which resources browsers can load.",

    "strict-transport-security":
        "Instructs browsers to use HTTPS for future requests.",

    "x-frame-options":
        "Controls whether the response can be displayed in a frame.",

    "x-content-type-options":
        "Helps prevent MIME-type sniffing.",

    "referrer-policy":
        "Controls how referrer information is sent.",

    "permissions-policy":
        "Controls access to selected browser features."
}


# ============================================================
# ALL SECURITY HEADERS
# ============================================================

ALL = list(DESCRIPTIONS.keys())


# ============================================================
# SECURITY PAGE
# ============================================================

def security_page(request, history):

    # --------------------------------------------------------
    # SESSION CHECK
    # --------------------------------------------------------

    user_id = request.session.get("user_id")

    if not user_id:

        return RedirectResponse(
            url="/login",
            status_code=303
        )

    # --------------------------------------------------------
    # CHECK HISTORY
    # --------------------------------------------------------

    if history is None:

        return RedirectResponse(
            url="/dashboard",
            status_code=303
        )

    # --------------------------------------------------------
    # PRESENT SECURITY HEADERS
    # --------------------------------------------------------

    try:

        present_data = history.present_security_headers or "[]"

        present = [
            str(x).lower().strip()
            for x in json.loads(present_data)
        ]

    except (json.JSONDecodeError, TypeError, AttributeError):

        present = []


    # --------------------------------------------------------
    # MISSING SECURITY HEADERS
    # --------------------------------------------------------

    try:

        missing_data = history.missing_security_headers or "[]"

        missing = [
            str(x).lower().strip()
            for x in json.loads(missing_data)
        ]

    except (json.JSONDecodeError, TypeError, AttributeError):

        missing = []


    # --------------------------------------------------------
    # CREATE SECURITY HEADER ROWS
    # --------------------------------------------------------

    rows = []

    for header in ALL:

        rows.append({

            "name": header,

            "present": header in present,

            "missing": header in missing,

            "description": DESCRIPTIONS[header]
        })


    # --------------------------------------------------------
    # SECURITY SCORE
    # --------------------------------------------------------

    security_score = (
        history.security_score
        if history.security_score is not None
        else 0
    )


    # --------------------------------------------------------
    # MISSING HEADER PERCENTAGE
    # --------------------------------------------------------

    missing_percentage = (
        history.missing_header_percentage
        if history.missing_header_percentage is not None
        else 0
    )


    # --------------------------------------------------------
    # TEMPLATE CONTEXT
    # --------------------------------------------------------

    context = {

        "request": request,

        "user": request.session.get(
            "user_name",
            "User"
        ),

        "user_id": user_id,

        "history": history,

        "security_headers": rows,

        "security_score": security_score,

        "missing_percentage": missing_percentage,

        "present_headers": present,
        "missing_headers": missing
    }
    return templates.TemplateResponse(
        request=request,
        name="security.html",
        context=context
    )