# -*- coding: cp1251

from random import *


class Population():
    '''
    ����� ��������� for minimizing his functions.
    '''
    # ������������� ����� ���������� ���������. �������� ���������� �� ���������� ���� ��������.
    
    # ������������� ��� ���������� (������� ������� ������������ ����, ����������� ���
    # ������� ���������� ������.
    # ���������� ��� ������ �� �����-����������, �������������� ��� ���������� 
    # ��������-����������, ��������������� ��� ������� ������ ������.


    def __init__(self,
                 Species,                   # ������������� ��� (�����) ���������� ���������;
                 nOfOrganisms,              # ����� ���������� ���������;
                 crossoverProbability,
                 nOfCrossoverPoints,
                 mutationProbability,
                 nOfMutatingPoints):
        '''
        �������� ��������� ���������
        '''
        #!!!
        #!!! ��������� ������ ���������  � ������� ����������� �������.
        #!!!
        # ��������� ��������� ����������
        
        self.Species = Species
        self.nOfOrganisms = nOfOrganisms
        self.crossoverProbability = crossoverProbability
        self.nOfCrossoverPoints = nOfCrossoverPoints
        self.mutationProbability = mutationProbability
        self.nOfMutatingPoints = nOfMutatingPoints
        
        self.organisms = []
        for i in range(self.nOfOrganisms):
            self.organisms.append(self.Species())
        
        # ������ ������� ������ ���������.
        self.Fitness(self.organisms)
        
        # ������ � �����
        self.listInfo = []
        self.currentGeneration = 0
    
    
    def __getitem__(self, index):
        '''
        �������� [], ���������� ������ � ���������� ���������.
        '''
        return self.organisms[index]
        
        
    def Fitness(self, organisms):
        '''
        ����������� ������� ����������������� (�������) ��� ������� ��������� 
        �� organisms.
        '''
        
        # ������ ������������� (���������������) ������-��������.
        tmpFitnessList = []
        for i in range(len(organisms)):
            tmpFitnessList.append(organisms[i].OptFunction())
        
        # ������ ������� ���� ��������� (����� �������� ���������).
        totalFitness = sum(tmpFitnessList)
        # ������ ������������� �������.
#        print tmpFitnessList
        maxFitness = max(tmpFitnessList)

        # ����� �������������� ��������.   
        for org in organisms:
            org.FitnessFunction(totalFitness, maxFitness, len(organisms))
#            org.CountFittness(totalFitness, maxFitness, len(organisms))
#        for i in range(k):
#            organisms[i].fitness = self.FitnessFunction1(organisms[i].sign, )
        
        # ��������� ���������� �� �������� �� �������.
        organisms.sort(reverse=True)
    
    
    def GetSignList(self, organisms):
        '''
        ���������� ������ ��������� ���������� �� organisms.
        '''
        signList = []
        for org in organisms:
            signList.append(org.sign)
        return signList  
    
    
    def GetFitnessList(self, organisms):
        '''
        ���������� ������ �������� ���������� �� organisms.
        '''
        fitnessList = []
        for org in organisms:
            fitnessList.append(org.fitness)
        return fitnessList

    
    def Generate(self):
        '''
        ��������� ������ ���������.
        '''
         
         #
         #    �������� ��������
         #
         
         # ���������� ������ ������� ��� ��������.
         
        # �������� ������� (������������ ������������ ��������� �������� ��
        # ������ ���������� � ������ ��������.
        # �.�. ����������� ��������� ���� �������� �������� �� ��������� ����
        # ����������.
        mapRoulette = {}
        for i in range(self.nOfOrganisms):
            if mapRoulette.has_key(self.organisms[i].fitness):
                mapRoulette[self.organisms[i].fitness].append(self.organisms[i])
            else:
                mapRoulette[self.organisms[i].fitness] = [self.organisms[i]]
        
        numberOfIntervals = len(mapRoulette.keys()) 
        # ��������� ���������� ������� [a, b]. ����� ���������� ����� mapRoulette.keys().
        intervals = []
        for i in range(1,numberOfIntervals+1):
            sum = 0
            for j in range(i):
                sum += j
            intervals.append([sum, sum+i])
        totalSum = sum + i
        
        
        def GetIntervalNumber(r, intervals):
            '''
            ��������� �������. �������� ����� ��������� �� intervals, � ������� �������� �� r.
            '''
            for i in range(len(intervals)):
                if intervals[i][0] <= r <= intervals[i][1]:
                    return i
        
#        print str(self.currentGeneration)
        self.listInfo.append('\n��������� ' + str(self.currentGeneration) + '\n')
        self.listInfo.append(self.GetSignList(self.organisms))
        self.listInfo.append('\n')
        self.listInfo.append(self.GetFitnessList(self.organisms))
        self.listInfo.append('\n')
        keys = sorted(mapRoulette.keys())
        childrenPool = []
        for i in range(self.nOfOrganisms):
            # ������� 2 ��������� ����� � ������� (��� ���� � ����).        
            # ������� �� ����� �������� ������ �� ��� ��������.
            # �� ������ �������� �������� ������ ���������� �� ����������� mapRoulette
            # �� ����� ������ �������� �������� ���������-��������.
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
            # �������� ����� ��� �������
            #
            
            

            # ����������� �� �����������
            if random() <= self.crossoverProbability:
                # 1. ����������.
                child = father.Crossover(mother, self.nOfCrossoverPoints)
                self.listInfo.append(father.GetLastCrossoverInfo())
                self.listInfo.append('\n')
                # ����������� �� �������
                if random() <= self.mutationProbability:
                    # 2. ��������.
                    child.Mutate(self.nOfMutatingPoints)
                    self.listInfo.append(child.GetLastMutationInfo())
                    self.listInfo.append('\n')
                childrenPool.append(child)

        # ���� N - ����������� �����; �������� N ���������� �������� ���������,
        # �� N ���������� �����.
        self.organisms = self.organisms[:-len(childrenPool)] + childrenPool
        self.Fitness(self.organisms)
#        print '++++++1'
        self.currentGeneration += 1




if __name__ == '__main__':
    pass
#    # �������� ���������
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
#    # �������� ���������
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
