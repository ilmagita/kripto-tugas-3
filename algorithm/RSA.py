import sympy
import random
from . functionList import *

def public_key(p, q, e):
    return (e, p*q)

def private_key(p,q,e):
    totient = (p-1) * (q-1)
    d = sympy.mod_inverse(e, totient)
    return (d, p*q)

def generate_key(fileName):
    p = random_prime_number()
    q = random_prime_number()
    e = random_prime_number()
    
    totient = (p-1) * (q-1)
    
    while not are_relatife_prime(e,totient):
        p = random_prime_number()
        q = random_prime_number()
        e = random_prime_number()
        
    pubKey = public_key(p,q,e)
    privKey = private_key(p,q,e)

    filepath = os.path.join(key_dir, fileName)

    save_key_file(pubKey,f'{filepath}.pub')
    save_key_file(privKey,f'{filepath}.pri')

def rsa_encrypt(plain,pubKey):
    e,n = pubKey
    cipher = ''.join(hex(pow(ord(char),e,n)) for char in plain)
    return utf8_to_base64(str(cipher))
    
def rsa_decrypt(cipher,privKey):
    d,n = privKey
    cipher = base64_to_utf8(cipher).split('0x')
    cipher = cipher[1:]
    plain = [pow(int('0x'+c,16),d,n) for c in cipher]
    plaintext = "".join(chr(p) for p in plain)
    return plaintext

def rsa_enc_text_file(fileName,pubKey):
    filename_type = get_file_type(fileName)
    filename_ori = get_base_file_name(fileName)
    plain = read_text_file(fileName)
    result = rsa_encrypt(plain,pubKey)
    save_text_file(result, f'{filename_ori}_rsa_encrypted{filename_type}')
    return result

def rsa_dec_text_file(fileName,priKey):
    "hanya menerima base64 text file "
    filename_type = get_file_type(fileName)
    filename_ori = get_base_file_name(fileName)
    plain = read_text_file(fileName)
    result = rsa_decrypt(plain,priKey)
    save_text_file(result, f'{filename_ori}_rsa_decrypted{filename_type}')
    return result


def rsa_enc_binary_file(fileName,pubKey):
    filename_type = get_file_type(fileName)
    filename_ori = get_base_file_name(fileName)
    
    plain = read_binary_file(fileName)
    e,n = pubKey
    plain = binary_data_to_int_array(plain)
    print(plain)
    cipher = [(pow(num,e,n)) for num in plain]
    #cipher = int_array_to_binary_data(cipher)
    save_int_file(cipher, f'{filename_ori}_rsa_encrypted{filename_type}')
    return cipher

def rsa_dec_binary_file(fileName,priKey):
    filename_type = get_file_type(fileName)
    filename_ori = get_base_file_name(fileName)
    
    cipher = read_int_file(fileName)
    d,n = priKey
    plain = [(pow(num,d,n)) for num in cipher]
    plain = int_array_to_binary_data(plain)
    save_binary_file(plain, f'{filename_ori}_rsa_decrypted{filename_type}')
    return plain

#print(type(rsa_enc_binary_file("ESP32.png",pubKey)))
#print(rsa_enc_binary_file("ESP32.png",pubKey))
#print(rsa_dec_binary_file("ESP32_rsa_encrypted.png",privKey))
#rsa_enc_text_file("tes.txt",pubKey)
#rsa_dec_text_file("tes_rsa_encrypted.txt",privKey)


# get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# go back up one folder
parent_dir = os.path.dirname(current_dir)
key_dir = os.path.join(parent_dir, 'key')

privKey_path = os.path.join(key_dir, 'key.pri')
pubKey_path = os.path.join(key_dir, 'key.pub')
pubKey = read_key_file(privKey_path)
privKey = read_key_file(pubKey_path)


## TEST
# file_path = os.path.join(parent_dir, 'tes.txt')
# rsa_enc_text_file(file_path, pubKey)
# dec_file_path = os.path.join(parent_dir, 'tes_rsa_encrypted.txt')
# rsa_dec_text_file(dec_file_path, privKey)


    