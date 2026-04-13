from ..clients.graphql import query_graphql
from ..models.responses import SafetyProfileResponse, TractabilityResponse, AdverseEventsResponse

async def get_safety_profile(target_id: str) -> SafetyProfileResponse:
    """Retrieves safety liabilities and toxicities for a specific target."""
    gql_query = """
    query TargetSafety($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        approvedSymbol
        safetyLiabilities {
          event
          datasource
          url
          effects {
            direction
            dosing
          }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"ensemblId": target_id})
    target = data.get("target")
    if not target:
        raise ValueError("Target not found.")
    
    return SafetyProfileResponse(
        symbol=target["approvedSymbol"],
        liabilities=target.get("safetyLiabilities", [])
    )

async def get_tractability_summary(target_id: str) -> TractabilityResponse:
    """Returns the tractability (druggability) assessment for a target."""
    gql_query = """
    query TargetTractability($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        approvedSymbol
        tractability {
          modality
          label
          value
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"ensemblId": target_id})
    target = data.get("target")
    if not target:
        raise ValueError("Target not found.")
    
    return TractabilityResponse(
        symbol=target["approvedSymbol"],
        tractability=target.get("tractability", [])
    )

async def get_drug_adverse_events(drug_id: str) -> AdverseEventsResponse:
    """Retrieves FDA FAERS pharmacovigilance data for a drug."""
    gql_query = """
    query DrugAdverseEvents($chemblId: String!) {
      drug(chemblId: $chemblId) {
        name
        adverseEvents {
          count
          rows {
            name
            meddraCode
            logLR
          }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"chemblId": drug_id})
    drug = data.get("drug")
    if not drug:
        raise ValueError("Drug not found.")
    
    events = drug.get("adverseEvents", {})
    return AdverseEventsResponse(
        drug=drug["name"],
        total_adverse_events=events.get("count", 0),
        top_events=[{"name": r["name"], "meddraCode": r["meddraCode"], "logLR": r["logLR"]} 
                    for r in events.get("rows", [])[:25]]
    )
