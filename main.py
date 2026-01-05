from fastapi import FastAPI
import asyncio
import uvicorn

from routers.spy_cats import router as spy_cats_router
from routers.missions_targets import router as missions_targets_router

import db

import logging

import aiohttp
import config


async def main():
    app = FastAPI()
    
    app.include_router(spy_cats_router, prefix="/spy-cat", tags=["Spy Cats"])
    app.include_router(missions_targets_router, prefix="/missions-targets", tags=["Missions / Targets"])
    
    
    @app.get("/health")
    def health():
        return {"message": "Welcome to Spy Cat Agency"}
    
    await db.create()
    
    
    async with aiohttp.ClientSession() as sess:
        async with sess.get(config.BreadsUrl) as resp:
            try:
                breeds = await resp.json()
            except:
                pass
    config.breeds = [breed["name"] for breed in breeds]
    
    
    app_config = uvicorn.Config(app=app, host="0.0.0.0", log_level="info")
    server = uvicorn.Server(app_config)
    
    await server.serve()
    
    
if __name__ == "__main__":
    asyncio.run(main())
