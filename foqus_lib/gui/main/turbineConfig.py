'''
    turbineConfig.py

    * This is the workings of the Turbine profile editor.

    John Eslick, Carnegie Mellon University, 2014

    This Material was produced under the DOE Carbon Capture Simulation
    Initiative (CCSI), and copyright is held by the software owners:
    ORISE, LANS, LLNS, LBL, PNNL, CMU, WVU, et al. The software owners
    and/or the U.S. Government retain ownership of all rights in the
    CCSI software and the copyright and patents subsisting therein. Any
    distribution or dissemination is governed under the terms and
    conditions of the CCSI Test and Evaluation License, CCSI Master
    Non-Disclosure Agreement, and the CCSI Intellectual Property
    Management Plan. No rights are granted except as expressly recited
    in one of the aforementioned agreements.
'''
import os
from foqus_lib.framework.sim.turbineConfiguration\
    import TurbineInterfaceEx
from foqus_lib.framework.sim.turbineConfiguration\
    import turbineConfiguration
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog
mypath = os.path.dirname(__file__)
_turbineConfigUI, _turbineConfigFrame = \
        uic.loadUiType(os.path.join(mypath, "turbineConfig_UI.ui"))


class turbineConfig(_turbineConfigFrame, _turbineConfigUI):
    '''
        This class provides a dialog box that allows you to create, a
        Turbine configuration file.
    '''
    def __init__(self, dat, cfile=None, parent=None):
        super(turbineConfig, self).__init__(parent=parent)
        self.setupUi(self)
        self.dat = dat
        # Check if the cfile path is an actual turbine config
        if not self.isTurbineConfig(cfile):
            self.cfile = None
        else:
            self.cfile = cfile
        # make a turbine config object to save and load turbine configs
        if self.cfile:
            self.tconf = turbineConfiguration(self.cfile)
            self.tconf.readConfig()
        else:
            self.tconf = turbineConfiguration()
        # fill out default information
        self.addressEdit.setText(self.tconf.address)
        self.userEdit.setText(self.tconf.user)
        self.pwdEdit.setText(self.tconf.pwd)
        # Set up the turbine version select box
        if self.tconf.turbVer == "Lite":
            self.verBox.setCurrentIndex(0)
            self.selectTV(0)
        else:
            self.verBox.setCurrentIndex(1)
            self.selectTV(1)
        self.verBox.currentIndexChanged.connect(self.selectTV)
        # connect the buttons
        self.saveButton.clicked.connect(self.saveConf)
        self.saveAsButton.clicked.connect(self.saveAsConf)
        self.cancelButton.clicked.connect(self.reject)
        self.testButton.clicked.connect(self.testConfig)

    def isTurbineConfig(self, cfile):
        try:
            if not os.path.isfile(cfile):
                return False
        except:
            return False
        #need to add check file format
        return True

    def apply(self):
        self.tconf.address = self.addressEdit.text()
        self.tconf.user = self.userEdit.text()
        self.tconf.pwd = self.pwdEdit.text()

    def selectTV(self, i):
        if i == 0:
            self.userEdit.setEnabled(False)
            self.pwdEdit.setEnabled(False)
        else:
            self.userEdit.setEnabled(True)
            self.pwdEdit.setEnabled(True)

    def saveConf(self):
        self.apply()
        if self.isTurbineConfig(self.cfile):
            self.accept()
        else:
            self.saveAsConf()

    def saveAsConf(self):
        self.apply()
        fileName, filtr = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "cfg files (*.cfg);;All Files (*)")
        if fileName:
            self.tconf.path = fileName
            self.accept()
        else:
            return

    def accept(self):
        '''
            If pressed the save button make the configuration file
        '''
        if self.tconf.getFile() != None:
            self.tconf.writeConfig()
        self.done(QDialog.Accepted)

    def reject(self):
        self.done(QDialog.Rejected)

    def testConfig(self):
        QMessageBox.information(
            self,
            "Test",
            ("The Turbine configuration format and Turbine connection"
             " will be tested.  This may take some time." ))
        errList = self.dat.flowsheet.turbConfig.testConfig()
        if len(errList) == 0:
            QMessageBox.information(
                self,
                "Success",
                "The Turbine configuration is okay.")
        else:
            QMessageBox.information(
                self,
                "Error",
                str(errList))
