import base64
import sympy
import random
import os
from math import gcd

def utf8_to_base64(utf8_text):
    return base64.b64encode(utf8_text.encode("utf-8")).decode("utf-8")

def base64_to_utf8(base64_text):
    utf8_text = base64.b64decode(base64_text).decode("utf-8")
    return utf8_text

def binary_data_to_int_array(binary_data):
    array_of_integers = [int(byte) for byte in binary_data]
    return array_of_integers

def int_array_to_binary_data(array_of_integers):
    binary_data = bytearray()
    for num in array_of_integers:
        binary_data.append(num % 256)
    return binary_data


def are_relatife_prime(a,b):
    gcd_val = gcd(a,b)
    return gcd_val == 1

def random_prime_number():
    number = random.randint(1,9999999999)
    while not sympy.isprime(number):
        number = random.randint(1,9999999999)
    return number

def save_key_file(key,fileName):
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

def save_binary_file(cipherText, fileName):
    with open(fileName, 'wb') as f:
        f.write(cipherText)
        
def save_text_file(cipherText, fileName):
    with open(fileName, 'w') as f:
        f.write(cipherText)
        
def get_file_name(filepath):
    name_without_extension = os.path.splitext(filepath)[0]
    return name_without_extension

def get_file_type(filepath):
    basename = os.path.basename(filepath)
    _, extension = os.path.splitext(basename)

    return extension

def get_base_file_name(filepath):
    basename = os.path.basename(filepath)
    basename_without_extension = os.path.splitext(filepath)[0]
    return basename_without_extension
    
#print(read_key_file("ken1.pub"))

#print(hex_to_binary_data("0x1a87b4168ec4c07a0x3620932d0cfb23130x1b9fa786c834cf140xaf7d7d93fc19eb80x154d7b5413da979f"))

