#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys
reload(sys) 
sys.setdefaultencoding('utf8') 

import xlwt
from datetime import datetime
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

BOX_SIZE = 40
PALLET_SIZE = 60

def exportExcel(frame):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
    num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    al = xlwt.Alignment()
    al.horz = xlwt.Alignment.HORZ_CENTER
    al.vert = xlwt.Alignment.VERT_CENTER
    
    styleTitleBkg = xlwt.easyxf('pattern: pattern solid, fore_colour gray_ega; font: color-index white,bold on; borders: left dashed, right dashed, top medium, bottom dashed;'); # 80% like
    styleTitleBkg.alignment = al
    #     row_style = xlwt.easyxf('pattern: pattern solid, back_colour #202020')
    tall_style = xlwt.easyxf('font:height 360;') # 36pt
    context_style = xlwt.easyxf('font: color-index black,bold on; borders: left dashed, right dashed, top dashed, bottom dashed;'); # 80% like
    context_style.alignment = al
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    #     ws.row(0).set_style(styleBlueBkg)
    ws.col(0).width = 256 * 25
    ws.col(1).width = 256 * 15
    ws.col(2).width = 256 * 15
    ws.col(3).width = 256 * 35
    ws.col(4).width = 256 * 35
    ws.col(5).width = 256 * 35
    ws.col(6).width = 256 * 35
    ws.col(7).width = 256 * 20
    ws.col(8).width = 256 * 35
    ws.col(9).width = 256 * 35
    
    ws.write(0, 0, "BATTERY_NO", styleTitleBkg)
    ws.write(0, 1, "COLOR", styleTitleBkg)
    ws.write(0, 2, "MAC", styleTitleBkg)
    ws.write(0, 3, "PRODUCT_BARCODE", styleTitleBkg)
    ws.write(0, 4, "PRODUCT_DATE", styleTitleBkg)
    ws.write(0, 5, "MID_CASE_BARCODE", styleTitleBkg)
    ws.write(0, 6, "PALLET_ID", styleTitleBkg)
    ws.write(0, 7, "WEIGHT", styleTitleBkg)
    ws.write(0, 8, "SOFTWARE_VERSION", styleTitleBkg)
    ws.write(0, 9, "VIRTUAL_ROOT", styleTitleBkg)


    count = getcount(frame)
    first_row = ws.row(0)
    first_row.set_style(tall_style)
    BOX_SIZE = int(frame.m_textCtrl_box_cont.GetValue());
    PALLET_SIZE = int(frame.m_textCtrl_ban_cont.GetValue());
    for i in range(1, count+2):
        first_row = ws.row(i)
        first_row.set_style(tall_style)
        ws.write(i, 0, "",context_style)
        ws.write(i, 1, frame.m_textCtrl_color.GetValue(),context_style)
        ws.write(i, 2, "",context_style)
        value = frame.m_textCtrl_bar_code_start.GetValue()
        try:
            first_title = value[:-5]
            code_value = int(value[-5:])+i-1
            formate_value = "%05d"%(code_value)
            bar_code = first_title+formate_value
            ws.write(i, 3,bar_code,context_style)
        except Exception,e:
            logger.debug(e)
            
        ws.write(i, 4, frame.m_textCtrl_date.GetValue(),context_style)
        mid_case = frame.m_textCtrl_bar_code_box.GetValue()
        try:
            first_title = mid_case[:-5]
            
            code_value = int(mid_case[-5:])+(i-1)/BOX_SIZE
            formate_value = "%05d"%(code_value)
            ws.write(i, 5,first_title+formate_value,context_style)
        except Exception,e:
            logger.debug(e)
            
        pallet = frame.m_textCtrl_bar_code_ban.GetValue()
        try:
            first_title = pallet[:-5]
            code_value = int(pallet[-5:])+(i-1)/BOX_SIZE/PALLET_SIZE
            formate_value = "%05d"%(code_value)
            ws.write(i, 6,first_title+formate_value,context_style)
        except Exception,e:
            logger.debug(e)
        ws.write(i, 7, frame.m_textCtrl_weight.GetValue(),context_style)
        ws.write(i, 8, "",context_style)
        ws.write(i, 9, bar_code,context_style)
    
    wb.save('export.xls')


