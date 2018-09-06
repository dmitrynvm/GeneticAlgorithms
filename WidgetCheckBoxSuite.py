# -*- coding: cp1251

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SetPlatformSpecPreferences import *

class WidgetCheckBoxSuite(QWidget):
    
    
    def __init__(self, title):
        QWidget.__init__(self)
        
        self.lblTitle = QLabel(title)
        self.checkBox = QCheckBox()
        
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.lblTitle)
        self.hbox.addWidget(self.checkBox)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
    spinBoxSuite = WidgetCheckBoxSuite('Все различны')
    spinBoxSuite.show()
    sys.exit(app.exec_())