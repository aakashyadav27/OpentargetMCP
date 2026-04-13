from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TargetHit(BaseModel):
    id: str
    entity: str
    name: str

class DiscoveryResult(BaseModel):
    hits: List[TargetHit]

class TargetSafetyLiability(BaseModel):
    event: str
    datasource: str
    url: Optional[str] = None
    effects: List[Dict] = []

class SafetyProfileResponse(BaseModel):
    symbol: str
    liabilities: List[TargetSafetyLiability]

class TractabilityItem(BaseModel):
    modality: str
    label: str
    value: bool

class TractabilityResponse(BaseModel):
    symbol: str
    tractability: List[TractabilityItem]

class AdverseEventRow(BaseModel):
    name: str
    meddraCode: str
    logLR: float

class AdverseEventsResponse(BaseModel):
    drug: str
    total_adverse_events: int
    top_events: List[AdverseEventRow]
