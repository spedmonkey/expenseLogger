import sys
from PyQt4 import QtGui
import datetime
import json
import os

from time import gmtime, strftime

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.expensetype=['work clothes', 'work lunch', 'office equipment','work equipment', 'phone', 'internet', 'power']
        self.now = datetime.datetime.now()
        self.initUI()

    def initUI(self):
        #create widgets
        self.shapeTypeCB=QtGui.QComboBox(parent=self)
        self.description=QtGui.QLineEdit(self)
        self.myDate=QtGui.QDateEdit(self)
        self.myDate.setDate(self.now)
        self.receipt=QtGui.QLineEdit(self)
        self.submitBtn=QtGui.QPushButton('submit', self)

        self.amount=QtGui.QDoubleSpinBox()
        self.amount.setSingleStep(0.01)
        self.amount.setMaximum(10000)

        for i in self.expensetype:
            self.shapeTypeCB.addItem(i)
        #create action layout
        actionLayout = QtGui.QBoxLayout(QtGui.QBoxLayout.LeftToRight, self)

        #add widgets to layout
        actionLayout.addWidget(self.description)
        actionLayout.addWidget(self.shapeTypeCB)
        actionLayout.addWidget(self.myDate)
        actionLayout.addWidget(self.receipt)
        actionLayout.addWidget(self.amount)
        actionLayout.addWidget(self.submitBtn)

        #Connecting Signals
        self.submitBtn.clicked.connect(self.writeData)
        #self.connect(self.shapeTypeCB, QtCore.SIGNAL("currentIndexChanged(int)"), self.changeLabels)
        #self.connect(self.saveBtn, QtCore.SIGNAL("clicked()"), self.saveButton)
        #self.connect(self.loadBtn, QtCore.SIGNAL("clicked()"), self.loadAttr)
        self.show()

    def buttonPressed(self):
        try:
            self. copyImage()
            self.writeData()
            print 'data written'
        except:
            print "fail"

    def copyImage(self):
        self.receiptDate = self.myDate.date().toPyDate()
        os.system(
               "cp {0} ./reportData/{1}_{2}.jpg".format( self.receipt.text(),self.description.text(), self.receiptDate)
               )
        self.copyImageOutput="success"
        print "{0} receipt saved".format (self.description.text() )

    def getData(self):
        description=str(self.description.text())
        category=str(self.shapeTypeCB.currentText())
        amount=self.amount.value()
        self.expenseReport={}
        self.expenseReport[description]=[["description", description],["category", category ],['amount',amount]]
        return self.expenseReport

    def mergeData(self):
        myList=[]
        try:
            myList=self.readData()
        except:
            myList=[]
            pass
        myList.append([self.getData()])
    return myList


    def writeData(self):
        with open("./reportData/expenseReport.json", mode="a") as feedsjson:
            json.dump(myList, feedsjson, indent=4)
            feedsjson.write('\n')
        self.copyImage()

    def readData(self):
        try:
            with open (self.sceneDirectory+"./reportData/expenseReport.json") as feedsjson:
                expenseReport=json.load(feedsjson)
        except:
            expenseReport = []
        return  expenseReport

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()