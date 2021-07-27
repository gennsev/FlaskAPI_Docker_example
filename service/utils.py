'''
    Utils
    =====

    Provides
      1. Functions that handle utilities for the application
'''
import hashlib
import time


def get_hash():
    ''' Get a secure hash using MD5 algorithm
    '''

    hash_base = str(time.time()).encode('utf-8')
    run_hash = hashlib.md5()
    run_hash.update(hash_base)
    return run_hash.hexdigest()
