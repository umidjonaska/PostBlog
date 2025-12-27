import redis
import orjson
import re

class RedisCLI:
    def __init__(self, redis=redis.Redis, host='localhost', port=6379, db=0):
        super(RedisCLI, self).__init__()
        self.host = host
        self.port = port
        self.db = db
        self.redis = redis

    def parse_user_string(self, user_string):
        # Regular expression to extract key-value pairs
        pattern = r"(\w+)=['\"]([^'\"]+)['\"]"
        matches = re.findall(pattern, user_string)
        return {key: value for key, value in matches}

    def connect_redis_and_get(self, hall):
        connect = self.redis(self.host, self.port, self.db)
        data = connect.get(hall)
        if not data:
            return None
        return data
    
    def set(self, hall, data):
        connect = self.redis(self.host, self.port, self.db)
        user_dict = {key: value for key, value in data.__dict__.items() if not key.startswith("_")}
        user_json = orjson.dumps(user_dict, default=str)  # `default=str` handles any non-serializable types
        connect.set(hall, user_json)
        return True

    def setex(self, hall: str, data: str, expire_time: int):
        connect = self.redis(self.host, self.port, self.db)
        user_dict = {key: value for key, value in data.__dict__.items() if not key.startswith("_")}
        user_json = orjson.dumps(user_dict, default=str)  # `default=str` handles any non-serializable types
        connect.setex(hall, expire_time ,user_json)
        return True

    def delete(self, hall):
        connect = self.redis(host=self.host, port=self.port, db=self.db)
        data = connect.get(hall)
        if data:
            data = connect.delete(hall)
        return None
