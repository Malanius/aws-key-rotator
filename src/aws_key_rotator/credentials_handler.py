import configparser
from typing import List, TypedDict

config = configparser.ConfigParser()


class Credentials(TypedDict):
    key_id: str
    secret_key: str


def get_profiles(credentials_path: str) -> List[str]:
    print(f"Listing profiles from credentials file {credentials_path}.")
    config.read(credentials_path)
    profiles = config.sections()
    print(f"Found credentials for profiles: {profiles}")
    return profiles


def get_profile_credentials(profile_name: str, credentials_path: str) -> Credentials:
    print(f"Retrieving credentials for profile: {profile_name}")
    config.read(credentials_path)
    return {
        "key_id": config.get(profile_name, "aws_access_key_id"),
        "secret_key": config.get(profile_name, "aws_secret_access_key")
    }
