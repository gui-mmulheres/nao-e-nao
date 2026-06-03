from msal import SerializableTokenCache


class RedisTokenCache:
    def __init__(self, redis_client, key):
        self.redis = redis_client
        self.key = key

    def load(self):
        cache = SerializableTokenCache()

        data = self.redis.get(self.key)

        if data:
            cache.deserialize(data)

        return cache

    def save(self, cache):
        if cache.has_state_changed:
            self.redis.set(
                self.key,
                cache.serialize()
            )
