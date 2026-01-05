from fastapi import APIRouter, Body, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import db

import config


router = APIRouter()

class Target(BaseModel):
    name: str
    country: str
    notes: str
    
class Mission(BaseModel):
    targets: list[Target]
    


@router.post("/", description="Create mission")
async def create_mission(
    payload: Mission = Body(examples=[{"targets":[{
        "name": "Test",
        "country": "Ukraine",
        "notes": ""
    },{
        "name": "Test2",
        "country": "Poland",
        "notes": ""
    }]}]),
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
        
    if len(payload.targets)>3:
        return JSONResponse(
            content = {
                "success": False,
                "description": "No more than three targets"
            },
            status_code=400
        )
    elif len(payload.targets)==0:
        return JSONResponse(
            content = {
                "success": False,
                "description": "You need at least one target"
            },
            status_code=400
        )
    
    mission_id = await db.update(f'''INSERT INTO missions DEFAULT VALUES''')
    
    target_ids = []
    for target in payload.targets:
        target_id = await db.update(f'''INSERT INTO targets (name, country, notes, mission_id) VALUES ('{target.name}', '{target.country}', '{target.notes}', '{mission_id}')''')
        target_ids.append(target_id)
    
    return JSONResponse(
        content = {
            "success": True,
            "mission_id": mission_id,
            "target_ids": target_ids
        }
    )
    


@router.get("/", description="Get all missions")
async def get_missions(
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
        
        
    missions_row = await db.select(f'''SELECT 
        missions.id, missions.complete, missions.cat_id, spy_cats.name, targets.id, targets.name, targets.country, targets.notes, targets.complete
    FROM missions
    INNER JOIN targets ON targets.mission_id=missions.id
    LEFT JOIN spy_cats ON spy_cats.id=missions.cat_id
    ''')

    missions = {}
    for mission_id, mission_complete, spy_cat_id, spy_cat_name, target_id, target_name, target_country, target_notes, target_complete in missions_row:
        missions.setdefault(mission_id, {
            "id": mission_id,
            "cat": {
                "id": spy_cat_id,
                "name": spy_cat_name
            },
            "targets": [],
            "complete": mission_complete==1
        })
        missions[mission_id]["targets"].append({
            "id": target_id,
            "name": target_name,
            "country": target_country,
            "notes": target_notes,
            "complete": target_complete==1
        })
        
    missions = list(missions.values())
    
    
    
    return JSONResponse(
        content = {
            "success": True,
            "missions": missions
        }
    )


@router.get("/{id}", description="Get mission by id")
async def get_mission(
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
        
        
        
    missions_row = await db.select(f'''SELECT 
        missions.id, missions.complete, missions.cat_id, spy_cats.name, targets.id, targets.name, targets.country, targets.notes, targets.complete
    FROM missions
    INNER JOIN targets ON targets.mission_id=missions.id
    LEFT JOIN spy_cats ON spy_cats.id=missions.cat_id
    WHERE missions.id = {id}
    ''')

    mission = None
    for mission_id, mission_complete, spy_cat_id, spy_cat_name, target_id, target_name, target_country, target_notes, target_complete in missions_row:
        if mission == None:
            mission = {
                "id": mission_id,
                "cat": {
                    "id": spy_cat_id,
                    "name": spy_cat_name
                },
                "targets": [],
                "complete": mission_complete==1
            }
        mission["targets"].append({
            "id": target_id,
            "name": target_name,
            "country": target_country,
            "notes": target_notes,
            "complete": target_complete==1
        })
        
    
    return JSONResponse(
        content = {
            "success": True,
            "mission": mission
        }
    )


@router.patch("/complete/{id}", description="Set target to complete")
async def set_complete(
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
        
    resp = await db.select(f'''SELECT mission_id, complete FROM targets WHERE id={id}''')
    
    if len(resp) == 0:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Wrong id"
            },
            status_code=400
        )
        
    mission_id, complete = resp[0]
    
    if complete:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Already complete"
            },
            status_code=400
        )
        
        
    cat_id = await db.select(f'''SELECT cat_id FROM missions WHERE id={mission_id}''')
    
    if cat_id[0][0] == None:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Mission not assigned to cat"
            },
            status_code=400
        )
        
    
    await db.update(f'''UPDATE targets SET complete=1 WHERE id={id}''')
    
    
    resp = await db.select(f'''SELECT complete FROM targets WHERE mission_id={mission_id}''')
     
    if all(target[0] for target in resp):
        await db.update(f'''UPDATE missions SET complete=1 WHERE id={mission_id}''')
    
    
    return JSONResponse(
        content = {
            "success": True
        }
    )
    

@router.delete("/", description="Delete mission")
async def delete_mission(
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
        
        
    cat_id = await db.select(f'''SELECT cat_id FROM missions WHERE id={id}''')
    
    if len(cat_id)==0:
        return JSONResponse(
            content = {
                "success": False,
                "description": "This id not in db"
            },
            status_code=400
        )
    
    cat_id = cat_id[0][0]
    
    if cat_id==None:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Mission not assigned to cat"
            },
            status_code=400
        )
        
    await db.update(f'''DELETE FROM missions WHERE id={id}''')
    
    
    return JSONResponse(
        content = {
            "success": True
        }
    )
    
    
    

@router.patch("/assign/{mission_id}/{spy_cat_id}", description="Assign cat to the mission")
async def assign_cat(
    mission_id: int,
    spy_cat_id: int, 
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
        
    cat_id = await db.select(f'''SELECT cat_id FROM missions WHERE id={mission_id}''')
    
    if len(cat_id) == 0:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Wrong mission id"
            },
            status_code=400
        )
    elif cat_id[0][0] != None:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Mission already assigned to cat"
            },
            status_code=400
        )
        
    await db.update(f'''UPDATE missions SET cat_id={spy_cat_id} WHERE id={mission_id}''')
    
    
    return JSONResponse(
        content = {
            "success": True
        }
    )
    
    

@router.patch("/note/{id}", description="Update target notes")
async def update_target_notes(
    id: int,
    notes: str,
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
        
    complete = await db.select(f'''SELECT complete FROM targets WHERE id={id}''')
    
    if len(complete) == 0:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Wrong target id"
            },
            status_code=400
        )
    elif complete[0][0]:
        return JSONResponse(
            content = {
                "success": False,
                "description": "Already completed"
            },
            status_code=400
        )
        
    await db.update(f'''UPDATE targets SET notes='{notes}' WHERE id={id}''')
    
    
    return JSONResponse(
        content = {
            "success": True
        }
    )
    