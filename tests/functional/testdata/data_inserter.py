from elasticsearch._async.helpers import async_bulk


async def data_gather(row_data: list, index: str) -> list[dict]:
    return [
        {"_index": index, "_id": obj.get("id"), **obj}
        for obj in row_data
    ]


async def insert_data_in_es(client, index: str, row_data: list):
    data = await data_gather(row_data=row_data, index=index)
    await async_bulk(client=client, actions=data)
