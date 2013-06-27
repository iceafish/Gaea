import redis
import os
import json
from configure import redis_host
from judger import Judger


def GetRequest(queue):
    return queue.blpop('request')[1]

    '''
    return {
        '_id': 1,
        'problem_id': 1,
        'language_type': 'g++',
        'time_limit': 1,
        'memory_limit': 64,
        'source_file_name': 'tle.cpp',
        'input_files': ['1.in'],
        'output_files': ['1.out']
    }
    result = {
        'type': 'AC',
        'time_used': 1,
        'err_code'; None
    }
    '''

def GetDataFile(problem_id):
    pass

def Init(data_file_status):
    dir = './DataFile/'
    for folders in os.listdir(dir):
        tf = os.path.join(dir, folders)
        print tf
        if os.path.isdir(tf):
            data_file_status.append( int(folders) )


def LocalMain():
    queue = redis.Redis(host=redis_host)

    while True:
        info  = json.loads(GetRequest(queue))
        queue.rpush('result', json.dumps(Judger(info)))


def Main():
    queue = redis.Redis(host=redis_host)
    data_file_status = []

    Init(data_file_status)

    while True:
        info  = json.loads(GetRequest(queue))

        id = info['problem_id']

        if id not in data_file_status:
            if GetDataFile(id):
                data_file_status.append(id)
            else:
                print 'get data file %d error.' % id
                continue

        queue.rpush(json.dumps('result',Judger(info)))

if __name__ == '__main__':
    if redis_host=='localhost' or redis_host=='127.0.0.1':
        LocalMain()
    else:
        Main()