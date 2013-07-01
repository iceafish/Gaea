import lorun
import os
import subprocess

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

RESULT_STR = [
    'Yes',
    'Presentation Error',
    'Time Limit Exceeded',
    'Memory Limit Exceeded',
    'Wrong Answer',
    'Runtime Error',
    'Output Limit Exceeded',
    'Compile Error',
    'System Error'
]

def Compile(id, file_name, language_name):
    executable_name = "%d.x" % id
    cmd = compile_cmd[language_name] % (file_name, executable_name)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err= p.communicate()

    if not p.returncode:
        return (True, executable_name)
    return (False, err+out)

def RunOne(runcfg, in_path, out_path, temp_path):
    fin = file(in_path)
    ftemp = file(temp_path, 'w')

    runcfg['fd_in'] = fin.fileno()
    runcfg['fd_out'] = ftemp.fileno()

    rst = lorun.run(runcfg)
    fin.close()
    ftemp.close()

    if rst['result'] == 0:
        ftemp = file(temp_path)
        fout = file(out_path)
        crst = lorun.check(fout.fileno(), ftemp.fileno())
        fout.close()
        ftemp.close()
        os.remove(temp_path)
        if crst != 0:
            return {'result':crst}

    return rst

def Judge(request_info):
    res = Compile(request_info['_id'], request_info['source_file_name'], request_info['language_type'])
    if not res[0]:
        result = {
            '_id': request_info['_id'],
            'type': 'Compile Error',
            'time_used': 0,
            'memory_used': 0,
            'err_code': res[-1]
        }
        return result

    exe_file = res[-1]
    files = request_info['data_files']

    data_dir = "./DataFile/%s/" % str(request_info['problem_id'])
    temp_dir = "./Temp/"
    tempfile = temp_dir + 'temp.out'
    record = {
        '_id': request_info['_id'],
        "time_used": 0,
        "memory_used": 0,
        "type": None,
        "err_code": None
    }
    for item in files:
        data_path = data_dir + item
        infile = data_path + '.in'
        outfile = data_path + '.out'
        runcfg = {
            'args':[temp_dir + exe_file],
            'timelimit':request_info['time_limit']*1000,
            'memorylimit':request_info['memory_limit']
        }
        rst = RunOne(runcfg, infile, outfile, tempfile)

        print rst

        if not rst['result']:
            if not record['type']:
                record['type'] = RESULT_STR[rst['result']]
                record['time_used'] = rst['timeused']
                record['memory_used'] = rst['memoryused']
            else:
                if rst['timeused'] > record['time_used']:
                    record['time_used'] = rst['timeused']
                if rst['memoryused'] > record['memory_used']:
                    record['memory_used'] = rst['memoryused']
        else:
            record['type'] = RESULT_STR[rst['result']]
            break
    else:
        if not record['type']:
            record['type'] = 'Yes'

    return record
