# -*- coding: cp1251

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *


from BinCodec import *
from FitnessFunctions import *
from OptimizingFunctions import *
from Organism import *
from Population import *


from WidgetCheckBoxSuite import *
from WidgetComboBoxSuite import *
from WidgetSpinBoxSuite import *
from WidgetTableSuite import *


class WidgetGA(QWidget):
    def __init__(self):
        QWidget.__init__(self)
    
        title = 'База данных функций'
        horizontalHeaders = QStringList()
        horizontalHeaders << 'Название' << 'Вид' << 'x*' << 'f(x*)'
        A = [['Квадратичная функция', 'x^2 - 31*x', '(15.5)', '-240.25'],
             ['Функция Розенброка', '100*(x2-x1^2)^2 + (1-x1)^2', '(1,1)', '0'],
             ['Функция Матье', '0.26*(x1^2 + x2^2) - 0.48*x1*x2', '(0,0)', '0']] 
        self.tblSuiteFunctionsDB = WidgetTableSuite(title, horizontalHeaders, A)
        self.tblSuiteFunctionsDB.table.setMinimumWidth(400)
        self.tblSuiteFunctionsDB.table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        
        self.spinSuiteNOfFunction = WidgetSpinBoxSuite('Номер', 3)
        self.spinSuiteNOfFunction.spinBox.setMinimum(1)
        self.lblToleranceRange = QLabel('Область допустимых значений')
        self.lblToleranceRange.setAlignment(Qt.AlignHCenter)
        self.spinSuiteA1 = WidgetSpinBoxSuite('a1', 1000)
        self.spinSuiteA1.spinBox.setMinimum(-1000)
        self.spinSuiteA2 = WidgetSpinBoxSuite('a2', 1000)
        self.spinSuiteA2.spinBox.setMinimum(-1000)
        self.spinSuiteB1 = WidgetSpinBoxSuite('b1', 1000)
        self.spinSuiteB1.spinBox.setMinimum(-1000)
        self.spinSuiteB2 = WidgetSpinBoxSuite('b2', 1000)
        self.spinSuiteB2.spinBox.setMinimum(-1000)
        self.butOptimize = QPushButton('Оптимизировать')
        self.butOptimize.setFixedSize(100, 32)
        QObject.connect(self.butOptimize, SIGNAL('clicked()'), self.ButOptimizeClick)
        self.butSetToDefaults = QPushButton('По-умолчанию')
        self.butSetToDefaults.setFixedSize(100, 32)
        QObject.connect(self.butSetToDefaults, SIGNAL('clicked()'), self.SetToDefaults)
        self.progressGeneration = QProgressBar()
        self.lblx = QLabel('x* =')
        self.lblfx = QLabel('f(x*) =')
        
        self.spinSuiteNOfOrganisms = WidgetSpinBoxSuite('Число организмов популяции', 300, step=5)
        self.spinSuiteNOfGenes = WidgetSpinBoxSuite('Число генов организма', 16)
        self.comboSuiteCodingProcedure = WidgetComboBoxSuite('Способ кодирования',['Код Грея', 'Бинарный код'])
        self.spinSuiteNOfGenerations = WidgetSpinBoxSuite('Число поколений', 1000, False, 5)
