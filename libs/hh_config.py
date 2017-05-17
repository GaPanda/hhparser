# -*- coding: utf-8 -*-

from configparser import ConfigParser

class data:
    def __init__(self):
        self.db_name = None
        self.server_name = None
        self.username = None
        self.password = None
        self.timeout = 0
        self.requirments = []
        self.conditions = []
        self.expectations = []
        self.config_parser = ConfigParser()

    def load_from_conf(self):
        try:
            self.config_parser.read('config.ini', encoding='utf-8')
            self.server_name = self.config_parser.get('DB Settings', 'server_name')
            self.db_name = self.config_parser.get('DB Settings', 'db_name')
            self.username = self.config_parser.get('DB Settings', 'username')
            self.password = self.config_parser.get('DB Settings', 'password')
            self.timeout = float(self.config_parser.get('Parsing Settings', 'timeout'))
            self.conditions = self.string_to_list(
                self.config_parser.get('Parsing Settings', 'conditions'))
            self.requirments = self.string_to_list(
                self.config_parser.get('Parsing Settings', 'requirments'))
            self.expectations = self.string_to_list(
                self.config_parser.get('Parsing Settings', 'expectations'))
        except:
            print('Ошибка при загрузке config.ini!')

    def write_to_conf(self):
        try:
            self.config_parser.set(
                'DB Settings', 'server_name', self.server_name)
            self.config_parser.set('DB Settings', 'db_name', self.db_name)
            self.config_parser.set('DB Settings', 'username', self.username)
            self.config_parser.set('DB Settings', 'password', self.password)
            self.config_parser.set('Parsing Settings', 'timeout', str(self.timeout))
            self.config_parser.set(
                'Parsing Settings', 'conditions', self.list_to_string(self.conditions))
            self.config_parser.set(
                'Parsing Settings', 'requirments', self.list_to_string(self.requirments))
            self.config_parser.set(
                'Parsing Settings', 'expectations', self.list_to_string(self.expectations))
        except:
            print('Ошибка при сохранении.')

    def string_to_list(self, s):
        temp = s.replace('\n', '')
        in_list = temp.split(';')
        out_list = []
        for key in in_list:
            out_list.append(key.strip())
        return out_list

    def list_to_string(self, l):
        s = ''
        for i in range(0, len(l)):
            if i == (len(l) - 1):
                s = s + l[i] + ';'
            else:
                s = s + l[i]
        return s

    def dbs_to_conf(self, db_name, server_name, username, password):
        self.server_name = server_name
        self.db_name = db_name
        self.username = username
        self.password = password

    def ps_to_conf(self, timeout, requirments, conditions, expectations):
        self.timeout = timeout
        self.requirments = requirments
        self.conditions = conditions
        self.expectations = expectations

    def rdb_name(self):
        return self.db_name

    def rusername(self):
        return self.username

    def rpassword(self):
        return self.password

    def rserver_name(self):
        return self.server_name

    def rtimeout(self):
        return self.timeout

    def rrequirments(self):
        return self.requirments

    def rconditions(self):
        return self.conditions

    def rexpectations(self):
        return self.expectations
