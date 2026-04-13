from ..clients.graphql import query_graphql

async def get_schema_info():
    """
    Returns high-level information about the Open Targets GraphQL schema.
    Use this tool when you are unsure which fields are available for a Target, Disease, or Drug.
    """
    gql_query = """
    query IntrospectSchema {
      __schema {
        queryType {
          fields {
            name
            description
            args {
              name
              type {
                name
                kind
              }
            }
          }
        }
      }
    }
    """
    data = await query_graphql(gql_query)
    # Simplify the fields list for the agent
    fields = data.get("__schema", {}).get("queryType", {}).get("fields", [])
    simplified = [{"name": f["name"], "desc": f["description"]} for f in fields]
    return {"available_top_level_queries": simplified}
