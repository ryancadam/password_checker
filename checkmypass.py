import requests
import hashlib
import sys


def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range//" + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, check the api and give it another go")
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first_five_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first_five_char)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f"Dude, your password {password} was found {count} number of times. You should probably come up with a different one.")
        else:
            print(f"Your password \"{password}\" was not found. Woo-hoo!")
        return "done!"

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
