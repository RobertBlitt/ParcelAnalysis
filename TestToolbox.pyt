"""
Minimal Hawaii Matrix Toolbox - Test Version
"""

import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = "Hawaii Matrix Test"
        self.alias = "HawaiiTest"
        self.tools = [TestTool]

class TestTool(object):
    def __init__(self):
        self.label = "Test Tool"
        self.description = "Simple test tool"
        
    def getParameterInfo(self):
        return []
        
    def isLicensed(self):
        return True
        
    def updateParameters(self, parameters):
        return
        
    def updateMessages(self, parameters):
        return
        
    def execute(self, parameters, messages):
        messages.addMessage("Test successful!")
