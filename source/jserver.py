import os
import json
import redis
import pymongo
import threading
import time

class MongoScannerThreading(threading.Thread):

    def __init__(self, p, mongodb, redisdb):
        threading.Thread.__init__(self)
        self.mongo_db = mongodb
        self.redis_db = redisdb
        self.period = p

    def scanner(self):
        requests = self.mongo_db.judge_queues.find({'result': None})

        for item in requests:
            problem = self.mongo_db.problems.find_one({'_id': item['problem_id']})
            req = {
                '_id': item['_id'],
                'problem_id': item['problem_id'],
                'language_type': item['language_type'],
                'time_limit': problem['time_limit'],
                'memory_limit': 64,
                'source_file_name': item['code_file'].split('/')[-1],
                'input_files': problem['input_data'],
                'output_files': problem['output_data']
            }
            print req
            self.redis_db.rpush('request', json.dumps(req))

    def run(self):
        while True:
            print 'scanner start...'
            self.scanner()
            time.sleep(self.period)

class ResultListenerThreading(threading.Thread):

    def __init__(self):
        pass

    def run(self):
        pass

def AddRequest():
    pass

def main():
    request_db = pymongo.Connection('localhost',27017).Gaea
    sync_queue = redis.Redis(host='localhost')

    scan_threading = MongoScannerThreading(120, request_db, sync_queue)
    scan_threading.start()

if __name__ == '__main__':
    main()