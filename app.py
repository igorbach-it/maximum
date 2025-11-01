from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import secrets, string
from threading import Lock
from typing import Optional, List
from fastapi.responses import HTMLResponse

app = FastAPI(title="Unique ID Generator", version="0.1.0")
DEFAULT_ALPHABET = string.ascii_letters + string.digits
_seen: set[str] = set()
_lock = Lock()

class GenerateRequest(BaseModel):
    length: int = 12
    count: int = 1

class GenerateResponse(BaseModel):
    items: List[str]
    length: int
    count: int

def gen_one(alphabet: str, length: int) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(length))

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    if req.length <= 0 or req.count <= 0:
        raise HTTPException(400, "length and count must be > 0")
    alphabet = DEFAULT_ALPHABET
    if len(set(alphabet)) < 2:
        raise HTTPException(400, "alphabet must have >=2 unique symbols")
    out: list[str] = []
    with _lock:
        tries = 0
        while len(out) < req.count:
            if tries > req.count * 20:
                raise HTTPException(503, "too many collisions")
            candidate = gen_one(alphabet, req.length)
            tries += 1
            if candidate in _seen:
                continue
            _seen.add(candidate)
            out.append(candidate)
    return GenerateResponse(items=out, length=req.length, count=req.count)

@app.get("/healthz")
def healthz():
    return {"status": "ok", "seen": len(_seen)}


HOME_HTML = """
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>ДЕМО Задание</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>
    :root{
      /* Палитра под референс */
      --bg: #0d1422;          /* тёмно-синяя подложка */
      --card: #0f172a;        /* тёмный блок-карта */
      --fg: #e6eaf0;          /* основной текст */
      --muted: #94a3b8;       /* приглушённый текст */
      --tile-bg: #ffffff;     /* светлые плитки */
      --tile-fg: #0b1220;     /* текст на плитках */
      --tile-border: #e6e8ee; /* тонкая рамка плиток */
      --accent: #ff404d;      /* красные акценты */
      --accent-2:#ef4444;     /* второй оттенок красного */
      --ring: rgba(255,64,77,.25); /* подсветка при :hover */
    }

    * { box-sizing: border-box; }
    html, body { height: 100%; }
    body {
      margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial;
      color: var(--fg); background: var(--bg);
      position: relative; overflow-x: hidden;
    }

    /* Фон как на референсе: дуги + точки */
    body::before{
      content:"";
      position: fixed; inset: -10% -10% 0 -10%;
      pointer-events:none; z-index:-1;
      background:
        radial-gradient(1000px 600px at 110% -10%, rgba(255,64,77,.18), transparent 60%),
        radial-gradient(800px 480px at -15% 105%, rgba(255,64,77,.14), transparent 60%),
        radial-gradient(320px 320px at 15% 15%, rgba(255,64,77,.10), transparent 70%),
        radial-gradient(320px 320px at 85% 35%, rgba(255,64,77,.08), transparent 70%),
        /* сетка точек */
        radial-gradient(circle at 50% 50%, rgba(255,255,255,.08) 1px, transparent 1.5px) 0 0/14px 14px,
        linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,0));
      filter: saturate(105%);
    }

    .wrap { max-width: 960px; margin: 8vh auto; padding: 24px; }
    .card {
      background: var(--card);
      border: 1px solid rgba(148,163,184,.12);
      border-radius: 20px;
      padding: 28px;
      box-shadow: 0 10px 30px rgba(0,0,0,.35);
      position: relative;
    }

    h1 { margin: 0 0 6px; font-size: 32px; letter-spacing:.2px; }
    h1::after{
      content:"";
      display:block; width: 76px; height: 3px; margin-top: 8px;
      background: linear-gradient(90deg, var(--accent), transparent);
      border-radius: 3px;
    }
    .muted { color: var(--muted); font-size: 14px; }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px,1fr));
      gap: 16px; margin-top: 18px;
    }

    /* «Белые» плитки с объёмом как на картинке */
    a.tile {
      display:block; text-decoration:none;
      background: var(--tile-bg); color: var(--tile-fg);
      border: 1px solid var(--tile-border);
      border-radius: 16px; padding: 16px 18px;
      box-shadow:
        0 10px 20px rgba(0,0,0,.15),
        inset 0 1px 0 rgba(255,255,255,.6);
      transform: translateZ(0);
      transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
      position: relative;
    }
    a.tile strong { font-weight: 700; }
    a.tile .muted { color: #64748b; } /* чуть темнее для белой плитки */

    a.tile::after{
      /* тонкая красная отбивка слева как акцент */
      content:""; position:absolute; left:-1px; top:10px; bottom:10px; width:4px;
      background: linear-gradient(180deg, var(--accent), var(--accent-2));
      border-radius: 4px; opacity:.65;
      transition: opacity .2s ease;
    }

    a.tile:hover{
      transform: translateY(-2px);
      box-shadow:
        0 14px 28px rgba(0,0,0,.22),
        0 0 0 6px var(--ring);
      border-color: #d9dde6;
    }
    a.tile:hover::after{ opacity: 1; }

    code {
      background: #0b1220; color:#dbe3f0;
      padding: 2px 6px; border-radius: 6px; border:1px solid rgba(148,163,184,.2);
    }
    .footer { margin-top:16px; font-size:13px; color:var(--muted); }

    /* Небольшие «декоративные» линии */
    .card::before, .card::after{
      content:""; position:absolute; pointer-events:none; opacity:.28;
      border-radius:999px; filter: blur(.2px);
    }
    .card::before{ width: 180px; height: 1px; top: 28px; right: 24px; background: linear-gradient(90deg, transparent, #fff3 40%, transparent); }
    .card::after{  width: 1px; height: 160px; bottom: 22px; left: 28px; background: linear-gradient(180deg, transparent, #fff2 40%, transparent); }

    /* Адаптив: компактнее отступы на узких экранах */
    @media (max-width: 520px){
      .wrap{ margin: 5vh auto; padding: 16px; }
      .card{ padding: 20px; }
      h1{ font-size: 26px; }
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <h1>ДЕМО Задание</h1>
      <p class="muted">Мини-демо: генератор ID, CLI-погода, класс Matrix.</p>

      <div class="grid">
        <a class="tile" href="/docs">
          <strong>API документация</strong><br>
          <span class="muted">Swagger UI для генератора ID</span>
        </a>
        <a class="tile" href="/term">
          <strong>Веб-терминал</strong><br>
          <span class="muted">Для проверки погоды и матрицы</span>
        </a>
        <a class="tile" href="https://github.com/igorbach-it/maximum">
          <strong>Исходный код</strong><br>
          <span class="muted">GitHub репозиторий</span>
        </a>
      </div>

      <p class="footer">
        Быстрый старт: <code>POST /generate {"length":8,"count":3}</code>
      </p>
    </div>
  </div>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def homepage():
    return HTMLResponse(content=HOME_HTML, status_code=200)
