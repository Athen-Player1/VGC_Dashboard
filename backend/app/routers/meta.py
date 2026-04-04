from fastapi import APIRouter

from app.models.schemas import MetaSnapshotResponse
from app.services.meta_store import get_active_meta_snapshot, list_meta_snapshots

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/snapshots", response_model=list[MetaSnapshotResponse])
def get_meta_snapshots() -> list[MetaSnapshotResponse]:
    return [MetaSnapshotResponse.model_validate(snapshot) for snapshot in list_meta_snapshots()]


@router.get("/snapshots/active", response_model=MetaSnapshotResponse)
def get_active_snapshot() -> MetaSnapshotResponse:
    return MetaSnapshotResponse.model_validate(get_active_meta_snapshot())
