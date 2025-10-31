from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import secrets, string
from threading import Lock
from typing import Optional, List

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
