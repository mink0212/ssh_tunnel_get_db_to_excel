import configparser

from py_module.exception.my_exception import MyException

class ConfigAccess:
    config = None
    section = None

    def __init__(self, file_name, section=None) -> None:
        config_parser = configparser.ConfigParser()
        config_parser.read(file_name, encoding='utf-8')
        self.config = config_parser
        self.section = section

    def input_value(self, section, key) -> str:
        print(section + 'の' + key + 'は読み込めませんでした。値を入力してください')
        print('>>> ', end='')
        value = input()
        return value

    def get_str(self, key, section=None) -> str:
        section = self.section if section is None else section

        try:
            value = self.config[section][key]
            if value is None or value == '':
                return self.input_value(section, key)

        except:
            return self.input_value(section, key)

    def get_int(self, key, section=None):
        section = self.section if section is None else section

        try:
            return self.config.getint(section, key)

        except:
            try:
                return int(self.input_value(section, key))

            except Exception as e:
                raise MyException('入力が不正です。', e)

    def get_section_items(self, section=None):
        section = self.section if section is None else section

        return self.config[section]
