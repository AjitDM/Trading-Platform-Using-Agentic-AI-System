from src.persistence.repositories import TradingAuditRepository
from src.states.state import TradingState


def audit_node(state: TradingState) -> dict:
    try:
        record_id = TradingAuditRepository().create_record(state)
        return {"audit_record_id": record_id}
    except Exception as exc:
        return {"errors": [f"Audit logging failed: {exc}"]}