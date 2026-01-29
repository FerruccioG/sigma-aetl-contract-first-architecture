#  =========================
#  SIGMA-AETL Validator — Contract v1.0 (FROZEN)
#
#  This service enforces the authoritative ingestion contract for the
#  SIGMA-AETL pipeline.
# 
#  CONTRACT STATUS
# - Version: v1.0
# - Status: FROZEN
# - This contract MUST NOT be modified in place.
#
#  GUARANTEES
# - Deterministic schema validation (Pydantic)
# - Explicit PASS / FAIL response contract
# - No side effects
# - No data mutation
# - No heuristic repair

#  CHANGE POLICY
# Any change to validation rules, schema shape, or semantics requires:
# - A new versioned contract (v2, v3, …)
# - A new validator service instance
# - Explicit orchestration changes
#
# This file is the single source of truth for ingestion correctness.
# =========================

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

app = FastAPI(title="SIGMA-AETL Validator")

# =========================
# Pydantic Contract (v1)
# =========================
class ShipmentPayload(BaseModel):
    shipment_id: str = Field(..., min_length=1, description="Unique shipment identifier")
    weight_kg: float = Field(..., gt=0, description="Weight in kilograms")
    destination: str = Field(..., min_length=1, description="Destination city")
    priority: int = Field(..., ge=1, le=3, description="Priority level (1–3)")


# =========================
# Unified Response Contract
# =========================
def failed_response(reason: str, errors, received_payload):
    return JSONResponse(
        status_code=200,
        content={
            "status": "FAILED",
            "reason": reason,
            "errors": errors,
            "received_payload": received_payload,
        },
    )


# =========================
# Validator Endpoint
# =========================
@app.post("/api/validate")
async def validate(payload: dict):

    # 1️⃣ Schema validation
    try:
        shipment = ShipmentPayload(**payload)
    except ValidationError as e:
        return failed_response(
            reason="Schema validation failed",
            errors=e.errors(),
            received_payload=payload,
        )

    # 2️⃣ Business rules
    business_errors: List[str] = []

    if shipment.weight_kg > 1000:
        business_errors.append("weight_kg exceeds maximum allowed limit")

    if business_errors:
        return failed_response(
            reason="Business rule violation",
            errors=business_errors,
            received_payload=payload,
        )

    # 3️⃣ PASSED
    return JSONResponse(
        status_code=200,
        content={
            "status": "PASSED",
            "clean_data": shipment.model_dump(),
        },
    )
