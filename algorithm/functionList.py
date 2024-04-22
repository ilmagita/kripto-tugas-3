import base64
from typing import List
import sympy
import random
import os
import math
from math import gcd

def utf8_to_base64(utf8_text):
    return base64.b64encode(utf8_text.encode("utf-8")).decode("utf-8")

def base64_to_utf8(base64_text):
    utf8_text = base64.b64decode(base64_text).decode("utf-8")
    return utf8_text

def min_binary_length(int):
    lenght = math.floor(math.log2((int)))
    return lenght
    
def max_binary_length(int):
    max_length = math.ceil(math.log2(int + 1))
    return max_length

def binary_data_to_int_array(binary_data):
    array_of_integers = [int(byte) for byte in binary_data]
    return array_of_integers

def int_array_to_binary_data(array_of_integers):
    binary_data = bytes(array_of_integers)
    return binary_data

def read_hex_file(file):
    f = open(file,'r')
    contents = f.read()
    contents = contents.split('0x')
    contents = contents[1:]
    return (int('0x'+content,16) for content in contents)

def save_hex_file(cipherText, fileName):
    with open(fileName, 'w') as f:
        bytes = ""
        for value in cipherText:
                bytes += (str(value))
        f.write(bytes)

def are_relatife_prime(a,b):
    gcd_val = gcd(a,b)
    return gcd_val == 1

def random_prime_number():
    number = random.randint(1,9999999999)
    while not sympy.isprime(number):
        number = random.randint(1,9999999999)
    return number

def save_key_file(key, fileName):
    with open(fileName, 'w') as f:
        f.write(str(key))
        
def read_key_file(file):
    f = open(file,'r')
    content = f.read()
    content = eval(content)
    return content

def read_binary_file(file):
    f = open(file,'rb')
    content = f.read()
    return content

def read_text_file(file):
    f = open(file,'r')
    content = f.read()
    return content

def read_int_file(file):
    f = open(file,'r')
    content = f.read()
    contents = content.split()
    return (int(content) for content in contents)

def save_int_file(cipherText, fileName):
    with open(fileName, 'w') as f:
        bytes = ""
        for value in cipherText:
                bytes += (str(value) + "\n")
        f.write(bytes)

def save_binary_file(cipherText, fileName):
    with open(fileName, 'wb') as f:
        f.write(cipherText)
        
def save_text_file(cipherText, fileName):
    with open(fileName, 'w') as f:
        f.write(cipherText)
        
def get_file_name(filepath):
    # if it's path/to/file.txt
    # returns file
    name_without_extension = os.path.splitext(filepath)[0]

    return name_without_extension

def get_file_type(filepath):
    # if it's path/to/file.txt
    # returns .txt
    basename = os.path.basename(filepath)
    _, extension = os.path.splitext(basename)

    return extension

def get_base_file_name(filepath):
    # if it's path/to/file.txt
    # returns file.txt
    basename = os.path.basename(filepath)
    basename_without_extension = os.path.splitext(filepath)[0]
    return basename_without_extension
    
#print(read_key_file("ken1.pub"))


#x = min_binary_length(12)
#y = (max_binary_length(12))

#input = b'd\xc8\x2c'
#print(input)

#int_array,bit_data=((binary_data_to_int_array(input,x)))
#binary_data,bit_data2=(int_array_to_binary_data(int_array,y))

#print(int_array)
#print(binary_data)

