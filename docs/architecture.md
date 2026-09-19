# RoadResQ — Architecture Notes

Based on the SIH2026 pitch (Team MOTHER HACKER).

## Workflow

1. **Disaster Occurs** — landslide/avalanche/cloudburst blocks or disrupts a road.
2. **Detection & Info Gathering** — sensors, cameras, satellite data, and user
   reports feed in.
3. **AI Analysis & Risk Assessment** — system analyzes data, confirms the
   blockage, and assesses severity.
4. **Alert & Notify** — instant alerts sent to authorities, travelers, and
   nearby communities.
5. **Reroute & Traffic Management** — dynamic detours calculated and pushed
   to affected users.
6. **Rescue & Clearance** — emergency teams coordinate site clearing.
7. **Road Reopens** — status updated once confirmed clear.
8. **Post-Event Analysis & Improvement** — logged data feeds back into the
   prediction model.

## Offline-first design

- **Backend** (`/backend`) is the source of truth when reachable, but every
  client keeps a local cache (SQLite) and can operate fully without it.
- **Store-Carry-Forward**: a device with no signal can still record and
  hand off incident/alert data to a nearby peer over Bluetooth
  (`frontend/lib/services/bluetooth_service.dart`), which later syncs it
  to the backend once it has connectivity.
- **Edge AI on device**: incident photos get a preliminary on-device
  analysis before (or instead of) a round-trip to the server.

## Services

| Concern            | Where |
|--------------------|-------|
| Incident reporting | `backend/app/routers/incidents.py` |
| Alerts             | `backend/app/routers/alerts.py` |
| Weather risk        | `backend/app/services/weather.py` (Open-Meteo) |
| Route planning     | `backend/app/services/maps.py` (Google Directions) |
| Persistent storage | Supabase (`backend/app/services/supabase_client.py`) |
| Offline cache      | `frontend/lib/services/offline_storage_service.dart` (SQLite) |
| Peer sync          | `frontend/lib/services/bluetooth_service.dart` |

## Open items for the hackathon build

- Define the Bluetooth GATT service/characteristic contract and de-dup
  logic for relayed records.
- Decide the on-device Edge AI model for incident-photo triage (e.g. a
  small TFLite classifier) and where it plugs into the report flow.
- Add authentication (Supabase Auth) for field responders vs. the public.
- Add a Supabase schema migration for `incidents` and `alerts` tables
  matching `backend/app/models/schemas.py`.
