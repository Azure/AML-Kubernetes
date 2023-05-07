from logging import getLogger
import argparse
from utils import config_logging, read_yaml, write_yaml_file, hash_string
from microsoft_graph import get_group_transitive_members_by_group_id, get_user_oid_by_mail, get_token

logger = getLogger(__name__)
userIdentifiers = []
crTemplateFilePath = "./quotaoverridesCRTemplate.yaml"


def add_unique_identifier(identifier):
    if identifier not in userIdentifiers:
        userIdentifiers.append(identifier)


def process_identities(identities):
    users, groups = identities.get('users', []), identities.get('groups', [])    

    token = get_token()
    
    for user in users:
        logger.info(f"processing user {user}")
        user_oid = get_user_oid_by_mail(user, token)
        add_unique_identifier(hash_string(user_oid))

    for group in groups:
        logger.info(f"processing group {group}")
        for member in get_group_transitive_members_by_group_id(group, token):
            add_unique_identifier(hash_string(member))


def get_quotaoverride_cr(args):
    config_file, output_file, name = args.config, args.output, args.name

    config, output = read_yaml(config_file), read_yaml(crTemplateFilePath)

    output['metadata']['name'] = name
    output['metadata']['labels']['app.kubernetes.io/instance'] = name
    output['spec']['tierOverrides'] = config['tierOverrides']
    process_identities(config['userIdentifiers'])
    output['spec']['userIdentifiers'] = userIdentifiers

    write_yaml_file(output_file, output)

    logger.info(f"generated quotaoverrides custom resource file, file path : {output_file} ")

    
def main():
    config_logging()

    parser = argparse.ArgumentParser(description='give a config yaml, generate quotaoverrides custom resource yaml, suggests to run [az login] first before using the command')

    parser.add_argument('--config', required=True, help="yaml file path of user's quota override config file")
    parser.add_argument('--output', required=True, help="yaml file path of generated k8s quotaoverrides custom resource file")
    parser.add_argument('--name', required=True, help="name of quotaoverrides custom resource")

    parser.set_defaults(func=get_quotaoverride_cr)	

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
