# -*- coding: utf-8 -*-

import configparser

class data:
    def __init__(self):
        self.db_name = ''
        self.server_name = ''
        self.username = None
        self.password = None
        self.timeout = 0
        self.requirments = []
        self.conditions = []
        self.expectations = []

    def load_from_conf(self):
        try:
            config = configparser.ConfigParser()
            config.read(['config\config.ini'], encoding='utf-8')
            self.server_name = config['DB Settings']['server_name']
            self.db_name = config['DB Settings']['db_name']
            self.username = config['DB Settings']['username']
            self.password = config['DB Settings']['password']
            self.timeout = int(config['Parsing Settings']['timeout'])
            self.conditions = self.string_to_list(config['Parsing Settings']['conditions'])
            self.requirments = self.string_to_list(config['Parsing Settings']['requirments'])
            self.expectations = self.string_to_list(config['Parsing Settings']['expectations'])
        except:
            print('Load config error!')

    def string_to_list(self, s):
        temp = s.replace('\n', '')
        in_list = temp.split(';')
        out_list = []
        for key in in_list:
            out_list.append(key.strip())
        return out_list

    def write_dbs_to_conf(self, db_name, server_name, username, password):
        pass

    def write_ps_to_conf(self, timeout, requirments, conditions, expectations):
        pass

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
