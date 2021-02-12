import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'

def get_forms(url):
    soup = bs(requests.get(url).content, 'html.parser')
    return soup.find('form')

def get_form_details(form):
    details = {}
    action = form.attrs.get('action').lower()
    method = form.attrs.get('method', 'get').lower()
    inputs = []

    for i in form.find_all('input'):
        input_type = i.attrs.get('type', 'text')
        input_name = i.attrs.get('name')
        inputs.append({'type': input_type, 'name': input_name})

    details['action'] = action
    details['method'] = method
    details['inputs'] = inputs

    return details

def is_vulnerable(response):
    errors = {
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
    }

    for i in errors:
        if i in response.content.decode().lower():
            return True

    return False

def scan_sqli(url):

    for c in "\"'":
        new_url = f'{url}{c}'
        print(f'[!] Scaning on {new_url}')

        res = s.get(new_url)

        if is_vulnerable(res):
            print(f"[!!] SQL Injection detected on {new_url}")
            return

    forms = get_forms(url)

    for i in forms:
        details = get_form_details(i)
        for c in "\"'":
            data = {}

            for j in details['inputs']:
                if j['type'] == 'hidden' or j['value']:
                    try:
                        data[j['name']] = j['value'] + c
                    except:
                        pass
                elif j['type'] != 'submit':
                    data[j['name']] = f'teste{c}'

            url = urljoin(url, details['action'])

            if details['method'] == 'post':
                res = s.post(url, data=data)
            elif details['method'] == 'get':
                res = s.get(url, params=data)

            if is_vulnerable(res):
                print(f'[!] SQL Injection detected {url}\n[+] Form:')
                print(details)
                break


if __name__ == '__main__':
    target = 'http://testphp.vulnweb.com/artists.php?artist=1'
    scan_sqli(target)