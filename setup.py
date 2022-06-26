#!/usr/bin/python3
import subprocess, sys

def install(lib) -> bool:
    try:
        subprocess.check_call(f'{sys.executable} -m pip install {lib}')
        return True
    except subprocess.CalledProcessError:
        print(f'Process failed to execute properly. SUBPROCESS ERROR CODE: {subprocess.CalledProcessError.output}')
        return False

if __name__ == '__main__':
    with open('req.txt', 'r') as file:
        requirements = file.readlines()
        for req in requirements:
            req = req.replace('\n', '')
            install(req)
        file.close()
        print('\033[1;32m' + 'Happy hacking!')