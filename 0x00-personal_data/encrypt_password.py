#!/usr/bin/env python3
'''
Implementing a hash_password function that accept one
argument password and returns a salted, hashed password
which is a byte string
'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''
    Function to hash and salt a password
    '''
    # convert the password to an array of bytes
    bytes = password.encode('utf-8')

    # generate salt
    salt = bcrypt.gensalt()

    # hash the password
    hashed_password = bcrypt.hashpw(bytes, salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    Function to validate password
    '''
    # Converting password into an array
    user_password = password.encode('utf-8')

    # check if password matches
    result = bcrypt.checkpw(user_password, hashed_password)

    return result
