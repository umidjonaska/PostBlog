import redis
import orjson
from typing import Any, Optional

class RedisCLI:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        decode_responses = True,
    ):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
        )

    def get(self, key: str) -> Optional[dict]:
        data = self.client.get(key)
        if not data:
            return None
        return orjson.loads(data)

    def set(self, key: str, value: dict, expire: int | None = None) -> bool:
        data = orjson.dumps(value)
        if expire:
            self.client.setex(key, expire, data)
        else:
            self.client.set(key, data)
        return True

    def delete(self, key: str) -> bool:
        return bool(self.client.delete(key))
