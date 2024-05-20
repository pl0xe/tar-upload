import os
import tarfile

def clean_sample(fname):

    '''Prepare for the upload by ensuring old file does not exist and deleting it so
    the process starts cleanly everytime.'''

    if os.path.isfile(fname):
        try:
            os.remove(fname)
            return True
        except FileNotFoundError as e:
            print(f'[-] Warning : Could not find file {fname} but marked as existing.')
        except OSError as e:
            print(f'[!] Error : OS could not delete file, may be in use. {e}')
        except Exception as e:
            print(f'[!] Error : Unknown error occured while deleting file {e}')
        return None

def create_bin(fname):

    '''Creates a basefile with random binary data in it to be tar'd or gzipped'''

    length = 0xFFFF
    sample_data = os.urandom(length)

    clean_sample(fname)

    try:
        with open(fname, 'wb') as f:
            written = f.write(sample_data)
    except Exception as e:
        print('[!] Error : Can not create file {fname} {e}')
        return None
    
    return written

def translate_mode(mode):
    
    tarmodes = ['archive', 'gzip']

    if mode == None:
        print('[!] Error : Select a tar mode to use {tarmodes}')
        return None
    
    if mode not in tarmodes:
        print('[!] Error : Invalid tar mode, use {tarmodes}')
        return None
    
    match mode:
        case 'archive':
            return 'x'
        case 'gzip':
            return 'w:gz'
        case _:
            print('[!] Error : Could not set {mode}')
            return None

def create_tar(fname, mode):

    '''Creates a random tarball to be uploaded to the server'''

    tarname = fname + '.tar'

    if mode == 'gzip':
        tarname += '.gz'

    # ensures the previous binary was deleted if it exists
    clean_sample(fname)
    clean_sample(tarname)

    # creates binary with random bytes in it for user to tar
    print(f'[+] Creating file {fname}')
    if create_bin(fname) == None:
        print('[!] Error : Could not create bin')
        return None

    # set the tar utility to either archive or gzip the binary
    mode = translate_mode(mode)
    print(f'[+] Setting tar mode : {mode}')
    if not mode:
        return None

    # creates the tar by adding the binary
    print(f'[+] Creating tar file {tarname}')
    try:
        with tarfile.open(name=tarname, mode=mode) as tar:
            tar.add(fname)
            tar.close()
            print('[+] Tar creation success')
            return tarname
    except Exception as e:
        print(f'[!] Error could not create tar file {e}')
        return None        