def getcount(frame):
    logger.debug("get count");
    start = frame.m_textCtrl_bar_code_start.GetValue()
    end = frame.m_textCtrl_bar_code_end.GetValue()
    start_value=int(start[-5:])
    end_value=int(end[-5:])
    logger.debug(end_value-start_value)
    return end_value-start_value


class MyPanel4 ( wx.Panel ):
    
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.Point( 150,150 ), size = wx.Size( 1024,250 ), style = wx.TAB_TRAVERSAL )
        
        bSizer4 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        
        bSizer4.Add( bSizer6, 1, 0, 5 )
        
        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"颜色(手工录入)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        bSizer3.Add( self.m_staticText1, 0, wx.ALL, 8 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"重量(手工录入)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        bSizer3.Add( self.m_staticText4, 0, wx.ALL, 8 )
        
        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"生产日期(手工录入)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        bSizer3.Add( self.m_staticText5, 0, wx.ALL, 8 )
        
        
        bSizer7.Add( bSizer3, 1, 0, 5 )
        
        bSizer31 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_textCtrl_color = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer31.Add( self.m_textCtrl_color, 0, wx.ALL, 5 )
        
        self.m_textCtrl_weight = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer31.Add( self.m_textCtrl_weight, 0, wx.ALL, 5 )
        
        self.m_textCtrl_date = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer31.Add( self.m_textCtrl_date, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer31, 1, 0, 5 )
        
        bSizer322 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"产品条码", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        bSizer322.Add( self.m_staticText11, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 8 )
        
        self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, u"中箱条码", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )
        bSizer322.Add( self.m_staticText41, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 8 )
        
        self.m_staticText51 = wx.StaticText( self, wx.ID_ANY, u"卡板条码", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText51.Wrap( -1 )
        bSizer322.Add( self.m_staticText51, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 8 )
        
        
        bSizer7.Add( bSizer322, 1, 0, 5 )
        
        bSizer32 = wx.BoxSizer( wx.VERTICAL )
        
        bSizer311 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText33 = wx.StaticText( self, wx.ID_ANY, u"起", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText33.Wrap( -1 )
        bSizer311.Add( self.m_staticText33, 0, wx.ALL, 5 )
        
        self.m_textCtrl_bar_code_start = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl_bar_code_start.SetToolTipString( u"后5位为数字" )
        self.m_textCtrl_bar_code_start.SetMinSize( wx.Size( 200,-1 ) )
        
        bSizer311.Add( self.m_textCtrl_bar_code_start, 0, wx.ALL, 5 )
        
        self.m_staticText34 = wx.StaticText( self, wx.ID_ANY, u"止", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText34.Wrap( -1 )
        bSizer311.Add( self.m_staticText34, 0, wx.ALL, 5 )
        
        self.m_textCtrl_bar_code_end = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl_bar_code_end.SetToolTipString( u"后5位为数字" )
        self.m_textCtrl_bar_code_end.SetMinSize( wx.Size( 200,-1 ) )
        
        bSizer311.Add( self.m_textCtrl_bar_code_end, 0, wx.ALL, 5 )
        
        
        bSizer32.Add( bSizer311, 1, wx.SHAPED, 5 )
        
        bSizer3112 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_textCtrl_bar_code_box = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl_bar_code_box.SetToolTipString( u"后5位为数字" )
        self.m_textCtrl_bar_code_box.SetMinSize( wx.Size( 200,-1 ) )
        
        bSizer3112.Add( self.m_textCtrl_bar_code_box, 0, wx.ALL, 5 )
        
        
        bSizer3112.AddSpacer( ( 20, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText111 = wx.StaticText( self, wx.ID_ANY, u"每箱", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText111.Wrap( -1 )
        bSizer3112.Add( self.m_staticText111, 0, wx.ALL, 8 )
        
        self.m_textCtrl_box_cont = wx.TextCtrl( self, wx.ID_ANY, u"40", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.m_textCtrl_box_cont.SetToolTipString( u"数字" )
        
        bSizer3112.Add( self.m_textCtrl_box_cont, 0, wx.ALL, 5 )
        
        self.m_staticText341 = wx.StaticText( self, wx.ID_ANY, u"个", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText341.Wrap( -1 )
        bSizer3112.Add( self.m_staticText341, 0, wx.ALL, 8 )
        
        
        bSizer32.Add( bSizer3112, 1, wx.SHAPED, 5 )
        
        bSizer31121 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_textCtrl_bar_code_ban = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl_bar_code_ban.SetToolTipString( u"后5位为数字" )
        self.m_textCtrl_bar_code_ban.SetMinSize( wx.Size( 200,-1 ) )
        
        bSizer31121.Add( self.m_textCtrl_bar_code_ban, 0, wx.ALL, 5 )
        
        
        bSizer31121.AddSpacer( ( 20, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText3411 = wx.StaticText( self, wx.ID_ANY, u"每板", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3411.Wrap( -1 )
        bSizer31121.Add( self.m_staticText3411, 0, wx.ALL, 8 )
        
        self.m_textCtrl_ban_cont = wx.TextCtrl( self, wx.ID_ANY, u"60", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.m_textCtrl_ban_cont.SetToolTipString( u"数字" )
        
        bSizer31121.Add( self.m_textCtrl_ban_cont, 0, wx.ALL, 5 )
        
        self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"箱", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        bSizer31121.Add( self.m_staticText12, 0, wx.ALL, 8 )
        
        
        bSizer32.Add( bSizer31121, 1, wx.SHAPED, 5 )
        
        
        bSizer7.Add( bSizer32, 1, 0, 5 )
        
        bSizer321 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_button6 = wx.Button( self, wx.ID_ANY, u"手工查询", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button6.Enable( False )
        
        bSizer321.Add( self.m_button6, 0, wx.ALL, 5 )
        
        self.m_button7 = wx.Button( self, wx.ID_ANY, u"条码枪查询", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button7.Enable( False )
        
        bSizer321.Add( self.m_button7, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer321, 1, 0, 5 )
        
        bSizer3111 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_textCtrl211 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl211.Enable( False )
        
        bSizer3111.Add( self.m_textCtrl211, 0, wx.ALL, 5 )
        
        self.m_textCtrl311 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl311.Enable( False )
        
        bSizer3111.Add( self.m_textCtrl311, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer3111, 1, 0, 5 )
        
        
        bSizer8.Add( bSizer7, 1, 0, 5 )
        
        
        bSizer4.Add( bSizer8, 1, 0, 5 )
        
        bSizer55 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_button1 = wx.Button( self, wx.ID_ANY, u"生成数据(彩盒)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button1.Enable( False )
        
        bSizer55.Add( self.m_button1, 0, wx.ALIGN_CENTER, 5 )
        
        self.m_button3 = wx.Button( self, wx.ID_ANY, u"生成数据(裸机)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button3.Enable( False )
        
        bSizer55.Add( self.m_button3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_button4 = wx.Button( self, wx.ID_ANY, u"保存", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button4.Enable( False )
        
        bSizer55.Add( self.m_button4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"导出Excel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer55.Add( self.m_button2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        
        bSizer4.Add( bSizer55, 1, wx.ALIGN_CENTER, 5 )
        
        
        self.SetSizer( bSizer4 )
        self.Layout()
        
        # Connect Events
        self.m_button2.Bind( wx.EVT_BUTTON, self.m_button2OnButtonClick )
    
    def __del__( self ):
        # Disconnect Events
        self.m_button2.Unbind( wx.EVT_BUTTON, None )
    
    
    # Virtual event handlers, overide them in your derived class
    def m_button2OnButtonClick( self, event ):
        exportExcel(self)
    
    

class MyFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    CODE_TEXT = wx.NewId()
    def __init__(self, parent, title):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Excel文档导出程序", pos = wx.Point( 150,150 ), size = wx.Size( 1024,250 ), style = wx.DEFAULT_FRAME_STYLE )
        
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
        panel = MyPanel4(self)
        
      
        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        

    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        print "See ya later!"
        self.Close()

   
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
          


