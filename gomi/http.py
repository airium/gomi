from __future__ import annotations

__all__ = ["get1", "getN", "async_getN"]


import asyncio
import warnings
from typing import Optional
from functools import partial

import httpx
import requests
import asynciolimiter
from tqdm.asyncio import tqdm_asyncio as tqdm

from .helpers import getkey
from .__conf import _USER_AGENT


def __add_useragent(req_params: dict, user_agent: str = _USER_AGENT) -> dict:
    if isinstance((headers_key := getkey(req_params, "headers", case_sensitive=False)), str):
        if isinstance(getkey(req_params[headers_key], "user-agent", case_sensitive=False), str):
            pass
        else:
            req_params[headers_key]["User-Agent"] = user_agent
    else:
        req_params["headers"] = {"User-Agent": user_agent}
    return req_params


def get1(url: str, **kwargs) -> requests.Response:
    kwargs = __add_useragent(kwargs)
    return requests.get(url, **kwargs)


async def __async_getN_impl(
    urls: list[str],
    _rate: Optional[int] = None,
    _timeout: Optional[float] = None,
    _tqdm: bool = False,
    **kwargs,
) -> list[httpx.Response]:

    gather = asyncio.gather
    if _tqdm and "tqdm" in globals():
        gather = partial(tqdm.gather, ascii=True)
    elif _tqdm:
        warnings.warn("Missing tqdm. Ignoring given tqdm option.")

    timeout = httpx.Timeout(timeout=_timeout, connect=10)
    if "asynciolimiter" in globals() and _rate is not None:
        limiter = asynciolimiter.Limiter(_rate)
        async with httpx.AsyncClient(timeout=timeout) as client:
            return await gather(*[limiter.wrap(client.get(url, **kwargs)) for url in urls])
    else:
        if _rate is not None:
            warnings.warn(f"Missing asynciolimiter. Ignoring given rate limit {_rate}.")
        async with httpx.AsyncClient(timeout=timeout) as client:
            return await gather(*[client.get(url, **kwargs) for url in urls])


def async_getN(urls: list[str], _rate: Optional[int] = None, _tqdm: bool = False, **kwargs) -> list[httpx.Response]:
    kwargs = __add_useragent(kwargs)
    return asyncio.run(__async_getN_impl(urls, _rate=_rate, _tqdm=_tqdm, **kwargs))


def __getN_impl(urls: list[str], **kwargs) -> list[httpx.Response]:
    with httpx.Client() as session:
        return [session.get(url, **kwargs) for url in urls]


def getN(urls: list[str], **kwargs) -> list[httpx.Response]:
    kwargs = __add_useragent(kwargs)
    return __getN_impl(urls, **kwargs)
