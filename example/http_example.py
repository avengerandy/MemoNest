import uvicorn
from fastapi import FastAPI

from src.factory import MemoNestFactory, MemoNestMode
from src.interaction import MemoCreateData, MemoDeleteData, MemoGetData, MemoUpdateData

memo_nest_factory = MemoNestFactory()


def get_memo_nest():
    return memo_nest_factory.create_memo_nest(MemoNestMode.COLLABORATION)


app = FastAPI()


@app.post("/memo/create")
async def create_memo(data: MemoCreateData):
    memo_nest = get_memo_nest()
    memo_nest.create_memo(data)
    return memo_nest.output_handler.data


@app.get("/memo/get")
async def get_memo(data: MemoGetData):
    memo_nest = get_memo_nest()
    memo_nest.get_memo(data)
    return memo_nest.output_handler.data


@app.get("/memo/get_all")
async def get_memos():
    memo_nest = get_memo_nest()
    memo_nest.get_memos()
    return memo_nest.output_handler.data


@app.put("/memo/update")
async def update_memo(data: MemoUpdateData):
    memo_nest = get_memo_nest()
    memo_nest.update_memo(data)
    return memo_nest.output_handler.data


@app.delete("/memo/delete")
async def delete_memo(data: MemoDeleteData):
    memo_nest = get_memo_nest()
    memo_nest.delete_memo(data)
    return memo_nest.output_handler.data


if __name__ == "__main__":
    uvicorn.run("client.http_example:app", host="0.0.0.0", port=8000, reload=True)
