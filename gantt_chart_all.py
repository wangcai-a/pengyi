import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from readwordtable import word_to_excel


def get_gantt_chart(version, fig1_size=(12,16), fig1_left=0.45, fig1_bottom=0.09 ):
    plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
    plt.rcParams['axes.unicode_minus'] = False
    filename = "/Users/pengyi/PycharmProjects/pengyi/data/work_split/%s任务分解图.png" % version
    filename2 = "/Users/pengyi/PycharmProjects/pengyi/data/work_split/%s工作量统计.png" % version
    data = pd.read_excel('/Users/pengyi/PycharmProjects/pengyi/data/work_split/%s_需求任务拆解.xlsx'% version,)
    data = data.sort_values(by=4)

    total_time = data.groupby(2).sum()
    owner = list(data[2])
    labels = list(data[1])
    end_time = list(data[4])
    spend_time = list(data[3])
    start_time = np.array(end_time)
    N = len(spend_time)
    width = 0.55

    # 日期格式的转换
    xtime = []
    for i in start_time:
        i = i.replace('.', '-')
        xtime.append(np.datetime64(i))
    xtime = np.array(xtime)

    # 求时间间隔
    xt = []
    for i in range(0, len(xtime)):
        if i==0:
            xt.append(0)
        else:
            xt.append(xtime[i] - xtime[i-1])


    x_sp = np.array(xt).astype(int)     # 计算日程起始点
    x_sp = [x*4 for x in x_sp]
    x_days = np.array([float(x)/2 for x in spend_time])   # 计划天数
    x_finish = np.array([float(x)/2 for x in spend_time])    # 已完成天数


    y = -np.sort(-np.arange(N))

    # 计算总天数
    # xtick = np.arange('2018-06-07', '2018-06-13', dtype='datetime64[D]')

    # 累计求和
    x_sp = np.cumsum(x_sp)
    fig1 = plt.figure(figsize=fig1_size)
    # gs = gridspec.GridSpec(6,3)
    # ax1 = fig.add_subplot(gs[:2,2])
    # ax1.set_title('SDP2_0.3时长统计', fontsize=20)
    ax2 = fig1.add_subplot(1,1,1)

    ax2.barh(y, x_sp+x_days, width+0.1, tick_label=labels, color='pink', alpha=1)
    ax2.barh(y, x_sp+x_finish, width-0.1, tick_label=labels, color='#006633', alpha=1)
    ax2.barh(y, x_sp, width+0.2, tick_label=labels, color='w', alpha=1)

    n = 0
    for xy in zip((x_sp+x_days),y):
        plt.annotate( str("开发者:" + owner[n] + "    " + "时长:" + str(spend_time[n]))
                      , xy=xy, xytext=((x_sp+x_days)[n]+1,y[n]), fontsize=10 )
        n += 1

    ax2.tick_params(length=7, width=2)
    # ax.locator_params('x', nbins=5)

    plt.ylabel("任务")
    plt.xlabel("日期", )
    fig1.subplots_adjust(left=fig1_left, bottom=fig1_bottom)
    ax2.set_title('%s任务分解图' % version, fontsize=20)
    # ax.set_xticks(x_sp,)
    plt.xticks(x_sp, np.array(end_time), rotation=45)
    ax2.set_xlim(0, 40)
    # ax.xaxis.set_major_locator(np.array(end_time))
    plt.savefig(filename)

    fig2 = plt.figure()
    ax1 = fig2.add_subplot(1,1,1)
    ax1.bar(range(len(total_time)), total_time[3], width)
    ax1.set_title('%s工作量统计' % version, fontsize=20)
    plt.xticks(range(len(total_time)),list(total_time.index))
    plt.ylabel('工作量(小时)')
    plt.xlabel('开发者')

    for xy in zip(range(len(total_time)), list(total_time[3]) ):
        plt.annotate( str(xy[1]) , xy=xy, xytext=xy )

    plt.savefig(filename2)


if __name__ == "__main__":
    version = 'SDP2_v0.3'
    fig1_size = (12, 16)
    fig1_left = 0.45
    fig1_bottom = 0.09
    # word_to_excel(version)
    get_gantt_chart(version)
    print("完成")