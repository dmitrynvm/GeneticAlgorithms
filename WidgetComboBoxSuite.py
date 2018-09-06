# -*- coding: cp1251

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from SetPlatformSpecPreferences import *

class WidgetComboBoxSuite(QWidget):
    
    
    def __init__(self, title, items):
        QWidget.__init__(self)
        
        self.lblTitle = QLabel(title)
        self.comboBox = QComboBox()
        for item in items:
            self.comboBox.addItem(item)
        self.comboBox.setFixedSize(100, 20)
            
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.lblTitle)
        self.hbox.addWidget(self.comboBox)       
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
    spinBoxSuite = WidgetComboBoxSuite('Число организмов популяции', ['1', '2'])
    spinBoxSuite.show()
    sys.exit(app.exec_())