import asyncio
import httpx
from fastmcp import FastMCP
from typing import List, Optional, Dict, Any
import json

# Initialize FastMCP server
mcp = FastMCP("Open Targets Specialist 🧬")

API_URL = "https://api.platform.opentargets.org/api/v4/graphql"

async def query_graphql(query: str, variables: dict = None) -> dict:
    """Helper function to execute GraphQL queries."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                API_URL, 
                json={"query": query, "variables": variables or {}}
            )
            response.raise_for_status()
            result = response.json()
            
            if "errors" in result:
                error_msg = result["errors"][0].get("message", "Unknown GraphQL error")
                raise Exception(f"GraphQL Error: {error_msg}")
            
            return result.get("data", {})
        except httpx.HTTPStatusError as e:
            raise Exception(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Error connecting to Open Targets API: {str(e)}")

# --- CORE TOOLS ---

@mcp.tool
async def resolve_id(query: str, entity_type: str = "any") -> dict:
    """
    Resolves a common name (e.g., 'BRCA2', 'aspirin', 'asthma') to its standardized Open Targets ID.
    """
    gql_query = """
    query Search($queryString: String!) {
      search(queryString: $queryString, entityNames: []) {
        hits {
          id
          entity
          name
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"queryString": query})
    hits = data.get("search", {}).get("hits", [])
    if not hits:
        return {"error": f"No entity found for '{query}'"}
    return {"hits": hits[:5]}

@mcp.tool
async def get_prioritized_targets(disease_id: str, limit: int = 25) -> dict:
    """
    Returns the top associated targets for a given disease ID, ranked by association score.
    """
    gql_query = """
    query DiseaseTargets($efoId: String!, $size: Int!) {
      disease(efoId: $efoId) {
        id
        name
        associatedTargets(page: {index: 0, size: $size}) {
          rows {
            target { id approvedSymbol approvedName }
            score
            datatypeScores { id score }
          }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"efoId": disease_id, "size": limit})
    disease_data = data.get("disease")
    if not disease_data:
        return {"error": f"Disease '{disease_id}' not found."}
    
    rows = disease_data.get("associatedTargets", {}).get("rows", [])
    targets = []
    for row in rows:
        targets.append({
            "target_id": row["target"]["id"],
            "symbol": row["target"]["approvedSymbol"],
            "score": round(row["score"], 4),
            "evidence_breakdown": {d["id"]: round(d["score"], 4) for d in row.get("datatypeScores", [])}
        })
    return {"disease": disease_data["name"], "targets": targets}

@mcp.tool
async def get_safety_profile(target_id: str) -> dict:
    """
    Retrieves safety liabilities and toxicities for a specific target.
    """
    gql_query = """
    query TargetSafety($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        approvedSymbol
        safetyLiabilities {
          event
          datasource
          url
          effects { direction dosing }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"ensemblId": target_id})
    target_data = data.get("target")
    if not target_data:
        return {"error": f"Target '{target_id}' not found."}
    return {
        "symbol": target_data["approvedSymbol"], 
        "liabilities": target_data.get("safetyLiabilities", [])
    }

@mcp.tool
async def get_tractability_summary(target_id: str) -> dict:
    """
    Returns the tractability (druggability) assessment for a target.
    """
    gql_query = """
    query TargetTractability($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        approvedSymbol
        tractability { label modality value }
      }
    }
    """
    data = await query_graphql(gql_query, {"ensemblId": target_id})
    target_data = data.get("target")
    if not target_data:
        return {"error": "Target not found."}
    return {"symbol": target_data["approvedSymbol"], "tractability": target_data.get("tractability", [])}

# --- ADVANCED TOOLS ---

@mcp.tool
async def get_drug_adverse_events(drug_id: str) -> dict:
    """
    Retrieves FDA FAERS pharmacovigilance data (adverse events) for a specific drug (ChEMBL ID).
    """
    gql_query = """
    query DrugAdverseEvents($chemblId: String!) {
      drug(chemblId: $chemblId) {
        name
        adverseEvents {
          count
          rows { name meddraCode logLR }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"chemblId": drug_id})
    drug_data = data.get("drug")
    if not drug_data:
        return {"error": "Drug not found."}
    ae_data = drug_data.get("adverseEvents", {})
    return {
        "drug": drug_data["name"],
        "total_adverse_events": ae_data.get("count", 0),
        "top_events": ae_data.get("rows", [])[:25]
    }

@mcp.tool
async def get_cancer_profile(target_id: str) -> dict:
    """
    Retrieves cancer hallmarks and gene essentiality scores (DepMap) for a target.
    """
    gql_query = """
    query TargetCancerProfile($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        approvedSymbol
        hallmarks { attributes { name description } }
        depMapEssentiality { tissueName screens { geneEffect } }
      }
    }
    """
    data = await query_graphql(gql_query, {"ensemblId": target_id})
    target_data = data.get("target")
    if not target_data:
        return {"error": "Target not found."}
    
    # Extract attributes from hallmarks
    hallmarks_raw = target_data.get("hallmarks", {})
    attributes = []
    if hallmarks_raw and "attributes" in hallmarks_raw:
        attributes = hallmarks_raw["attributes"]

    return {
        "symbol": target_data["approvedSymbol"],
        "hallmarks": attributes,
        "essentiality": target_data.get("depMapEssentiality", [])[:10]
    }

@mcp.tool
async def get_mouse_phenotypes(target_id: str) -> dict:
    """
    Retrieves significant phenotypes observed in biological mouse models for a target.
    """
    gql_query = """
    query TargetMousePhenotypes($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        approvedSymbol
        mousePhenotypes { 
          modelPhenotypeLabel
          modelPhenotypeClasses { label }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"ensemblId": target_id})
    target_data = data.get("target")
    if not target_data:
        return {"error": "Target not found."}
    
    # Flatten phenotypes for easier consumption
    raw_phenotypes = target_data.get("mousePhenotypes", [])
    phenotypes = []
    for p in raw_phenotypes:
        classes = [c.get("label") for c in p.get("modelPhenotypeClasses", [])]
        phenotypes.append({
            "phenotype": p.get("modelPhenotypeLabel"),
            "categories": classes
        })

    return {
        "symbol": target_data["approvedSymbol"],
        "mouse_phenotypes": phenotypes[:25]
    }

@mcp.tool
async def get_disease_phenotypes(disease_id: str) -> dict:
    """
    Maps a disease to its clinical signs and symptoms using Human Phenotype Ontology (HPO).
    """
    gql_query = """
    query DiseasePhenotypes($efoId: String!) {
      disease(efoId: $efoId) {
        name
        phenotypes(page: {index: 0, size: 25}) {
          count
          rows { phenotypeHPO { id name } }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"efoId": disease_id})
    disease_data = data.get("disease")
    if not disease_data:
        return {"error": "Disease not found."}
    pheno_data = disease_data.get("phenotypes", {})
    return {
        "disease": disease_data["name"],
        "total_phenotypes": pheno_data.get("count", 0),
        "phenotypes": [p["phenotypeHPO"] for p in pheno_data.get("rows", [])]
    }

if __name__ == "__main__":
    # Using 'http' (Streamable HTTP) which is the modern standard 
    # and uses a single endpoint at /mcp
    mcp.run(transport="http", host="0.0.0.0", port=8000)
