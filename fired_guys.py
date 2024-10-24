import argparse
import os
import requests
import datetime


def get_cohorts(members, display_name, count):
    for i in range(len(members)):
        member = members[i]
        if member['profile']['display_name'] == display_name:
            min = i - count if (i - count) > 0 else 0
            max = i + count if (i + count) < len(members) else len(members) - 1
            return members[min:max]

    return []


def _is_member_deactivated(member: dict) -> bool:
    if not member["deleted"]:
        return False

    if "enterprise_user" in member:
        # some users are showing as deleted in the API response, but it seems like they're
        # still active if they have teams under enterprise_user
        return not member["enterprise_user"]["teams"]
    return True


def run(count=5, slack_id=None):
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    r = requests.get('https://slack.com/api/users.list?token={}'.format(SLACK_TOKEN))
    response_dict = r.json()
    members = response_dict['members']
    deleted = [member for member in members if _is_member_deactivated(member)]
    deleted.sort(key=lambda member: member['updated'])
    for i in range(-min(count, len(deleted)), 0):
        print('{} - updated at {}'.format(deleted[i]['profile']['real_name'], datetime.datetime.fromtimestamp(deleted[i]['updated'])))

    if slack_id:
        print('----')
        cohorts = get_cohorts(members, slack_id, count)
        for cohort in cohorts:
            print('{} - Current Status: {}'.format(cohort['profile']['real_name'],
                                                   'Terminated' if cohort['deleted'] else 'Active'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--count',
        help='Number of most recent fired guys to print',
        default=5,
    )
    parser.add_argument(
        '--slack_id',
        help='Enter your slack id if you want to see the status of those who joined around the same time as you.',
        default=None,
    )
    args = parser.parse_args()
    count = int(args.count)
    slack_id = args.slack_id
    run(count, slack_id)
