from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.graphs.trading_graph import resume_trading_run

router = APIRouter()


class ApprovalRequest(BaseModel):
    approved: bool
    note: str | None = None


@router.post("/{run_id}")
def submit_approval(run_id: str, request: ApprovalRequest) -> dict:
    try:
        return resume_trading_run(
            run_id=run_id,
            approved=request.approved,
            note=request.note,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc