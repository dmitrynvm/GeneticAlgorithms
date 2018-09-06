# -*- coding: cp1251
import sys, random


def bin2gray(bin, numberOfDigits):
    '''
    Convert binary string to gray string.
    E.g. bin2gray('1010') ==> '1111' and  bin2gray('') ==> '0'.
    '''
    if not bin:
        return '0'
    cnt = 0
    gray = bin[0]
    while cnt < len(bin)-1:
        # Do XOR.
        gray = gray + str(int(bin[cnt] != bin[cnt+1]))
        # `...` returns '0' or '1'
        cnt = cnt + 1
    return Pad(gray, numberOfDigits)


def gray2bin(gray, numberOfDigits):
    '''
    Convert gray string to binary string.
    E.g. gray2bin('1111') ==> '1010' and gray2bin('') ==> '0.
    '''
    if not gray:
        return '0'
    cnt = 0
    bin = gray[0]
    while cnt < len(gray)-1:
        # Do XOR.
#        print int(bin[cnt] != gray[cnt+1])
        bin = bin + str(int(bin[cnt] != gray[cnt+1]))
        # `...` returns '0' or '1'
        cnt = cnt + 1
    return Pad(bin, numberOfDigits)


def dec2bin(num, numberOfDigits):
    """Convert long/integer number to binary string.
    E.g. dec2bin(12) ==> '1100'."""
    assert num >= 0, "Decimal number must be >= 0!"
    # Gracefully handle degenerate case.
    # (Not really needed, but anyway.)    
    if num == 0:
        return StringOfZeros(numberOfDigits)
    # Find highest value bit.
    val, j = 1L, 1L
    while val < num:
        val, j = val*2L, j+1L
    # Convert.
    bin = '' 
    i = j - 1
    while i + 1L:
        k = pow(2L, i)
        if num >= k:
            bin = bin + '1'
            num = num - k
        else:
            if len(bin) > 0:
                bin = bin + '0'
        i = i - 1L
    return Pad(bin, numberOfDigits)


def dec2gray(num, numberOfDigits):
    """Convert integer/long to gray string.
    E.g. dec2gray(8) ==> '1100'."""

    assert num >= 0, "Decimal number must be >= 0!"
    
    # Gracefully handle degenerate case.
    # (Not really needed, but anyway.)    
    if num == 0:
        return StringOfZeros(numberOfDigits)
    bin = dec2bin(num, numberOfDigits)
    gray = bin2gray(bin, numberOfDigits)
    return Pad(gray, numberOfDigits)
    

def bin2dec(bin):
    """Convert binary string to integer/long.
    E.g. bin2dec('1100') ==> 12."""
    # Gracefully handle degenerate case.
    # (Not really needed, but anyway.)    
    if bin in ('0', ''):
        return 0
    # Find highest value bit.
    val, j = 1L, 1L
    while j < len(bin):
        val, j = val*2, j+1L
    # Convert.
    num = 0L
    for j in range(len(bin)):
        if bin[j] == '1':
            num = num+val
        val = val/2
    # Return integer if possible, long otherwise.
    try:
        return int(num)
    except OverflowError:
        return num
    

def gray2dec(gray):
    """Convert gray string to integer/long.
    E.g. gray2dec('1100') ==> 10."""
    
    # Gracefully handle degenerate case.
    # (Not really needed, but anyway.)    
    if gray in ('0', ''):
        return 0
        
    bin = gray2bin(gray, len(gray))
    return bin2dec(bin)

   
def StringOfZeros(numberOfZeros):
    '''
    Возвращает строку из заданного числа нулей.
    '''
    str = ''
    for i in range(numberOfZeros):
        str += '0'
    return str


def Pad(binstr, numberOfDigits):
    '''
    Заполняет слева строку битов определенным числом (numberOfDigits) нулей.
    '''
    numberOfAdditionalZeros = numberOfDigits - len(binstr)
    if  numberOfAdditionalZeros > 0:
            return StringOfZeros(numberOfAdditionalZeros) + binstr
    else:
        return binstr[-numberOfAdditionalZeros:]
    
    
if __name__ == '__main__':
    print dec2bin(0)
