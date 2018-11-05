#!/usr/bin/env python3

import requests
import re
import urllib.request
import sys
import argparse

# Maybe we could just check if response is 404?
UserNotFound = "<h2>Sorry, this page isn&#39;t available.</h2>"
# spinnerFrames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']


def getID(username):
    url = "https://www.instagram.com/{}"

    r = requests.get(url.format(username))

    html = r.text

    if UserNotFound in html:
        print("\033[91m✘ Invalid username\033[0m")
        sys.exit()

    return re.findall('"id":"(.*?)",', html)[0]


def fetchDP(userID):
    url = "https://i.instagram.com/api/v1/users/{}/info/"

    try:
        r = requests.get(url.format(userID))
    except requests.ConnectionError:
        print("\033[91m✘ Connection error\033[0m")
        sys.exit()

    data = r.json()

    return data["user"]["hd_profile_pic_url_info"]["url"]


def main():
    desc = (
        "Download any user's Instagram display profile "
        "picture in full quality"
    )
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "username", action="store", help="username of the Instagram user"
    )

    args = parser.parse_args()

    username = args.username

    userID = getID(username)
    file_url = fetchDP(userID)
    fname = "{}.jpg".format(username)

    urllib.request.urlretrieve(file_url, fname)
    print("\033[92m✔ Downloaded:\033[0m {}".format(fname))


if __name__ == "__main__":
    main()
