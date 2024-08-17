import hashlib
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URL(BaseModel):
    key: str
    url: str


class Req(BaseModel):
    url: str


@app.post("/")
def shorten_URL(req: Req, request: Request, db: Session = Depends(get_db)):
    print(len(req.url))
    if len(req.url) >= 1:
        url = req.url
        res = db.query(models.URLs).filter(models.URLs.url == url).first()
        if res:
            return {
                "key": res.key,
                "long_url": req.url,
                "short_url": f'{request.base_url}{res.key}'
            }

        key = hashlib.sha1(req.url.encode("UTF-8")).hexdigest()
        repeated = db.query(models.URLs).filter(models.URLs.key == key).first()
        while repeated:
            url += url
            key = hashlib.sha1(req.url.encode("UTF-8")).hexdigest()
            repeated = db.query(models.URLs).filter(
                models.URLs.key == key).first()

        url_model = models.URLs()
        url_model.key = key[0:10]
        url_model.url = url
        db.add(url_model)
        db.commit()
        return {
            "key": url_model.key,
            "long_url": url_model.url,
            "short_url": f'{request.base_url}{url_model.key}'
        }
    return JSONResponse(status_code=400, content='No provided')


@app.get('/{key}')
def get_original_url(request: Request, key: str,
                     db: Session = Depends(get_db)):
    res = db.query(models.URLs).filter(models.URLs.key == key).first()
    if not res:
        return JSONResponse(status_code=404, content='URL not found')
    return RedirectResponse(f"http://{res.url}")


@app.delete('/{key}', status_code=200)
def delete_url(request: Request, key: str,
               db: Session = Depends(get_db)):
    res = db.query(models.URLs).filter(models.URLs.key == key).first()
    if not res:
        return JSONResponse(status_code=404, content='URL not found')

    db.query(models.URLs).filter(models.URLs.key == key).delete()
    db.commit()
    return
