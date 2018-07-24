from openpyxl import load_workbook
from openpyxl.drawing.image import Image
import pandas as pd
from datetime import date
from datetime import timedelta
from datetime import datetime
from xiamen_analysis.get_data import get_data, get_token


def save_data(total_data, user_slice, merchant_award, word):
    filename = "data/" + date + ".xlsx"
    writer = pd.ExcelWriter(filename)
    total_data.to_excel(writer, '总数据')
    user_slice.to_excel(writer, '用户明细')
    merchant_award.to_excel(writer, '商家明细数据')
    word.to_excel(writer, '商家集字明细')
    writer.save()

def save_report(today ,start_col, date, total_data, user_slice, merchant_award, word):
    if start_col == 66:
        filepath = "D:\\pycharm\\test\\xiamen_analysis\\报表模板.xlsx"
    else:
        filepath = "D:\\pycharm\\test\\xiamen_analysis\\%s.xlsx" % today

    wb = load_workbook(filename=filepath)

    sheet_total = wb.get_sheet_by_name('主页')
    sheet_figure = wb.get_sheet_by_name('趋势图表')
    sheet_user = wb.get_sheet_by_name('用户明细')
    sheet_merchant = wb.get_sheet_by_name('商家明细')


    total_data = list(total_data[date])
    i = 9
    for cell in total_data:
        sheet_total[str(chr(start_col)+ str(i))] = cell
        i += 1

    img = Image("D:\\pycharm\\test\\xiamen_analysis\\figure\\%s.png" % date)
    sheet_figure.add_image(img, 'B6')

    user_pv_slice = list(user_slice['pv'])
    user_uv_slice = list(user_slice['uv'])
    j, k = 8, 33
    for cell_pv in user_pv_slice[5:]:
        sheet_user[str(chr(start_col) + str(j))] = cell_pv
        j += 1
    for cell_uv in user_uv_slice[5:]:
        sheet_user[str(chr(start_col) + str(k))] = cell_uv
        k += 1


    if today == date:
        if merchant_award.empty:
            pass
        else:
            merchant_award = merchant_award
            merchant_row = 8
            benediction_row = 8
            no_threshold_pend_row = 8
            no_threshold_used_row = 8
            threshold_pend_row = 8
            threshold_used_row = 8
            prize_total_row = 8



            for merchant in merchant_award.index:
                sheet_merchant[chr(66) + str(merchant_row)] = merchant
                merchant_row += 1
            for benediction in merchant_award['benediction']:
                sheet_merchant[chr(67) + str(benediction_row)] = benediction
                benediction_row += 1
            for no_threshold_pend in merchant_award['no_threshold_pend']:
                sheet_merchant[chr(68) + str(no_threshold_pend_row)] = no_threshold_pend
                no_threshold_pend_row += 1
            for no_threshold_used in merchant_award['no_threshold_used']:
                sheet_merchant[chr(69) + str(no_threshold_used_row)] = no_threshold_used
                no_threshold_used_row += 1
            for threshold_pend in merchant_award['threshold_pend']:
                sheet_merchant[chr(70) + str(threshold_pend_row)] = threshold_pend
                threshold_pend_row += 1
            for threshold_used in merchant_award['threshold_used']:
                sheet_merchant[chr(71) + str(threshold_used_row)] = threshold_used
                threshold_used_row += 1
            for prize_total in merchant_award['prize_total']:
                sheet_merchant[chr(72) + str(prize_total_row)] = prize_total
                prize_total_row += 1


        if word.empty:
            pass
        else:
            merchant_name_row = 22
            word_row = 22
            completed_word_row = 22
            pv_row = 22

            for merchant_name in word.index:
                sheet_merchant[chr(66) + str(merchant_name_row)] = merchant_name
                merchant_name_row += 1

            for words in word['word']:
                sheet_merchant[chr(67) + str(word_row)] = words
                word_row += 1

            for completed_word_pv in word['complete_word_pv']:
                sheet_merchant[chr(68) + str(completed_word_row)] = completed_word_pv
                completed_word_row += 1

            for pv in word['pv']:
                sheet_merchant[chr(69) + str(pv_row)] = pv
                pv_row += 1

    wb.save("%s.xlsx" % today)


def get_days(n, end_day):
    n_days_ago = end_day - timedelta(days=n)
    return str(n_days_ago)

if __name__ == "__main__":

    # date = '2018-05-15'
    # token = get_token()
    # data = get_data(token, date)
    # word = data['word']
    # total_data = data['total_data']
    # user_slice = data['user_slice']
    # merchant_award = data['merchant_award']
    # save_data(total_data, user_slice, merchant_award, word)



    # days = ['2018-05-15', '2018-05-16', '2018-05-17', '2018-05-18',
    #         '2018-05-19', '2018-05-20', '2018-05-21', '2018-05-22',]
    end_day = date(2018, 5, 21)
    start_day = date(2018, 5 ,15)
    n = (end_day - start_day).days
    days = []
    while n > -1:
        days.append(get_days(n, end_day))
        n -= 1

    # (today - get_days(5)).days

    today = days[-1]
    start_col = 66
    for date in days:
        token = get_token()
        data = get_data(token, date)
        word = data['word']
        total_data = data['total_data']
        user_slice = data['user_slice']
        merchant_award = data['merchant_award']
        save_report(today, start_col, date, total_data,user_slice, merchant_award, word)
        start_col += 1