"""
Real-time logistics & supply chain endpoints.

Provides convoy tracking, highway corridor status, and automated SITREP
(Situation Report) generation for disaster management authorities.

When Supabase is not configured the endpoints serve high-fidelity demo
data so the EOC dashboard is fully functional out of the box.
"""

from datetime import datetime, timezone, timedelta
from uuid import uuid4

from fastapi import APIRouter

from app.models.schemas import (
    ConvoyStatus,
    CorridorStatus,
    SitrepReport,
    SupplyConvoy,
)

router = APIRouter(prefix="/logistics", tags=["logistics"])


# ---------------------------------------------------------------------------
# Demo seed data — realistic convoy & corridor telemetry for NE India
# ---------------------------------------------------------------------------

def _now() -> datetime:
    return datetime.now(timezone.utc)


def _seed_convoys() -> list[SupplyConvoy]:
    return [
        SupplyConvoy(
            id="CVY-001",
            call_sign="MEDEVAC-03",
            cargo_type="Medical Supplies",
            status=ConvoyStatus.ON_ROUTE,
            origin="Guwahati Central Depot",
            destination="Haflong District Hospital",
            current_latitude=25.2048,
            current_longitude=92.6120,
            eta_minutes=142,
            delay_hours=0.0,
            corridor="NH-6",
            last_updated=_now(),
        ),
        SupplyConvoy(
            id="CVY-002",
            call_sign="FUEL-NH6-12",
            cargo_type="Fuel Tanker (Diesel)",
            status=ConvoyStatus.DELAYED,
            origin="Numaligarh Refinery",
            destination="Shillong Fuel Depot",
            current_latitude=25.1843,
            current_longitude=92.3686,
            eta_minutes=280,
            delay_hours=2.4,
            corridor="NH-6",
            last_updated=_now(),
        ),
        SupplyConvoy(
            id="CVY-003",
            call_sign="RATION-NE-07",
            cargo_type="Rations & Essential Supplies",
            status=ConvoyStatus.HALTED,
            origin="Silchar FCI Godown",
            destination="Jowai Distribution Center",
            current_latitude=25.0780,
            current_longitude=92.2100,
            eta_minutes=-1,  # halted, no ETA
            delay_hours=6.1,
            corridor="NH-6",
            last_updated=_now(),
        ),
        SupplyConvoy(
            id="CVY-004",
            call_sign="BRO-DOZER-04",
            cargo_type="BRO Heavy Earthmover",
            status=ConvoyStatus.ON_ROUTE,
            origin="BRO Camp Lumding",
            destination="Landslide Site (Sonapur Tunnel)",
            current_latitude=25.1650,
            current_longitude=92.3200,
            eta_minutes=48,
            delay_hours=0.5,
            corridor="NH-6",
            last_updated=_now(),
        ),
        SupplyConvoy(
            id="CVY-005",
            call_sign="O2-TANKER-01",
            cargo_type="Oxygen Cylinder Transport",
            status=ConvoyStatus.DIVERTED,
            origin="Guwahati Medical College",
            destination="Dima Hasao Field Hospital",
            current_latitude=25.2200,
            current_longitude=92.4500,
            eta_minutes=195,
            delay_hours=3.8,
            corridor="NH-6",
            last_updated=_now(),
        ),
    ]


def _seed_corridors() -> list[CorridorStatus]:
    return [
        CorridorStatus(
            corridor_id="NH-6",
            name="NH-6 Assam–Meghalaya–Mizoram (Lumshnong–Sonapur)",
            status="total_block",
            active_incidents=3,
            delay_index_hours=4.2,
            detour_available=True,
            detour_summary="Old NH-6 Bypass via Jatinga (single lane, +2.1 hrs)",
            last_updated=_now(),
        ),
        CorridorStatus(
            corridor_id="NH-10",
            name="NH-10 Sikkim–West Bengal (Sevoke–Gangtok)",
            status="partial_block",
            active_incidents=1,
            delay_index_hours=1.5,
            detour_available=True,
            detour_summary="Alternate via Pedong–Lava road (+1.8 hrs)",
            last_updated=_now(),
        ),
        CorridorStatus(
            corridor_id="NH-58",
            name="NH-58 Rishikesh–Badrinath (Devprayag–Joshimath)",
            status="open",
            active_incidents=0,
            delay_index_hours=0.0,
            detour_available=False,
            detour_summary=None,
            last_updated=_now(),
        ),
    ]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/convoys", response_model=list[SupplyConvoy])
