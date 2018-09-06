# -*- coding: cp1251

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SetPlatformSpecPreferences import *

class WidgetLog(QWidget):
    def __init__(self, title):
        QWidget.__init__(self)
        
        self.lblTitle = QLabel(title)
        self.txtLog = QTextEdit()
        self.txtLog.setFixedHeight(100)
        self.txtLog.setReadOnly(True)
        
        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.lblTitle)
        self.vbox.addWidget(self.txtLog)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
    log = WidgetLog('Лог')
    log.show()
    sys.exit(app.exec_())