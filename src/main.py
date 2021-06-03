import re
import sys
import traceback
from datetime import datetime
from dateutil.relativedelta import relativedelta

from py_module.db.db_access import DbAccess
from py_module.exception.my_exception import MyException
from py_module.file.config_access import ConfigAccess
from py_module.file.excel_access import ExcelAccess
from py_module.ssh.ssh_access import SshAccess

def main():
    mode = input_check()

    try:
        ssh_config = ConfigAccess('../config/ssh.ini', mode)
        db_config = ConfigAccess('../config/db.ini', mode)
        excel = ExcelAccess('../excel/input.xlsx')
        db = DbAccess(db_config.get_section_items())

        if mode != 'LOCAL':
            ssh = SshAccess(ssh_config)
            ssh.ssh_start()

        exec_sql_edit_excel(excel, db)
        excel.save('../excel/output.xlsx')

    finally:
        if excel is not None:
            excel.close()

        if db is not None:
            db.close()

        if ssh is not None:
            ssh.ssh_close()

def exec_sql_edit_excel(excel, db):
    now_datetime = datetime.now()
    start_datetime = now_datetime - relativedelta(months=1)

    excel.insert_cols('追加数一覧', 5, True)
    excel.edit_cell('追加数一覧', 2, 5, datetime.strftime(start_datetime, '%m月'))

    rows = excel.get_row('取得用SQL', 3)
    for row_num, row in enumerate(rows):
        query = query_create(now_datetime, start_datetime, row)

        db_values = db.exec_multi_query_str(query)

        for db_value in db_values:
            result = 0 if db_value[0] is None else db_value[0]

            excel.edit_cell('追加数一覧', row_num + 3, 5, result)

def query_create(now_datetime, start_datetime, row):
    query = row[2].value
    query = re.sub(
        'time > \'[0-9]{4}-[0-9]{2}-[0-9]{2}\'',
        datetime.strftime(start_datetime, 'time > \'%Y/%m/%d 00:00:00\''),
        query
    )
    query = re.sub(
        'time < \'[0-9]{4}-[0-9]{2}-[0-9]{2}\'',
        datetime.strftime(now_datetime, 'time < \'%Y/%m/%d 00:00:00\''),
        query
    )
    return query

def input_check() -> str:
    if len(sys.argv) == 2:
        mode = sys.argv[1]
    else:
        print('DB環境を入力してください。')
        print('LOCAL, DEVELOP, PRODUCTION')
        print('>>> ', end='')
        mode = input()
    return mode

if __name__ == '__main__':
    try:
        main()
    except MyException as e:
        print('*** エラーメッセージ ***')
        print(e.my_message)
        print('*** トレースバック ***')
        print(traceback.format_exc())
