import os
import socket
import random
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def generate_color_from_name(name: str) -> str:
    random.seed(name)
    r = random.randint(200, 255)
    g = random.randint(200, 255)
    b = random.randint(200, 255)

    return f"#{r:02x}{g:02x}{b:02x}"


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    container_id = socket.gethostname()

    server_name = os.getenv("SERVER_NAME", "Instância Desconhecida")

    bg_color = generate_color_from_name(server_name)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "server_name": server_name,
            "container_id": container_id,
            "bg_color": bg_color,
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host="0.0.0.0",
        port=8000,
        log_config=None,
    )
