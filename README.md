# FastAPI Magic Router

Have you come here seeking magical powers to define FastAPI routes the following way?

```python
app = FastAPI()
route = magic_router(app)

route("GET     /api/users          ", list_users)
route("GET     /api/users/{user_id}", get_user)
route("POST    /api/users          ", create_user)
route("PATCH   /api/users/{user_id}", update_user)
route("DELETE  /api/users/{user_id}", delete_user)
```

Come, I shall grant you your wish!

### Default Router vs Magic Router

```python
from magic_router import NoMagic, magic_router, magic
from fastapi import FastAPI
from pydantic import BaseModel


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


async def magical_endpoint():
    return Response(path=magic(magical_endpoint).path)


magical_endpoint.nomagic = NoMagic(response_model=Response)


route("GET /api/magical", magical_endpoint)

# --------------------------------------------------------------------------------------
```
