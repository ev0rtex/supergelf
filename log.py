#!/usr/bin/python
import sys
import os.path as osp
import logging
from os import environ as env

from pygelf import GelfUdpHandler

def extract_kv(s):
    return dict([x.split(':') for x in s.split()])

def merged(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r

def events(stdin, stdout):
    while True:
        # Signal ready state
        stdout.write('READY\n')
        stdout.flush()

        # Wait for an event
        line = stdin.readline()
        headers = extract_kv(line)
        payload = stdin.read(int(headers['len']))
        h, _, d = payload.partition('\n')

        yield headers, {'headers': extract_kv(h), 'data': d}

        # Signal success
        stdout.write('RESULT 2\nOK')
        stdout.flush()

def main():
    # Set up logger
    logging.basicConfig(level=logging.INFO)
    gelf_handler = GelfUdpHandler(
            host=env.get('GRAYLOG_HOST', '127.0.0.1'),
            port=int(env.get('GRAYLOG_PORT', '12201')),
            include_extra_fields=True
        )
    logger = logging.getLogger()
    logger.addHandler(gelf_handler)

    # Default record info
    defaults = {
        'name': 'supervisor_gelf',
        'level': logging.getLevelName(logging.INFO),
        'levelno': logging.INFO,
        'pathname': osp.realpath(__file__),
        'msg': '',
        'args': None,
        'exc_info': None
    }

    # Log each event
    for headers, event in events(sys.stdin, sys.stdout):
        record = merged(defaults, {
                'msg': "Supervisor event: {eventname}".format(**merged(headers, event['headers'])),
                'data': event['data'],
                'eventname': headers['eventname']
            },
            event['headers']
        )

        logger.handle(logging.makeLogRecord(record))

if __name__ == '__main__':
    main()
