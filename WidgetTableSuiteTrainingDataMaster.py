# -*- coding: cp1251

import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from WidgetTableSuite import *


class WidgetTableSuiteTrainingDataMaster(WidgetTableSuite):
    def __init__(self, title, horizontalHeaders, textData):
        WidgetTableSuite.__init__(self, title, horizontalHeaders, textData)
        
        self._textData = textData
        self._horizontalHeaders = horizontalHeaders
        self.setWindowTitle('Мастер формирования обучающего множества')
        self._table.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        self._actSetFactorsData = QAction('Факторы', self)
        QObject.connect(self._actSetFactorsData, SIGNAL('triggered()'), self.__SetFactorsData)
        self._table.addAction(self._actSetFactorsData)
        
        self._actSetResponseData = QAction("Отклик", self)
        QObject.connect(self._actSetResponseData, SIGNAL('triggered()'), self.__SetResponseData)
        self._table.addAction(self._actSetResponseData)
        
        QObject.connect(self, SIGNAL("close()"), self.__Close)
    
    
    def __SetFactorsData(self):
        self._factorsColumns = set()
        for item in self._table.selectedItems():
            self._factorsColumns.add(self._table.column(item))

    
    def __SetResponseData(self):
        self._responseColumns = set()
        for item in self._table.selectedItems():
            self._responseColumns.add(self._table.column(item))
        
        nFactors = len(self._factorsColumns)
        nResponse = len(self._responseColumns)
        m = len(self._textData)
        listFactorsColumns = list(self._factorsColumns)
        listResponseColumns = list(self._responseColumns)
        
        listFactorsData=[]
        factorHeaders = QStringList()
        for i in range(len(listFactorsColumns)):
            listCur = list(self._textData[:,listFactorsColumns[i]])
            listFactorsData.append(listCur)
            factorHeaders << self._horizontalHeaders[listFactorsColumns[i]]
        factorsData = numpy.array(listFactorsData).transpose()
#        print factorHeaders.count()
        
        listResponseData=[]
        responseHeaders = QStringList()
        for i in range(len(listResponseColumns)):
            listCur = list(self._textData[:,listResponseColumns[i]])
            listResponseData.append(listCur)
            responseHeaders << self._horizontalHeaders[listResponseColumns[i]]
        responseData = numpy.array(listResponseData).transpose()
#        print responseHeaders.count()

        print responseData
        self._mainWindow.CreateWidgetInputData(factorHeaders, factorsData, responseHeaders, responseData)
    
    def SetMainWindow(self, mainWindow):
        self._mainWindow = mainWindow
 
    def __Close(self):
        print 'Closing'
    
def SetPlatformSpecPreferences():
    # Кодировка символов.
    codec = QTextCodec.codecForName('CP-1251')
    QTextCodec.setCodecForCStrings(codec)
    QTextCodec.setCodecForLocale(codec)
    QTextCodec.setCodecForTr(codec)      


if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
        
    horizontalHeaders = QStringList()
    horizontalHeaders << 'X' << 'Y'
    A = [['1', '2'], ['3', '4'], ['5', '6'], ['7', '8'], ['9', '10']] 
#    self._widgetTableSuiteInputData = WidgetTableSuite('Исходные данные', horizontalHeaders, A)
#    self._widgetTableSuiteInputData._table.setContextMenuPolicy(Qt.ActionsContextMenu)
#    dlg = DialogTrainingDataMaster()
    ts = WidgetTableSuiteTrainingDataMaster('Исходные данные', horizontalHeaders, A)
    ts.show()
    sys.exit(app.exec_())