"""Breach check using the Have I Been Pwned 'range' API (k-anonymity).

Only the first 5 characters of the SHA-1 hash leave this server.
The full password and the full hash are never sent anywhere.
"""
import hashlib

import requests

API_URL = "https://api.pwnedpasswords.com/range/"


def check_breach(password):
    """Return how many times the password appears in known breaches.

    Returns 0 if it was not found. Raises requests.RequestException
    if the breach service cannot be reached.
    """
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    response = requests.get(API_URL + prefix, timeout=5)
    response.raise_for_status()

    # Each line looks like  SUFFIX:COUNT
    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0
