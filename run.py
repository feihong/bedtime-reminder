import os
import sys
from pathlib import Path
import json
from pprint import pprint
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

import hjson
import arrow
import boto3


here = Path(__file__).parent

log_file = here / 'log.txt'
handlers = [
    RotatingFileHandler(log_file, maxBytes=1024, backupCount=1),
    # logging.StreamHandler(),
]
logging.basicConfig(
    handlers=handlers, level=logging.DEBUG, format='%(asctime)s: %(message)s')

config_file = here / 'config.hjson'
config = hjson.load(config_file.open())


def send_text(number, message):
    aws = config['aws']
    client = boto3.client(
        'sns',
        region_name='us-east-1',
        aws_access_key_id=aws['access_key'],
        aws_secret_access_key=aws['secret_key'],
    )

    resp = client.publish(
        PhoneNumber=number,
        Message=message,
        MessageAttributes={
            'SMSType': {
                'StringValue': 'Promotional',
                'DataType': 'String',
            }
        }
    )
    # pprint(resp)
    status_code = resp['ResponseMetadata']['HTTPStatusCode']
    return status_code == 200


def is_time_to_send(time_str, timezone):
    """
    When given time is within 60 seconds of current time, return True.

    """
    now = arrow.now(timezone)
    dt = arrow.get(time_str, 'HH:mm')
    dt = now.replace(hour=dt.hour, minute=dt.minute)
    delta = now - dt
    return delta.seconds <= 60


if __name__ == '__main__':
    number = sys.argv[1]
    time_str = sys.argv[2]
    timezone = config['time_zone']

    if is_time_to_send(time_str, timezone):
        success = send_text(number, "It's time to go to sleep! You have a busy day tomorrow.")
        if success:
            logging.info('Successfully sent text message')
    else:
        logging.info('It is not {}, so text message was not sent'.format(time_str))
