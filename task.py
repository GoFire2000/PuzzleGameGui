import os
import sys
import random
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QPixmap
from PyQt5.QtWidgets import QGridLayout, QMessageBox, QWidget, QApplication, QLabel

UPKEY = 0
DOWNKEY = 1
LEFTKEY = 2
RIGHTKEY = 3

ImageGame = 1
DigitalGame = 2

class NumberHuaRong(QWidget):
    # 华容道主体
    def __init__(self, K, mode):
        super().__init__()
        self.blocks = []
        self.zeroX = 0
        self.zeroY = 0
        self.K = K
        self.mode = mode
        self.gltMain = QGridLayout()

        self.initUI()
    
    def initUI(self):
        # 设置方块的间隔
        self.gltMain.setSpacing(5)
        self.onInit()

        # 设置布局
        self.setLayout(self.gltMain)
        # 设置宽和高
        self.setFixedSize(400, 400)
        # 设置标题
        self.setWindowTitle('数字华容道')
        # 设置背景颜色
        self.setStyleSheet('background-color:gray;')
        self.show()
    
    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        numbers = list(range(1, self.K * self.K))
        numbers.append(0)
        for i in  range(self.K):
            self.blocks.append([])
            for j in range(self.K):
                val = numbers[i * self.K + j]
                self.blocks[i].append(val)

                if val == 0:
                    self.zeroX = i
                    self.zeroY = j

        for i in range(500):
            random_num = random.randint(0, 3)
            self.move(random_num)
        
        self.updatePanel()
    
    # 将16个Block添加到self.gltMain
    def updatePanel(self):
        for i in range(self.K):
            for j in range(self.K):
                self.gltMain.addWidget(Block(self.blocks[i][j], self.K, self.mode), i, j)
        self.setLayout(self.gltMain)

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        if key == Qt.Key_Up or key == Qt.Key_W:
            self.move(DOWNKEY)
        if key == Qt.Key_Down or key == Qt.Key_S:
            self.move(UPKEY)
        if key == Qt.Key_Left or key == Qt.Key_A:
            self.move(RIGHTKEY)
        if key == Qt.Key_Right or key == Qt.Key_D:
            self.move(LEFTKEY)
        self.updatePanel()

        if self.checkResult() == 1:
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战!'):
                self.onInit()

    def move(self, direction):
        if direction == UPKEY:
            if self.zeroX != 0:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX - 1][self.zeroY]
                self.blocks[self.zeroX - 1][self.zeroY] = 0
                self.zeroX -= 1
        elif direction == DOWNKEY:
            if self.zeroX != self.K - 1:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX + 1][self.zeroY]
                self.blocks[self.zeroX + 1][self.zeroY] = 0
                self.zeroX += 1
        elif direction == LEFTKEY:
            if self.zeroY != 0:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX][self.zeroY - 1]
                self.blocks[self.zeroX][self.zeroY - 1] = 0
                self.zeroY -= 1
        elif direction == RIGHTKEY:
            if self.zeroY != self.K - 1:
                self.blocks[self.zeroX][self.zeroY] = self.blocks[self.zeroX][self.zeroY + 1]
                self.blocks[self.zeroX][self.zeroY + 1] = 0
                self.zeroY += 1
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


class imageProcess():
    def __init__(self, filePath, K):
        self.filePath = filePath
        self.K = K
        self.image = Image.open(filePath)
        # image.show()
        self.image = self.fill_image()
        self.image_list = self.cut_image()
        self.save_images()

    # 将图片填充为正方形
    def fill_image(self):
        width, height = self.image.size
        new_image_length = width if width > height else height
        new_image = Image.new(self.image.mode, (new_image_length, new_image_length))
        if width > height:
            new_image.paste(self.image, (0, int((new_image_length-height) / 2)))
        else:
            new_image.paste(self.image, (int((new_image_length-width) / 2), 0))
        return new_image

    # 将图片分割
    def cut_image(self):
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
    def save_images(self):
        index = 0
        for image in self.image_list:
            image.save('.\\mypic\\' + str(index) + '.jpg')
            index += 1


if __name__ == '__main__': 
    if not os.path.exists('.\\mypic'):
        os.makedirs('.\\mypic')
    os.system('del .\\mypic\\*.jpg')
    mode = 2
    img_path = '.\\pic2.jpg'
    K = 5
    imageProcess(img_path, K)

    app = QApplication(sys.argv)
    ex = NumberHuaRong(K, mode)
    sys.exit(app.exec_())