from fastapi import HTTPException 
import httpx
from app.models import validationgist

GITHUB_API = "https://api.github.com"  


async def get_gituser_gist(username: str) -> list[validationgist]:  
    user_url = f"{GITHUB_API}/users/{username}/gists"

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response =  await client.get(user_url)
            response.raise_for_status()
        data = response.json()  
        result = []
        for i in data:
            obj = validationgist(id = i["id"],description=i.get("description"), url=i["html_url"])
            result.append(obj)
        return result        
    # 500/400 erros    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code,detail=f"GitHub API error: {e.response.status_code}")        
    # 503 ERRORS
    except httpx.RequestError as e:
        raise HTTPException(status_code=503,detail=f"Network error: {str(e)}")
    #Internal Server Error
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Unexpected error: {str(e)}")