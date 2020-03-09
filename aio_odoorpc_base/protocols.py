import sys


if sys.version_info >= (3, 8, 0):

    from typing import Callable, Mapping, Protocol, Union

    class ProtoAsyncResponse(Protocol):
        async def json(self) -> Mapping:
            ...


    class ProtoResponse(Protocol):
        def json(self) -> Mapping:
            ...


    class ProtoAsyncHttpClient(Protocol):
        async def post(self, url: str, *, json: Mapping) -> Union[ProtoResponse, ProtoAsyncResponse]:
            ...


    class ProtoHttpClient(Protocol):
        def post(self, json: Mapping) -> ProtoResponse:
            ...

    T_AsyncResponse = Union[ProtoResponse, ProtoAsyncResponse]
    T_AsyncHttpClient = Union[Callable[[Mapping], T_AsyncResponse], ProtoAsyncHttpClient]
    T_Response = ProtoResponse
    T_HttpClient = Union[Callable[[Mapping], ProtoResponse], ProtoHttpClient]
else:
    from typing import Any
    
    T_AsyncResponse = Any
    T_AsyncHttpClient = Any
    T_Response = Any
    T_HttpClient = Any