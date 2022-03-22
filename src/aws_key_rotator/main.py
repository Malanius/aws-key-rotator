import boto3

import credentials_handler
import config_handler


credentials_path = "./.aws/credentials"
config_path = "./.aws/config"

for profile in credentials_handler.get_profiles(credentials_path):
    profile_credentials = credentials_handler.get_profile_credentials(
        profile, credentials_path)
    profile_config = config_handler.get_config_for_profile(
        profile, config_path)

    print(f"Getting identity for profile {profile}")

    sts = boto3.client('sts', region_name=profile_config["region"],
                       endpoint_url="http://localhost:4566",
                       aws_access_key_id=profile_credentials["key_id"],
                       aws_secret_access_key=profile_credentials["secret_key"],
                       )
    identity = sts.get_caller_identity()
    original_user_arn = identity["Arn"]
    print(f"Identity: {identity}")

    old_iam = boto3.client('iam', region_name=profile_config["region"],
                           endpoint_url="http://localhost:4566",
                           aws_access_key_id=profile_credentials["key_id"],
                           aws_secret_access_key=profile_credentials["secret_key"],
                           )

    new_access_key = old_iam.create_access_key()['AccessKey']
    print(f'New key: {new_access_key}')

    new_sts = boto3.client('sts', region_name=profile_config["region"],
                           endpoint_url="http://localhost:4566",
                           aws_access_key_id=new_access_key["AccessKeyId"],
                           aws_secret_access_key=new_access_key["SecretAccessKey"],
                           )
    new_iam = boto3.client('iam', region_name=profile_config["region"],
                           endpoint_url="http://localhost:4566",
                           aws_access_key_id=new_access_key["AccessKeyId"],
                           aws_secret_access_key=new_access_key["SecretAccessKey"],
                           )
    new_identity = sts.get_caller_identity()
    new_user_arn = new_identity["Arn"]
    print(f"New identity: {new_identity}")
    assert original_user_arn == new_user_arn

    credentials_handler.update_profile_credentials(new_access_key["AccessKeyId"],
                                                   new_access_key["SecretAccessKey"],
                                                   profile, credentials_path)

    old_iam.delete_access_key(AccessKeyId=profile_credentials["key_id"])

    print(f"Deleting access old key for profile {profile}...")
    access_keys = new_iam.list_access_keys()
    print(f"Deleted access old key for profile {profile}")
    print(f"Profile {profile} access keys: {access_keys}")
