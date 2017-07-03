# Bedtime Reminder

Server-side script that sends a text message to remind you to go to bed. The
time you choose to send the message is locked to a particular timezone, so daylight
savings will not disrupt the operation of this script.

## Installation

```
mkvirtualenv -p python3 bedtime
pip install -r requirements.txt
```

## Config file

config.hjson

```
{
  time_zone: US/Central
  aws: {
    access_key: <your access key>
    secret_key: <your secret key>
  }
}
```

## Shell script

bedtime-reminder.sh

```bash
source ~/.virtualenvs/bedtime/bin/activate
cd /path/to/app
python run.py +15551112222 21:00
```

## Crontab entry

Run every hour, on the hour

```
0 * * * * source ~/bin/bed-time-reminder.sh
```
