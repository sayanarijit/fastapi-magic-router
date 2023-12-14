__version__ = "0.2.0"


from dataclasses import dataclass
from enum import Enum
from inspect import signature
from typing import Any, Callable

from fastapi import FastAPI


@dataclass
class Magic:
    """This object will magically appear as <endpoint>.magic attribute when the route is
    defined.

    You can also access this using `magic(endpoint)`.
    """

    path: str
    method: str


@dataclass
class NoMagic:
    """Add this object to <endpoint>.nomagic attribute to manually pass arguments to
    the route."""

    tags: list[str | Enum] | None = None
    name: str | None = None
    operation_id: str | None = None
    response_model: Any = None
    fastapi_kwargs: dict[str, Any] | None = None


_defaults = NoMagic()


def magic(endpoint: Callable[..., Any]) -> Magic:
    """This function provides a typed api for accessing the auto attached
    <endpoint>.magic object."""

    return endpoint.magic


def nomagic(
    tags: list[str | Enum] | None = None,
    name: str | None = None,
    operation_id: str | None = None,
    response_model: Any = None,
    **kwargs: Any,
):
    """Decorator to manually set the endpoint attributes."""

    def decorator(endpoint: Callable[..., Any]):
        endpoint.nomagic = NoMagic(
            tags=tags,
            name=name,
            operation_id=operation_id,
            response_model=response_model,
            fastapi_kwargs=kwargs,
        )
        return endpoint

    return decorator


def magic_router(app: FastAPI):
    """Give it a FastAPI object and it will give you a function with magical powers.

    Example:

    >>> app = FastAPI()
    >>> route = magic_router(app)
    >>> route("GET     /api/users          ", user.list_)
    >>> route("GET     /api/users/{user_id}", user.get)
    >>> route("POST    /api/users          ", user.create)
    >>> route("PATCH   /api/users/{user_id}", user.update)
    >>> route("DELETE  /api/users/{user_id}", user.delete_)

    """

    def route(
        location: str,
        endpoint: Callable[..., Any],
        name: str | None = None,
        operation_id: str | None = None,
        tags: list[Enum | str] | None = None,
        response_model: Any = None,
        **kwargs: Any,
    ):
        """Format: `route("METHOD   /path", endpoint)."""

        method, path = location.split()
        endpoint.magic = Magic(path=path, method=method)
        nomagic: NoMagic = getattr(endpoint, "nomagic", _defaults)

        _kwargs = nomagic.fastapi_kwargs or {}
        _kwargs.update(kwargs)

        module = endpoint.__module__.split(".")[-1].strip("_")

        if tags is None:
            tags = nomagic.tags

        if tags is None:
            tags = [module]

        if operation_id is None:
            operation_id = nomagic.operation_id

        if operation_id is None:
            ep = endpoint.__name__.strip("_")
            operation_id = f"{ep}_{module}"

        if response_model is None:
            response_model = signature(endpoint).return_annotation

        app.add_api_route(
            path,
            endpoint,
            name=name or nomagic.name or operation_id,
            methods=[method],
            response_model=response_model,
            operation_id=operation_id,
            tags=tags,
            **_kwargs,
        )

    return route
