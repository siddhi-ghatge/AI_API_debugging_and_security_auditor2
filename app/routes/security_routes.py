# ============================================================
# SECURITY ROUTES
# AI API DEBUGING AND SECURITY AUDITOR
# ============================================================

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.api_history import APIHistory
from app.controllers.security_controller import security_page


# ============================================================
# ROUTER
# ============================================================

router = APIRouter()


# ============================================================
# SECURITY ANALYSIS PAGE
# ============================================================

@router.get("/security/{history_id}")
def security(
    history_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Find API history
    # --------------------------------------------------------

    history = (
        db.query(APIHistory)
        .filter(APIHistory.id == history_id)
        .first()
    )


    # --------------------------------------------------------
    # History not found
    # --------------------------------------------------------

    if history is None:

        return {
            "error": "API history not found",
            "history_id": history_id
        }


    # --------------------------------------------------------
    # Show security analysis page
    # --------------------------------------------------------

    return security_page(
        request,
        history
    )