#        self.spinSuiteEpsilon = WidgetSpinBoxSuite('Эпсилон', 10, True, 0.1)
        self.spinSuiteCrossoverProbability = WidgetSpinBoxSuite('Вероятность кроссовера', 1, True, 0.1)
        self.spinSuiteNOfCrossoverPoints = WidgetSpinBoxSuite('Число точек кроссовера', 16)
        self.checkSuiteAreCrossoverPointsDiffer = WidgetCheckBoxSuite('Все точки кроссовера различны')
        self.spinSuiteMutationProbability = WidgetSpinBoxSuite('Вероятность мутации', 1, True, 0.1)
        self.spinSuiteNOfMutatingPoints = WidgetSpinBoxSuite('Число мутирующих генов', 16)
        self.checkSuiteAreMutationPointsDiffer = WidgetCheckBoxSuite('Все мутирующие гены различны')
        
        self.hboxA1B1 = QHBoxLayout()
        self.hboxA1B1.addWidget(self.spinSuiteA1)
        self.hboxA1B1.addWidget(self.spinSuiteB1)
        self.hboxA2B2 = QHBoxLayout()
        self.hboxA2B2.addWidget(self.spinSuiteA2)
        self.hboxA2B2.addWidget(self.spinSuiteB2)
        self.hboxButtons = QHBoxLayout()
        self.hboxButtons.addWidget(self.butOptimize)
        self.hboxButtons.addWidget(self.butSetToDefaults)
        
        self.vboxFunctionOptions = QVBoxLayout()
        self.vboxFunctionOptions.addWidget(self.tblSuiteFunctionsDB)
        
        self.vboxGroupedFunctionOptions = QVBoxLayout()
        self.vboxGroupedFunctionOptions.addWidget(self.spinSuiteNOfFunction)
        self.vboxGroupedFunctionOptions.addWidget(self.lblToleranceRange)
        self.vboxGroupedFunctionOptions.addLayout(self.hboxA1B1)
        self.vboxGroupedFunctionOptions.addLayout(self.hboxA2B2)
        
        
        self.groupFunctionOptions = QGroupBox()
        self.groupFunctionOptions.setTitle('Настройки минимизируемых функций')
        self.groupFunctionOptions.setLayout(self.vboxGroupedFunctionOptions)
        self.vboxFunctionOptions.addWidget(self.groupFunctionOptions)
        self.vboxFunctionOptions.addWidget(self.lblx)
        self.vboxFunctionOptions.addWidget(self.lblfx)
        self.vboxFunctionOptions.addWidget(self.progressGeneration)
        self.vboxFunctionOptions.addLayout(self.hboxButtons)
       

        self.vboxGAOptions = QVBoxLayout()
        self.vboxIntegralOptions = QVBoxLayout()
        self.vboxCrossoverOptions = QVBoxLayout()
        self.vboxMutationOptions = QVBoxLayout()
        self.groupIntegralOptions = QGroupBox()
        self.groupCrossoverOptions = QGroupBox()
        self.groupMutationOptions = QGroupBox()
        
        
        self.vboxIntegralOptions.addWidget(self.spinSuiteNOfOrganisms)
        self.vboxIntegralOptions.addWidget(self.spinSuiteNOfGenes)
        self.vboxIntegralOptions.addWidget(self.comboSuiteCodingProcedure)
        self.vboxIntegralOptions.addWidget(self.spinSuiteNOfGenerations)
#        self.vboxIntegralOptions.addWidget(self.spinSuiteEpsilon)
        self.vboxCrossoverOptions.addWidget(self.spinSuiteCrossoverProbability)
        self.vboxCrossoverOptions.addWidget(self.spinSuiteNOfCrossoverPoints)
        self.vboxCrossoverOptions.addWidget(self.checkSuiteAreCrossoverPointsDiffer)
        self.vboxMutationOptions.addWidget(self.spinSuiteMutationProbability)
        self.vboxMutationOptions.addWidget(self.spinSuiteNOfMutatingPoints)
        self.vboxMutationOptions.addWidget(self.checkSuiteAreMutationPointsDiffer)
        
        self.groupIntegralOptions.setTitle('Общие настройки ГА')
        self.groupIntegralOptions.setLayout(self.vboxIntegralOptions)
        self.groupCrossoverOptions.setTitle('Настройки оператора кроссовера')
        self.groupCrossoverOptions.setLayout(self.vboxCrossoverOptions)
        self.groupMutationOptions.setTitle('Настройки оператора мутации')
        self.groupMutationOptions.setLayout(self.vboxMutationOptions)
        
        self.vboxGAOptions.addWidget(self.groupIntegralOptions)
        self.vboxGAOptions.addWidget(self.groupCrossoverOptions)
        self.vboxGAOptions.addWidget(self.groupMutationOptions)
        
        
        
        self.hboxTotal = QHBoxLayout(self)
        self.hboxTotal.addLayout(self.vboxFunctionOptions)
        self.hboxTotal.addLayout(self.vboxGAOptions)
        
        self.SetToDefaults()
        
        
    def SetToDefaults(self):
        self.spinSuiteNOfFunction.spinBox.setValue(2)
        self.spinSuiteA1.spinBox.setValue(-10)
        self.spinSuiteB1.spinBox.setValue(10)
        self.spinSuiteA2.spinBox.setValue(-10)
        self.spinSuiteB2.spinBox.setValue(10)
        self.spinSuiteNOfOrganisms.spinBox.setValue(20)
        self.spinSuiteNOfGenes.spinBox.setValue(8)
        self.comboSuiteCodingProcedure.comboBox.setCurrentIndex(0)
        self.spinSuiteNOfGenerations.spinBox.setValue(10)