async def list_convoys(corridor: str | None = None) -> list[SupplyConvoy]:
    """
    Return live positions and status of tracked supply convoys.
    Optionally filter by corridor (e.g. ?corridor=NH-6).
    """
    convoys = _seed_convoys()
    if corridor:
        convoys = [c for c in convoys if c.corridor.upper() == corridor.upper()]
    return convoys


@router.get("/corridors", response_model=list[CorridorStatus])
async def list_corridors() -> list[CorridorStatus]:
    """Return status and delay metrics for all monitored highway corridors."""
    return _seed_corridors()


@router.get("/corridors/{corridor_id}", response_model=CorridorStatus | None)
async def get_corridor(corridor_id: str) -> CorridorStatus | None:
    """Return status for a specific corridor by ID."""
    for c in _seed_corridors():
        if c.corridor_id.upper() == corridor_id.upper():
            return c
    return None


@router.post("/sitrep", response_model=SitrepReport)
async def generate_sitrep(corridor_id: str = "NH-6") -> SitrepReport:
    """
    Generate a Logistics Situation Report (SITREP) for the given corridor.

    Aggregates active incidents, convoy delays, and road statuses into a
    structured report suitable for NDMA / SDRF / District Commissioner
    consumption.
    """
    corridors = _seed_corridors()
    target = next((c for c in corridors if c.corridor_id.upper() == corridor_id.upper()), None)

    if target is None:
        # Fallback: generate a generic report
        target = CorridorStatus(
            corridor_id=corridor_id,
            name=corridor_id,
            status="open",
            active_incidents=0,
            delay_index_hours=0.0,
            detour_available=False,
            detour_summary=None,
            last_updated=_now(),
        )

    convoys = [c for c in _seed_convoys() if c.corridor.upper() == corridor_id.upper()]
    affected = [c for c in convoys if c.status != ConvoyStatus.ON_ROUTE]
    total_delay = sum(c.delay_hours for c in convoys)

    status_counts = {"total_block": 0, "partial_block": 0, "open": 0}
    for c in corridors:
        if c.status in status_counts:
            status_counts[c.status] += 1

    recommendations = []
    if target.status == "total_block":
        recommendations.append(
            f"URGENT: Deploy additional BRO earthmovers to {target.name} for debris clearance."
        )
        recommendations.append(
            "Halt all non-essential civilian convoys until the primary lane is cleared."
        )
    if target.detour_available and target.detour_summary:
        recommendations.append(
            f"Reroute priority convoys via detour: {target.detour_summary}"
        )
    if total_delay > 3.0:
        recommendations.append(
            f"Total supply chain delay is {total_delay:.1f} hrs. Notify SDMA for emergency airlift evaluation."
        )
    if not recommendations:
        recommendations.append("Corridor operating normally. Continue standard monitoring.")

    return SitrepReport(
        report_id=f"SITREP-{corridor_id}-{uuid4().hex[:8].upper()}",
        generated_at=_now(),
        corridor_id=corridor_id,
        summary=f"Logistics situation report for {target.name}. "
                f"Status: {target.status.upper()}. "
                f"{target.active_incidents} active incident(s), "
                f"{len(affected)} convoy(s) affected with cumulative delay of {total_delay:.1f} hrs.",
        active_incidents=target.active_incidents,
        convoys_affected=len(affected),
        total_delay_hours=total_delay,
        roads_blocked=status_counts["total_block"],
        roads_partial=status_counts["partial_block"],
        roads_open=status_counts["open"],
        recommendations=recommendations,
    )
