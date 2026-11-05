from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from tools.phone_cleanser import clean_phone_rows

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Kanekes",
    description="A modular collection of office-work automation tools.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_tool": "phone-cleanser"},
    )


@app.post("/api/tools/phone-cleanser")
async def phone_cleanser(payload: dict):
    raw_text = payload.get("text", "")
    if not isinstance(raw_text, str):
        return {"result": "", "processed_rows": 0, "error": "Input must be plain text."}

    result, processed_rows = clean_phone_rows(raw_text)
    return {"result": result, "processed_rows": processed_rows}