#        self.spinSuiteEpsilon.spinBox.setValue(0.1)
        self.spinSuiteCrossoverProbability.spinBox.setValue(0.8)
        self.spinSuiteNOfCrossoverPoints.spinBox.setValue(1)
        self.checkSuiteAreCrossoverPointsDiffer.checkBox.setChecked(True)
        self.spinSuiteMutationProbability.spinBox.setValue(0.1)
        self.spinSuiteNOfMutatingPoints.spinBox.setValue(1)
        self.checkSuiteAreMutationPointsDiffer.checkBox.setChecked(True)
        
    
    def GetOptions(self):
        self.nOfFunction = self.spinSuiteNOfFunction.spinBox.value()
        self.a1 = self.spinSuiteA1.spinBox.value()
        self.b1 = self.spinSuiteB1.spinBox.value()
        self.a2 = self.spinSuiteA2.spinBox.value()
        self.b2 = self.spinSuiteB2.spinBox.value()
        self.nOfOrganisms = self.spinSuiteNOfOrganisms.spinBox.value()
        self.nOfGenes = self.spinSuiteNOfGenes.spinBox.value()
        self.nOfCodingProcedure = self.comboSuiteCodingProcedure.comboBox.currentIndex()
        self.nOfGenerations = self.spinSuiteNOfGenerations.spinBox.value()
#        self.epsilon = self.spinSuiteEpsilon.spinBox.value()
        self.crossoverProbability = self.spinSuiteCrossoverProbability.spinBox.value()
        self.nOfCrossoverPoints = self.spinSuiteNOfCrossoverPoints.spinBox.value()
        self.areCrossoverPointsDiffer = self.checkSuiteAreCrossoverPointsDiffer.checkBox.isChecked()
        self.mutationProbability = self.spinSuiteMutationProbability.spinBox.value()
        self.nOfMutatingPoints = self.spinSuiteNOfMutatingPoints.spinBox.value()
        self.areMutationPointsDiffer = self.checkSuiteAreMutationPointsDiffer.checkBox.isChecked()
        

    def PrintOptions(self):
        print 'nOfFunction:', self.nOfFunction
        print 'a1:', self.a1
        print 'b1:', self.b1
        print 'a2:', self.a2
        print 'b2:', self.a2
        print 'nOfOrganisms:', self.nOfOrganisms
        print 'nOfGenes:', self.nOfGenes
        print 'nOfCodingProcedure:', self.nOfCodingProcedure
        print 'nOfGenerations:', self.nOfGenerations
#        print 'epsilon:', self.epsilon
        print 'crossoverProbability:', self.crossoverProbability
        print 'nOfCrossoverPoints:', self.nOfCrossoverPoints
        print 'areCrossoverPointsDiffer', self.areCrossoverPointsDiffer
        print 'mutationProbability:', self.mutationProbability
        print 'nOfMutatingPoints:', self.nOfMutatingPoints
        print 'areMutationPointsDiffer', self.areMutationPointsDiffer
    
    
    def SaveOptionsToStream(self, outf):
        outf << 'ХОД ЭВОЛЮЦИИ' << '\n\n\n'
        outf << 'Характеристики генетической системы' << '\n'
        outf << 'nOfFunction: ' << self.nOfFunction << '\n'
        outf << 'a1:  ' << self.a1 << '\n'
        outf << 'b1: ' << self.b1 << '\n'
        outf << 'a2: ' << self.a2 << '\n'
        outf << 'b2: ' << self.a2 << '\n'
        outf << 'nOfOrganisms: ' << self.nOfOrganisms << '\n'
        outf << 'nOfGenes: ' << self.nOfGenes << '\n'
        outf << 'nOfCodingProcedure: ' << self.nOfCodingProcedure << '\n'
        outf << 'nOfGenerations: ' << self.nOfGenerations << '\n'
