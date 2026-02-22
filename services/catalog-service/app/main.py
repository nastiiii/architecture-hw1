from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="catalog-service", version="0.1.0")

@app.get("/health")
def health():
    return JSONResponse({"status": "ok"}, status_code=200)

@app.get("/")
def root():
    return {"service": "catalog-service", "message": "no business logic here"}