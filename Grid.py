# -*- coding: cp1251

class Grid():
    '''
    Класс сеток.
    '''
    
    partitions = []

    def __init__(self, toleranceRange, nOfGenes):
        '''
        Представляет ОДЗ toleranceRange в виде сетки из 
        2**nOfGenes гиперпараллелепипедов меньшего размера.
        '''
        
        self.nOfGenes = nOfGenes
        self.nOfIntervalsInDimension = 2**self.nOfGenes
        self.nOfDimensions = len(toleranceRange)
        
        self.partitions = []
        for interval in toleranceRange:
            a = float(interval[0])
            b = float(interval[1])
            h = (b - a)/float(self.nOfIntervalsInDimension)
            oneDimensionIntervals = []
            for i in range(self.nOfIntervalsInDimension):
                oneDimensionIntervals.append([a+i*h, a+(i+1)*h])
            self.partitions.append(oneDimensionIntervals)
            
            
    def __getitem__(self, index):
        '''
        Возвращает центр интервала закодированного идентификатором index.
        '''
#        i = int(index//self.nOfIntervalsInDimension)
        center = []
        for i in range(len(self.partitions)):
            center.append( (self.partitions[i][index][0] + self.partitions[i][index][1])/2 )
#            print (self.partitions[i][index][0] + self.partitions[i][index][1])/2
        return center
        
    
    def __len__(self):
        return len(self.partitions)
            
if __name__ == '__main__':
#    pass
    toleranceRange = [[-10, 10], [-100, 100], [-200, 200]]
    grid = Grid(toleranceRange, 5)
    print grid[0]
#    for i in range(grid.nOfDimensions):
#        print grid.partitions[i]
#    print grid[0]
