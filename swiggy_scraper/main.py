# main.py
from fastapi import FastAPI, Query
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from swiggy_client import SwiggyClient

app = FastAPI()
client = SwiggyClient()

# Initialize cache on app startup
@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="swiggy-cache")

# Route with simple in-memory caching
@app.get("/search")
@cache(expire=60)  # Cache results for 1 minute
def search_products(query: str = Query(...)):

    # Handle spaces in query
    query = query.replace(' ', '')
    return {"results": client.search_products(query)}
