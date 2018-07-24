import pandas as pd
import json, requests
import time
from matplotlib import pyplot as plt
import numpy as np
from pandas import DataFrame


def time_to_timestamp(times):
    timeArray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)
    return int(timestamp)


def get_token():
    base_url = "http://api.bus.soundbus.cn"
    token_api = "/authentication"
    token_url = base_url + token_api

    headers = {'Accept':'application/vnd.flask.v1+json',
               'Authorization':'Basic dm9raWE6MTIzMTIz=',
               'content_type':'application/json'}
    r = requests.get(token_url, headers=headers)
    print("获取token成功")
    return r.json()['access_token']


def get_json(token, api):
    headers = {
        'Accept': 'application/vnd.flask.v1+json',
        'Authorization': 'Bearer  ' + token,
        'content_type': 'application/json'
    }
    base_url = "http://api.bus.soundbus.cn"
    url = base_url + api
    request = requests.get(url, headers=headers)
    json = request.json()
    return json




def get_data(token , date):

    start_time = date + " 00:00:00"
    end_time = date + " 23:59:59"
    start_timestamp = time_to_timestamp(start_time)
    end_timestamp = time_to_timestamp(end_time)

    merchant_api = "/merchant/pv?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    bus_brt_api = "/bus/brt?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    merchant_award_api = "/merchant/award?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    total_merchant_award_api = "/merchant/award?start_time=1526313600&end_time=%s" % (end_timestamp)
    bus_line_api = "/bus/line?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    app_api = "/app/slice?start_time=%s&end_time=%s&slice=day" % (start_timestamp, end_timestamp)
    user_api = "/user/slice?start_time=%s&end_time=%s&slice=hour" % (start_timestamp, end_timestamp)
    app_award_api = "/app/award?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    total_uv_api = "/user/uv?start_time=1526313600&end_time=%s" % (end_timestamp)
    total_pv_api = "/user/pv?start_time=1526313600&end_time=%s" % (end_timestamp)
    day_uv_api = "/user/uv?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    day_pv_api = "/user/pv?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    word_api = "/word/merchant?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    total_word_api = "/word/merchant?start_time=%s&end_time=%s" % (1526313600, end_timestamp)
    cpm_api = "/ad/merchant/cpm?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    cpc_api = "/ad/merchant/cpc?start_time=%s&end_time=%s" % (start_timestamp, end_timestamp)
    total_cpm_api = "/ad/merchant/cpm?start_time=%s&end_time=%s" % (1526313600, end_timestamp)
    total_cpc_api = "/ad/merchant/cpc?start_time=%s&end_time=%s" % (1526313600, end_timestamp)

    #用户pv, uv 明细
    user_json = get_json(token, user_api)
    user_slice = pd.read_json(json.dumps(user_json)).T
    user_slice = user_slice.reset_index(list(np.arange(23, 1)), drop=True)
    user_slice.index.name = 'hour'


    # 商家pv, uv
    merchant_json = get_json(token, merchant_api)
    merchant = pd.read_json(json.dumps(merchant_json))

    # 商家奖品
    merchant_award_json = get_json(token, merchant_award_api)
    merchant_award = pd.read_json(json.dumps(merchant_award_json), )
    merchant_award = merchant_award.set_index('merchant_name')
    merchant_award.loc['总计'] = merchant_award.apply(lambda x: x.sum(), axis=0)
    prize_total = merchant_award['prize_total']
    merchant_award.drop(labels=['prize_total'], axis=1, inplace=True)
    merchant_award.insert(5, 'prize_total', prize_total)
    day_pend_total =  merchant_award.ix['总计', 'prize_total']
    day_no_threshold_pend = merchant_award.ix['总计', 'no_threshold_pend']
    day_threshold_pend = merchant_award.ix['总计', 'threshold_pend']
    day_no_threshold_used = merchant_award.ix['总计', 'no_threshold_used']
    day_threshold_used = merchant_award.ix['总计', 'threshold_used']
    day_benediction = merchant_award.ix['总计', 'benediction']

    # 总商家奖品
    total_merchant_award_json = get_json(token, total_merchant_award_api)
    total_merchant_award = pd.read_json(json.dumps(total_merchant_award_json), )
    total_merchant_award = total_merchant_award.set_index('merchant_name')
    total_merchant_award.loc['总计'] = total_merchant_award.apply(lambda x: x.sum(), axis=0)
    total_pend_total = total_merchant_award.ix['总计', 'prize_total']
    total_no_threshold_pend = total_merchant_award.ix['总计', 'no_threshold_pend']
    total_threshold_pend = total_merchant_award.ix['总计', 'threshold_pend']
    total_no_threshold_used = total_merchant_award.ix['总计', 'no_threshold_used']
    total_threshold_used = total_merchant_award.ix['总计', 'threshold_used']
    total_benediction = total_merchant_award.ix['总计', 'benediction']

    # 商家集字
    word_json = get_json(token, word_api)
    word = pd.read_json(json.dumps(word_json))
    total_word_json = get_json(token, total_word_api)
    total_word = pd.read_json(json.dumps(total_word_json))
    day_word_pend = 0
    day_word_complete = 0
    total_word_pend = 0
    total_word_complete = 0


    if word.empty:
        print(date + '无集字发放')
    else:
        word = word.set_index('merchant_name')
        word = word[['word','pv','complete_word_pv']]
        for pv in word['pv']:
            day_word_pend = day_word_pend + pv
        for complete in word['complete_word_pv']:
            day_word_complete = day_word_complete + complete


    if total_word.empty:
        print(date + '无集字发放')
    else:
        total_word = total_word.set_index('merchant_name')
        for pv in total_word['pv']:
            total_word_pend = total_word_pend + pv
        for complete in total_word['complete_word_pv']:
            total_word_complete = total_word_complete + complete


    #车辆
    bus_line_json = get_json(token, bus_line_api)
    bus_line_data = pd.read_json(json.dumps(bus_line_json))
    if bus_line_data.empty:
        lines = 0
        car_count = 0
        print(date + '无线路信息')
    else:
        bus_line_data = bus_line_data.set_index('line_name')
        lines = len(bus_line_data['pv'])
        bus_line_data.loc["总计"] = bus_line_data.apply(lambda x: x.sum(), axis=0)
        car_count = bus_line_data.ix['总计', 'car_count']



    # 接收,独立用户
    total_pv_json = get_json(token, total_pv_api)
    total_uv_json = get_json(token, total_uv_api)
    day_pv_json = get_json(token, day_pv_api)
    day_uv_json = get_json(token, day_uv_api)
    total_pv = total_pv_json['pv']
    total_uv = total_uv_json['uv']
    day_pv = day_pv_json['pv']
    day_uv = day_uv_json['uv']

    # 足迹点击
    cpc_json = get_json(token, cpc_api)
    cpm_json = get_json(token, cpm_api)
    total_cpc_json = get_json(token, total_cpc_api)
    total_cpm_json = get_json(token, total_cpm_api)
    day_cpm = cpm_json['cpm_pv_total']
    day_cpc = cpc_json['cpc_pv_total']
    total_cpm = total_cpm_json['cpm_pv_total']
    total_cpc = total_cpc_json['cpc_pv_total']

    # total_data = DataFrame({
    #
    #         '总接收次数': 0,
    #         '总独立用户数': 0,
    #         '单日接收次数': 0,
    #         '单日独立用户数': 0,
    #         '单日奖券发放数': 0,
    #         '单日无门槛奖券发放': 0,
    #         '单日有门槛奖券': 0,
    #         '单日祝福数量': 0,
    #     })
    # total_data.index = [
    #     '总接收次数',
    #     '总独立用户数',
    #     '单日接收次数',
    #     '单日独立用户数',
    #     '单日奖券发放数',
    #     '单日无门槛奖券发放',
    #     '单日有门槛奖券',
    #     '单日祝福数量', ]
    total_data = DataFrame({
        date:{
            '01总接收次数': total_pv,
            '02总独立用户数': total_uv,
            '03总公交车安装数量': 1956,
            '04总线路数量': 186,
            '05总足迹点击数':total_cpm,
            '06总足迹列表点击数':total_cpc,
            '07总集字发放': total_word_pend,
            '08总集字集齐': total_word_complete,
            '09总奖券发放数':total_pend_total,
            '10总无门槛奖券发放数':total_no_threshold_pend,
            '11总有门槛奖券发放数':total_threshold_pend,
            '12总祝福数':total_benediction,
            '13无门槛奖券核销': total_no_threshold_used,
            '14总有门槛奖券核销': total_threshold_used,
            '15单日接收次数': day_pv,
            '16单日独立用户数': day_uv,
            '17单日公交车使用数量': car_count,
            '18单日线路使用数量': lines,
            '19单日足迹点击数': day_cpm,
            '20单日足迹列表点击数': day_cpc,
            '21单日集字发放':day_word_pend,
            '22单日集字集齐':day_word_complete,
            '23单日奖券发放数': day_pend_total,
            '24单日无门槛奖券发放': day_no_threshold_pend,
            '25单日有门槛奖券发放': day_threshold_pend,
            '26单日祝福数': day_benediction,
            '27单日无门槛奖券核销': day_no_threshold_used,
            '28单日有门槛奖券核销': day_threshold_used,

        }})
    # total_data = total_data[['总接收次数',
    #         '总独立用户数',
    #         '总公交车安装数量',
    #         '总线路数量',
    #         '总足迹点击数',
    #         '总足迹列表点击数',
    #         '总集字发放',
    #         '总集字集齐',
    #         '总奖券发放数',
    #         '总无门槛奖券发放数',
    #         '总有门槛奖券发放数',
    #         '总祝福数',
    #         '无门槛奖券核销',
    #         '总有门槛奖券核销',
    #         '单日接收次数',
    #         '单日独立用户数',
    #         '单日公交车使用数量',
    #         '单日线路使用数量',
    #         '单日足迹点击数',
    #         '单日足迹列表点击数',
    #         '单日集字发放',
    #         '单日集字集齐',
    #         '单日奖券发放数',
    #         '单日无门槛奖券发放',
    #         '单日有门槛奖券发放',
    #         '单日祝福数',
    #         '单日无门槛奖券核销',
    #         '日有门槛奖券核销',]]

    figname = "figure/" + date + ".png"
    plt.figure(figsize=(10, 5))
    plt.style.use('seaborn-whitegrid')
    plt.rcParams['font.sans-serif'] = ['Microsoft Yahei']
    plt.plot(user_slice, marker='*')
    plt.title(date + "用户活跃趋势表", fontsize=20)
    plt.xlabel("时间")
    plt.ylabel("接收次数/用户人数")
    plt.subplots_adjust(left=0.08, right=0.95, top=0.9, bottom=0.1)
    plt.legend(labels=['pv', 'uv'])
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    pv_x = np.array(user_slice.index)
    pv_y = np.array(user_slice['pv'])
    uv_x = np.array(user_slice.index)
    uv_y = np.array(user_slice['uv'])

    for a, b in zip(pv_x, pv_y):
        plt.text(a, b, b, size=7)

    for a, b in zip(uv_x, uv_y):
        plt.annotate(b, xy=(a, b), xytext=(a, b), fontsize=7)

    plt.savefig(figname)


    return {'total_data':total_data,
            'user_slice':user_slice,
            'merchant_award':merchant_award,
            'word': word,}



