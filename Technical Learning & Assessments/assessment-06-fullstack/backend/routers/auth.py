from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


# Q3 — POST /auth/register
#
# Q4 — authenticate_user(db, username, password)
#      POST /auth/token
#      GET  /auth/me
#
# See ASSESSMENT.md.
