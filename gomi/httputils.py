from __future__ import annotations

__all__ = ["get1", "getAsyncN", "getSyncN"]


import asyncio
import warnings
from pathlib import Path
import importlib.util
from typing import Optional
from functools import partial

from .helpers import indexD

__gomi = Path(importlib.util.find_spec("gomi").origin).parent
__file = Path(__file__).relative_to(__gomi).with_suffix("").as_posix()

try:
    import requests
except ImportError:
    warnings.warn(f"{__file}: Missing requests.")

try:
    import httpx
except ImportError:
    warnings.warn(f"{__file}: Missing httpx.")

try:
    import asynciolimiter
except ImportError:
    warnings.warn(f"{__file}: Missing asynciolimiter.")

try:
    from tqdm.asyncio import tqdm_asyncio as tqdm
except ImportError:
    warnings.warn(f"{__file}: Missing tqdm.asyncio.")


_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"


def _addUA(params: dict, user_agent: str = _USER_AGENT) -> dict:
    if isinstance((headers_key := indexD(params, "headers")), str):
        if isinstance(useragent_key := indexD(params[headers_key], "user-agent"), str):
            pass
        else:
            params[headers_key]["User-Agent"] = user_agent
    else:
        params["headers"] = {"User-Agent": user_agent}
    return params


def get1(url: str, **kwargs) -> requests.Response:
    kwargs = _addUA(kwargs)
    return requests.get(url, **kwargs)


async def _getAsyncN_v1(
    urls: list[str],
    _rate: Optional[int] = None,
    _tqdm: bool = False,
    **kwargs,
) -> list[httpx.Response]:

    gather = asyncio.gather
    if _tqdm and "tqdm" in globals():
        gather = partial(tqdm.gather, ascii=True)
    elif _tqdm:
        warnings.warn("Missing tqdm. Ignoring given tqdm option.")

    if "asynciolimiter" in globals() and _rate is not None:
        limiter = asynciolimiter.Limiter(_rate)
        async with httpx.AsyncClient() as client:
            return await gather(*[limiter.wrap(client.get(url, **kwargs)) for url in urls])
    else:
        if _rate is not None:
            warnings.warn(f"Missing asynciolimiter. Ignoring given rate limit {_rate}.")
        async with httpx.AsyncClient() as client:
            return await gather(*[client.get(url, **kwargs) for url in urls])

async def _getAsyncN_v2(
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

    limit = httpx.Limits(max_connections=_rate)
    timeout = httpx.Timeout(timeout=_timeout, connect=10)
    async with httpx.AsyncClient(limits=limit, timeout=timeout) as client:
        return await gather(*[client.get(url, **kwargs) for url in urls])



async def _getAsyncN(
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


def getAsyncN(urls: list[str], _rate: Optional[int] = None, _tqdm: bool = False, **kwargs) -> list[httpx.Response]:
    kwargs = _addUA(kwargs)
    return asyncio.run(_getAsyncN(urls, _rate=_rate, _tqdm=_tqdm, **kwargs))


def _getSyncN(urls: list[str], **kwargs) -> list[httpx.Response]:
    with httpx.Client() as session:
        return [session.get(url, **kwargs) for url in urls]


def getSyncN(urls: list[str], **kwargs) -> list[httpx.Response]:
    kwargs = _addUA(kwargs)
    return _getSyncN(urls, **kwargs)
