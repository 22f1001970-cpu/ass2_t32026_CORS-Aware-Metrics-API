"""CORS-aware descriptive statistics API for the TDS assignment."""

import time
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "22f1001970@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-y6o5rm.example.com"

app = FastAPI(title="CORS-Aware Metrics API", version="1.0.0")

# Added before the timing middleware so timings and request IDs also appear on
# CORS preflight responses and on framework-generated error responses.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=False,
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


@app.middleware("http")
async def add_request_headers(request: Request, call_next):
    started = time.perf_counter()
    request_id = str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{max(0.0, time.perf_counter() - started):.6f}"
    return response


@app.get("/stats")
async def stats(values: str = Query(...)):
    try:
        parts = values.split(",")
        if not parts or any(not part.strip() for part in parts):
            raise ValueError("empty value")
        numbers = [int(part.strip()) for part in parts]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="values must be comma-separated integers") from exc

    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }


@app.get("/")
async def root():
    return {"message": "Metrics API is running", "endpoint": "/stats?values=1,2,3"}
