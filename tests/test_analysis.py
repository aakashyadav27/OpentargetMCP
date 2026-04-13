import pytest
from src.opentarget_mcp.tools import analysis
from src.opentarget_mcp.models.responses import SafetyProfileResponse

@pytest.mark.asyncio
async def test_get_safety_profile_format():
    """Smoke test to verify BRCA2 safety profile returns a valid Pydantic model."""
    # ENSG00000139618 = BRCA2
    result = await analysis.get_safety_profile("ENSG00000139618")
    assert isinstance(result, SafetyProfileResponse)
    assert result.symbol == "BRCA2"
    assert isinstance(result.liabilities, list)
