import pandas as pd
from sqlalchemy import create_engine
import datetime
import paramiko
from sshtunnel import SSHTunnelForwarder

def get_voerhaul_data(filename):
      # ssh = paramiko.SSHClient()
      # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      # ssh.connect(hostname='192.168.2.192', port=22, username='root', password='soundbus')

      # filename = 'D:\\pycharm\\test\\xiamen_analysis\\voerhaul_data\\6-14-15.log'

      with SSHTunnelForwarder(
              ('192.168.2.192', 22),
              ssh_password="soundbus",
              ssh_username="root",
              remote_bind_address=('soundsdp00pan.mysqldb.chinacloudapi.cn', 3306)) as server:
            code = pd.read_table(filename, header=None, names=['date', 'sonic_code'])



            codes = (',').join("'"+(str(s)+"'") for s in tuple(code['sonic_code']))


            bus_db = {
                'user': 'soundsdp00pan%pan',
                'password': 'Soundbus2017#@!',
                'host': '127.0.0.1',
                'database': 'sdp',
                  'port' : server.local_bind_port
            }


            con = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s?charset=utf8' % bus_db
                                , encoding='utf-8', echo=True)

            sql = "SELECT " \
                  "plate_number, " \
                  "`name`, " \
                  "tmp1.sn_number, " \
                  "sonic_code " \
                  "FROM " \
                  "( " \
                  "( " \
                  "SELECT " \
                  "plate_number, " \
                  "id, " \
                  "sn_number " \
                  "FROM " \
                  "bus_car " \
                  "WHERE " \
                  "sn_number IN ( " \
                  "SELECT " \
                  "sn_number " \
                  "FROM " \
                  "bus_sonic_sn WHERE " \
                  "sonic_code IN ( %s ) ) ) tmp1 " \
                  "LEFT JOIN ( SELECT " \
                  "carline_id, car_id " \
                  "FROM " \
                  "bus_car_line_cars " \
                  ") tmp2 ON tmp1.id = tmp2.car_id " \
                  "LEFT JOIN ( SELECT `name`, id " \
                  "FROM bus_car_line ) tmp3 ON tmp2.carline_id = tmp3.id " \
                  "LEFT JOIN ( SELECT sonic_code, sn_number FROM " \
                  "bus_sonic_sn " \
                  ") tmp4 ON tmp4.sn_number = tmp1.sn_number" \
                  ")"  % (codes)

            bus_data = pd.read_sql(sql, con)
            result = pd.merge(bus_data, code, how='left', on='sonic_code')
            result_name = 'voerhaul_data/' + filename.split('/')[-1][:-4] + "检修数据.xlsx"
            result['时间'] = [datetime.datetime.strptime(('2018 ' + time).strip(),'%Y %b %d %H:%M:%S') for time in result['date']]
            result = result.drop(['sonic_code', 'date'], axis=1)
            result.rename(columns={'plate_number':'车牌', 'name':'线路', }, inplace=True)
            result = result.drop_duplicates(['车牌']).reset_index(drop=True)
            result.to_excel(result_name, index=True, columns=['线路', '车牌','sn_number','时间'])
            print(result)


if __name__ == "__main__":
      filename = '/Users/pengyi/PycharmProjects/pengyi/data/voerhaul_data/code_2018_07_18.log'
      get_voerhaul_data(filename)