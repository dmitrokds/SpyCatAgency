from fastapi import FastAPI
import asyncio
import uvicorn

from routers.spy_cats import router as spy_cats_router


async def main():
    app = FastAPI()
    
    app.include_router(spy_cats_router, prefix="/spy-cat", tags=["Spy Cats"])
    
    uvicorn.run(app=app)
    
    
if __name__ == "__main__":
    asyncio.run(main())
