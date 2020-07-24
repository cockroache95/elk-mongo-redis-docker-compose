from elasticsearch import Elasticsearch
from datetime import datetime
from dateutil import tz
import redis
import json
import time

def querry():
	es = Elasticsearch(['http://elastic:changeme@localhost:9200'])
	paristimezone = tz.gettz('Ho Chi Minh')
	res = es.search(index='dungnt94-2020',body={"query": {"bool":{"must":[{"range": {"@timestamp": {"gte": "now-1m","lte": "now"}}}]}}}, )

	print(json.dumps(res))

def add_log():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.lpush("history",json.dumps({"hello":"dungnt94"}))

add_log()
time.sleep(4)
querry()
