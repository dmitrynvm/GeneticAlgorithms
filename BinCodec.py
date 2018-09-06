# -*- coding: cp1251
import GrayCode

'''
������-������� (wrapper) ��� ������ GrayCode.
������������ ������� Organism ��-�� �������� � ������ ���������� self ��� ��������������� ���������-���������.
'''
    
    
def Dec2Gray(self, num, numberOfDigits):
    '''
    [Encoder] ��������� ���������� ����� � ��� ����.
     '''
    return GrayCode.dec2gray(num, numberOfDigits)
    
    
def Gray2Dec(self, gray):
    '''
    [Decoder] ��������� ��� ���� � ���������� �����.
    '''
    return GrayCode.gray2dec(gray)
    
    
def Dec2Bin(self, num, numberOfDigits):
    '''
    [Encoder] ��������� ���������� ����� � �������� ���.
    '''
    return GrayCode.dec2bin(num, numberOfDigits)
    
    
def Bin2Dec(self, bin):
    '''
    [Decoder] ��������� �������� ��� � ���������� �����.
    '''
    return GrayCode.bin2dec(bin)