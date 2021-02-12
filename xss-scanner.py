import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

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

def send_form(form_details, url, value):
    turl = urljoin(url, form_details['action'])
    inputs = form_details['inputs']

    data = {}

    for i in inputs:
        if i['type'] == 'text' or i['type'] == 'search':
            i['value'] = value

        input_name = i.get('name')
        input_value = i.get('value')

        if input_name and input_value:
            data[input_name] = input_value

    if form_details['method'] == 'post':
        return requests.post(turl, data=data)
    else:
        return requests.get(turl, params=data)

def scan_for_xss(url):
    forms = get_forms(url)
    js = "<script>window.alert('XSS ON!')</script>"
    state = False

    for i in forms:
        form_info = get_form_details(forms)
        content = send_form(form_info, url, js).content.decode()

        if js in content:
            print(f'[!] XSS Detected on {url}\n[*] Details:')
            print(form_info)
            state = True

    return state

if __name__ == '__main__':
    print("""
        XSS SCANER
        
        This is a simple xss scanner.
        Limitations:
            don't detect URL based xss attacks and many others. Just form based...
    """)
    target = 'https://xss-game.appspot.com/level1/frame#3'
    print(scan_for_xss(target))
