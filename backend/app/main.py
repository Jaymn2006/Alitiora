from fastapi import FastAPI

app = FastAPI(title="Alitiora API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api")
def root():
    return {"message": "ALITIORA backend scaffold"}
