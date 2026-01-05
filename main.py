from fastapi import FastAPI
import asyncio
import uvicorn

from routers.spy_cats import router as spy_cats_router


async def main():
    app = FastAPI()
    
    app.include_router(spy_cats_router, prefix="/spy-cat", tags=["Spy Cats"])
    
    
    config = uvicorn.Config(app=app, log_level="info")
    server = uvicorn.Server(config)
    
    await server.serve()
    
    
if __name__ == "__main__":
    asyncio.run(main())
