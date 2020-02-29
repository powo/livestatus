#!/bin/env python3
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import StreamingResponse
import asyncio
import json

app = FastAPI()

class State(object):
    def __init__(self):
        self._data = {
            "test": {"text": "Hello World", "value": 123},
        }

    def get(self, key):
        return self._data.get(key, None)

    def set(self, key, value):
        self._data[key] = value

    def delete(self, key):
        if key in self._data:
            del self._data[key]

    def get_items(self):
        return sorted(self._data.items())

globalstate = State()

class DataItem(BaseModel):
    text: str = ""
    value: float = 0

@app.get("/")
def read_root():
    return globalstate.get_items()


@app.get("/data/{key}")
def read_item(key: str):
    return globalstate.get(key)

@app.get("/data/{key}/watch")
def watch_item(key: str):
    async def event_stream():
        prevval = {"uninitialized": ""}
        while True:
            currentval = globalstate.get(key)
            if currentval != prevval:
                if currentval is None:
                    yield "data: null\n\n"
                else:
                    yield "data: %s\n\n" % currentval.json()
                prevval = currentval
            await asyncio.sleep(0.5)
    return StreamingResponse(event_stream(), media_type='text/event-stream')


@app.put("/data/{key}")
def put_item(key: str, item: DataItem):
    return globalstate.set(key, item)

@app.delete("/data/{key}")
def del_item(key: str):
    return globalstate.delete(key)
