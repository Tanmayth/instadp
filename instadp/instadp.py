#!/usr/bin/env python3

import argparse
import re
import sys
import requests
from fake_useragent import UserAgent


# Avoiding HTTP status_code 429 Error :
user_agent = UserAgent()
headers = requests.utils.default_headers()
headers.update({'User-Agent': user_agent.random})


def fetchDP(username):
    url = f"https://www.instagram.com/{username}/?__a=1"

    r = requests.get(url, headers=headers)

    if r.ok:
        data = r.json()
        return data.get('graphql').get('user').get('profile_pic_url_hd')

    else:
        print("\e[91m✘ Cannot find user ID \e[0m")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description="Download any users Instagram display picture/profile picture in full quality")

    parser.add_argument('username', action="store", help="username of the Instagram user")

    args = parser.parse_args()

    username = args.username

    file_url = fetchDP(username)
    fname = f"{username}.jpg"

    r = requests.get(file_url, stream=True)

    if r.ok:
        with open(fname, 'wb') as f:
            f.write(r.content)
            print(f"\033[92m✔ Downloaded:\033[0m {fname}")
    else:
        print("Cannot make connection to download image")


if __name__ == "__main__":
    main()
