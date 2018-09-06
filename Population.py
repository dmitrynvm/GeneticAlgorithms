# -*- coding: cp1251

from random import *


class Population():
    '''
    Класс популяции for minimizing his functions.
    '''
    # Фиксированное число организмов популяции. Остается постоянным на протяжении всей эволюции.
    
    # Биологический вид организмов (Которым присуща совокупность черт, необходимых для
    # решения конкретной задачи.
    # Фактически это ссылка на класс-организмов, предназаченный для порождения 
    # объектов-организмов, предназначенных для решения данной задачи.


    def __init__(self,
                 Species,                   # Биологический вид (класс) организмов популяции;
                 nOfOrganisms,              # Число организмов популяции;
                 crossoverProbability,
                 nOfCrossoverPoints,
                 mutationProbability,
                 nOfMutatingPoints):
        '''
        Создание начальной популяции
        '''
        #!!!
        #!!! Настройка класса популяции  с помощью статической функции.
        #!!!
        # Заполняем контейнер организмов
        
        self.Species = Species
        self.nOfOrganisms = nOfOrganisms
        self.crossoverProbability = crossoverProbability
        self.nOfCrossoverPoints = nOfCrossoverPoints
        self.mutationProbability = mutationProbability
        self.nOfMutatingPoints = nOfMutatingPoints
        
        self.organisms = []
        for i in range(self.nOfOrganisms):
            self.organisms.append(self.Species())
        
        # Расчет фитнеса особей популяции.
        self.Fitness(self.organisms)
        
        # Список с инфой
        self.listInfo = []
        self.currentGeneration = 0
    
    
    def __getitem__(self, index):
        '''
        Оператор [], определяет доступ к организмам популяции.
        '''
        return self.organisms[index]
        
        
    def Fitness(self, organisms):
        '''
        Расчитывает уровень приспособленности (фитнесс) для каждого организма 
        из organisms.
        '''
        
        # Список промежуточных (ненормированных) фитнес-значений.
        tmpFitnessList = []
        for i in range(len(organisms)):
            tmpFitnessList.append(organisms[i].OptFunction())
        
        # Расчет фитнеса ВСЕЙ популяции (Сумма значений признаков).
        totalFitness = sum(tmpFitnessList)
        # Расчет максимального фитнеса.
#        print tmpFitnessList
        maxFitness = max(tmpFitnessList)

        # Рачет индивидуальных фитнесов.   
        for org in organisms:
            org.FitnessFunction(totalFitness, maxFitness, len(organisms))
#            org.CountFittness(totalFitness, maxFitness, len(organisms))
#        for i in range(k):
#            organisms[i].fitness = self.FitnessFunction1(organisms[i].sign, )
        
        # Сортируем организмов по убыванию их фитнеса.
        organisms.sort(reverse=True)
    
    
    def GetSignList(self, organisms):
        '''
        Возвращает список признаков организмов из organisms.
        '''
        signList = []
        for org in organisms:
            signList.append(org.sign)
        return signList  
    
    
    def GetFitnessList(self, organisms):
        '''
        Возвращает список фитнесов организмов из organisms.
        '''
        fitnessList = []
        for org in organisms:
            fitnessList.append(org.fitness)
        return fitnessList

    
    def Generate(self):
        '''
        Генерация нового поколения.
        '''
         
         #
         #    ОПЕРАТОР СЕЛЕКЦИИ
         #
         
         # Реализация метода рулетки для селекции.
         
        # Создание рулетки (представлена отображением множества фитнесов на
        # список организмов с данным фитнесом.
        # Т.е. отображение множества всех значений фитнесов на множество всех
        # организмов.
        mapRoulette = {}
        for i in range(self.nOfOrganisms):
            if mapRoulette.has_key(self.organisms[i].fitness):
                mapRoulette[self.organisms[i].fitness].append(self.organisms[i])
            else:
                mapRoulette[self.organisms[i].fitness] = [self.organisms[i]]
        
        numberOfIntervals = len(mapRoulette.keys()) 
        # Множество интервалов рулетки [a, b]. Число интервалов равно mapRoulette.keys().
        intervals = []
        for i in range(1,numberOfIntervals+1):
            sum = 0
            for j in range(i):
                sum += j
            intervals.append([sum, sum+i])
        totalSum = sum + i
        
        
        def GetIntervalNumber(r, intervals):
            '''
            Локальная функция. Получить номер интервала из intervals, в которое попадает СВ r.
            '''
            for i in range(len(intervals)):
                if intervals[i][0] <= r <= intervals[i][1]:
                    return i
        
#        print str(self.currentGeneration)
        self.listInfo.append('\nПоколение ' + str(self.currentGeneration) + '\n')
        self.listInfo.append(self.GetSignList(self.organisms))
        self.listInfo.append('\n')
        self.listInfo.append(self.GetFitnessList(self.organisms))
        self.listInfo.append('\n')
        keys = sorted(mapRoulette.keys())
        childrenPool = []
        for i in range(self.nOfOrganisms):
            # Бросаем 2 случайных числа в рулетку (Для мамы и папы).        
            # Смотрим на какой интервал каждый из них попадает.
            # По номеру интевала выбираем список организмов из отображения mapRoulette
            # Из этого списка случайно выбираем организма-родителя.
            r = randrange(totalSum)
            q = randrange(totalSum)
            ri = GetIntervalNumber(r, intervals)
            qi = GetIntervalNumber(q, intervals)
            father = choice(mapRoulette[keys[ri]])
            mother = choice(mapRoulette[keys[qi]])
            #
            #    CROSSOVER OPERATOR
            #
#            probCrossover = random()
            
            #
            # Начинаем вести ЛОГ событий
            #
            
            

            # Разыгрываем СВ размножения
            if random() <= self.crossoverProbability:
                # 1. Скрещиваем.
                child = father.Crossover(mother, self.nOfCrossoverPoints)
                self.listInfo.append(father.GetLastCrossoverInfo())
                self.listInfo.append('\n')
                # Разыгрываем СВ мутации
                if random() <= self.mutationProbability:
                    # 2. Мутируем.
                    child.Mutate(self.nOfMutatingPoints)
                    self.listInfo.append(child.GetLastMutationInfo())
                    self.listInfo.append('\n')
                childrenPool.append(child)

        # Путь N - численность детей; заменяем N Организмов прошлого поколения,
        # на N организмов детей.
        self.organisms = self.organisms[:-len(childrenPool)] + childrenPool
        self.Fitness(self.organisms)
#        print '++++++1'
        self.currentGeneration += 1




if __name__ == '__main__':
    pass
#    # Атрибуты организма
#    nOfGenes = 8
#    areCrossoverPointsDiffer = True
#    areMutationPointsDiffer = True
#    Organism.Configure(QuadraticFunction,
#                       [[0,31]],
#                       nOfGenes,
#                       FitnessFunction1,
#                       Dec2Gray,
#                       Gray2Dec,
#                       areCrossoverPointsDiffer,
#                       areMutationPointsDiffer)
#    
#    # Атрибуты популяции
#    
#    pop = Population(Organism,
#                     100,
#                     0.8,
#                     1,
#                     0.1,
#                     1)
#    print pop.GetSignList(pop.organisms)
#    print pop.GetFitnessList(pop.organisms)
#    for i in range(10):
#        pop.Generate()
#        print pop.GetSignList(pop.organisms)
#        print pop.GetFitnessList(pop.organisms)
###   
#    print 'x* =', pop[0].argopt()
#    print 'f(x*) =', pop[0].opt()
