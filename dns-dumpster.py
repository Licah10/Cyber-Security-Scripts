from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
import base64

def magic(domain):

    print('Testing... : {}'.format(domain))

    res = DNSDumpsterAPI(True).search(domain)

    print("[+] DOMAIN: {}".format(res['domain']))

    print("\n[!] DNS SERVERS")
    for entry in res['dns_records']['dns']:
        print(("{domain} ({ip}) {as} {provider} {country}".format(**entry)))

    print("\n[!] MX RECORDS")
    for entry in res['dns_records']['mx']:
        print(("{domain} ({ip}) {as} {provider} {country}".format(**entry)))

    print("\n[!] HOST RECORDS")
    for entry in res['dns_records']['host']:
        if entry['reverse_dns']:
            print(("{domain} ({reverse_dns}) ({ip}) {as} {provider} {country}".format(**entry)))
        else:
            print(("{domain} ({ip}) {as} {provider} {country}".format(**entry)))

    try:
        xls_retrieved = res['xls_data'] is not None
        print("\n\n\nRetrieved XLS hosts? {} (accessible in 'xls_data')".format(xls_retrieved))
        print(repr(base64.b64decode(res['xls_data'])[:20]) + '...')
    except:
        pass

if __name__ == '__main__':
    import sys

    banner = """
  ___  _  _ ___   ___                           
 |   \| \| / __| |   \ _  _ _ __  _ __  ___ _ _ 
 | |) | .` \__ \ | |) | || | '  \| '_ \/ -_) '_|
 |___/|_|\_|___/ |___/ \_,_|_|_|_| .__/\___|_|  
                                 |_|            

     Developed by boxtrot
    """
    print(banner)

    try:
        domain = sys.argv[1]
    except:
        print("USAGE:\npython3 dnsdumper.py domain")
        sys.exit(1)

    if len(domain) == 0:
        print("USAGE:\npython3 dnsdumper.py domain")
        sys.exit(1)
    else:
        try:
            magic(domain)
        except:
            print("MAKE SURE THAT THE DOMAIN EXISTS OR IS UP...")

