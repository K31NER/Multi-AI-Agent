import redis

r = redis.Redis(host="localhost",
                        port=6379,db=0,
                        encoding="utf-8",
                        decode_responses=True)


for key in r.scan_iter(match='*'):
    print(key)


print(r.lrange("history:💵 Financiero",start=0,end=-1))
