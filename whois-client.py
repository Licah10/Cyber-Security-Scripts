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

def pull_whois(target):
    results = whois.query(target, ignore_returncode=1)
    whois_out['name'] = results.name
    whois_out['resgistrar'] = results.registrar
    whois_out['status'] = results.status
    out = json.dumps(whois_out, indent=4)
    save_output(str(target), out)
    print(out)

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
    pull_whois(str(target))
    ip = prepare_ip(target)
    pull_ipwhois_legacy_whois(str(ip))

if __name__ == '__main__':
    
    banner = """
                                               ______
 _       _   _       _______        _______   |   ___|
| |  _  | | | |     |       |      |__   __|  |  |___
| | | | | | | |___  |   |   |         | |     |___   |
| |_| |_| | |  _  | |   |   |       __| |__   ____|  |
|_________| |_| |_| |_______|      |_______| |_______|

 ____   _____   _______   _____
|  _ \ |  _  | |__   __| |  _  |
| |_|| |  _  |    | |    |  _  |
|____/ |_| |_|    | |    |_| |_|
                  | |
 _____   ____     | |  _____   _______  _     _   ____   _____
| __  | |  __|    | | | __  | |__   __| \ \  / / |  __| | __  |
|    _| | |__     | | |    _|  __| |__   \ \/ /  | |__  |    _|
|_|\_\  |  __|    |_| |_|\_\  |_______|   \__/   |  __| |_|\_\ 
        | |__                                    | |__
        |____|                                   |____|

"""
    print(banner)

    main()
