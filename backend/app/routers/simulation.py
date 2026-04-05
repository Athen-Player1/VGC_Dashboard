from fastapi import APIRouter

from app.models.schemas import SimulationJobCreateRequest, SimulationJobResponse
from app.services.simulation_store import (
    create_simulation_job,
    get_simulation_job,
    list_simulation_jobs,
)

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.get("/jobs", response_model=list[SimulationJobResponse])
def get_simulation_jobs() -> list[SimulationJobResponse]:
    return [SimulationJobResponse.model_validate(job) for job in list_simulation_jobs()]


@router.get("/jobs/{job_id}", response_model=SimulationJobResponse)
def get_simulation_job_by_id(job_id: str) -> SimulationJobResponse:
    return SimulationJobResponse.model_validate(get_simulation_job(job_id))


@router.post("/jobs", response_model=SimulationJobResponse)
def create_job(payload: SimulationJobCreateRequest) -> SimulationJobResponse:
    return SimulationJobResponse.model_validate(create_simulation_job(payload))
