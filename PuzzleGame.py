import os
import sys
import time
import random

from PyQt5 import QtCore
from DfsFind import DfsFinder
from PIL import Image
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QPixmap
from PyQt5.QtWidgets import QAbstractItemDelegate, QDialog, QFileDialog, QGridLayout, QHeaderView, QMessageBox, QSplitter, QTextEdit, QWidget, QApplication, QLabel
from Ui_GAME import Ui_MainWindow

UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

REACT = [1, 0, 3, 2]

PUZZLEGAME = 1
DIGITALGAME = 2

class PuzzleGame(QtWidgets.QMainWindow, Ui_MainWindow):
    # 拼图游戏主体
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = None
        self.image_list = []
        self.K = 4
        self.zeroX = self.K - 1
        self.zeroY = self.K - 1
        self.step = 0
        self.path = []
        self.blocks = []
        for i in range(self.K):
            self.blocks.append([])
            for j in range(self.K):
                self.blocks[i].append(i * self.K + j + 1)
        self.blocks[self.K - 1][self.K - 1] = 0
        # print(self.blocks)
        self.mode = PUZZLEGAME
        # self.mode = DIGITALGAME
        self.autoLoadImage()
        self.tableWidget.horizontalHeader().hide()  # 隐藏行头，列头
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 自适应调整行高，列宽
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.puzzleDisplay()
        
        self.pushButton_5.clicked.connect(self.loadImage)
        self.action_7.triggered.connect(self.changeK2)
        self.action_8.triggered.connect(self.changeK3)
        self.action_9.triggered.connect(self.changeK4)
        self.action_10.triggered.connect(self.changeK5)
        self.action_11.triggered.connect(self.changeK6)
        self.action_13.triggered.connect(self.changePuzzleGame)
        self.action_14.triggered.connect(self.changeDigitalGame)
        self.pushButton_4.clicked.connect(self.helpImg)
        self.pushButton_2.clicked.connect(self.exitGame)
        self.pushButton_3.clicked.connect(self.startGame)
        self.pushButton.clicked.connect(self.autoOperation)
        
    def changePuzzleGame(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "拼图游戏"))
        self.mode = PUZZLEGAME
        self.reStartGame()
    
    def changeDigitalGame(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "数字华容道"))
        self.mode = DIGITALGAME
        self.reStartGame()

    # 自动操作
    def autoOperation(self):
        ansFind = DfsFinder(self.blocks, self.K, self.path)
        print('ansPath:', ansFind.ansPath)

        for key in ansFind.ansPath:
            self.move(key)
            self.step += 1
            self.textEdit.setText(str(self.step))
            self.puzzleDisplay()
            QApplication.processEvents()
            time.sleep(0.2)
            if self.checkResult() == 1:
                if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战!'):
                    self.onInit()
                self.textEdit.setText(str(0))
                break
            


    # 退出游戏
    def exitGame(self):
        sys.exit()
    
    # 帮助，也就是展示完整图片
    def helpImg(self):
        dialog = QDialog()
        dialog.setWindowTitle("帮助")
        h, w = self.image.size
        dialog.resize(h, w)
        label = QLabel('show', dialog)
        pix = QPixmap('.\\mypic\\' + 'image' + '.jpg')
        label.setPixmap(pix)
        label.setScaledContents(True)
        dialog.exec_()

    # 修改难度
    def changeK2(self):
        self.K = 2
        self.reStartGame()

    def changeK3(self):
        self.K = 3
        self.reStartGame()

    def changeK4(self):
        self.K = 4
        self.reStartGame()

    def changeK5(self):
        self.K = 5
        self.reStartGame()
        
    def changeK6(self):
        self.K = 6
        self.reStartGame()

    # 将图片填充为正方形
    def fillImage(self):
        width, height = self.image.size
        new_image_length = width if width > height else height
        new_image = Image.new(self.image.mode, (new_image_length, new_image_length))
        if width > height:
            new_image.paste(self.image, (0, int((new_image_length-height) / 2)))
        else:
            new_image.paste(self.image, (int((new_image_length-width) / 2), 0))
        return new_image

    # 将图片分割
    def cutImage(self):
        width, height = self.image.size
        item_width = int(width/self.K)
        box_list = []
        for i in range(0, self.K):
            for j in range(0, self.K):
                box = (j * item_width, i * item_width, (j + 1) * item_width, (i + 1) * item_width)
                box_list.append(box)
        image_list = []
        image_list.append(Image.new(self.image.mode, (width, height)).crop(box_list[0]))
        image_list = image_list + [self.image.crop(box) for box in box_list]
        return image_list

    # 保存图片
    def saveImages(self):
        if not os.path.exists('.\\mypic'):
            os.makedirs('.\\mypic')
        os.system('del .\\mypic\\*.jpg')
        index = 0
        for image in self.image_list:
            image.save('.\\mypic\\' + str(index) + '.jpg')
            index += 1
        self.image.save('.\\mypic\\image.jpg')
    
    # 从外部导入图片
    def loadImage(self):
        image_path,_ = QFileDialog.getOpenFileName(self,'选择文件','','Image files(*.jpg , *.png, *.jpeg)')
        # print(len(image_path))
        if len(image_path) == 0:
            self.autoLoadImage()
            return
        self.image = Image.open(image_path)
        self.image = self.fillImage()
        self.image_list = self.cutImage()
        self.saveImages()
        self.reStartGame()
        
    # 自动导入图片
    def autoLoadImage(self):
        if self.image == None:
            self.image = Image.open('.\\pic.jpg')
        self.image = self.fillImage()
        self.image_list = self.cutImage()
        self.saveImages()
        self.reStartGame()

    def reStartGame(self):
        self.blocks = []
        for i in range(self.K):
            self.blocks.append([])
            for j in range(self.K):
                self.blocks[i].append(i * self.K + j + 1)
        # print(self.blocks)
        self.blocks[self.K - 1][self.K - 1] = 0
        self.zeroX = self.K - 1
        self.zeroY = self.K - 1
        if self.image != None:
            self.image = self.fillImage()
            self.image_list = self.cutImage()
            self.saveImages()
        self.puzzleDisplay()

    def puzzleDisplay(self):
        # self.gltMain.setSpacing(5)
        # self.onInit()
        self.tableWidget.clear()
        self.tableWidget.setRowCount(self.K)  # 设置行数，列数
        self.tableWidget.setColumnCount(self.K)
        if self.image is None:
            self.autoLoadImage()
            return
        # 设置图片
        for i in range(self.K):
            for j in range(self.K):
                id = self.blocks[i][j]
                # if self.blocks[i * self.K +  j] == 0:
                #     continue
                newItem = QtWidgets.QLabel(self)
                if self.mode == PUZZLEGAME:
                    pix = QPixmap('.\\mypic\\' + str(id) + '.jpg')
                    newItem.setPixmap(pix)
                    newItem.setScaledContents(True)
                else:
                    font = QFont()
                    font.setPointSize(30)
                    font.setBold(True)
                    newItem.setFont(font)

                    # 设置字体颜色
                    pa = QPalette()
                    pa.setColor(QPalette.WindowText, Qt.white)
                    newItem.setPalette(pa)

                    # 设置文字位置
                    newItem.setAlignment(Qt.AlignCenter)

                    # 设置背景颜色\圆角和文本内容
                    if id == 0:
                        newItem.setStyleSheet('background-color: rgb(214, 214, 214);border-radius:10px;')
                    else:
                        newItem.setStyleSheet('color: rgb(85, 85, 127);background-color:rgb(177, 177, 0);;border-radius:10px;')
                        newItem.setText(str(id))
                self.tableWidget.setCellWidget(i, j, newItem)
    # 开始游戏
    def startGame(self):
        self.onInit()
        self.puzzleDisplay()
        
    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        numbers = list(range(1, self.K * self.K))
        numbers.append(0)
        self.step = 0
        for i in  range(self.K):
            for j in range(self.K):
                val = numbers[i * self.K + j]
                self.blocks[i][j] = val

                if val == 0:
                    self.zeroX = i
                    self.zeroY = j
        self.path = []
        # lis = [2, 1, 2, 0, 3, 1, 0, 1, 3]
        # lis = [REACT[x] for x in lis]
        # lis = list(reversed(lis))
        # for random_num in lis:
        #     tag = self.move(random_num)
        #     if tag == 1:
        #         self.path.append(REACT[random_num])
        #     self.puzzleDisplay()

        # return
        if self.K <= 4:
            bor = random.randint(1, int(15 + self.K * self.K * self.K / 8))
        else:
            bor = random.randint(1, int(15 + self.K * self.K * self.K / 2))
        
        for i in range(bor):
            # for i in range(6):
            random_num = random.randint(0, 3)
            tag = self.move(random_num)
            if tag == 1:
                self.path.append(REACT[random_num])

        if self.checkResult() == 1:
            self.reStartGame()
        
            

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        # print(key)
        # print(self.blocks)
        if key == Qt.Key_W:
            tag = self.move(DOWNKEY)
            if tag == 1:
                self.path.append(REACT[DOWNKEY])
            self.step += 1
            self.textEdit.setText(str(self.step))
        if key == Qt.Key_S:
            tag = self.move(UPKEY)
            if tag == 1:
                self.path.append(REACT[UPKEY])
            self.step += 1
            self.textEdit.setText(str(self.step))
        
        if key == Qt.Key_A:
            tag = self.move(RIGHTKEY)
            if tag == 1:
                self.path.append(REACT[RIGHTKEY])
            self.step += 1
            self.textEdit.setText(str(self.step))

        if key == Qt.Key_D:
            tag = self.move(LEFTKEY)
            if tag == 1:
                self.path.append(REACT[LEFTKEY])
            self.step += 1
            self.textEdit.setText(str(self.step))

        # print(self.blocks)
        self.puzzleDisplay()

        if self.checkResult() == 1:
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战!'):
                self.onInit()
            self.textEdit.setText(str(0))

    # 按WASD移动
    def move(self, direction):
        tag = 0
        if direction == UPKEY:
            if self.zeroX != 0:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX - 1][self.zeroY]
                self.blocks[self.zeroX - 1][self.zeroY] = 0
                self.zeroX -= 1
                tag = 1
        elif direction == DOWNKEY:
            if self.zeroX != self.K - 1:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX + 1][self.zeroY]
                self.blocks[self.zeroX + 1][self.zeroY] = 0
                self.zeroX += 1
                tag = 1
        elif direction == LEFTKEY:
            if self.zeroY != 0:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX][self.zeroY - 1]
                self.blocks[self.zeroX][self.zeroY - 1] = 0
                self.zeroY -= 1
                tag = 1
        elif direction == RIGHTKEY:
            if self.zeroY != self.K - 1:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX][self.zeroY + 1]
                self.blocks[self.zeroX][self.zeroY + 1] = 0
                self.zeroY += 1
                tag = 1
        return tag
    
    # 检测是否成功，1为是0为否
    def checkResult(self):
        for i in range(self.K):
            for j in range(self.K):
                if i == self.K - 1 and j == self.K - 1:
                    if self.blocks[i][j] != 0:
                        return 0
                elif self.blocks[i][j] != i * self.K + j + 1:
                    return 0
        return 1

    
class Block(QLabel):
    # 数字方块
    def __init__(self, number, K, mode):
        super().__init__()

        self.number = number
        self.setFixedSize(int(350 / K), int(350 / K))

        if mode == ImageGame: # 拼图游戏
            pix = QPixmap('.\\mypic\\' + str(number) + '.jpg')
            self.setPixmap(pix)
            self.setScaledContents(True)

        elif mode == DigitalGame: # 数字华容道
            # 设置字体
            font = QFont()
            font.setPointSize(30)
            font.setBold(True)
            self.setFont(font)

            # 设置字体颜色
            pa = QPalette()
            pa.setColor(QPalette.WindowText, Qt.white)
            self.setPalette(pa)

            # 设置文字位置
            self.setAlignment(Qt.AlignCenter)

            # 设置背景颜色\圆角和文本内容
            if self.number == 0:
                self.setStyleSheet('background-color:white;border-radius:10px;')
            else:
                self.setStyleSheet('background-color:borwn;border-radius:10px;')
                self.setText(str(self.number))


if __name__ == '__main__': 
    app = QApplication(sys.argv)
    ui = PuzzleGame()
    ui.show()
    sys.exit(app.exec_())