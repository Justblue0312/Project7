import uvicorn

from pre_setup import get_application

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
