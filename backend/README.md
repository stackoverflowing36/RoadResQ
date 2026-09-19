# RoadResQ Backend

FastAPI backend for RoadResQ: incident reporting, alerts, weather-risk checks,
and hazard-aware route planning.

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # fill in Supabase + Google Maps keys
uvicorn app.main:app --reload
```

API docs will be live at `http://localhost:8000/docs`.

## Notes

- Works in "demo mode" with no keys set: incidents/alerts are kept in
  memory and routes fall back to a straight-line estimate. Add Supabase
  and Google Maps credentials for the real thing.
- Endpoints are versioned under `/api/v1`.

## Structure

```
app/
  core/       # settings/config
  models/     # Pydantic schemas
  routers/    # incidents, alerts, routes
  services/   # Supabase, weather (Open-Meteo), maps (Google Directions)
  main.py     # FastAPI app + router registration
```
