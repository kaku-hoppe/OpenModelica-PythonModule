from OMPython import OMCSessionZMQ

import os


class OMModule(object):
    def __init__(self, filedir=None, lmodel=[], useCorba=False, commandLineOptions=None):
        """
        Basic module for Python.
        :param filedir : ~~.mo
        :param lmodel :
        :param useCorba:
        :param commandLineOptions:
        """

        if filedir is None:
            print("File does not exist")
            return

        self.getSession = OMCSessionZMQ()

        self.fileDir = filedir
        self.fileName = ""
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

    def __getModelName(self, fileName):
        # メインファイルの一行目を取得し、スペースで分割。
        # 後ろの文字を返してくれる。
        print("")

    def loadFile(self, filedir):
        print("=====startLoadFile======")
        self.__sendCommand("loadFile", filedir + ", ")
