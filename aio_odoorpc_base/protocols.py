from typing import Awaitable, Callable, Mapping, Protocol, Union


class ProtoAsyncResponse(Protocol):
    async def json(self) -> Mapping:
        ...


class ProtoResponse(Protocol):
    def json(self) -> Mapping:
        ...


class ProtoAsyncHttpClient(Protocol):
    async def post(self, url: str, *, json: Mapping) -> ProtoResponse or ProtoAsyncResponse:
        ...


class ProtoHttpClient(Protocol):
    def post(self, json: Mapping) -> ProtoResponse:
        ...


T_AsyncResponse = Union[ProtoResponse, ProtoAsyncResponse]
T_AsyncHttpClient = Union[Callable[[Mapping], Awaitable[T_AsyncResponse]], ProtoAsyncHttpClient]
T_Response = ProtoResponse
T_HttpClient = Union[Callable[[Mapping], ProtoResponse], ProtoHttpClient]
