# RoadResQ — AI Powered Road Risk Prediction & Emergency Detection

**Team:** MOTHER HACKER · **Theme:** Transportation & Logistics · **SIH 2026**

Offline-first road safety app: predicts hazards, reports and relays
incidents even without connectivity (via device-to-device Bluetooth
store-carry-forward), and reroutes travelers around active dangers.

## Repo layout

```
RoadResQ/
├── desktop-web/   Desktop EOC Control Room & Surveillance Dashboard (Leaflet map, Convoy SITREP, Landing page)
├── mobile-web/    Mobile Field Responder Web App (Offline BLE mesh simulator, Edge AI triage, SOS beacon)
├── frontend/      Native Flutter Mobile App (Hardware BLE mesh via flutter_blue_plus, SQLite cache)
├── backend/       FastAPI backend (Google OAuth 2.0, automated SITREP, Open-Meteo risk analysis)
└── docs/          Architecture notes and emergency corridor specifications
```

See the respective `README.md` in each folder for setup instructions.

## Core ideas from the pitch

- **Offline-First Intelligence** — works fully offline using cached data
  for routes, alerts, and navigation.
- **Store-Carry-Forward** — devices act as mobile nodes, relaying locally
  stored data peer-to-peer until one reaches the cloud.
- **Edge AI on Device** — on-device analysis of incident photos gives
  immediate, preliminary alerts without needing connectivity.
- **Offline Rerouting** — on-device logic calculates safe detours around
  new hazards even during network outages.

## Tech stack

- **App:** Flutter, Dart, Bluetooth (flutter_blue_plus)
- **Backend:** Python, FastAPI, REST APIs
- **Data:** Supabase, Open-Meteo, Google Maps
- **Tooling:** GitHub, VS Code

## Pushing this to GitHub

```bash
cd RoadResQ
git init
git add .
git commit -m "Initial scaffold: FastAPI backend + Flutter frontend"
git branch -M main
git remote add origin https://github.com/<your-username>/RoadResQ.git
git push -u origin main
```
