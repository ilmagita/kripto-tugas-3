import sympy
import random
from . import functionList as fl

def public_key(p, q, e):
    """
    Returns public key.
    """

    return (e, p*q)

def private_key(p,q,e):
    """
    Returns private key.
    """

    totient = (p-1) * (q-1)
    d = sympy.mod_inverse(e, totient)
    return (d, p*q)

def generate_key(fileName):
    """
    Generates RSA public and private keys in .pub and .pri files.
    """

    e_list = [3, 5, 17, 65537]
    p = fl.random_prime_number()
    q = fl.random_prime_number()
    e = fl.random_prime_number()
    
    totient = (p-1) * (q-1)
    
    while not fl.are_relatife_prime(e,totient):
        p = fl.random_prime_number()
        q = fl.random_prime_number()
        e = random.choice(e_list)
        
    pubKey = public_key(p,q,e)
    privKey = private_key(p,q,e)
    fl.save_key_file(pubKey, f'{fileName}.pub')
    fl.save_key_file(privKey, f'{fileName}.pri')

def rsa_encrypt(plain,pubKey):
    """
    Encrypts a plaintext.
    """

    e, n = pubKey
    # plain = plain.upper().replace(" ",'')
    cipher = ''.join(hex(pow(ord(char),e,n)) for char in plain)
    return fl.utf8_to_base64(str(cipher))
    
def rsa_decrypt(cipher, privKey):
    """
    Decrypts a string.
    """

    d,n = privKey
    cipher = fl.base64_to_utf8(cipher).split('0x')
    cipher = cipher[1:]
    plain = [pow(int('0x'+c,16),d,n) for c in cipher]
    plaintext = "".join(chr(p) for p in plain)
    return plaintext

def rsa_enc_text_file(fileName, pubKey):
    """
    Encrypts base64 text files only using RSA algorithm.
    """

    filename_type = fl.get_file_type(fileName)
    filename_ori = fl.get_base_file_name(fileName)

    plain = fl.read_text_file(fileName)
    result = fl.rsa_encrypt(plain, pubKey)

    fl.save_text_file(result, f'{filename_ori}_rsa_encrypted{filename_type}')

    # return result

def rsa_dec_text_file(fileName, priKey):
    """
    Decrypts base64 text files only using RSA algorithm.
    """

    filename_type = fl.get_file_type(fileName)
    filename_ori = fl.get_base_file_name(fileName)
    plain = fl.read_text_file(fileName)
    result = fl.rsa_decrypt(plain,priKey)

    fl.save_text_file(result, f'{filename_ori}_rsa_decrypted{filename_type}')

    # return result

def rsa_enc_binary_file(fileName, pubKey):
    """
    Encrypts binary file that aren't .txt.
    """

    filename_type = fl.get_file_type(fileName)
    filename_ori = fl.get_base_file_name(fileName)
    
    plain = fl.read_binary_file(fileName)
    e,n = pubKey
    plain = fl.binary_data_to_int_array(plain)
    cipher = [pow(num,e,n) for num in plain]
    cipher = fl.int_array_to_binary_data(cipher)
    fl.save_binary_file(cipher, f'{filename_ori}_rsa_encrypted{filename_type}')

    # return cipher

def rsa_dec_binary_file(fileName, priKey):
    """
    Decrypts binary file.
    """

    filename_type = fl.get_file_type(fileName)
    filename_ori = fl.get_base_file_name(fileName)
    
    cipher = fl.read_binary_file(fileName)
    d,n = priKey
    cipher = fl.binary_data_to_int_array(cipher)
    plain = [pow(num,d,n) for num in cipher]
    plain = fl.int_array_to_binary_data(plain)
    fl.save_binary_file(plain, f'{filename_ori}_rsa_decrypted{filename_type}')

generate_key('ilma')
pubKey = fl.read_key_file('ilma.pub')
privKey = fl.read_key_file('ilma.pri')

msg = 'Apa kabar'
enc = rsa_encrypt(msg, pubKey)
print(enc)
dec = rsa_decrypt(enc, privKey)
print(dec)

# rsa_enc_binary_file('../inputs/ESP32.png', pubKey)
# rsa_dec_binary_file('../inputs/ESP32_rsa_encrypted.png', privKey)

#rsa_enc_text_file("tes.txt",pubKey)
#rsa_dec_text_file("tes_rsa_encrypted.txt",privKey)

"""
cipher = rsa_encrypt("HELLO WORLD",pubKey)
plain = rsa_decrypt(cipher,privKey)
print(cipher)
print(plain)
"""


    