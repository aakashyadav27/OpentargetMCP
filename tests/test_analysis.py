import pytest
from src.opentarget_mcp.tools import analysis
from src.opentarget_mcp.models.responses import SafetyProfileResponse, TractabilityResponse, AdverseEventsResponse

@pytest.mark.asyncio
async def test_get_safety_profile_format():
    """Smoke test to verify BRCA2 safety profile returns a valid Pydantic model."""
    result = await analysis.get_safety_profile("ENSG00000139618")
    assert isinstance(result, SafetyProfileResponse)
    assert result.symbol == "BRCA2"

@pytest.mark.asyncio
async def test_get_tractability_parp1():
    """Test tractability summary for a known druggable target (PARP1)."""
    result = await analysis.get_tractability_summary("ENSG00000143799")
    assert isinstance(result, TractabilityResponse)
    assert result.symbol == "PARP1"
    assert any(item.modality == "SM" and item.value is True for item in result.tractability)

@pytest.mark.asyncio
async def test_get_drug_adverse_events_olaparib():
    """Test adverse events for Olaparib."""
    result = await analysis.get_drug_adverse_events("CHEMBL521686")
    assert isinstance(result, AdverseEventsResponse)
    assert result.drug.lower() == "olaparib"
    assert result.total_adverse_events > 0
