import configparser
import logging
import os


class configUtils:
    cf = None

    def __init__(self):
        logging.info("start parse config...")

    @classmethod
    def _readConfig(cls):
        # 实例化ConfigParser
        cls.cf = configparser.ConfigParser()
        cls.cf.read('config.ini')


    # 读取配置文件
    @classmethod
    def getConfigProperties(cls, category, propertiesName):
        if cls.cf is None:
            cls._readConfig()
        return cls.cf.get(category, propertiesName)


