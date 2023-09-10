from OMPython import OMCSessionZMQ

import os


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
        self.simulateOptions = {}
        self.overridevariables = {}
        self.simoptionsoverride = {}
        # self.linearOptions = {'startTime': 0.0, 'stopTime': 1.0, 'numberOfIntervals': 500, 'stepSize': 0.002,
        #                       'tolerance': 1e-8}
        # self.optimizeOptions = {'startTime': 0.0, 'stopTime': 1.0, 'numberOfIntervals': 500, 'stepSize': 0.002,
        #                         'tolerance': 1e-8}
        # self.linearquantitiesList = []  # linearization  quantity list
        # self.linearparameters = {}
        # self.linearinputs = []  # linearization input list
        # self.linearoutputs = []  # linearization output list
        # self.linearstates = []  # linearization  states list
        self.tempdir = ""

    def __sendCommand(self, api, string):
        self.getSession.sendExpression(api + "(" + string + ")")
        result = self.getSession.sendExpression("getErrorString()")
        if result is None:
            result = True
        return result

    def __getModelName(self):
        # メインファイルの一行目を取得し、スペースで分割。
        # 後ろの文字を返してくれる。
        self.modelName = "test"
        return True

    def loadFile(self, mainfile=None, submodels=None):
        if mainfile is None:
            print("File does not exist")
            return False
        self.mainFile = mainfile
        self.__getModelName()

        print("=====Start LoadFile======")
        print("======Load main file======")
        print("=======1. " + self.mainFile)
        self.__sendCommand("loadFile", "\"" + self.mainFile + "\", \"" + self.modelName + "\"")

        if submodels is not None:
            self.subModels = submodels
            print("=======Load subModel======")
            for _filepath in self.subModels:
                self.__sendCommand("loadFile", _filepath + ", ")
        print("=====End LoadFile======")
        return True