#        outf << 'epsilon: ' << self.epsilon << '\n'
        outf << 'crossoverProbability: ' << self.crossoverProbability << '\n'
        outf << 'nOfCrossoverPoints: ' << self.nOfCrossoverPoints << '\n'
        outf << 'areCrossoverPointsDiffer: ' << self.areCrossoverPointsDiffer << '\n'
        outf << 'mutationProbability: ' << self.mutationProbability << '\n'
        outf << 'nOfMutatingPoints: ' << self.nOfMutatingPoints << '\n'
        outf << 'areMutationPointsDiffer: ' << self.areMutationPointsDiffer << '\n'
    
    
    def SaveIntegralInfoToFile(self, filename, integralInfo):
        file = QFile(filename)  
        file.open(QFile.WriteOnly | QFile.Text)
        outf = QTextStream(file)
        self.SaveOptionsToStream(outf)
        for i in range(len(integralInfo)):
            outf << str(integralInfo[i])
  
    
    def ButOptimizeClick(self):
        self.GetOptions()
#        self.PrintOptions()
        
        # Интерпретация пользовательского ввода.
        if self.nOfFunction == 1:
            self.OptFunction = QuadraticFunction
            self.toleranceRange = [[self.a1, self.b1]]
        elif self.nOfFunction == 2:
            self.OptFunction = RosenbrokFunction
            self.toleranceRange = [[self.a1, self.b1], [self.a2, self.b2]]
        elif self.nOfFunction == 3:
            self.OptFunction = MatyasFunction
            self.toleranceRange = [[self.a1, self.b1], [self.a2, self.b2]]
        
        self.FitnessFunction = FitnessFunction1
        if self.nOfCodingProcedure == 0:
            self.Encode = Dec2Gray
            self.Decode = Gray2Dec
        elif self.nOfCodingProcedure == 1:
            self.Encode = Dec2Bin
            self.Decode = Bin2Dec
        
        # Настраиваем класс Organism методом его метакласса Configure.
        Organism.Configure(self.OptFunction,                         # Оптимизируемая функция;
                           self.toleranceRange,                 # Ее ОДЗ;
                           self.nOfGenes,                       # Число генов организма;
                           self.FitnessFunction,                # Его фитнес-функция;
                           self.Encode,                         # Функция кодирования признака;
                           self.Decode,                         # Функция декодирования признака;
                           self.areCrossoverPointsDiffer,       # Различны ли точки кроссовера?;
                           self.areMutationPointsDiffer)        # Различны ли точки мутации?
       
       # Создаем популяцию организмов.
        pop = Population(Organism,                  # Класс организмов, населяющих популяцию;
                         self.nOfOrganisms,         # Число организмов, , населяющих популяцию;
                         self.crossoverProbability, # Вероятность кроссовера;
                         self.nOfCrossoverPoints,   # Число точек кроссовера;
                         self.mutationProbability,  # Вероятность мутации;
                         self.nOfMutatingPoints)    # Число точек мутации.
        
        
        
        
#        self.progressGeneration.setModal(True)
#        self.progressGeneration.show()
        self.progressGeneration.setMaximum(self.nOfGenerations-1)
        
        for i in range(self.nOfGenerations):
            pop.Generate()
            self.progressGeneration.setValue(i)
        
        self.lblx.setText('x* = ' + str(pop[0].argopt()))
        self.lblfx.setText('f(x*) = ' + str(pop[0].opt()))
        
        pop.listInfo.append(['x* =' , pop[0].argopt()])
        pop.listInfo.append(['f(x*) = ', pop[0].opt()])
        
        self.SaveIntegralInfoToFile('SystemInfo.txt', pop.listInfo)
#        for i in range(len(pop.listInfo)):
#            print pop.listInfo[i]
#        print 'x* =', pop[0].argopt()
#        print 'f(x*) =', pop[0].opt()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    SetPlatformSpecPreferences()
    widgetGA = WidgetGA()
    widgetGA.show()
    sys.exit(app.exec_())