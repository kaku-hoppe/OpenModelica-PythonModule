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

    def __sendCommand(self, api, string):
        api_string = api + "(" + string + ")"
        result = self.getSession.sendExpression(api_string)
        print("api: "+api_string)
        print("result: "+str(result))
        return result

    def __getModelName(self):
        with open(self.mainFile) as f:
            for line in f:
                if line != "":
                    mName = line.split()
                    self.modelName = mName[1]
                    return True
        return False

    def loadFile(self, mainfile=None, submodels=None):
        if mainfile is None:
            print("File does not exist")
            return False
        self.mainFile = mainfile

        print("=====Start LoadFile=======")
        print("======Load main file======")
        print("=======1. " + self.mainFile)
        self.__sendCommand("loadFile", "\"" + self.mainFile + "\"")

        if submodels is None:
            print("=====End LoadFile======")
            return False

        self.subModels = submodels
        print("=======Load subModel======")
        for _filepath in self.subModels:
            self.__sendCommand("loadFile", "\"" + _filepath + "\"")
        print("=====End LoadFile=========")
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
        if self.baseDir is None:
            self.baseDir = tempfile.mkdtemp()
        change_dir = self.__sendCommand("cd", "\"" + self.baseDir + "\"") # self.baseDir
        print("cd result: "+str(change_dir))
        # if not change_dir:
        #     print("Folder does not exist.")
        #     return False

        # build_result = self.__sendCommand("buildModel", self.modelName)
        api = "buildModel(BouncingBall)"
        build_result = self.getSession.sendExpression(api)
        print(api+" : "+build_result[0]+" "+build_result[1])
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
        _overrideFile_Path = self.baseDir + "/" + self.modelName + "_SimParameter.txt"
        print(_overrideFile_Path)
        _cmd_override = " -overrideFile=" + _overrideFile_Path
        f = open(_overrideFile_Path, "w")
        f.write("stopTime=10")
        f.close()

        for _simOption in self.simOptions:
            f.write(_simOption[0] + "=" + _simOption[1] + "\n")

        for _parameter in self.contilist:
            f.write(_parameter[0] + "=" + _parameter[1] + "\n")
        f.close()
        print("======End of writing parameter=========")

        # sample data
        # cmd = "C:/Users/test/デスクトップ/OMPython_testScript/BouncingBall.exe -overrideFile=C:/Users/test/デスクトップ/OMPython_testScript/BouncingBall_override.txt"
        cmd = self.baseDir + "/" + self.modelName + ".exe" + _cmd_override
        print(cmd)
        OMHome = os.path.join(os.environ.get("OPENMODELICAHOME"))
        dllPath = os.path.join(OMHome, "bin").replace("\\", "/") + os.pathsep + os.path.join(OMHome, "lib/omc").replace("\\", "/") + os.pathsep + os.path.join(OMHome, "lib/omc/cpp").replace("\\", "/") + os.pathsep + os.path.join(OMHome, "lib/omc/omsicpp").replace("\\", "/")
        my_env = os.environ.copy()
        my_env["PATH"] = dllPath + os.pathsep + my_env["PATH"]
        p = subprocess.run(cmd, env=my_env)

        # result_simulation = omc.sendExpression("simulate(BouncingBall, stopTime=20.0, numberOfIntervals = 200, outputFormat=\"csv\")")
        # print("=====result_simulation====")
        # print(result_simulation)
        print(p)
        return True


if __name__ == '__main__':
    output_dir = input("write output directory : ")
    sim_dir = input("write simfile directory : ")
    OMM = OMModule(output_dir)
    OMM.loadFile(sim_dir)
    OMM.buildModel()
    OMM.simulate()
    print("Hello World")
