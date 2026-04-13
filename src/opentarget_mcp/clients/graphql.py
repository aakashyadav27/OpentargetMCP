import httpx

API_URL = "https://api.platform.opentargets.org/api/v4/graphql"

async def query_graphql(query: str, variables: dict = None):
    """Sends a query to the Open Targets GraphQL API."""
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
            raise Exception(f"Internal Error: {str(e)}")
