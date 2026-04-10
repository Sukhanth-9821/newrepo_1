import pytest
import httpx
from gist import get_gituser_gist
from fastapi import HTTPException


class MockClient:
    def __init__(self, response=None, exception=None):
        self.response = response
        self.exception = exception
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        pass
    async def get(self, url):
        if self.exception:
            raise self.exception
        return self.response


# SUCCESS
@pytest.mark.asyncio
async def test_get_gists_success(monkeypatch):
    mock_response = httpx.Response(
        status_code=200,
        json=[{"id": "123","description": "Test gist","html_url": "https://gist.github.com/test/123",}],
        request=httpx.Request("GET", "https://api.github.com/users/user/gists"),  
    )
    monkeypatch.setattr(httpx,"AsyncClient",lambda *args, **kwargs: MockClient(response=mock_response))
    result = await get_gituser_gist("user")
    assert len(result) == 1
    assert result[0].id == "123"
    assert result[0].description == "Test gist"
    assert result[0].url == "https://gist.github.com/test/123"
# EMPTY
@pytest.mark.asyncio
async def test_get_gists_empty(monkeypatch):
    mock_response = httpx.Response(
        status_code=200,
        json=[],
        request=httpx.Request("GET", "https://api.github.com/users/user/gists"), 
    )
    monkeypatch.setattr(httpx,"AsyncClient",lambda *args, **kwargs: MockClient(response=mock_response))
    result = await get_gituser_gist("user")
    assert result == []

# 404
@pytest.mark.asyncio
async def test_user_not_found(monkeypatch):
    request = httpx.Request("GET", "https://api.github.com/users/wronguser/gists")
    response = httpx.Response(status_code=404, request=request)
    exception = httpx.HTTPStatusError("Not found", request=request, response=response)
    monkeypatch.setattr(httpx,"AsyncClient",lambda *args, **kwargs: MockClient(exception=exception))
    with pytest.raises(HTTPException) as exc:
        await get_gituser_gist("wronguser")
        
    assert exc.value.status_code == 404
    assert "404: GitHub API error: 404" in str(exc.value)

# NETWORK ERROR
@pytest.mark.asyncio
async def test_network_error(monkeypatch):
    request = httpx.Request("GET", "https://api.github.com/users/user/gists")
    exception = httpx.RequestError("Network issue", request=request) 
    monkeypatch.setattr(httpx,"AsyncClient",lambda *args, **kwargs: MockClient(exception=exception))
    with pytest.raises(HTTPException) as exc:
        await get_gituser_gist("user")
    assert "Network error" in str(exc.value)


# UNEXPECTED
@pytest.mark.asyncio
async def test_unexpected_error(monkeypatch):
    exception = ValueError("Boom")
    monkeypatch.setattr(httpx,"AsyncClient",lambda *args, **kwargs: MockClient(exception=exception))
    with pytest.raises(HTTPException):
        await get_gituser_gist("user")