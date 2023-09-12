import subprocess
import os
import tempfile
import xml.etree.ElementTree as XMLtree

from OMPython import OMCSessionZMQ


class OMModule(object):
    def __init__(self):
        """
        Basic module for Python.
        """

        self.getSession = OMCSessionZMQ()

        self.mainFile = ""
        self.modelName = ""
        self.subModels = []
        self.xmlFilePath = ""
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
        result = self.getSession.sendExpression(api + "(\"" + string + "\")")
        Error_message = self.getSession.sendExpression("getErrorString()")
        if Error_message is not None:
            return Error_message
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

        print("=====Start LoadFile=======")
        print("======Load main file======")
        print("=======1. " + self.mainFile)
        self.__sendCommand("loadFile", self.mainFile)

        if submodels is not None:
            self.subModels = submodels
            print("=======Load subModel======")
            for _filepath in self.subModels:
                self.__sendCommand("loadFile", _filepath)
        print("=====End LoadFile======")
        return True

    def __getValueFromXML(self):
        paraTree = XMLtree.ElementTree(file=self.xmlFilePath)
        paraRoot = paraTree.getroot()
        for defExp in paraRoot.iter("DefaultExperiment"):
            self.simOptions["startTime"] = defExp.attrib["startTime"]
            self.simOptions["stopTime"] = defExp.attrib["stopTime"]
            self.simOptions["stepSize"] = defExp.attrib["stepSize"]
            self.simOptions["outputFormat"] = defExp.attrib["outputFormat"]
            self.simOptions["variableFilter"] = defExp.attrib["variableFilter"]

        for Models in paraRoot.iter("ModelVariables"):
            for scalar in Models.iter("ScalarVariable"):
                _variability = scalar.attrib["variability"]
                _name = scalar.attrib["name"]
                if _variability == "parameter" or _variability == "continuous":
                    for _reals in scalar.iter("Real"):
                        _reals_atrib = _reals.attrib
                        if "start" in _reals_atrib.keys():
                            self.paralist[_name] = _reals_atrib['start']

        return

    def buildModel(self):
        self.__getModelName()
        self.tempdir = tempfile.mktemp()
        xlmfiles = self.__sendCommand("buildModel", self.modelName)
        # check the error message
        if "error" in xlmfiles:
            return xlmfiles

        self.XMLFilePath = os.path.join(os.path.dirname(xlmfiles[0]), xlmfiles[1]).replace("\\", "/")
        self.__getValueFromXML()
        return True

    def getConti(self):
        return True

    def getPara(self):
        return True

    def getQuant(self):
        return True

    def simulate(self):
        # sample data
        cmd = "C:/Users/test/デスクトップ/OMPython_testScript/BouncingBall.exe -overrideFile=C:/Users/test/デスクトップ/OMPython_testScript/BouncingBall_override.txt"

        OMHome = os.path.join(os.environ.get("OPENMODELICAHOME"))
        dllPath = os.path.join(OMHome, "bin").replace("\\", "/") + os.pathsep + os.path.join(OMHome, "lib/omc").replace(
            "\\", "/") + os.pathsep + os.path.join(OMHome, "lib/omc/cpp").replace("\\",
                                                                                  "/") + os.pathsep + os.path.join(
            OMHome, "lib/omc/omsicpp").replace("\\", "/")
        my_env = os.environ.copy()
        my_env["PATH"] = dllPath + os.pathsep + my_env["PATH"]
        p = subprocess.Popen(cmd, env=my_env)
        p.wait()
        p.terminate()

        # result_simulation = omc.sendExpression("simulate(BouncingBall, stopTime=20.0, numberOfIntervals = 200, outputFormat=\"csv\")")
        # print("=====result_simulation====")
        # print(result_simulation)
        print("\n")
        return True
