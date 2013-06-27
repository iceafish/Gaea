import subprocess
import threading
import time
import filecmp
import os

proceeding = None
judge_switch = True

compile_cmd = {
    "gcc"   : "gcc ./SourceCode/%s -o ./Temp/%s -ansi -fno-asm -O2 -Wall -lm --static -DONLINE_JUDGE",
    "g++"   : "g++ ./SourceCode/%s -o ./Temp/%s -ansi -fno-asm -O2 -Wall -lm --static -DONLINE_JUDGE",
    "java"  : "javac Main.java",
    "ruby"  : "ruby -c main.rb",
    "perl"  : "perl -c main.pl",
    "pascal": 'fpc main.pas -O2 -Co -Ct -Ci',
    "go"    : '/opt/golang/bin/go build -ldflags "-s -w"  main.go',
    "lua"   : 'luac -o main main.lua',
    "python2": 'python2 -m py_compile main.py',
    "python3": 'python3 -m py_compile main.py',
}

def Killer():
    global proceeding, judge_switch

    if not proceeding.returncode:
        judge_switch = False
        proceeding.kill()
        print 'kill done.'

def Compile(judge_info):
    file_name = judge_info['source_file_name']
    executable_name = str(judge_info['_id']) + '.x'
    language_name = judge_info['language_type']
    cmd = compile_cmd[language_name] % (file_name, executable_name)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err= p.communicate()

    if not p.returncode:
        return (True, executable_name)
    return (False, err+out)

def StartTestRun(program_name, problem_id, time_limit, input_files):
    global proceeding, judge_switch

    runerr = False
    killer = threading.Timer(time_limit, Killer)

    start_time = time.time()
    killer.start()

    for item in input_files:

        if not judge_switch: break

        out_file = item.split('.')[0] + '.testout'

        data_dir = "./DataFile/%s/" % str(problem_id)
        temp_dir = "./Temp/"

        infile = open(data_dir+item, 'r')
        outfile = open(temp_dir+out_file, 'w')

        proceeding = subprocess.Popen('./'+program_name, cwd=temp_dir,
            stdin=infile, stdout=outfile, universal_newlines=True)

        proceeding.wait()

        if proceeding.returncode != 0:
            runerr = True

    total_time = time.time()-start_time

    killer.cancel()

    if runerr:
        return (False, 'runerr', total_time)

    if judge_switch:
        return (True, total_time)
    return (False, 'timeout', total_time)

def Verify(problem_id, output_files):

    data_dir = './DataFile/%s/' % str(problem_id)
    temp_dir = './Temp/'
    for item in output_files:
        runner_file = item.split('.')[0] + '.testout'
        if not filecmp.cmp(data_dir+item, temp_dir+runner_file):
            break
    else:
        return True
    return False

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

def StartJudging(info):
    global judge_switch

    res = Compile(info)

    if not res[0]:
        result = {
            'type': 'CE',
            'time_used': 0,
            'err_code': res[1]
        }
        return result

    judge_switch = True
    res = StartTestRun(res[1], info['problem_id'], info['time_limit'], info['input_files'])
    if (not res[0]) and res[1]=='timeout':
        result = {
            'type': 'TLE',
            'time_used': res[2],
            'err_code': None
        }
        return result

    if not Verify(info['problem_id'], info['output_files']):
        if res[1] == 'runerr':
            return {
                'type': 'RE',
                'time_used': res[2],
                'err_code': None
            }

        result = {
            'type': 'WA',
            'time_used': res[1],
            'err_code': None
        }
        return result

    return {
        'type': 'AC',
        'time_used': res[1],
        'err_code': None
    }

def Judger(info):
    res = StartJudging(info)
    CleanTemp()
    return res