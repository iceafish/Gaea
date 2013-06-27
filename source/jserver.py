import os
import json
import redis
import pymongo
import threading
import time

class RequestListenerThreading(threading.Thread):

    def __init__(self, p, mongodb, redisdb):
        threading.Thread.__init__(self)
        self.mongo_db = mongodb
        self.redis_db = redisdb
        self.period = p

    def scanner(self):
        requests = self.mongo_db.find({'result': None})

        '''
        {
            "_id": self.getNextSequence(),
            "problem_id": int(problem_id),
            "language_id": int(self.get_argument("language")),
            "user_name": self.current_user,
            "submit_date": time.ctime(),
            "result": None
        }
        {
            '_id': 1,
            'problem_id': 1,
            'language_type': 'g++',
            'time_limit': 1,
            'memory_limit': 64,
            'source_file_name': 'tle.cpp',
            'input_files': ['1.in'],
            'output_files': ['1.out']
        }
        '''

        for item in requests:

            req = {
                '_id': item['_id'],
                'problem_id': item['problem_id'],
                'language_type': item['language_type'],
                'time_limit': item['']
            }


    def run(self):
        while True:
            self.scanner()
            time.sleep(self.period)


def main():

    request_db = pymongo.Connection('localhost',27017)
    sync_queue = redis.Redis(host='localhost')


if __name__ == '__main':
    main()