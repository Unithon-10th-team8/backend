from fastapi.routing import APIRouter
from app.views import user, contact, calendar


router = APIRouter()

router.include_router(user.router, tags=["User"])
router.include_router(contact.router, tags=["Contact"])
router.include_router(calendar.router, tags=["Calendar"])
