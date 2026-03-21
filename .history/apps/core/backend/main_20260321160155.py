from fastapi import FastAPI

app = FastAPI(title="Seoualmate Minimal API")

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
