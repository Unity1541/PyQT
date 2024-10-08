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
# button = getattr(ui, Button_name) 是 Python 中的一個常用語法，用來動態獲取對象的屬性。在這裡，我們使用它來根據按鈕的名稱動態獲取對應的按鈕對象。
# 語法分解：
# getattr() 是 Python 的內置函數，它接受兩個參數：
# 對象 (ui)：我們希望從中獲取屬性的對象。
# 屬性名稱 (Button_name)：這是我們要獲取的屬性的名稱，這個屬性名稱需要是字符串格式。

turn=0#玩家開始
playerWin=""
computerWin=""

def Buttons(Button_name):
    global turn  
# global turn：這行告訴 Python，我們在 Buttons 函數內使用的是全局範圍的 turn 變量，
# 而不是局部變量。這樣每次調用函數時都能更新全局的 turn 變量。
    button = getattr(ui, Button_name)#注意這邊是button.text()方法，不是用button.text屬性
    if turn == 0 and button.text()=="":
        button.setText("O")  # 設置按鈕文本為 "X"
        turn = 1  # 更新 turn 的值，切換到 "O"
        CheckWin()
        if not CheckWin():
            computer_move()
    # elif turn == 1 and button.text()=="":
    #     button.setText("X")  # 設置按鈕文本為 "O"
    #     turn = 0  # 更新 turn 的值，切換到 "X"
    #     CheckWin()
    
def ReStartGame(Button_name):
    global turn
    turn=0
    for i in range(1,10):
        button = getattr(ui,f"pushButton_{i}")
        button.setText("")
        ui.label.setText("")

def CheckWin():
    global playerWin
    global computerWin
    playerWin = "OOO"
    computerWin="XXX"
    #更改方式比較簡短list裡面放tuple
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
def computer_move():
    # 取得當前的棋盤狀態取得是O或X文字
    board = [ui.pushButton_1.text(), ui.pushButton_2.text(), ui.pushButton_3.text(),
             ui.pushButton_4.text(), ui.pushButton_5.text(), ui.pushButton_6.text(),
             ui.pushButton_7.text(), ui.pushButton_8.text(), ui.pushButton_9.text()]
    
    best_score = -float('inf')#初始值為負無窮大，代表還沒找到任何有利的走法。
    move = None
    
    # 模擬電腦（"X"）的所有可能走法
    for i in range(9):
        if board[i] == "":  # 空的格子
            board[i] = "X"  # 模擬電腦下棋
            score = minimax(board, False)  # 玩家下一步
            board[i] = ""  # 回復
            if score > best_score:
                best_score = score
                move = i
    
    # 找到最佳移動後，更新棋盤
    if move is not None:
        button = getattr(ui, f"pushButton_{move + 1}")  # +1 因為索引從 1 開始
        button.setText("X")
        CheckWin()
        global turn
        turn = 0  # 讓玩家接著下棋

def minimax(board, is_maximizing):
    # 終止條件
    winner = check_winner(board)
    if winner == 'X':  # 電腦贏電腦設定為得分最大的棋局
        return 1
    elif winner == 'O':  # 玩家贏玩家讓電腦得分最小的棋局
        return -1
    elif "" not in board:  # 平局
        return 0

    if is_maximizing:  # 電腦的回合
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"  # 電腦的棋子
                score = minimax(board, False)
                board[i] = ""  # 回復
                best_score = max(score, best_score)
        return best_score
    else:  # 玩家回合
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"  # 玩家棋子
                score = minimax(board, True)
                board[i] = ""  # 回復
                best_score = min(score, best_score)
        return best_score
            
def check_winner(board):
    win_combinations = [
        {0, 1, 2}, {3, 4, 5}, {6, 7, 8},  # 橫向
        {0, 3, 6}, {1, 4, 7}, {2, 5, 8},  # 縱向
        {0, 4, 8}, {2, 4, 6}              # 斜向
    ]
    
    for combo in win_combinations:
        if board[list(combo)[0]] == board[list(combo)[1]] == board[list(combo)[2]] != "":
            return board[list(combo)[0]]  # 回傳勝者 "X" 或 "O"
    return None
          
widget.show()
app.exec_()