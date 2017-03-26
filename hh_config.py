class data:
    def __init__(self):
        self.db_name = ''
        self.server_name = ''
        self.timeout = 0
        self.requirments = []
        self.conditions = []
        self.expectations = []

    def load_from_conf(self):
        cfg = {}
        try:
            exec(open("config.ini").read(), cfg)
            self.db_name = cfg['db_name']
            self.server_name = cfg['server_name']
            self.timeout = cfg['timeout']
            self.requirments = cfg['requirments']
            self.conditions = cfg['conditions']
            self.expectations = cfg['expectations']
        except:
            print('Ошибка при загрузке config.ini!')
    
    def rdb_name(self):
        return self.db_name

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