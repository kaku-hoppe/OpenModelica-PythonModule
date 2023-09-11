from OMPython import OMCSessionZMQ

import os
import tempfile


class OMModule(object):
    def __init__(self):
        """
        Basic module for Python.
        """

        self.getSession = OMCSessionZMQ()

        self.mainFile = ""
        self.modelName = ""
        self.subModels = []

        self.quantitiesList = []
        self.paralist = {}
        self.inputlist = {}
        self.outputlist = {}
        self.contilist = {}
        self.simOptions = {}
        self.overridevariables = {}
        self.simoptionsoverride = {}
        self.tempdir = ""

    def __sendCommand(self, api, string):
        self.getSession.sendExpression(api + "(\"" + string + "\")")
        result = self.getSession.sendExpression("getErrorString()")
        if result is not None:
            return result
        return True

    def __getModelName(self):
        # メインファイルの一行目を取得し、スペースで分割。
        # 後ろの文字を返してくれる。
        self.modelName = "test"
        return True

    def __paraFromXML(self):
        return

    def loadFile(self, mainfile=None, submodels=None):
        if mainfile is None:
            print("File does not exist")
            return False
        self.mainFile = mainfile

        print("=====Start LoadFile======")
        print("======Load main file======")
        print("=======1. " + self.mainFile)
        self.__sendCommand("loadFile", "\"" + self.mainFile + "\"")

        if submodels is not None:
            self.subModels = submodels
            print("=======Load subModel======")
            for _filepath in self.subModels:
                self.__sendCommand("loadFile", _filepath)
        print("=====End LoadFile======")
        return True

    def buildModel(self):
        self.__getModelName()
        self.tempdir = tempfile.mktemp()
        self.__sendCommand("buildModel", self.modelName)
        return True

    def getXMLpara(self):
        return True

    def getConti(self):
        return True

    def getPara(self):
        return True

    def getQuant(self):
        return True

    def simulate(self):
        return True
