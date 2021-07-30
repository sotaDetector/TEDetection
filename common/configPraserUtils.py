import configparser
import logging
import os


class configUtils:


    cf = configparser.ConfigParser()
    cf.read('../config.ini')

    # 读取配置文件
    @classmethod
    def getConfigProperties(cls,category, propertiesName):

        return cls.cf.get(category, propertiesName)


print(configUtils.getConfigProperties("stun","urls"))