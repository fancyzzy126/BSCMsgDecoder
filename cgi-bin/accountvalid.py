#!/usr/bin/python
#module:
#author: jzhao019

import os, pwdGenerator, errorpage, accountrecord, normalpage

class accountvalid(object):
    def __init__(self):
        self.__filename = '.rttppasswd'
        self.__username = 'anony'
        self.__passwd = "null"
    def fileexist(self):
        return os.path.isfile(self.__filename.strip())

    def checkuser(self, user):
##        print 'checkuser'
        if self.fileexist():
            try:
                pwdfile = file(self.__filename)
                contents = [it.strip().split(':')[0].strip()
                            for it in pwdfile.readlines() if len(it.strip()) > 0 and
                            it.startswith('#') == False]
                pwdfile.close()
                return [user.strip() in contents, "succ"]
            except Exception, ex:
                return [False, "checkuser: " + str(ex) + "\n"]
        else:
            return [False, "checkuser: internal\n"]

    def checkpasswd(self, user, passwd):
##        print 'checkpasswd'
        cu = self.checkuser(user)
        if cu[0]:
            try:
                pwdfile = file(self.__filename)
                contents = [it.strip().split(':')
                            for it in pwdfile.readlines() if len(it.strip()) > 0 and
                            it.startswith('#') == False]
                for it in contents:
                    if len(it) == 2:
                        if it[0].strip() == user.strip():
                            if pwdGenerator.checkpasswd(it[1].strip(), passwd):
                                return [True, 'succ']
                            else:
                                return [False, 'checkpasswd internal\n']
                    else:
                        break
                return [False, "checkpasswd: user not reged!\n"]
            except Exception, ex:
                return [False, str(ex) + "checkpasswd\n"]
        else:
            return [False, cu[1] + "checkpasswd\n"]

    def addaccount(self, user, passwd):
        cu = self.checkuser(user)
        if cu[0] == True:
            return (False, "Username already existed!")
        try:
            pwdfile = file(self.__filename, 'aw')
            cryptedpasswd = pwdGenerator.generatepasswd(passwd)
            pwdfile.write(user.strip() + ":" + cryptedpasswd + "\n")
            pwdfile.close()
            return (True,'succ')
        except Exception, ex:
            return (False, str(ex))
        
    def do_error(self, param1, param2):
        errorpage.showerror(param1, param2)

    def do_rediret(self, targ):
        normalpage.sendRedirect(targ)
        return

    def do_login(self, param):
        if len(param) == 2:
            ckp = self.checkpasswd(param[0], param[1])
            if ckp[0]:
                self.do_rediret('temp/mainframe.html')
                return
        self.do_error("Logon Error", "Invalid username or password!")

    def do_reg(self, param):
        if len(param) == 6:
            result = self.addaccount(param[0], param[5])
            if result[0]:
                ar = accountrecord.recaccount(param[0], param[1],
                                          param[2], param[3], param[4])
                if ar[0]:
                    self.do_rediret("temp/mainframe.html")
                else:
                    self.do_error("Registration Error2", ar[1])
            else:
                self.do_error("Registration Error", result[1])
        else:
            self.do_error("Registration Error1", "Parameters are not sufficient!")

def process(action, param):
    va = accountvalid()
    if hasattr(va, "do_%s" % action):
        actual_func = getattr(va, "do_%s" % action)
        actual_func(param)
    else:
        errorpage.showerror("Unknow Action: " + action, "Account: Invalid Access!")
    

def Test():
    print 'Test'
    func = process('login',['jzhao019','123456'])
    #func = process('reg', ['name', 'realname', 'you@mail.com', '8504', 'team', 'passwd'])


if __name__ == '__main__':
    Test()
