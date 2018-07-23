import pandas as pd
import json


def change_to_csv():
    filename = '/Users/pengyi/PycharmProjects/pengyi/data/bus8684.json'
    datas = open(filename, encoding='utf8')
    lines = datas.readlines()

    for line in lines:
        line = json.loads(line)
        information = [line['province'], line['city'], line['line__name'], line['line_attribute'], line['run_time'],
                       line['ticket_price'], line['company'], line['update_time'], str(line['bus_stations'])]
        print(information)
        information = pd.DataFrame(information).T
        information.to_csv('/Users/pengyi/PycharmProjects/pengyi/data/bus8684.csv', mode='a', encoding='gb18030', header=None, index=False)


def get_city_information(city):
    all_data = pd.read_csv('/Users/pengyi/PycharmProjects/pengyi/data/bus8684.csv', encoding='gb18030' ,
                           names=['province', 'city', 'line_name', 'line_attribute', 'run_time',
                                  'ticket_price', 'company', 'update_time', 'bus_stations'])
    try:
        city_information = all_data[all_data['city'] == city].reset_index(drop=True)
        filename = '/Users/pengyi/PycharmProjects/pengyi/data/bus_line/%s.xlsx' % city
        city_information.to_excel(filename)
        print(city_information)
    # except:
    #     print('没有%s这个城市' % city )
    except Exception as e:
        print(e)


if __name__ == '__main__':
    get_city_information('无锡')