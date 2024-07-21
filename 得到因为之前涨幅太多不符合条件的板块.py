from crazy import *
def get_zhangfu_bankua(StockID):
    url = 'https://apphis.longhuvip.com/w1/api/index.php'
    headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N976N Build/QP1A.190711.020)'}
    data = f"""st	850
a	GetPlateKLineDay
c	ZhiShuKLine
PhoneOSNew	1
DeviceID	ffffffff-d151-c2cd-0000-00002cd5753b
VerSion	5.14.0.4
Token	0
Index	0
apiv	w36
Type	d
StockID	{StockID}
UserID	0"""
    datas = parse_data_to_dict(data)
    response = requests.post(url, data=datas, headers=headers)
    response.encoding = response.apparent_encoding
    data = json.loads(response.text)
    return data
def zhangfy_comply_condition_bankua(date):
    all_bankua = get_all_bankua()
    donnt_list = []
    for i in tqdm(all_bankua):
        try:
            dict1 = get_zhangfu_bankua(i)
            start_date = dict1['x'].index(f'{date}') - 9
            mi_date = dict1['x'].index(f'{date}') - 5
            end_date = dict1['x'].index(f'{date}') - 1
            # print(dict1['y'][start_date:end_date])#开盘价，收盘价，最高价，最低价
            four_day_zhangfu = (dict1['y'][end_date][1] - dict1['y'][mi_date][1]) / dict1['y'][mi_date][1] * 100
            eight_day_zhangfu = (dict1['y'][end_date][1] - dict1['y'][start_date][1]) / dict1['y'][start_date][1] * 100
            if four_day_zhangfu > 8.2 or eight_day_zhangfu > 14:
                print(i)
                donnt_list.append(i)
        except:
            pass
    return donnt_list
if __name__ == '__main__':
    print(zhangfy_comply_condition_bankua(20240412))#这样可以得到因为之前涨幅太多，现在不符合条件的板块