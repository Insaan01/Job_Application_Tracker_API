from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import SessionLocal
from app import models, schemas
from app.security import hash_password, verify_password, create_access_token, get_current_user
from app.ai_service import summarize_job_search, suggest_followups

app = FastAPI(title="Job Application Tracker")

VALID_STATUSES = {"APPLIED", "INTERVIEW", "TECHNICAL", "OFFER", "REJECTED"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_status(statuses):
    return max(statuses, key=lambda s: s.changed_at)

def prepare_app_data(apps):
    return [
        {
            "company": a.company,
            "role": a.role,
            "status": get_current_status(a.statuses).status,
            "updated": get_current_status(a.statuses).changed_at.isoformat()
        }
        for a in apps
    ]

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    db.add(models.User(email=user.email, hashed_password=hash_password(user.password)))
    db.commit()
    return {"message": "registered"}

@app.post("/login", response_model=schemas.Token)
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    u = db.query(models.User).filter_by(email=user.email).first()
    if not u or not verify_password(user.password, u.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token({"sub": str(u.id)}), "token_type": "bearer"}

@app.post("/applications", response_model=schemas.ApplicationResponse)
def create_application(app_data: schemas.ApplicationCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    app_obj = models.Application(company=app_data.company, role=app_data.role, user_id=user_id)
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    db.add(models.ApplicationStatusHistory(application_id=app_obj.id, status="APPLIED"))
    db.commit()
    return app_obj

@app.post("/applications/{application_id}/status")
def update_status(application_id: int, status_data: schemas.ApplicationStatusCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    if status_data.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid status")
    app_obj = db.query(models.Application).filter_by(id=application_id, user_id=user_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.add(models.ApplicationStatusHistory(application_id=application_id, status=status_data.status, note=status_data.note))
    db.commit()
    return {"message": "updated"}

@app.get("/applications")
def list_applications(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    apps = db.query(models.Application).filter_by(user_id=user_id).all()
    return [
        {
            "id": a.id,
            "company": a.company,
            "role": a.role,
            "current_status": get_current_status(a.statuses).status,
            "created_at": a.created_at
        }
        for a in apps
    ]

@app.get("/applications/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    a = db.query(models.Application).filter_by(id=application_id, user_id=user_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "id": a.id,
        "company": a.company,
        "role": a.role,
        "current_status": get_current_status(a.statuses).status,
        "history": [
            {"status": s.status, "note": s.note, "changed_at": s.changed_at}
            for s in a.statuses
        ]
    }

@app.get("/applications/stuck")
def stuck_applications(days: int = 14, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    threshold = datetime.utcnow() - timedelta(days=days)
    apps = db.query(models.Application).filter_by(user_id=user_id).all()
    return [
        {
            "company": a.company,
            "role": a.role,
            "status": get_current_status(a.statuses).status,
            "last_update": get_current_status(a.statuses).changed_at
        }
        for a in apps
        if get_current_status(a.statuses).changed_at < threshold
        and get_current_status(a.statuses).status not in {"REJECTED", "OFFER"}
    ]

@app.get("/ai/summary")
def ai_summary(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    apps = db.query(models.Application).filter_by(user_id=user_id).all()
    return {"summary": summarize_job_search(prepare_app_data(apps))}

@app.get("/ai/followups")
def ai_followups(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return {"suggestions": suggest_followups(stuck_applications(db=db, user_id=user_id))}

@app.get("/health")
def health():
    return {"status": "ok"}
