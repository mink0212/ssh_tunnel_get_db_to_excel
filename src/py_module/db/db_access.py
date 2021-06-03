from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from py_module.exception.my_exception import MyException

CONNECT_STR = '{driver}://{user}:{password}@{host}:{port}/{db_name}'

class DbAccess:
    engine = None
    session = None

    def __init__(self, db_config) -> None:
        try:
            connect_str = CONNECT_STR.format(**db_config)
            self.engine = create_engine(connect_str)
            self.session = sessionmaker(self.engine)

        except Exception as e:
            raise MyException('DB接続の設定が不正です。db_config.initを見直してください。', e)

    def exec_multi_query_str(self, queries) -> list:
        local_session = self.session()
        ret = []

        try:
            for query in queries.split(';'):
                if query.replace('\n', '') != '':
                    q = text(query + ';')
                    result = local_session.execute(q)

                    for row in result:
                        ret.append(row)

        except Exception as e:
            raise MyException('DBまたはSQLが不正です。DB設定またはSQLを見直してください。SQL: ' + queries, e)

        finally:
            local_session.close()

        return ret

    def close(self):
        self.session.close_all()
        self.engine.dispose()
