#!/usr/bin/env python3
'''
A function to return the log message obfuscated
'''

import re


def filter_datum(fields, redaction, message, separator):
    pattern = f"({'|'.join(map(re.escape, fields))})=.+?{separator}"
    return re.sub(pattern,
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)