from fastapi import APIRouter, Body, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import db

import config



router = APIRouter()


class Cat(BaseModel):
    name: str
    years_of_exp: int
    breed: str
    salary: int
    


@router.post("/", description="Create spy cat")
async def create_cat(
    payload: Cat = Body(examples=[{
        "name": "Supercat",
        "years_of_exp": 2,
        "breed": "",
        "salary": 1000
    }]),
    api_key: str = Header(description="Write an api key to access my api")
):
    if api_key != config.API_KEY:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Invailed api key"
            },
            status_code=401
        )
    
    if payload.breed not in config.breeds:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Not a vailed breed"
            },
            status_code=400
        )
            
    
    cat_id = await db.update(f'''INSERT INTO spy_cats (name, years_of_exp, breed, salary)
VALUES ('{payload.name}', '{payload.years_of_exp}', '{payload.breed}', '{payload.salary}');''')
    
    return JSONResponse(
        content = {
            "success": True,
            "cat_id": cat_id
        }
    )
    


@router.get("/", description="Get all spy cats")
async def get_cats(
    api_key: str = Header(description="Write an api key to access my api")
):
    if api_key != config.API_KEY:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Invailed api key"
            },
            status_code=401
        )
        
        
    spy_cats = await db.select(f'''SELECT * FROM spy_cats''')
    spy_cats = [{
        "id": spy_cat[0],
        "name": spy_cat[1],
        "years_of_exp": spy_cat[2],
        "breed": spy_cat[3],
        "salary": spy_cat[4]
    } for spy_cat in spy_cats]
    
    
    return JSONResponse(
        content = {
            "success": True,
            "spy_cats": spy_cats
        }
    )


@router.get("/{id}", description="Get spy cat by id")
async def get_cat(
    id: int,
    api_key: str = Header(description="Write an api key to access my api")
):
    if api_key != config.API_KEY:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Invailed api key"
            },
            status_code=401
        )
        
        
    spy_cat = await db.select(f'''SELECT * FROM spy_cats WHERE id={id}''')
    
    if len(spy_cat)==0:
        return JSONResponse(
            content = {
                "success": False,
                "description": "This id not in db"
            },
            status_code=401
        )
        
    spy_cat = spy_cat[0]
    spy_cat = {
        "id": spy_cat[0],
        "name": spy_cat[1],
        "years_of_exp": spy_cat[2],
        "breed": spy_cat[3],
        "salary": spy_cat[4]
    }
    
    return JSONResponse(
        content = {
            "success": True,
            "spy_cat": spy_cat
        }
    )


@router.patch("/", description="Update spy cat salary")
async def update_salary(
    id: int,
    new_salary: int,
    api_key: str = Header(description="Write an api key to access my api")
):
    if api_key != config.API_KEY:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Invailed api key"
            },
            status_code=401
        )
        
    await db.update(f'''UPDATE spy_cats SET salary={new_salary} WHERE id={id}''')
    
    
    return JSONResponse(
        content = {
            "success": True
        }
    )
    

@router.delete("/", description="Delete spy cat")
async def delete_cat(
    id: int,
    api_key: str = Header(description="Write an api key to access my api")
):
    if api_key != config.API_KEY:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Invailed api key"
            },
            status_code=401
        )
        
        
        
    await db.update(f'''DELETE FROM spy_cats WHERE id={id}''')
    
    
    return JSONResponse(
        content = {
            "success": True
        }
    )