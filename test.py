from GamePractice import Ui_Form#(注意這邊名稱要看原來建立class是甚麼類別，例如有Dialogue,or Form)
from PyQt5.QtWidgets import *
#從Anaconda的PyQT5的QtWidgets資料夾import all(*)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

app = QApplication(sys.argv)#創建應用程式的主對象，負責控制應用的啟動和結束。
#Pyuic5電腦會去找python.exe接著把-x,檔名,-o,檔名丟給Pyuic5等四個參數
widget = QWidget()#創建一個空白的主窗口（視窗）
ui = Ui_Form()
ui.setupUi(widget)
# 這段代碼的作用是在按鈕被點擊時，透過 lambda 匿名函數來調用 Buttons("B1")，並將 "B1" 作為參數傳遞給 Buttons 函數。
# 這樣可以讓 Buttons 函數知道是哪一個按鈕被點擊了（例如 "B1" 對應按鈕 1）。
ui.pushButton_1.clicked.connect(lambda:Buttons("pushButton_1"))
ui.pushButton_2.clicked.connect(lambda:Buttons("pushButton_2"))
ui.pushButton_3.clicked.connect(lambda:Buttons("pushButton_3"))
ui.pushButton_4.clicked.connect(lambda:Buttons("pushButton_4"))
ui.pushButton_5.clicked.connect(lambda:Buttons("pushButton_5"))
ui.pushButton_6.clicked.connect(lambda:Buttons("pushButton_6"))
ui.pushButton_7.clicked.connect(lambda:Buttons("pushButton_7"))
ui.pushButton_8.clicked.connect(lambda:Buttons("pushButton_8"))
ui.pushButton_9.clicked.connect(lambda:Buttons("pushButton_9"))
ui.ResetButton.clicked.connect(lambda:ReStartGame("ResetButton"))


turn=0#玩家開始
playerWin=""
computerWin=""

def Buttons(Button_name):
     global turn
     button = getattr(ui,Button_name)
     if turn==0 and button.text()=="":
        button.setText("O")
        Check_Win()
        if not Check_Win():
            Computer_Move()

def Check_Win():
    global playerWin
    global computerWin
    playerWin = "OOO"
    computerWin="XXX"
    win_combination=[
        (ui.pushButton_1, ui.pushButton_2, ui.pushButton_3),
        (ui.pushButton_4, ui.pushButton_5, ui.pushButton_6),
        (ui.pushButton_7, ui.pushButton_8, ui.pushButton_9),
        (ui.pushButton_1, ui.pushButton_4, ui.pushButton_7),
        (ui.pushButton_2, ui.pushButton_5, ui.pushButton_8),
        (ui.pushButton_3, ui.pushButton_6, ui.pushButton_9),
        (ui.pushButton_1, ui.pushButton_5, ui.pushButton_9),
        (ui.pushButton_3, ui.pushButton_5, ui.pushButton_7)
        ]
    for combination in win_combination:
        result = combination[0].text()+combination[1].text()+combination[2].text()
        if result ==playerWin:
            ui.label.setText("Player is the Winner")
            return True
        elif result ==computerWin:
            ui.label.setText("Computer is the Winner")
            return True
def Computer_Move():
    #取得目前棋盤的狀況:
    board=[ui.pushButton_1.text(), ui.pushButton_2.text(), ui.pushButton_3.text(),
             ui.pushButton_4.text(), ui.pushButton_5.text(), ui.pushButton_6.text(),
             ui.pushButton_7.text(), ui.pushButton_8.text(), ui.pushButton_9.text()]
    move=None
    best_score = -float('inf')#初始值為負無窮大，代表還沒找到任何有利的走法。
    for i in range(0,9):
        if board[i]=="":
            board[i]="X"
            score = minMax(board,False)
            board[i]=""
            if score > best_score:
                move=i
    if move is not None:
       button = getattr(ui,f"pushButton_{move+1}")
       button.setText("X")
       Check_Win()
       global turn
       turn = 0  # 讓玩家接著下棋
       
def minMax(board,isMinMax):
    winner = Check_Win(board)
    if winner == 'X':  # 電腦贏電腦設定為得分最大的棋局
        return 1
    elif winner == 'O':  # 玩家贏玩家讓電腦得分最小的棋局
        return -1
    elif "" not in board:  # 平局
        return 0
    if isMinMax:
        best_score = -float('inf')
        for i in range(0,9):
            if board[i]=="":
                board[i]="X"
                score = minMax(board,False)
                board[i]=""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(0,9):
            if board[i]=="":
                board[i]="O"
                score = minMax(board,True)
                board[i]=""
                best_score = min(score,best_score)
        return best_score
    

def Check_Win(board):
    win_combinations = [
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},  # 橫向
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},  # 縱向
        {0, 4, 8}, {2, 4, 6}              # 斜向
    ]
    for combo in win_combinations:
        if board[list(combo)[0]] ==board[list(combo)[1]]==board[list(combo)[2]]!="":
            return board[list(combo)[0]]
    return None
                