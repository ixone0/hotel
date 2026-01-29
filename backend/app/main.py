from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend is runningggggg HII hi"}

@app.get("/health")
def health():
    return {"status": "okkkkkk EIEI"}
