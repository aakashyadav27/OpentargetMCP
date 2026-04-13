from ..clients.graphql import query_graphql

async def resolve_id(query: str, entity_type: str = None):
    """Resolves a common name to a standardized Open Targets ID."""
    gql_query = """
    query Search($queryString: String!, $entityNames: [String!]) {
      search(queryString: $queryString, entityNames: $entityNames) {
        hits {
          id
          entity
          name
        }
      }
    }
    """
    variables = {"queryString": query}
    if entity_type:
        variables["entityNames"] = [entity_type]
        
    data = await query_graphql(gql_query, variables)
    return {"hits": data.get("search", {}).get("hits", [])[:5]}

async def get_prioritized_targets(disease_id: str, limit: int = 20):
    """Returns top associated targets for a given disease ID."""
    gql_query = """
    query PrioritizedTargets($diseaseId: String!, $size: Int!) {
      disease(efoId: $diseaseId) {
        name
        associatedTargets(page: {index: 0, size: $size}) {
          rows {
            target {
              id
              approvedSymbol
              approvedName
            }
            score
            datatypeScores {
              id
              score
            }
          }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"diseaseId": disease_id, "size": limit})
    disease = data.get("disease")
    if not disease:
        return {"error": "Disease not found."}
    
    targets = []
    for row in disease.get("associatedTargets", {}).get("rows", []):
        targets.append({
            "target_id": row["target"]["id"],
            "symbol": row["target"]["approvedSymbol"],
            "score": round(row["score"], 4),
            "evidence_breakdown": {s["id"]: round(s["score"], 4) for s in row["datatypeScores"]}
        })
    
    return {
        "disease": disease["name"],
        "targets": targets
    }
