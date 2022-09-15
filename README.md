# UCAS-COVID-Report

## 功能支持

1. 每日健康打卡，无需获取位置（默认使用雁栖湖校区位置进行打卡）
2. 使用配置文件读取个人信息
3. 每次运行时随机增加30分钟以内的延时，使得填报时间具有随机性
4. 使用息知API进行微信打卡结果推送

## 使用方法

1. 在`config.ini`中按照注释修改你的信息（与打卡界面的选项一一对应）

2. 使用以下命令来运行打卡程序（将配置文件路径更换为实际路径）：

   ```shell
   $ python3 main.py /path/to/your/config
   ```

## Crontab支持

在你的服务器的`/etc/crontab`文件中添加如下行：

```shell
30 7    * * *   root    /usr/bin/python3 /path/to/your/main.py /path/to/your/config >> /path/to/your/log
```

第一个数字修改为每天打卡的分钟值，第二个数字修改为每天打卡的小时值，如上面的代表每天早上七点半运行。

## 微信推送支持

支持息知API进行微信推送 <https://xz.qqoq.net/#/index>，注册绑定成功后在配置文件中添加对应API Key：

```ini
[WECHATPUSH]
XIZHI_API_KEY = xxx
```

在每次打卡结束后，程序将把打卡结果通过微信进行推送。