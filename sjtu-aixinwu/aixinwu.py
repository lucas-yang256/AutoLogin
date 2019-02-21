# For my roommate Kang

import requests
import re
import os
import logging
import http.cookiejar
from urllib.parse import urljoin
from config import account

login_url = 'http://aixinwu.sjtu.edu.cn/index.php/login'
captcha_url = 'https://jaccount.sjtu.edu.cn/jaccount/captcha?'
post_url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'
home_url = 'http://aixinwu.sjtu.edu.cn/index.php/home'
curr_path = os.path.dirname(os.path.abspath(__file__))
cookies_path = os.path.join(curr_path, "aixinwu.cookies")
log_path = os.path.join(curr_path, "aixinwu.log")
captcha_path = os.path.join(curr_path, "captcha.png")

logging.basicConfig(filename=log_path,
                    level='INFO',
                    format="%(asctime)s [line: %(lineno)d] - %(message)s",
                    filemode='w')


class SJTUer(object):
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/51.0'}
        self.s = requests.session()
        self.s.headers.update(self.headers)
        self.usr = account['username']
        self.psw = account['password']
    
    def save_cookies(self, cookies):
        cj = http.cookiejar.LWPCookieJar()
        ck = {c.name: c.value for c in cookies}
        requests.utils.cookiejar_from_dict(ck, cj)
        cj.save(cookies_path, ignore_expires=True, ignore_discard=True)
        logging.info("Cookies saved")
    
    def load_cookies(self):
        load_cj = http.cookiejar.LWPCookieJar()
        load_cj.load(cookies_path, ignore_expires=True, ignore_discard=True)
        load_ck = requests.utils.dict_from_cookiejar(load_cj)
        logging.info("Cookies loaded")
        return load_ck
    
    def download_captcha(self, url):
        with open(captcha_path, "wb") as f:
            f.write(self.s.get(url).content)
        logging.info("Captcha downloaded.")
    
    def captcha_rec(self, captcha):
        files = {
            'file': ('captcha.jpeg', open(captcha, 'rb'), 'image/jpeg')
        }
        req = requests.post('https://t.yctin.com/en/security/captcha-recognition/',
                            files=files,
                            headers=self.headers)
        
        return req.text.strip()
    
    def process_cookies(self):
        """ To process the first cookies. """
        cj = http.cookiejar.LWPCookieJar()
        ck = {
            "JASiteCookie": "",
            "PHPSESSID": "",
            "__utma": "",
            "__utmb": "",
            "__utmc": "",
            "__utmt": "1",
            "__utmv": "",
            "__utmz": "",
            "ci_session": ""
        }
        requests.utils.cookiejar_from_dict(ck, cj)
        cj.save(cookies_path, ignore_expires=True, ignore_discard=True)
    
    def login_by_cookies(self):
        if not os.path.exists(cookies_path):
            logging.info("Cookies don't exist.")
            return
        
        logging.info("Cookies exist.")
        ck = self.load_cookies()
        
        if not ck:
            logging.error("Failed to load cookies.")
            return
        
        self.s.cookies.update(ck)
        
        # 检测用户名是否存在，若存在即说明登录成功
        info = self.s.get(login_url).text
        if self.usr in info:
            logging.info("Successfully login by cookies!")
            self.save_cookies(self.s.cookies)
            return True
    
    def login(self):
        html0 = self.s.get(login_url).text
        url1 = re.findall(r'URL=(.*?)">', html0)[0]
        html = self.s.get(url1).text
        self.download_captcha(captcha_url)
        
        formdata = {}
        formdata['user'] = self.usr
        formdata['pass'] = self.psw
        formdata['sid'] = re.findall(r'name="sid" value="(.+?)"', html)[0]
        formdata['returl'] = re.findall(r'name="returl" value="(.+?)"', html)[0]
        formdata['se'] = re.findall(r'name="se" value="(.+?)"', html)[0]
        formdata['v'] = re.findall(r'name="v" value="(.*?)"', html)[0]
        formdata['captcha'] = self.captcha_rec(captcha_path)
        
        login = self.s.post(post_url, data=formdata, allow_redirects=False)
        redirect_url = urljoin('https://jaccount.sjtu.edu.cn', login.headers['Location'], )
        redirect_url2 = self.s.get(redirect_url, allow_redirects=False).headers['Location']
        req = self.s.get(redirect_url2, allow_redirects=False)
        redirect_url3 = urljoin('http://aixinwu.sjtu.edu.cn', req.headers['Location'])
        self.s.get(redirect_url3)  # 不知道为什么，要get两次。。
        self.s.get(redirect_url3)  # 不知道为什么，要get两次。。
        
        info = self.s.get(home_url).text
        if not self.usr in info:
            logging.error("Login failed.")
            return
        else:
            logging.info("Login successfully!")
            self.save_cookies(self.s.cookies)
            return True


sjtuer = SJTUer()
if sjtuer.login_by_cookies():
    print("Login by cookies successfully!")
else:
    sjtuer.login()
