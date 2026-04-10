from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from gist import get_gituser_gist

app = FastAPI()

#Calling Frontend
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("index.html") as f:
        return f.read()
# GET API endpoint
@app.get("/gists/{username}")
async def gists(username: str):
    return await get_gituser_gist(username)