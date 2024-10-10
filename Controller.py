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
            #board[i] = ""  # 回復
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
# 電腦的回合:
# 迴圈遍歷格子（i = 0 到 8）:
# 如果某個格子是空的 (""):
# 電腦下棋（board[i] = "X"）。
# 呼叫 minimax(board, False)，進入玩家的回合。

# 玩家的回合:
# 迴圈遍歷格子（i = 0 到 8）:
# 如果某個格子是空的 (""):
# 玩家下棋（board[i] = "O"）。
# 呼叫 minimax(board, True)，進入電腦的回合。
def minimax(board, is_maximizing):
    # 終止條件
    winner = check_winner(board)
    if winner == 'X':  # 電腦贏電腦設定為得分最大的棋局
        return 1
    elif winner == 'O':  # 玩家贏玩家讓電腦得分最小的棋局
        return -1
    elif "" not in board:  #表示遊戲平局。當棋盤滿了但沒有獲勝者時，minimax 函數會返回 0。
        return 0
# 終止條件滿足時：
# 如果這三個條件中的任意一個成立，函數立即返回值給呼叫者。
# 此時，minimax 函數會直接結束，後面的遞迴邏輯不會執行。    
# 在 minimax 函數中，當程式執行到 elif "" not in board: 並返回 0 時，表示棋盤已經滿了且沒有贏家（平局），
# 此時函數會直接返回 0。
# 因此，如果 return 0 已經被執行，則後面的 if is_maximizing 這一段代碼不會被執行。
# 這是因為一旦函數內部執行了 return，它會立即結束該函數的執行，並將值返回給呼叫它的上一層函數。
# 換句話說：
# 如果是平局，minimax 會直接返回 0，並且後面的 if is_maximizing 不會執行。
# 只有當棋盤還沒滿、且沒有出現贏家或平局時，if is_maximizing 和 else 的代碼才會繼續執    
    if is_maximizing:  # 電腦的回合
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "X"  # 電腦的棋子"X"  # 電腦下在位置 3
                score = minimax(board, False)
                #是score = minimax(board, False)：這行代碼會呼叫 minimax 函數，傳入更新後的棋盤狀態和 False（表示這次是玩家的回合）。
                # minimax 函數會根據當前棋盤狀態進行遞迴計算，評估該狀態的分數，返回給 score 變數。接著執行下一步的""和評估分數
                board[i] = ""  # 撤銷這一步棋，準備嘗試下一個位置
                best_score = max(score, best_score)
        return best_score
    # 呼叫 minimax：當電腦下棋並執行 score = minimax(board, False) 時，minimax 函數會被遞迴調用。
    # 這個調用會根據當前的棋盤狀態進行評估，並最終返回一個分數（score）。
    # 返回分數後的邏輯：一旦 minimax 完成計算並返回分數，控制會回到原來的函數（即電腦的回合），並繼續執行下一行程式碼。
    # 這一行是 board[i] = ""，表示撤銷剛剛下的棋步。
    # 更新 best_score：然後，程式會執行 best_score = max(score, best_score)。
    # 這裡的 max 函數會比較當前的分數（score）和之前的最佳分數（best_score），並將較大的那個值更新到 best_score。
    
    else:  # 玩家回合
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = "O"  # 玩家棋子
                score = minimax(board, True)
                board[i] = ""  # 回復
                best_score = min(score, best_score)
        return best_score

# 電腦回合，i = 0：

# 電腦嘗試在位置 i = 0 下 "X"，然後呼叫 minimax(board, False) 進入玩家回合。
# 玩家回合（電腦下棋後）：

# 玩家開始嘗試每個空位，依次從 i = 0 到 i = 8，在每個位置下 "O"，然後再次呼叫 minimax(board, True) 
# 進行下一次電腦回合（即遞迴進入更深層）。
# 當遞迴到終止條件（例如一方獲勝或棋盤填滿）時，minimax 開始回傳分數（1、-1 或 0），
# 這些分數根據遊戲結果（電腦贏、玩家贏或平局）來決定。
# 回傳分數到電腦回合：

# 當所有玩家的可能下棋位置都模擬完並回傳了分數，電腦回合會根據這些結果更新 best_score，然後執行 board[0] = "" 將棋盤恢復到未下棋的狀態，準備開始下一個位置的嘗試。
# 電腦回合，i = 1：

# 電腦現在嘗試在 i = 1 的位置下 "X"，然後再次呼叫 minimax(board, False) 進行玩家回合。
# 玩家回合（電腦下棋後，i = 1）：

# 與前一回合類似，玩家會依次嘗試從 i = 0 到 i = 8 下 "O"，每次都遞迴進入下一層，直到所有可能的結果都回傳給電腦。
# 重複上述步驟：

# 每次電腦嘗試在不同位置下 "X"，玩家回合都會模擬所有可能的走法，並回傳分數，最終電腦根據所有這些模擬更新 best_score，然後進行下一個位置的嘗試。
# 總結：
# 電腦的每一個棋步（如 i = 0, 1, 2, ...） 會導致玩家嘗試所有可能的棋步（i = 0 到 i = 8）。
# 玩家回合結束後，會遞迴回傳分數給電腦，電腦依據分數更新它的 best_score。
# 電腦會回復當前棋盤狀態（即 board[i] = ""），並嘗試下一個位置。

            
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