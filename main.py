import hashlib
import json
import os
import redis

from fastapi import FastAPI, status, Request, Response, HTTPException
from jsonschema import validate, ValidationError
app = FastAPI()

redis_host = os.getenv("REDIS_HOST", "localhost")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

with open('schema.json', 'r') as f:
    PLAN_SCHEMA = json.load(f)

def generate_etag(data: dict) -> str:
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode('utf-8')).hexdigest()

@app.get("/plan/{object_id}")
async def get_plan(object_id: str, request: Request):
    key = f"plan:{object_id}"
    plan_data_str = r.get(key)
    if not plan_data_str:
        raise HTTPException(status_code=404, detail="Plan not found")
    plan_data = json.loads(plan_data_str)
    current_etag = generate_etag(plan_data)
    if_none_match = request.headers.get("if-none-match")
    if if_none_match and if_none_match.strip('"') == current_etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)

    return Response(content=plan_data_str,
                    media_type="application/json",
                    headers={"ETag": f'"{current_etag}"'})

@app.post("/plan", status_code=status.HTTP_201_CREATED)
async def create_plan(request: Request):
    try:
        payload = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    try:
        validate(payload, schema=PLAN_SCHEMA)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Schema Validation Failed: {e.message}")

    plan_id = payload.get("objectId")
    key = f"plan:{plan_id}"

    if r.exists(key):
        raise HTTPException(status_code=409, detail="Plan already exists")

    r.set(key, json.dumps(payload))

    etag = generate_etag(payload)
    return Response(content=json.dumps({"message": "Plan created", "objectId": plan_id}),
                    media_type="application/json",
                    status_code=201,
                    headers={"ETag": f'"{etag}"'})

@app.delete("/plan/{object_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plan(object_id: str):
    key = f"plan:{object_id}"
    if not r.exists(key):
        raise HTTPException(status_code=404, detail="Plan not found")
    r.delete(key)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
