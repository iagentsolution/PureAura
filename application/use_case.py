from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

Request = TypeVar("Request")
Response = TypeVar("Response")


class UseCase(
    ABC,
    Generic[
        Request,
        Response,
    ],
):
    """
    Base class for every application use case.

    A use case exposes a single asynchronous entry point and
    returns the response type declared by each implementation.
    """

    @abstractmethod
    async def execute(
        self,
        request: Request,
    ) -> Response:
        ...