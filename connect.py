import  time, chardet
import subprocess
import requests
import logging
#import hashlib

connet_flag = 1
logging.basicConfig(filename='./log/connect.log', format='%(asctime)s: %(message)s', level=logging.INFO)

def is_net_ok(ping_target):
    #检查是否连网
    p = subprocess.Popen("ping " + ping_target, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE);
    (stdoutput, erroutput) = p.communicate();
    encoding = chardet.detect(stdoutput)['encoding'];
    output = stdoutput.decode(encoding);
    retcode = p.returncode;
    res = ("ms TTL=" not in output);
    
    if res:
        logging.info('Ping failed.')
        #print('Ping failed.');
        return False;
    else:
        logging.info('Ping success.')
        #print('Ping success.');
        return True;

def wlan_connect(name, interface):
    #连接指定WIFI
    res = subprocess.call('netsh wlan connect %s'%name);
        
    if res:
        logging.info('Connect wlan SNNU failed.')
        #print('Connect wlan SNNU failed.');
        return False;
    else:
        logging.info('Connect wlan SNNU success.')
        #print('Connect wlan SNNU success.');
        return True;
    
def login(username, password):
    data = {
        'sourceurl': 'null',
        'username': username,
        'password': password,
        #'password' : '{MD5_HEX}' + hashlib.md5(password.encode()).hexdigest(),

    }  

    headers = {
        'Host': '202.117.144.205:8602',
        'Origin': 'http://202.117.144.205:8602',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://202.117.144.205:8602/snnuportal/login',
    }
 
    try:
        response = requests.post(
            'http://202.117.144.205:8602/snnuportal/login', data=data, headers=headers, timeout=10)
        logging.info('login success.')
        # print("login success.")
        #print(response.text)
    except:
        logging.info("login error.")
        #print("login error.")
def logout():

    data = {
    'action' : 'logoff'
	}; # 不用自己进行urlencode

    headers = {
        'Host': '202.117.144.205:8602',
        'Origin': 'http://202.117.144.205:8602',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'Content-Type': 'text/html;charset=UTF-8',
        'Referer': "http://202.117.144.205:8602/snnuportal/userstatus.jsp",
        }
    
    response = requests.get(
        'http://202.117.144.205:8602/snnuportal/logoff', data=data, headers=headers)
    #print(response.text)


def connect_plan(username, password):

    interface = "Wireless Network Connection"  # "无线网络连接" #
    name = "SNNU"
    global connet_flag
    connet_flag = 1
    logging.info('plan start.')
    while True:
        if not is_net_ok("cas-snnu-edu-cn.vpn.snnu.edu.cn"):
            logging.info('The network is disconnected.')

            if wlan_connect(name, interface):
                # Win10连接wlan之后会立即自动弹出登录页面，造成"getaddrinfo failed"
                time.sleep(5)
                login(username, password)
        else:
            time.sleep(5) #每5秒检测一次
        
        if not connet_flag:
            break

def plan_stop():
    global connet_flag
    connet_flag = 0
    logging.info('plan stop.')


if __name__ == '__main__':
    
    username = 'username'
    password = 'password'
    interface = "Wireless Network Connection"  # "无线网络连接" 
    name = "SNNU"
    
    while True:
        if not is_net_ok("cas-snnu-edu-cn.vpn.snnu.edu.cn"):  
            logging.info("\n %s"%time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            logging.info('The network is disconnected.')

            if wlan_connect(name, interface):
                time.sleep(5); # Win10连接wlan之后会立即自动弹出登录页面，造成"getaddrinfo failed"
                login(username, password)
        else:
            time.sleep(1)
        

