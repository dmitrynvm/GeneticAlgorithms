# -*- coding: cp1251
import GrayCode

'''
Модуль-обертка (wrapper) для модуля GrayCode.
Используется классом Organism из-за проблемы с лишней переменной self при манипулировании объектами-функциями.
'''
    
    
def Dec2Gray(self, num, numberOfDigits):
    '''
    [Encoder] Переводит десятичное число в код Грея.
     '''
    return GrayCode.dec2gray(num, numberOfDigits)
    
    
def Gray2Dec(self, gray):
    '''
    [Decoder] Переводит код Грея в десятичное число.
    '''
    return GrayCode.gray2dec(gray)
    
    
def Dec2Bin(self, num, numberOfDigits):
    '''
    [Encoder] Переводит десятичное число в двоичный код.
    '''
    return GrayCode.dec2bin(num, numberOfDigits)
    
    
def Bin2Dec(self, bin):
    '''
    [Decoder] Переводит двоичный код в десятичное число.
    '''
    return GrayCode.bin2dec(bin)