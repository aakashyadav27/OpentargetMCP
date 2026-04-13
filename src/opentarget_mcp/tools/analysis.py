from ..clients.graphql import query_graphql

async def get_safety_profile(target_id: str):
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
        return {"error": "Target not found."}
    
    return {
        "symbol": target["approvedSymbol"],
        "liabilities": target.get("safetyLiabilities", [])
    }

async def get_tractability_summary(target_id: str):
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
        return {"error": "Target not found."}
    
    return {
        "symbol": target["approvedSymbol"],
        "tractability": target.get("tractability", [])
    }

async def get_drug_adverse_events(drug_id: str):
    """Retrieves FDA FAERS pharmacovigilance data for a drug."""
    gql_query = """
    query DrugAdverseEvents($chemblId: String!) {
      drug(chemblId: $chemblId) {
        name
        adverseEvents {
          count
          rows {
            event
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
        return {"error": "Drug not found."}
    
    events = drug.get("adverseEvents", {})
    return {
        "drug": drug["name"],
        "total_adverse_events": events.get("count", 0),
        "top_events": [{"name": r["event"], "meddraCode": r["meddraCode"], "logLR": r["logLR"]} 
                      for r in events.get("rows", [])[:25]]
    }
