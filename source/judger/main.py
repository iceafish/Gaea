import redis
import os
import json
from configure import redis_host
from judge import Judge


def GetRequest(queue):
    return queue.blpop('request')[1]

def GetDataFile(problem_id):
    pass

def Init(data_file_status):
    dir = './DataFile/'
    for folders in os.listdir(dir):
        tf = os.path.join(dir, folders)
        print tf
        if os.path.isdir(tf):
            data_file_status.append( int(folders) )

def CleanTemp():
    Dir = "./Temp/"
    for files in os.listdir(Dir):
        print files
        tfile = os.path.join(Dir, files)
        if os.path.isfile(tfile):
            os.remove(tfile)
        else:
            print "delete file error."
    else:
        print 'clear done.'


def LocalMain():
    queue = redis.Redis(host=redis_host)

    while True:
        info  = json.loads(GetRequest(queue))
        msg = json.dumps(Judge(info))
        CleanTemp()
        queue.rpush('result', msg)

def Main():
    '''
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
    '''
    pass

if __name__ == '__main__':
    if redis_host=='localhost' or redis_host=='127.0.0.1':
        LocalMain()
    else:
        Main()