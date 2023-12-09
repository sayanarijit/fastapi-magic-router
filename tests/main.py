from fastapi import FastAPI
from pydantic import BaseModel

from magic_router import magic, magic_router


class Response(BaseModel):
    path: str


# Default Router -----------------------------------------------------------------------

app = FastAPI()


not_so_magical_path = "/api/not-so-magical"


async def not_so_magical_endpoint():
    return Response(path=not_so_magical_path)


app.get(
    not_so_magical_path,
    response_model=Response,
    tags=["main"],
    operation_id="not_so_magical_endpoint",
    name="not_so_magical_endpoint",
)(not_so_magical_endpoint)


# Magic Router -------------------------------------------------------------------------

route = magic_router(app)


async def magical_endpoint() -> Response:
    return Response(path=magic(magical_endpoint).path)


route("GET /api/magical", magical_endpoint)

# --------------------------------------------------------------------------------------
