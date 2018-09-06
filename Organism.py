# -*- coding: cp1251

from random import *
from Grid import *


class MetaOrganism(type):
    '''
    Метакласс организма, реализующий базовую настройку класса.
    '''
    def __new__(cls, name, bases, dct):
#        print "meta: creating %s %s" % (name, bases)
        return type.__new__(cls, name, bases, dct)
    
    def Configure(cls, 
                  OptFunction,
                  toleranceRange,
                  nOfGenes,
                  FitnessFunction,
                  Encode,
                  Decode,
                  areCrossoverPointsDiffer,
                  areMutationPointsDiffer):
        
        cls.OptFunction = OptFunction
        cls.toleranceRange = toleranceRange
        cls.nOfGenes = nOfGenes
        cls.FitnessFunction = FitnessFunction
        cls.Encode = Encode
        cls.Decode = Decode
        cls.areCrossoverPointsDiffer = areCrossoverPointsDiffer
        cls.areMutationPointsDiffer = areMutationPointsDiffer
        
        cls.grid = Grid(toleranceRange, cls.nOfGenes)
#        print 'LENGTH', len(cls.grid)
        

class Organism(object):
    __metaclass__ = MetaOrganism
    '''
    Класс, реализующий функциональность организмов.
    '''
    #
    #    Сделать настройщик класса, который будет всегда вызываться при его использовании.
    #
    

    def __init__(self, isRandom=True, sign=0):
        '''
        Конструктор, генерирующий случайное значение признака.
        '''
        if isRandom:
            self.sign = randrange(2**self.nOfGenes)
        else:
            self.sign = sign 
    
    
    def __cmp__(self, other):
        '''
        Оператор сравнения организмов, используется для сравнеия их по фитнес-атрибуту.
        '''
        return cmp(self.fitness, other.fitness)
    
    
    def __getitem__(self, index):
        '''
        Определяет доступ к генам организма. Вкупе со срезкой творит чудеса.
        '''
        return self.Encode(self.sign, self.nOfGenes)[index]
    
    
#    def CountFittness(self, totalFitness, maxFitness, nOfOrganisms):
#        self.fitness = self.FitnessFunction(totalFitness, maxFitness, nOfOrganisms)
#        return self.fitness
    
    
    def opt(self):
        '''
        Возвращает текущее значение оптимимума.
        '''
#        
        return self.OptFunction()
    
    
    def argopt(self):
        '''
        Возвращает текущее значение аргумента оптимума.
        '''
#        print 'LENGTH', len(self.grid.partitions)
        return self.grid[self.sign]
    
    
    def GenerateRandomPointsListForCrossover(self, numberOfPoints, arePointsDiffer):
        '''
        Генерирует N раз случайных точек кроссовера. Снизу добавлен 0, 
        сверху добавлен numberOfPoints при areMarginsIncluded = True.
        
        ИСКЛЮЧЕНИЕ.
        numberOfPoints <= self.nOfGenes - 2
        '''
        setPoints = set()
       
        if arePointsDiffer:
            while len(setPoints) < numberOfPoints:
                setPoints.add(randrange(Organism.nOfGenes))
        else:
            for i in range(numberOfPoints):
                setPoints.add(randrange(Organism.nOfGenes))
        
#        if areMarginsIncluded:
        setPoints.add(0)
        setPoints.add(Organism.nOfGenes) 
#        print setPoints
        return sorted(list(setPoints))
    
    
    def GenerateRandomPointsListForMutation(self, numberOfPoints, arePointsDiffer):
        '''
        Генерирует N раз случайных точек кроссовера. Снизу добавлен 0, 
        сверху добавлен numberOfPoints при areMarginsIncluded = True.
        
        ИСКЛЮЧЕНИЕ.
        numberOfPoints <= self.nOfGenes - 2
        '''
        
        if arePointsDiffer:
            setPoints = set()
            while len(setPoints) < numberOfPoints:
                setPoints.add(randrange(Organism.nOfGenes))
            return sorted(list(setPoints))
        else:
            listPoints = []
            for i in range(numberOfPoints):
                listPoints.append(randrange(Organism.nOfGenes))
            return sorted(listPoints)
    
    
    def Chromo2List(self, chromo, listPoints):
        '''
        Разделяет хромосому точками кроссовера из listPoints
        '''
        lP = listPoints
        parts = []
        for i in range(len(lP)-1):
