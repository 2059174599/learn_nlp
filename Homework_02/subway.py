from fake_useragent import UserAgent
from lxml import etree
import traceback
import pymysql
import requests
import time
import re,logging



def get_html(url): # request
    ua = UserAgent()
    headers = {
    #'User-Agent':ua.random
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    r = requests.get(url,verify=False,headers=headers,timeout = 10)
    r.encoding = r.apparent_encoding
    return r.text
    
def get_line(html): # site list
    html = etree.HTML(html)
    site_lines = html.xpath('string(//div[@class="line_content"])').split('\r\n')
    site_lines = [site.strip().replace(' ','') for site in site_lines]
    site_lines = [site.replace('\u3000','@') for site in site_lines if site]
    dr = re.compile(r'@.*',re.S)
    site_lines = [dr.sub('',site) for site in site_lines]
    return site_lines
    # print(len(site_lines))
    
def items(test): # turn it into dict
    lin_site = []
    sites = {}
    for i ,j in enumerate(test):
        if '线' in j:
            lin_site.append(i)
    #print(lin_site)
    len_site = len(test)
    {sites.setdefault(test[i],[]).append(test[i+1]) for i in range(len_site-1) if i not in lin_site and i+1 not in lin_site}
    test_1 = list(reversed(test))
    lin_site_1 = []
    for i ,j in enumerate(test_1):
        if '线' in j:
            lin_site_1.append(i)
    #print(lin_site)
    {sites.setdefault(test_1[i],[]).append(test_1[i+1]) for i in range(len_site-1) if i not in lin_site_1 and i+1 not in lin_site_1}
    
    print(sites)

def main(url):
    cont_html = get_html(url)
    sites = get_line(cont_html)
    items(sites)
        
if __name__ == '__main__':
    start_url = 'https://www.bjsubway.com/station/xltcx/'
    main(start_url)