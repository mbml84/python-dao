from abc import abstractmethod, ABC
from typing import Optional, Union


class CacheAdapter(ABC):

    def __init__(self, host: str, port: int, credentials: dict = None, tls_context=None):
        self._host = host
        self._port = port
        self._credentials = credentials
        self._tls_context = tls_context

    @abstractmethod
    def set(self, key: Union[str, bytes], value: bytes, cache_time: int) -> None:
        pass

    @abstractmethod
    def get(self, key) -> Optional[dict]:
        pass
