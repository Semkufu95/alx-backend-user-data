#!/usr/bin/env python3
'''
A function to return the log message obfuscated
'''

import os
import re
import logging
from typing import List, Tuple
import mysql.connector
from mysql.connector.connection import MySQLConnection


PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    ''' return obfuscated log message '''
    pattern = f"({'|'.join(map(re.escape, fields))})=.+?{separator}"
    return re.sub(pattern,
                  lambda m: f"{m.group(1)}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
        initialize the formatter with fields to redact
        '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields: List[str] = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        Format a log record redacting sensitive fields
        '''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    '''
    Function taking no arguments but creates and
    configures a logger for user data
    '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    '''create and configure streamHandler '''
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    '''
    Connects to a secure database using credentials from environment variable
    '''
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    if not database:
        raise ValueError(
            "The Database must be set in the environment variable "
            "PERSONAL_DATA_DB_NAME")

    # create and return the database connection
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main() -> None:
    '''
    Main function to query user data and log it with sensitive fields redacted
    '''
    logger = get_logger()

    with get_db() as db:
        with db.cursor as cursor:
            cursor.execute("SELECT * FROM users")

            # Define columns to match the database layout
            columns = ('name', 'email', 'phone', 'ssn', 'password')

            # process and log each row
            for row in cursor:
                # create a log message with cursor from the database row
                row_dict = dict(zip(columns, row))
                message = "; ".join(f"{key}={value}" for key,
                                    value in row_dict.items()) + ";"
                logger.info(message)

                
if __name__ == '__main__':
    main()
