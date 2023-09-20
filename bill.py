import requests
import bs4
import urllib3
import pickle

def check_water_electric(username:str,password:str,token_pushplus:str)->None:
    session = requests.session()
    session.verify = False  # ignore certificate error
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    login_page = 'https://m.myhome.tsinghua.edu.cn/weixin/weixin_user_authenticate.aspx'
    cookie_file = '.thb_cookie'
    try:  # to load cookie
        with open(cookie_file, 'rb') as f:
            session.cookies.update(pickle.load(f))
    except Exception:
        pass
    session.get('https://m.myhome.tsinghua.edu.cn/weixin/index.aspx')
    res = session.get(login_page)
    res.encoding = 'gbk'
    soup = bs4.BeautifulSoup(res.text, features='html.parser')
    inputs = soup.find_all('input', recursive=True)

    keys = [
        '__VIEWSTATE',
        '__VIEWSTATEGENERATOR',
        '__EVENTVALIDATION',
        'weixin_user_authenticateCtrl1$txtUserName',
        'weixin_user_authenticateCtrl1$txtPassword',
        'weixin_user_authenticateCtrl1$btnLogin'
    ]
    data = dict()

    for key in keys:
        data[key] = None

    for x in inputs:
        if x['name'] in set(keys):
            try:
                if data[x['name']] is None:
                    data[x['name']] = x['value']
            except KeyError:
                pass

    data['weixin_user_authenticateCtrl1$btnLogin'] = '%B5%C7%C2%BC'
    data['weixin_user_authenticateCtrl1$txtUserName'] = username
    data['weixin_user_authenticateCtrl1$txtPassword'] = password

    for k in data.keys():
        if data[k] is None:
            data[k] = ''
        data[k] = data[k].encode('gbk')

    if 'weixin_user_authenticateCtrl1$txtUserName' not in [
        x['name'] for x in inputs
    ]:
        pass  # already logged in!
    else:
        res = session.post(login_page, data=data)
    try:  # to save cookie
        with open(cookie_file, 'wb') as f:
            pickle.dump(session.cookies, f)
    except Exception:
        pass
    targets = {
        'power': {
            'url': 'http://m.myhome.tsinghua.edu.cn/weixin/weixin_student_electricity_search.aspx',
            'id': 'weixin_student_electricity_searchCtrl1_lblele',
            'influxid': 'tsinghua_electricity_bill',
            'regex': (r'', '')  # (r'$','度')
        },
        'water': {
            'url': 'http://m.myhome.tsinghua.edu.cn/weixin/weixin_student_water_search.aspx',
            'id': 'weixin_student_water_searchCtrl1_lblele',
            'influxid': 'tsinghua_water_bill',
            'regex': (r'', '')  # regex applied to the output
        }
    }
    res = session.get(targets['power']['url'])
    res.encoding = 'gbk'
    soup = bs4.BeautifulSoup(res.text, features='html.parser')
    power_balance = soup.find('span', {'id': targets['power']['id']}).text
    res = session.get(targets['water']['url'])
    res.encoding = 'gbk'
    soup = bs4.BeautifulSoup(res.text, features='html.parser')
    water_balance = soup.find('span', {'id': targets['water']['id']}).text
    def push_msg(token:str,title:str,content:str)->None:
        url = 'http://www.pushplus.plus/send?token='+token+'&title='+title+'&content='+content
        requests.get(url)
    if float(power_balance)<=10:
        push_msg(token_pushplus,'电费余额不足','电费还剩余'+power_balance+'度')
    if float(water_balance[:-1])<=5:
        push_msg(token_pushplus,'水费余额不足','水费还剩余'+water_balance)

    return None
username = '吴林峰'
password = 'qhjy18800136325'
token = 'f77cc5b306394b6f9aeb6b29a73706bd'
check_water_electric(username=username,password=password,token_pushplus=token)
