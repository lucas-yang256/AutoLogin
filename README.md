# AutoLogin

部署在个人 VPS 上面，实现自动登录，~~领签到币~~的目的。
- [sjtu-aixinwu](./sjtu-aixinwu) : 自动登录[爱心屋网站](http://aixinwu.sjtu.edu.cn/index.php/home "SJTU爱心屋")，每日登录领爱心币，爱心币可以兑换物品。
- [readfree](./readfree) : 登录 [readfree](http://readfree.me "readfree") 并签到，一次可以随机领到1-3个额度值。

## 推荐用法
#### 购买 VPS
#### 克隆库
   ```bash
   $ git clone https://github.com/lucas-yang256/AutoLogin.git && cd AutoLogin
   ```
#### 配置
- 确保 python 版本为 3
- `pip install -r requirements.txt`
- [登录 sjtu-aixinwu](./sjtu-aixinwu/README.md)
- [登录 readfree.me](./readfree/README.md)

#### 利用 linux 系统 `crontab`函数实现定时执行。
- 先给以上脚本赋予执行权限

    ```bash
    sudo chmod +x ./aixinwu.py ./readfree.py
    ```

- 执行`crontab -e`进行编辑，crontab 的格式可以参考[ crontab 定时任务](http://linuxtools-rst.readthedocs.io/zh_CN/latest/tool/crontab.html#crontab)。比如我的设置就是
    ```
    31 0,12 * * * python3 /root/AutoLogin/readfree.py
    31 0,12 * * * python3 /root/AutoLogin/aixinwu.py
    ```
