#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Oct 18 2018
@author:zhang88a
"""
import wx
import winsound
import GomokuFunc

ARR = [[0 for i in range(15)] for j in range(15)]

class MyFrame(wx.Frame):
    PANEL_ORIG_POINT = wx.Point(15, 15)
    is_inited = False
    is_continue = False
    d_sum = 900 #棋盘宽度
    d_ele = 60 #单元格宽度
    d_edge = (d_sum-14*d_ele)/2 #棋盘边缘宽度
    next_color = 1

    def __init__(self,title):
        super(MyFrame,self).__init__(None, title=title, size=(1300,1000))
        # super() 函数是用于调用父类(超类)的一个方法。
        # super 是用来解决多重继承问题的，直接用类名调用父类方法在使用单继承的时候没问题，
        # 但是如果使用多继承，会涉及到查找顺序（MRO）、重复调用（钻石继承）等种种问题。     
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_UP, self.on_lclick)
        self.Bind(wx.EVT_SIZE, self.on_flesh)
        self.Bind(wx.EVT_MOVE, self.on_flesh)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
        self.Bind(wx.EVT_MOTION, self.on_move)

        # self.Bind(wx.EVT_KEY_DOWN,self.on_key)
        # EVT_PAINT事件 在初始化界面的时候是会被调用
        # EVT_KEY_DOWN 按键事件
        # 使用Bind() 方法，将1个对象Object和1个时间event建立绑定关系。
        self.Centre()
        self.SetFocus()
        self.Show()
        '''
        self.panel1 = wx.Panel(id = wx.NewId(), name='panel1', parent=self,pos=wx.Point(0, 0), size=wx.Size(412, 231),style=wx.TAB_TRAVERSAL)
        self.panel1.Show(False)
        '''
        
    def init_widgets(self):
        # 初始化部件
        self.button1 = wx.Button(self, -1, u"先手执黑", pos=(1050, 60), style = 2) 
        self.button2 = wx.Button(self, -1, u"后手执白", pos=(1050, 100), style = 2) 
        self.button3 = wx.Button(self, -1, u"热座对战", pos=(1050, 140), style = 2)
        self.button4 = wx.Button(self, -1, u"设置", pos=(1050, 180), style = 2)
        self.button3.Bind(wx.EVT_BUTTON, self.on_button_3)
        # self.button4.Bind(wx.EVT_BUTTON, self.on_button_4)

    def on_button_3(self, event):
        print('button3')
        self.reset_game()
        global HAND_AI
        HAND_AI = 3

    '''
    def on_button_4(self, event):
        print('button4')
        self.panel1.Show(True)
    '''

    def OnErase(self, event):
        # Do nothing, reduces flicker by removing
        # unneeded background erasures and redraws
        pass

    def on_flesh(self,event):
        self.draw_screen()
        self.draw_all_chess(ARR)

    def on_lclick(self,event):
        if HAND_AI == None:
            print(HAND_AI)
            wx.MessageBox(u"请先选择游戏模式", u"emmm...", wx.OK)
            winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC)
            return
        pos = event.GetPosition()
        print(pos)
        if pos.x<=self.PANEL_ORIG_POINT.x+self.d_sum and pos.y<=self.PANEL_ORIG_POINT.y+self.d_sum and pos.x>=self.PANEL_ORIG_POINT.x and pos.y>= self.PANEL_ORIG_POINT.y:
            pos_x = (pos.x-self.PANEL_ORIG_POINT.x-self.d_edge)//self.d_ele
            if (pos.x-self.PANEL_ORIG_POINT.x-self.d_edge)%self.d_ele > self.d_ele/2 :
                pos_x = pos_x + 1
            pos_y = (pos.y-self.PANEL_ORIG_POINT.y-self.d_edge)//self.d_ele
            if (pos.y-self.PANEL_ORIG_POINT.y-self.d_edge)%self.d_ele > self.d_ele/2 :
                pos_y = pos_y + 1
            print(pos_x,pos_y)
            if ARR[int(pos_x)][int(pos_y)] == 0:
                ARR[int(pos_x)][int(pos_y)] = self.next_color
                #self.draw_screen()
                #self.draw_chessman(pos_x,pos_y,self.next_color)
                self.draw_all_chess(ARR,[pos_x,pos_y])
                self.next_color = -self.next_color
                #print(ARR)
            else:
                winsound.PlaySound("SystemAsterisk", winsound.SND_ASYNC) # winsound.SND_ASYNC 程序可在声音没有播完时继续执行后面的操作。
            self.is_game_over(int(pos_x),int(pos_y))
            
        else:
            self.draw_background()

    def is_game_over(self,pos_x,pos_y):
        if GomokuFunc.Referee(ARR,'first_hand',[int(pos_x),int(pos_y)]) == "first_hand_win":
            # 胜负判断
            if HAND_AI == 1:
                #AI win
                wx.MessageBox(u"游戏结束，AI执黑胜利！", u"Lose", wx.OK)
            else:
                #先手胜利
                wx.MessageBox(u"游戏结束，玩家执黑胜利！", u"Win", wx.OK)
            self.reset_game()
        elif GomokuFunc.Referee(ARR,'first_hand',[int(pos_x),int(pos_y)]) == "back_hand_win":
            if HAND_AI == 0:
                #AI win
                wx.MessageBox(u"游戏结束，AI执白胜利！", u"Lose", wx.OK)
            else:
                #后手胜利
                wx.MessageBox(u"游戏结束，玩家执白胜利！", u"Win", wx.OK)
            self.reset_game()
        else:# 暂时没有考虑棋盘下满
            return

    def reset_game(self):
        global ARR 
        ARR = [[0 for i in range(15)] for j in range(15)]
        global HAND_AI
        HAND_AI = None
        self.next_color = 1
        self.draw_background()

    def on_paint(self, event):
        if not self.is_inited:
            self.reset_game()
            self.is_inited = True


    def on_move(self, event):
        pos = event.GetPosition()
        if pos.x<=self.PANEL_ORIG_POINT.x+self.d_sum and pos.y<=self.PANEL_ORIG_POINT.y+self.d_sum and pos.x>=self.PANEL_ORIG_POINT.x and pos.y>= self.PANEL_ORIG_POINT.y:
            self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        else:
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))


    def draw_background(self):
        # 绘制底色 棋盘 部件 棋子
        self.draw_screen()
        #self.draw_titles()
        self.init_widgets()
        self.draw_all_chess(ARR)

    def draw_screen(self):
        # 绘制底色和棋盘
        #dc = wx.BufferedPaintDC(self)
        dc = wx.ClientDC(self)
        dc.SetBackground(wx.Brush("#FAF8EF"))
        dc.Clear()
        self.draw_titles()
        
    
    def draw_titles(self):
        # 绘制棋盘
        dc = wx.ClientDC(self)
        dc.SetBrush(wx.Brush(wx.Colour(249,214,91)))
        dc.SetPen(wx.Pen("#FAF8EF", 1, wx.TRANSPARENT))
        d_sum = self.d_sum #棋盘宽度
        dc.DrawRectangle(self.PANEL_ORIG_POINT.x,self.PANEL_ORIG_POINT.y,d_sum,d_sum)
        d_ele = self.d_ele #单元格宽度
        d_edge = self.d_edge #棋盘边缘宽度
        dc.SetPen(wx.Pen(wx.Colour(10,10,10),2))
        for m in range(15):
            dc.DrawLine(self.PANEL_ORIG_POINT.x+d_edge,self.PANEL_ORIG_POINT.y+d_edge+m*d_ele,self.PANEL_ORIG_POINT.x+d_sum-d_edge,self.PANEL_ORIG_POINT.y+d_edge+m*d_ele) 
            dc.DrawLine(self.PANEL_ORIG_POINT.x+d_edge+m*d_ele,self.PANEL_ORIG_POINT.y+d_edge,self.PANEL_ORIG_POINT.x+d_edge+m*d_ele,self.PANEL_ORIG_POINT.y+d_sum-d_edge) 
        dc.SetBrush(wx.Brush(wx.Colour(10,10,10)))
        dc.DrawCircle(self.PANEL_ORIG_POINT.x+d_edge+7*d_ele,self.PANEL_ORIG_POINT.y+d_edge+7*d_ele,4)
        dc.DrawCircle(self.PANEL_ORIG_POINT.x+d_edge+3*d_ele,self.PANEL_ORIG_POINT.y+d_edge+11*d_ele,4)
        dc.DrawCircle(self.PANEL_ORIG_POINT.x+d_edge+3*d_ele,self.PANEL_ORIG_POINT.y+d_edge+3*d_ele,4)
        dc.DrawCircle(self.PANEL_ORIG_POINT.x+d_edge+11*d_ele,self.PANEL_ORIG_POINT.y+d_edge+3*d_ele,4)
        dc.DrawCircle(self.PANEL_ORIG_POINT.x+d_edge+11*d_ele,self.PANEL_ORIG_POINT.y+d_edge+11*d_ele,4)

    def draw_chessman(self,x,y,color):
        """
        :type x: int 棋子横坐标
        :typr y: int 棋子纵坐标
        :type color: int 1白 -1黑 其他无 
        :rtype: None/Boolean
        """
        dc = wx.ClientDC(self)
        if color == -1:
            dc.DrawBitmap(wx.Bitmap("white.png"),self.PANEL_ORIG_POINT.x+self.d_edge+x*self.d_ele-26,self.PANEL_ORIG_POINT.y+self.d_edge+y*self.d_ele-26,True)
        elif color == 1:
            dc.DrawBitmap(wx.Bitmap("black.png"),self.PANEL_ORIG_POINT.x+self.d_edge+x*self.d_ele-26,self.PANEL_ORIG_POINT.y+self.d_edge+y*self.d_ele-26,True)
        else:
            return False

    def draw_flag(self,x,y):
        """
        :type x: int 标志横坐标
        :typr y: int 标志纵坐标 
        :rtype: None
        """
        dc = wx.ClientDC(self)
        dc.SetPen(wx.Pen(wx.Colour(255,0,0)))
        dc.SetBrush(wx.Brush(wx.Colour(255,0,0)))
        dc.DrawCircle(self.PANEL_ORIG_POINT.x+self.d_edge+x*self.d_ele,self.PANEL_ORIG_POINT.y+self.d_edge+y*self.d_ele,4)
    
    def draw_all_chess(self,arr,pos_flag = None):
        """
        :type arr: list[int] 棋盘状态
        :typr pos_flag: list[int] 标志位置
        :rtype: None
        """
        for index1,m in enumerate(arr):
            for index2,n in enumerate(m):
                self.draw_chessman(index1,index2,n)
        if pos_flag != None:
            self.draw_flag(pos_flag[0],pos_flag[1])

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame('五子棋')
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()