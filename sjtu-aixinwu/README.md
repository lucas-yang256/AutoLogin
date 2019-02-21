# sjtu-aixinwu

## 网站

https://aixinwu.sjtu.edu.cn

## 使用方法
- 在 config.py 里填入自己的账号和密码。
- 运行 `aixinwu.py`。
- 如果登录成功会在当前目录下生成 aixinwu.cookies 文件，以后就可以用 cookies 直接登录了。
    

## 说明
- 网页请求全部采用 python 实现，其中验证码识别采用第三方网站接口，第一次登录时会把 cookies 存储在本地。

- 每次登录时优先选择 cookies 方式，如果 cookies 找不到或者 cookies 登录失败会继续选择账号密码登录然后更新 cookies。
