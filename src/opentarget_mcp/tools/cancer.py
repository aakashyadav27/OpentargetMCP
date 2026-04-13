from ..clients.graphql import query_graphql

async def get_cancer_profile(target_id: str):
    """Retrieves cancer hallmarks and gene essentiality scores (DepMap)."""
    gql_query = """
    query TargetCancerProfile($ensemblId: String!) {
      target(ensemblId: $ensemblId) {
        approvedSymbol
        hallmarks {
          cancerHallmarks {
            label
          }
          attributes {
            name
            description
          }
        }
        depMapEssentiality {
          tissueName
          screens {
            cellLineName
            geneEffect
            depmapId
          }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"ensemblId": target_id})
    target = data.get("target")
    if not target:
        return {"error": "Target not found."}
    
    # Flatten hallmarks
    hallmarks_raw = target.get("hallmarks", {})
    hallmarks = [h["label"] for h in hallmarks_raw.get("cancerHallmarks", [])]
    attributes = [{"name": a["name"], "desc": a["description"]} 
                  for a in hallmarks_raw.get("attributes", [])]

    return {
        "symbol": target["approvedSymbol"],
        "hallmarks": hallmarks,
        "hallmark_attributes": attributes,
        "essentiality": target.get("depMapEssentiality", [])[:10]
    }
