#!python3
# coding=utf-8

import os
import collections
import configparser


class IniConfig(object):
    """
    [section]
    key = value
    [mysql]
    user = xxx
    password = xxx
    port = 3306
    uri = %(user)s@%(password):%(port)s
    """

    def __init__(self, delimiters=('=',), ini_file=None):
        self.conf = configparser.ConfigParser(dict_type=collections.OrderedDict, delimiters=delimiters)
        self.ini_file = ini_file
        self.read()

    def __repr__(self):
        return self.details()

    def __str__(self):
        return self.details()

    def read(self):
        if os.path.exists(self.ini_file):
            self.conf.read(self.ini_file, encoding='utf-8')
        else:
            self.conf = None
        if self.conf is None:
            raise FileNotFoundError(self.ini_file)

    def write(self):
        with open(self.ini_file, "w") as f:
            self.conf.write(f)

    def details(self):
        msg = ""
        for section in self.get_sections():
            # print("[{}]".format(section))
            msg += "[{}]".format(section) + "\n"
            dict_items = self.get_items(section)
            for key, value in dict_items.get(section).items():
                # print("{} = {}".format(key, value))
                msg += "{} = {}\n".format(key, value)
        return msg

    def to_json(self):
        ini_to_json = {}
        for section in self.get_sections():
            ini_to_json = {**ini_to_json, **self.get_items(section)}
        return ini_to_json

    def get_items(self, section='DEFAULT', fmt='json'):
        """
        :return: get section all key-value pair, default json format
        """

        items_list = self.conf.items(section)
        if fmt != "json":
            return items_list
        section_dict = dict()
        section_dict[section] = dict()
        for key, value in items_list:
            section_dict[section][key] = value
        return section_dict

    def has_section(self, section):
        return self.conf.has_section(section)

    def get_sections(self):
        return self.conf.sections()

    def has_key(self, section, key):
        return self.conf.has_option(section, key)

    def get_keys(self, section):
        if self.has_section(section):
            return self.conf.options(section)
        else:
            return None

    def get_value(self, section, key):
        if self.has_key(section, key):
            return self.conf.get(section, key)
        else:
            return None

    def set_value(self, section, key, value):
        if self.has_section(section):
            self.conf.set(section, key, value)
            self.write()
        else:
            raise configparser.NoSectionError(section)

    def add_section(self, section):
        if not self.has_section(section):
            self.conf.add_section(section)

    def get_bool_value(self, section, key):
        """
        yes/on, 1/0, on/off, true/false...
        return True/False
        :param section:
        :param key:
        :return:
        """
        if self.has_key(section, key):
            return self.conf.getboolean(section, key)
        return None

    def compare(self, cmp):
        if not isinstance(cmp, self.__class__):
            raise TypeError(type(cmp))
        cur_json = self.to_json()
        cmp_json = cmp.to_json()
        diff_section = set(cur_json) ^ set(cmp_json)
        for section in self.get_sections():
            if section not in diff_section:
                cur_section = cur_json.get(section, {})
                cmp_section = cmp_json.get(section, {})
                for key, value in cur_section.items():
                    if key not in cmp_section.keys():
                        print("diff", section, key)
                        diff_section.add(section)
                    if value != cmp_section.get(key, value):
                        diff_section.add("{}:{}".format(section, key))
        return diff_section


class YamlConfig(object):
    def __init__(self, yaml_file):
        pass
        self.yaml_file = yaml_file
        self.yaml_config = None
        self.read()

    def read(self):
        """
        :return: json data
        """
        try:
            import yaml
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(e)
        if not os.path.exists(self.yaml_file):
            raise FileNotFoundError(self.yaml_file)
        with open(self.yaml_file, 'r') as f:
            self.yaml_config = yaml.load(f, Loader=yaml.FullLoader)

    def write(self):
        try:
            import yaml
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(e)
        
        with open(self.yaml_file, 'w') as yf:
            yf.write(yaml.dump(self.yaml_config, default_flow_style=False))

    def set_value(self, node, value):
        self.yaml_config.setdefault(node, value)

    def get_value(self, node):
        value = self.yaml_config.get(node, {})
        return value

    def details(self):
        print(self.yaml_config)


def test_ini():
    ini_file = "D:\\tmp\\business.ini"
    nms_file = "D:\\tmp\\nms.ini"
    ini_conf = IniConfig(ini_file=ini_file)
    nms_conf = IniConfig(ini_file=nms_file)

    a = ini_conf.compare(nms_conf)
    print(a)


def test_yaml():
    ycf = "D:\\tmp\\config.yml"
    ylc = YamlConfig(ycf)
    # print(ylc)
    ylc.details()
    print(ylc.get_value("pg_conn"))


if __name__ == '__main__':
    # test_ini()
    test_yaml()
