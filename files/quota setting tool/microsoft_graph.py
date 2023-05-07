from logging import getLogger
import subprocess, json, requests

logger = getLogger(__name__)

def get_token():
    exitcode, data = subprocess.getstatusoutput('az account get-access-token --resource-type ms-graph')
    if exitcode != 0:
        logger.exception(data)
        raise Exception('Exception in get-access-token')
    
    token = json.loads(data)['accessToken']
    
    logger.info('get ms-graph access token : {}'.format(token))
    return token


def _send_request(url, token):
    try:
        logger.info('sending url : {}'.format(url))

        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Host': 'graph.microsoft.com'
        }
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        response_json = response.json()
    except Exception as err:
        raise SystemExit(err)
    else:
        return response_json


def _iter_objects(url, token):
    while url is not None:
        response_json = _send_request(url, token)

        objects = response_json.get('value')
        logger.info('Fetched {} objects from {}'.format(len(objects), url))

        yield from objects
        url = response_json.get('@odata.nextLink')


def get_group_transitive_members_by_group_id(group_id, token):
    logger.info('get ms-graph group transitive members, group id : {}'.format(group_id))

    url = 'https://graph.microsoft.com/v1.0/groups/{}/transitiveMembers'.format(group_id)

    member_oids = []
    for member in _iter_objects(url, token):
        if member['@odata.type'] == '#microsoft.graph.user':
            member_oids.append(member['id'])

    return member_oids


def get_user_oid_by_mail(mail, token):
    logger.info('get ms-graph user oids, user mail : {}'.format(mail))

    url = 'https://graph.microsoft.com/v1.0/users/{}'.format(mail)

    response_json = _send_request(url, token)
    return response_json['id']
