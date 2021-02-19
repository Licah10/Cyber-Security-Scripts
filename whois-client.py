from ipwhois import IPWhois
from ipwhois.net import Net
from ipwhois.asn import IPASN
import whois
import json
import socket
import sys

whois_out = {}

def save_output(filename, content):
    filename = f'{filename}.txt'
    with open(filename, 'w') as f:
        f.write(content)

def pull_ipwhois_legacy_whois(target):
    eye = IPWhois(target)
    who_is = json.dumps(eye.lookup_whois(get_asn_description=True, inc_nir=True), indent=4)
    results = json.dumps(eye.lookup_rdap(depth=1), indent=4)
    save_output(str(target), who_is)
    save_output(str(target), results)
    print(f'{results}')
    print(f'{who_is}')

def pull_ipwhois_asn(target):
    net = Net(target)
    eye = IPASN(net)
    asn_results = json.dumps(eye.lookup(inc_raw=True), indent=4)
    save_output(str(target), asn_results)
    print(f'{asn_results}')

def prepare_ip(url):
    rawip = socket.gethostbyname(url)
    ip = f'{rawip}'
    return ip

def main():
    target = sys.argv[1]
    if len(target) <= 0:
        print('[-] WHO IS DATA RETRIVER')
        print(32*'='+'\n')
        print('\nUSAGE: python3 whois-client.py target.com')
    ip = prepare_ip(target)
    pull_ipwhois_legacy_whois(str(ip))

if __name__ == '__main__':
    print('[-] WHO IS DATA RETRIVER')
    print(32*'='+'\n')

    main()
