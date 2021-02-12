import argparse
import os
import requests

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', dest='ip', type=str,  required=True)
    parser.add_argument('-host', dest='host', type=str, required=True)
    parser.add_argument('-port', dest='port', type=int, default=80)
    parser.add_argument('-ignore-http-codes', dest='ignore_http_codes', type=str, help='comma separated list of http codes', default='404')
    parser.add_argument('-ignore-content-length', dest='ignore_content_length', type=int, default=0)
    parser.add_argument('-wordlist', dest='wordlist', type=str, help='file location', default='wordlist')
    parser.add_argument('-output', dest='output', type=str, help='output file', default='./output.txt')
    parser.add_argument('-ssl', dest='ssl', action='store_true', help='use SSL')

    args = parser.parse_args()
    
    ignore_http_codes = list(map(int, args.ignore_http_codes.replace(' ', '').split(',')))
    if os.path.exists(args.wordlist):
        virtual_host_list = open(args.wordlist).read().splitlines()
        results = ''
        
        for virtual_host in virtual_host_list:
            hostname = virtual_host.replace('%s', args.host)

            headers = {
                'Host': hostname if args.port == 80 else f'{args.host}:{args.port}',
                'Accept': '*/*',
                'X-Originating-IP': '127.0.0.1',
                'X-Forwarded-For': '127.0.0.1',
                'X-Remote-IP': '127.0.0.1',
                'X-Remote-Addr': '127.0.0.1'
            }

            dest_url = '{}://{}:{}/'.format('https' if args.ssl else 'http', args.ip, args.port)
            try:
                res = requests.get(dest_url, headers=headers, verify=False)
            except requests.exceptions.RequestException:
                continue

            if res.status_code in ignore_http_codes:
                continue

            if args.ignore_content_length > 0 and args.ignore_content_length == int(res.headers['content-length']):
                continue
            
            output = f'Found: {hostname} ({res.status_code})'
            results += output + '\n'
            print(output)
            
            with open(str(args.host+'.txt'), 'w') as f:
                for key, val in res.headers.items():
                    output = f'  {key}: {val}'
                    results += output + '\n'
                    print(output)
                    f.write(results)
    else:
        print(f'[!] ERROR: wordlist "{args.wordlist}" does not exist.')

def save(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

if __name__ == '__main__':

    banner = """
    ______                                                      ______
   /_____/| ###   ### ###   ### ######## ######### ########### /_____/|
   ###### | ###   ### ###   ### ######## ######### ########### ###### |
   ###### |  ### ###  ######### ###  ### ####          ###     ###### |
   ###### |  ### ###  ######### ###  ### #########     ###     ###### |
   ###### /   #####   ###   ### ########     #####     ###     ###### /
   ######/    ####    ###   ### ######## #########     ###     ######/
    """

    print(banner)
    main()
