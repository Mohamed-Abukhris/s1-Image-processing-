import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching data: {res.status_code},  check the api and try again")
    return res

def get_password_leaks_count(hashes , hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pass[:5], sha1pass[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response,tail)

def quick_strength_hint(password):
    tips = []
    if len(password) < 12:
        tips.append("use at least 12 characters")
    if password.islower() or password.isupper():
        tips.append("mix uppercase and lowercase letters")
    if password.isalpha() or password.isdigit():
        tips.append("add numbers and special characters")
    if tips:
        return " • Quick hint: " + ", ".join(tips) + "."
    else:
        return "Looks strong!"

def main():
    password = input('Enter your password: ')
    count = pwned_api_check(password)
    print(quick_strength_hint(password))
    if count:
        print(f'{password} is leaked {count} times.. change your password')
    else:
        print(f'{password} was NOT found.')

if __name__ == '__main__':
    sys.exit(main())