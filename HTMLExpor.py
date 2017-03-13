#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx  

import logging 
import logging.handlers  
LOG_FILE = 'tst.log'  
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
formatter = logging.Formatter(fmt)   # 实例化formatter  
handler.setFormatter(formatter)      # 为handler添加formatter  
logger = logging.getLogger('tst')    # 获取名为tst的logger  
logger.addHandler(handler)           # 为logger添加handler  
logger.setLevel(logging.DEBUG)  


import os  
from bs4 import BeautifulSoup

def updateHTML(path):
	fp = open(path,'r+')  
	new = open(path[:len(path)-5]+"_new.html",'w+')  
	#logger.debug(path[:len(path)-5]+"_new.html")
	soup = BeautifulSoup(fp) 
	all_tb = soup.find_all('td',valign="middle")  
	root_table = soup.find('table',align="left")
	root_table['width']="267px"  
	root_table.tbody.clear()
	for tag in all_tb:
		new_tr = soup.new_tag("tr")
		root_table.tbody.append(new_tr)
		new_tr.append(tag)

	new.seek(0,os.SEEK_SET)  
	new.write(str(soup))
	new.close;
	fp.close()  



class MyFrame ( wx.Frame ):
	
	def __init__( self, parent , title):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"HTML生成程序", pos = wx.Point( -1,-1 ), size = wx.Size( 500,100 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_filePicker1 = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"选择保存的网页", u"*.html", wx.DefaultPosition, wx.Size( 300,-1 ), wx.FLP_DEFAULT_STYLE, wx.DefaultValidator, u"选择保存的网页" )
		bSizer2.Add( self.m_filePicker1, 0, wx.ALIGN_CENTER|wx.ALL, 10 )
		
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"生成新网页", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		# Connect Events
		self.m_button2.Bind( wx.EVT_BUTTON, self.m_button2OnButtonClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def m_button2OnButtonClick( self, event ):
		updateHTML(self.m_filePicker1.GetPath())


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, u"HTML生成程序")
        self.SetTopWindow(frame)
        print "Print statements go to this stdout window by default."

        frame.Show(True)
        return True

app = MyApp(redirect=True,filename="app.log")
app.MainLoop()
