import configparser
from typing import TypedDict

config = configparser.ConfigParser()


class ProfileConfig(TypedDict):
    region: str
    output: str


def get_config_for_profile(profile: str, config_path: str) -> ProfileConfig:
    print(f"Getting configuration for profile: {profile}")
    config.read(config_path)
    profile_config: ProfileConfig = {}
    for section in config.sections():
        print(f"Section: {section}")
        print(f"Config keys: {config[section]}")
    if f"profile {profile}" in config:
        print(f"Profile {profile} config found")
        profile_config = {
            "region": config[f"profile {profile}"]["region"],
            "output": config[f"profile {profile}"]["output"]
        }
    elif "default" in config:
        print(f"Profile {profile} config found")
        profile_config = {
            "region": config["default"]["region"],
            "output": config["default"]["output"]
        }
    else:
        print(f"No config for profile {profile} found")
        profile_config = {
            "region": "us-east-1"
        }
    print(f"Profile {profile} config: {profile_config}")
    return profile_config
