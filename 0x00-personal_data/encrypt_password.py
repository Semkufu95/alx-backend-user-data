#!/usr/bin/env python3
'''
Implementing a hash_password function that accept one
argument password and returns a salted, hashed password
which is a byte string
'''

import bcrypt


def hash_password(password):
    '''
    Function to hash and salt a password
    '''
    # convert the password to an array of bytes
    bytes = password.encode('utf-8')

    # generate salt
    salt = bcrypt.gensalt()

    # hash the password
    hash = bcrypt.hashpw(bytes, salt)

    return hash
