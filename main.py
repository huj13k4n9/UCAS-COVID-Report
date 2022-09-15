import sys
import pytz
import requests
import configparser
from datetime import datetime


class UCASError(Exception):
    pass


s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-T505) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/15.0 Chrome/90.0.4430.210 Safari/537.36',
    'Referer': 'https://app.ucas.ac.cn/site/dailyReport/reportAll?appid=9'
})


def get_post_data(c: configparser.ConfigParser):
    config_data = c['DEFAULT']
    return {
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),
        'realname': config_data.get('姓名'),
        'number': config_data.get('学工号'),
        'jzdz': config_data.get('居住地址'),
        'zrzsdd': config_data.get('昨日住宿地点', '1'),
        'sfzx': config_data.get('今日是否在校', '1'),
        'dqszdd': config_data.get('当前所在地点', '1'),
        'geo_api_infot': '{"area":{"label":"","value":""},"city":{"label":"","value":""},"address":"","details":"","province":{"label":"","value":""}}',
        'szgj': '',
        'szgj_select_info[id]': '0',
        'szgj_select_info[name]': '',
        'geo_api_info': '{"address":"北京市怀柔区","details":"中国科学院大学雁栖湖校区","province":{"label":"北京市","value":""},"city":{"label":"","value":""},"area":{"label":"怀柔区","value":""}}',
        'dqsfzzgfxdq': config_data.get('当前是否在中高风险地区', '4'),
        'zgfxljs': config_data.get('是否有中高风险地区旅居史', '4'),
        'tw': config_data.get('体温', '1'),
        'sffrzz': config_data.get('是否出现发热等症状', '0'),
        'dqqk1': config_data.get('行程情况', '1'),
        'dqqk1qt': '',
        'dqqk2': config_data.get('隔离情况', '1'),
        'dqqk2qt': '',
        'sfjshsjc': config_data.get('昨日是否接受核酸检测', '1'),
        'dyzymjzqk': config_data.get('第一针疫苗接种情况'),
        'dyzwjzyy': '',
        'dyzjzsj': config_data.get('第一针疫苗接种时间'),
        'dezymjzqk': config_data.get('第二针疫苗接种情况'),
        'dezwjzyy': '',
        'dezjzsj': config_data.get('第二针疫苗接种时间'),
        'dszymjzqk': config_data.get('第三针疫苗接种情况'),
        'dszwjzyy': '',
        'dszjzsj': config_data.get('第三针疫苗接种时间'),
        'gtshryjkzk': config_data.get('共同生活人员健康情况', '1'),
        'extinfo': '',
        'app_id': 'ucas'
    }


def login(s: requests.Session, username, password):
    payload = {
        "username": username,
        "password": password
    }
    r = s.post("https://app.ucas.ac.cn/uc/wap/login/check", data=payload)

    if r.json().get('m') != "操作成功":
        raise UCASError("Login Error, API msg " + r.text)


def submit(s: requests.Session, c: configparser.ConfigParser):
    data = get_post_data(c)
    api_key = c['WECHATPUSH'].get("XIZHI_API_KEY", None)
    r = s.post("https://app.ucas.ac.cn/ucasncov/api/default/save", data=data)
    print("提交信息:", data)
    result = r.json()
    if result.get('m') == "操作成功":
        print("打卡成功")
        if api_key != None:
            message(api_key, result.get('m'), data)
    else:
        print("打卡失败，错误信息: ", r.json().get("m"))
        if api_key != None:
            message(api_key, result.get('m'), data)


def message(key, title, body):
    """
    微信通知打卡结果
    """
    msg_url = "https://xizhi.qqoq.net/{}.send?title=UCAS每日填报：{}&content={}".format(
        key, title, body)
    requests.get(msg_url)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        config_loc = "./config.ini"
    elif len(sys.argv) == 2:
        config_loc = sys.argv[1]
    else:
        raise UCASError("Argument Error")

    print("Current time:", datetime.now(tz=pytz.timezone(
        "Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z"))
    config = configparser.ConfigParser()
    config.read(config_loc, encoding='utf-8')
    if len(config['DEFAULT'].items()) == 0:
        raise UCASError("Config File Error")

    login(s, config['DEFAULT'].get('sep账号'), config['DEFAULT'].get('sep密码'))
    submit(s, config)
