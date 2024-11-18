#!/usr/bin/env python3
'''
A function to return the log message obfuscated
'''

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' return obfuscated log message '''
    pattern = f"({'|'.join(map(re.escape, fields))})=.+?{separator}"
    return re.sub(pattern,
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)
