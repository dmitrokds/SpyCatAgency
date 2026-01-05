from fastapi import FastAPI
import asyncio
import uvicorn


async def main():
    app = FastAPI()
    
    uvicorn.run(app=app)
    
if __name__ == "__main__":
    asyncio.run(main())
