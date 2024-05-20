# tar-upload : A python module for uploading files to a running updog module

import subprocess
import tar_util
import requests
import time
import os
import re

def run_updog():

    '''Runs the 3rd party webserver that will handle web request testing'''

    directory_name = 'files'
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)
    proc = subprocess.Popen(['python3', 'tar-upload/updog/updog', '-d', directory_name])
    time.sleep(3)
    return proc

def get_path(endpoint):

    '''Part of uploading a file you need to fill out the path value in the form for uplading
    this function finds it'''

    pattern = r'(<input type="hidden" name="path" value=")(.*)(">)'

    resp = requests.get(endpoint)
    if not resp.ok:
        print('[!] Error : Could not make a request to find path')
        return None

    match = re.search(pattern, resp.text)

    if not match:
        print('[!] Error : Regex failed could not find the path in web form')

    return match.group(2)

def upload(fname, ip='127.0.0.1', port=9090, protocol='http', endpoint='/upload', label='file'):

    '''Uploads the tarball or gzip file'''

    endpoint = f'{protocol}://{ip}:{port}{endpoint}'
    path = get_path(endpoint)
    data = {'path': path}

    print(f'[+] Preparing to send {fname} to {endpoint}')

    with open(fname, 'rb') as f:
        resp = requests.post(endpoint, files={label: f}, data=data)
        if not resp.ok:
            print(f'[!] Error : Request to {endpoint} failed. Status code {resp.status_code}')
            return None
        else:
            print('[+] Success sending file.')


if __name__ == '__main__':
    proc = run_updog()

    archive_name = 'sample_1'
    tar_name = tar_util.create_tar(archive_name, 'archive')
    if tar_name == None:
        quit()
    upload(tar_name)
    tar_util.clean_sample(tar_name)

    gzip_name = 'sample_2'
    tar_name = tar_util.create_tar(gzip_name, 'gzip')
    if tar_name == None:
        quit()
    upload(tar_name)
    tar_util.clean_sample(tar_name)

    tar_util.clean_sample(archive_name)
    tar_util.clean_sample(gzip_name)

    proc.kill()

    os.system('dir files')