from crazy import *
import requests
import threading
import json
from threading import Lock
def get_all_bankua():
    url = 'https://apphwhq.longhuvip.com/w1/api/index.php'
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N976N Build/QP1A.190711.020)'}
    bankua_list = []
    lock = Lock()  # 创建一个锁来确保线程安全
    threads = []
    # 定义fetch_bankua函数，但这次是在get_all_bankua内部
    def fetch_bankua(i, bankua_list, lock):
        data = f"""  
        Order	1  
        a	RealRankingInfo  
        st	30  
        c	ZhiShuRanking  
        PhoneOSNew	1  
        RStart	0925  
        DeviceID	ffffffff-d151-c2cd-0000-00002cd5753b  
        VerSion	5.14.0.4  
        Index	{i * 30}  
        REnd	1500  
        apiv	w36  
        Type	5  
        ZSType	5  
        """
        datas = parse_data_to_dict(data)  # 确保这个函数能正确解析数据
        response = requests.post(url, data=datas, headers=headers)
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            data_list = json.loads(response.text)['list']
            with lock:
                for item in data_list:
                    bankua_list.append(item[0])
                    # 创建并启动线程
    for i in range(14):
        t = threading.Thread(target=fetch_bankua, args=(i, bankua_list, lock))
        t.start()
        threads.append(t)
        # 等待所有线程完成
    for t in threads:
        t.join()
        # 打印并返回结果
    print(bankua_list)
    return bankua_list
if __name__ == '__main__':
    start_time = time.time()
    bankua_list = get_all_bankua()
    end_time = time.time()
    print(end_time - start_time)