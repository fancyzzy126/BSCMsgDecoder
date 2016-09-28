#!/usr/bin/python
#author: jzhao019

import random, crypt, getpass

def generatepasswd(cleartext):
    '''
    '''
    sample = ['./',
          'abcdefghijklmnopqrstuvwxyz',
          'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
          '0123456789']
    
    sample = [it for item in sample for it in item]
    salt = random.sample(sample, 2)
    salt = salt[0] + salt[1]
##    print salt
##    print cleartext
    cryptedpwd = crypt.crypt(cleartext, salt)
##    print cryptedpwd
    return cryptedpwd

def checkpasswd(cryptedpwd, cleartext):
    '''
    '''
    if len(cryptedpwd) <= 2:
        return false
    salt = cryptedpwd[:2]
    newcryptedpwd = crypt.crypt(cleartext, salt)
    return newcryptedpwd == cryptedpwd

def Test():
    print 'Test'
    generatepasswd('123456')
    print checkpasswd('edA3JuIDdVEMI', '123456')

if __name__ == '__main__':
    Test()
