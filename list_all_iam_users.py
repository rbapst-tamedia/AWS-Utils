'''List ALL AWS IAM Users'''
import boto3

def get_aws_profiles():
    aws_profiles = {
        '20min': 'eu-central-1',
        '20min': 'eu-central-1',
        '20min-dev': 'eu-central-1',
        '20min-sandbox': 'eu-central-1',
        'dai-sandbox': 'eu-central-1',
        'disco': 'eu-central-1',
        'disco-dev': 'eu-central-1',
        'disco-sandbox': 'eu-central-1',
        'ness': 'eu-central-1',
        'pmd-com': 'eu-central-1',
        'pmd-com-dev': 'eu-central-1',
        'sfmc': 'eu-central-1',
        'sfmc-dev': 'eu-central-1',
        'titan': 'eu-central-1',
        'titan-dev': 'eu-central-1',
        'unity': 'eu-central-1',
        'unity-demo': 'eu-central-1',
        'unity-dev': 'eu-central-1',
        'unity-preprod': 'eu-central-1',
        'unity-sandbox': 'eu-central-1'
        }
    return aws_profiles

def get_users():
    '''Returns the Users in the AWS account'''
    users = []
    for user in boto3.client('iam').list_users()['Users']:
        users.append(user)
    return users

def get_access_key(username):
    '''Returns the Users access keys'''
    access_keys = []
    for access_key in boto3.client('iam').list_access_keys(
            UserName = username)['AccessKeyMetadata']:
        access_keys.append(access_key['AccessKeyId'])
    return access_keys

if __name__ == "__main__":
    for aws_profile, aws_region in get_aws_profiles().items():
        boto3.setup_default_session(region_name=aws_region, profile_name=aws_profile)
        print('Profile\tUser\tUserId\tKeysId')
        for user in get_users():
            for key in get_access_key(user['UserName']):
                print("\t".join([aws_profile, user['UserName'], user['UserId'], key]))
