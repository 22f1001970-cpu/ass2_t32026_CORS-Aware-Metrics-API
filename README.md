# IITM TDS — CORS-Aware Metrics API

A ready-to-deploy FastAPI service for the `/stats` assignment.

## Assigned values

- Allowed CORS origin: `https://dash-y6o5rm.example.com`
- Email in responses: `22f1001970@ds.study.iitm.ac.in`

## API

`GET /stats?values=1,2,3`

Response:

```json
{"email":"22f1001970@ds.study.iitm.ac.in","count":3,"sum":6,"min":1,"max":3,"mean":2.0}
```

All responses, including OPTIONS and errors, get `X-Request-ID` and `X-Process-Time` headers. CORS allows only the assigned origin, never `*`.

## Deploy on Render (recommended)

1. Extract this ZIP, and upload the **contents** (including `main.py`, `requirements.txt`, and `render.yaml`) to a GitHub repository. Files must be at the repository root.
2. Open https://dashboard.render.com/ and choose **New > Web Service**.
3. Connect the GitHub repository and select the Python runtime.
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Select an available plan (Free, if offered), then deploy.
7. Wait until it is live and copy the **base URL**, such as `https://your-service.onrender.com` (no `/stats`). Paste that into the grader.

Alternatively, use **New > Blueprint** to deploy from `render.yaml` if your Render account supports blueprints and the listed plan.

Free Render instances may spin down when idle and take extra time on the first request.

## Local run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Test locally

```bash
curl -i 'http://127.0.0.1:8000/stats?values=1,2,3'

curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' \
  -H 'Origin: https://dash-y6o5rm.example.com' \
  -H 'Access-Control-Request-Method: GET'

curl -i -X OPTIONS 'http://127.0.0.1:8000/stats' \
  -H 'Origin: https://wrong.example.com' \
  -H 'Access-Control-Request-Method: GET'
```

Expected: allowed preflight returns exact `Access-Control-Allow-Origin`; disallowed preflight does **not** return that header.

Run automated tests:

```bash
pip install -r requirements-dev.txt
pytest -q
```