#            print lP[i],lP[i+1]
            part = chromo[lP[i]:lP[i+1]]
            parts.append(part)
        return parts
        
    
    def List2Chromo(self, list):
        '''
        Собирает список фрагментов в хромосому.
        '''
        str = ''
        for elem in list:
            str += elem
        return str
    
    
    def CrossoverLists(self, listFather, listMother):
        '''
        Скрещивает 2 списка, т.е. создает третий список, где четные элементы из первого списка,
        нечетные - из второго.
        '''
        listChild = []
        for i in range(min(len(listFather), len(listMother))):
            
            isOdd = i%2
            if not isOdd:
                listChild.append(listFather[i])
            else:
                listChild.append(listMother[i])
        return listChild 

    
    def Crossover(self, other, numberOfPoints):
        '''
        Многоточечный кроссовер.
        
        ИСКЛЮЧЕНИЕ: self, other из одного и того же класса.
        '''
        
        # Генерируем numberOfPoints точек кроссовера.
        self.lastCrossoverPoints = self.GenerateRandomPointsListForCrossover(numberOfPoints, self.areCrossoverPointsDiffer)
#        print listPoints
        # Разделяем хромосомы точками кроссовера.
        selfParts = self.Chromo2List(self[:], self.lastCrossoverPoints)
        otherParts = other.Chromo2List(other[:], self.lastCrossoverPoints)
        # "Скрещиваем" списки кусочков.
        childParts = self.CrossoverLists(selfParts, otherParts)
        childChromo = self.List2Chromo(childParts)
        
        # Заполним несколько полей для информации.
        self.lastOther = other
        self.lastChild = Organism(False, self.Decode(childChromo))
        
        return self.lastChild
    
    
    def Mutate(self, numberOfPoints):
        '''
        Оператор многоточечной мутации, инвертирует numberOfPoints случайных битов.
        '''
        # Генерируем numberOfPoints точек мутации.
        self.lastMutationPoints = self.GenerateRandomPointsListForMutation(numberOfPoints, self.areMutationPointsDiffer)
        # Изменим последний бит у всех частей, кроме последней
        mutatedChromo = self[:]
        for p in self.lastMutationPoints:
            if mutatedChromo[p] == '0':
                mutatedChromo = mutatedChromo[:p] + '1' + mutatedChromo[p+1:]
            else:
                mutatedChromo = mutatedChromo[:p] + '0' + mutatedChromo[p+1:]
        
        self.beforeMutationSign = self.sign
        self.sign = self.Decode(mutatedChromo)
        
        
        
    
    def GetLastCrossoverInfo(self):
        listInfo = []
        listInfo.append('Crossover:')
        listInfo.append(self.sign)
        listInfo.append(self[:])
        listInfo.append('+')
        listInfo.append(self.lastOther.sign)
        listInfo.append(self.lastOther[:])
        listInfo.append('=>')
        listInfo.append(self.lastCrossoverPoints)
        listInfo.append('=>')
        listInfo.append(self.lastChild.sign)
        listInfo.append(self.lastChild[:])
#        listInfo.append('\n')
        return listInfo
#        return self.sign, self[:], '+', self.lastOther.sign, self.lastOther.Encode(self.lastOther.sign, self.lastOther.nOfGenes )
    
    def GetLastMutationInfo(self):
        listInfo = []
        listInfo.append('Mutation:')
        listInfo.append(self.beforeMutationSign)
        listInfo.append(self.Encode(self.beforeMutationSign, self.nOfGenes))
        listInfo.append('=>')
        listInfo.append(self.lastMutationPoints)
        listInfo.append('=>')
        listInfo.append(self.sign)
        listInfo.append(self[:])
        return listInfo
            
if __name__ == '__main__':
    pass
#    Organism.nOfGenes =  8 
#    org1 = Organism()
#    print org1.Encode(0)
        