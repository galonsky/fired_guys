import os
import json
import requests
import datetime

def run(count=5):
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    r = requests.get('https://slack.com/api/users.list?token={}'.format(SLACK_TOKEN))
    response_dict = r.json()
    members = response_dict['members']
    deleted = [member for member in members if member['deleted']]
    deleted.sort(key=lambda member: member['updated'])
    for i in range(-count, 0):
        print('{} - updated at {}'.format(deleted[i]['profile']['real_name'], datetime.datetime.fromtimestamp(deleted[i]['updated'])))


if __name__ == '__main__':
    run()
