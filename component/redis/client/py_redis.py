from redis import StrictRedis

host = "127.0.0.1"
port = 6379
password = 'fy123456'
redis = StrictRedis(host=host, port=port, db=0, password=password)
redis.set('name', 'Bob')
print(redis.get('name'))

rd_keys = rd.keys("rms/room/*total")
print(rd_keys)
if len(rd_keys) > 1:
    redis.get(rd_keys[0])

# redis.getrange()


redis.hexists("room", "a")