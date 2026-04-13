from ..clients.graphql import query_graphql

async def get_disease_phenotypes(disease_id: str):
    """Maps a disease to its clinical signs and symptoms using HPO."""
    gql_query = """
    query DiseasePhenotypes($efoId: String!) {
      disease(efoId: $efoId) {
        name
        phenotypes(page: {index: 0, size: 100}) {
          count
          rows {
            phenotypeHPO {
              id
              name
            }
          }
        }
      }
    }
    """
    data = await query_graphql(gql_query, {"efoId": disease_id})
    disease = data.get("disease")
    if not disease:
        return {"error": "Disease not found."}
    
    phenotypes = disease.get("phenotypes", {})
    return {
        "disease": disease["name"],
        "total_phenotypes": phenotypes.get("count", 0),
        "phenotypes": [{"id": r["phenotypeHPO"]["id"], "name": r["phenotypeHPO"]["name"]} 
                      for r in phenotypes.get("rows", [])[:25] if r.get("phenotypeHPO")]
    }

async def get_mouse_phenotypes(target_id: str):
    """Retrieves significant mouse phenotypes for a target (Gene)."""
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
