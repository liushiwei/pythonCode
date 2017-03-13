#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
reload(sys) 
sys.setdefaultencoding('utf8') 

def fastExpMod(b, e, m):
    """
    e = e0*(2^0) + e1*(2^1) + e2*(2^2) + ... + en * (2^n)

    b^e = b^(e0*(2^0) + e1*(2^1) + e2*(2^2) + ... + en * (2^n))
        = b^(e0*(2^0)) * b^(e1*(2^1)) * b^(e2*(2^2)) * ... * b^(en*(2^n)) 

    b^e mod m = ((b^(e0*(2^0)) mod m) * (b^(e1*(2^1)) mod m) * (b^(e2*(2^2)) mod m) * ... * (b^(en*(2^n)) mod m) mod m
    """
    result = 1
    while e != 0:
        if (e&1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
            #print "result = ",result
        e >>= 1
        # b, b^2, b^4, b^8, ... , b^(2^n)
        b = (b*b) % m
        #print "b = ",b*b
    return result

def primeTest(n):
    q = n - 1
    k = 0
    #Find k, q, satisfied 2^k * q = n - 1
    while q % 2 == 0:
        k += 1;
        q /= 2
    a = random.randint(2, n-2);
    #If a^q mod n= 1, n maybe is a prime number
    if fastExpMod(a, q, n) == 1:
        return "inconclusive"
    #If there exists j satisfy a ^ ((2 ^ j) * q) mod n == n-1, n maybe is a prime number
    for j in range(0, k):
        if fastExpMod(a, (2**j)*q, n) == n - 1:
            return "inconclusive"
    #a is not a prime number
    return "composite"

def findPrime(halfkeyLength):
    while True:
        #Select a random number n 
        n = random.randint(0, 1<<halfkeyLength)
        if n % 2 != 0:
            found = True
            #If n satisfy primeTest 10 times, then n should be a prime number
            for i in range(0, 10):
                if primeTest(n) == "composite":
                    found = False
                    break
            if found:
                return n

def extendedGCD(a, b):
    #a*xi + b*yi = ri
    if b == 0:
        return (1, 0, a)
    #a*x1 + b*y1 = a
    x1 = 1
    y1 = 0
    #a*x2 + b*y2 = b
    x2 = 0
    y2 = 1
    while b != 0:
        q = a / b
        #ri = r(i-2) % r(i-1)
        r = a % b
        a = b
        b = r
        #xi = x(i-2) - q*x(i-1)
        x = x1 - q*x2
        x1 = x2
        x2 = x
        #yi = y(i-2) - q*y(i-1)
        y = y1 - q*y2
        y1 = y2
        y2 = y
    return(x1, y1, a)

def selectE(fn, halfkeyLength):
    while True:
        #e and fn are relatively prime
        e = random.randint(0, 1<<halfkeyLength)
        (x, y, r) = extendedGCD(e, fn)
        if r == 1:
            return e

def computeD(fn, e):
    (x, y, r) = extendedGCD(fn, e)
    #y maybe < 0, so convert it 
    if y < 0:
        return fn + y
    return y

def keyGeneration(keyLength):
    #generate public key and private key
    p = findPrime(keyLength/2)
    q = findPrime(keyLength/2)
    n = p * q
    fn = (p-1) * (q-1)
    e = selectE(fn, keyLength/2)
    d = computeD(fn, e)
    return (n, e, d)

def encryption(M, e, n):
    #RSA C = M^e mod n
    return fastExpMod(M, e, n)

def decryption(C, d, n):
    #RSA M = C^d mod n
    return fastExpMod(C, d, n)



#Unit Testing
(n, e, d) = keyGeneration(50)
n = 39868286845823
e = 2154277
d = 18937541565613
#AES keyLength = 256
X = 3705491966
# C = encryption(X, e, n)
# M = decryption(C, d, n)
# print "PlainText n:", n
# print "PlainText e:", e
# print "PlainText d:", d
# print "PlainText:", X
# print "Encryption of plainText:", C
# print "Decryption of cipherText:", M
# print "The algorithm is correct:", X == M


import wx


class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    CODE_TEXT = wx.NewId()
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(150, 150), size=(300, 200))

        # Create the menubar
        menuBar = wx.MenuBar()

        # and a menu 
        menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        #self.SetMenuBar(menuBar)

        self.CreateStatusBar()
        

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)
        
        code_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # and a few controls
        text = wx.StaticText(panel, -1, u"机器码：")
        #text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        self.code_textCtrl = wx.TextCtrl(panel, -1,size =(200, 25) )
        code_sizer.Add(text,0,wx.ALIGN_CENTER);
        code_sizer.Add(self.code_textCtrl,1,wx.ALIGN_CENTER);
        
        sn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # and a few controls
        sn_text = wx.StaticText(panel, -1, u"注册码：")
        #text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        sn_text.SetSize(text.GetBestSize())
        self.sn_textCtrl = wx.TextCtrl(panel, -1,size =(200, 25) )
        sn_sizer.Add(sn_text,0,wx.ALIGN_CENTER);
        sn_sizer.Add(self.sn_textCtrl,1,wx.ALIGN_CENTER);
        
        bt_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(panel, -1, u"关闭")
        funbtn = wx.Button(panel, -1, u"生成注册码")
        bt_sizer.Add(funbtn,0,wx.ALIGN_CENTER);
        bt_sizer.Add(btn,0,wx.ALIGN_CENTER);
        
        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnTimeToClose, btn)
        self.Bind(wx.EVT_BUTTON, self.OnFunButton, funbtn)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(code_sizer, 0, wx.ALL, 10)
        sizer.Add(sn_sizer, 0, wx.ALL, 10)
        sizer.Add(bt_sizer, 0, wx.ALL, 10)
        panel.SetSizer(sizer)
        panel.Layout()

        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        print "See ya later!"
        self.Close()

    def OnFunButton(self, evt):
        """Event handler for the button click."""
        print "Having fun yet?"
        code = self.code_textCtrl.GetValue();
        int_value = long(code)
        C =encryption(int_value, e, n)
        str_value = str(C)
        self.sn_textCtrl.WriteText(str_value)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, u"注册码生成器 V1.0")
        self.SetTopWindow(frame)

        print "Print statements go to this stdout window by default."

        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp(redirect=True,filename="app.log")
    app.MainLoop()
          


