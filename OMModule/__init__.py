import subprocess
import os
import tempfile
import xml.etree.ElementTree as XMLtree

from OMPython import OMCSessionZMQ


class OMModule(object):
    def __init__(self, outputDir=None):
        """
        Basic module for Python.
        """

        self.getSession = OMCSessionZMQ()
        self.baseDir = outputDir

        self.mainFile = ""
        self.modelName = ""
        self.subModels = []
        self.xmlFilePath = ""
        self.discretelist = {}
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

        for scalar in paraRoot.iter("ScalarVariable"):
            _variability = scalar.attrib["variability"]
            _name = scalar.attrib["name"]
            for _reals in scalar.iter("Real"):
                _reals_atrib = _reals.attrib
                if "start" in _reals_atrib.keys():
                    if _variability == "parameter":
                        self.paralist[_name] = _reals_atrib['start']
                    elif _variability == "continuous":
                        self.contilist[_name] = _reals_atrib['start']
                    elif _variability == "discrete":
                        self.discretelist[_name] = _reals_atrib['start']
        # must check other parameter

        return True

    def buildModel(self):
        self.__getModelName()
        self.tempdir = tempfile.mktemp()
        build_result = self.__sendCommand("buildModel", self.modelName)
        # check the error message
        if "error" in build_result:
            return build_result
        self.xmlFilePath = os.path.join(os.path.dirname(build_result[0]), build_result[1]).replace("\\", "/")
        self.__getValueFromXML()
        return True

    def getConti(self):
        return self.contilist

    def getPara(self):
        return self.paralist

    def getDiscrete(self):
        return self.discretelist

    def simulate(self):
        print("=====Start Simulation==================")
        print("======Write parameter in text file=====")
        f = open(self.modelName + "_SimParameter.txt", "w")
        # startTime, stopTime, stepSize and so on...

        for _parameter in self.contilist:
            f.write(_parameter[0] + "=" + _parameter[1] + "\n")
        f.close()
        print("======End of writing parameter=========")

        # sample data
        cmd = "C:/Users/test/デスクトップ/OMPython_testScript/BouncingBall.exe -overrideFile=C:/Users/test/デスクトップ/OMPython_testScript/BouncingBall_override.txt"

        OMHome = os.path.join(os.environ.get("OPENMODELICAHOME"))
        dllPath = os.path.join(OMHome, "bin").replace("\\", "/") + os.pathsep + os.path.join(OMHome, "lib/omc").replace(
            "\\", "/") + os.pathsep + os.path.join(OMHome, "lib/omc/cpp").replace("\\",
                                                                                  "/") + os.pathsep + os.path.join(
            OMHome, "lib/omc/omsicpp").replace("\\", "/")
        my_env = os.environ.copy()
        my_env["PATH"] = dllPath + os.pathsep + my_env["PATH"]
        p = subprocess.run(cmd, env=my_env)

        # result_simulation = omc.sendExpression("simulate(BouncingBall, stopTime=20.0, numberOfIntervals = 200, outputFormat=\"csv\")")
        # print("=====result_simulation====")
        # print(result_simulation)
        print(p)
        return True
