import json

from src.persistence.database import SessionLocal
from src.persistence.models import TradingAuditRecord
from src.states.state import TradingState


class TradingAuditRepository:
    def create_record(self, state: TradingState) -> int:
        execution = state.get("execution_result", {})
        status = execution.get(
            "status",
            state.get("approval_status", "ANALYZED"),
        )

        record = TradingAuditRecord(
            run_id=state["run_id"],
            symbol=state["symbol"],
            status=status,
            signal_json=(
                state["signal"].model_dump_json() if state.get("signal") else None
            ),
            order_json=(
                state["order"].model_dump_json() if state.get("order") else None
            ),
            execution_json=json.dumps(execution, default=str),
            errors_json=json.dumps(state.get("errors", [])),
        )

        with SessionLocal() as session:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id