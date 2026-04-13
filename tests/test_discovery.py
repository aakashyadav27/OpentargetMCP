import pytest
from src.opentarget_mcp.tools import discovery
from src.opentarget_mcp.models.responses import DiscoveryResult

@pytest.mark.asyncio
async def test_resolve_id_target():
    """Test resolving a common gene target name."""
    result = await discovery.resolve_id("BRCA2", entity_type="target")
    assert isinstance(result, DiscoveryResult)
    assert any(hit.name == "BRCA2" for hit in result.hits)
    assert any(hit.id == "ENSG00000139618" for hit in result.hits)

@pytest.mark.asyncio
async def test_get_prioritized_targets_valid():
    """Test retrieving prioritized targets for a valid disease ID (Rheumatoid Arthritis)."""
    # EFO_0000685 = Rheumatoid Arthritis
    result = await discovery.get_prioritized_targets("EFO_0000685", limit=5)
    assert "disease" in result
    assert result["disease"].lower() == "rheumatoid arthritis"
    assert len(result["targets"]) <= 5
    assert "symbol" in result["targets"][0]
