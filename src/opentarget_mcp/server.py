from fastmcp import FastMCP
from .tools import discovery, analysis, phenotypes, cancer

def create_server():
    mcp = FastMCP("Open Targets Specialist 🧬")

    # Discovery Tools
    @mcp.tool()
    async def resolve_id(query: str, entity_type: str = None):
        """Resolves a common name to its standardized Open Targets ID."""
        return await discovery.resolve_id(query, entity_type)

    @mcp.tool()
    async def get_prioritized_targets(disease_id: str, limit: int = 20):
        """Returns the top associated targets for a given disease ID."""
        return await discovery.get_prioritized_targets(disease_id, limit)

    # Analysis Tools
    @mcp.tool()
    async def get_safety_profile(target_id: str):
        """Retrieves safety liabilities and toxicities for a specific target."""
        return await analysis.get_safety_profile(target_id)

    @mcp.tool()
    async def get_tractability_summary(target_id: str):
        """Returns the tractability (druggability) assessment for a target."""
        return await analysis.get_tractability_summary(target_id)

    @mcp.tool()
    async def get_drug_adverse_events(drug_id: str):
        """Retrieves FDA FAERS pharmacovigilance data for a drug."""
        return await analysis.get_drug_adverse_events(drug_id)

    # Phenotype Tools
    @mcp.tool()
    async def get_disease_phenotypes(disease_id: str):
        """Maps a disease to its clinical signs and symptoms using HPO."""
        return await phenotypes.get_disease_phenotypes(disease_id)

    @mcp.tool()
    async def get_mouse_phenotypes(target_id: str):
        """Retrieves significant mouse phenotypes for a target (Gene)."""
        return await phenotypes.get_mouse_phenotypes(target_id)

    # Cancer Tools
    @mcp.tool()
    async def get_cancer_profile(target_id: str):
        """Retrieves cancer hallmarks and gene essentiality scores (DepMap)."""
        return await cancer.get_cancer_profile(target_id)

    return mcp
