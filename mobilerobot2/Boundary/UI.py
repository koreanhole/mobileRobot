import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox

from Controller.Manager import Manager

class ViewManager():

    def __init__(self):
        self.show_initialForm()

    def show_initialForm(self):
        self.__initialForm = InitialForm()
        self.__initialForm.switch_window.connect(self.show_viewForm)
        self.__initialForm.show()

    def show_viewForm(self, mapX, mapY, positionX, positionY, hazardNum, targetNum):
        self.__viewForm = ViewForm(mapX, mapY, positionX, positionY, hazardNum, targetNum)
        self.__initialForm.close()
        self.__viewForm.show()
        self.__viewForm.setGeometry(0, 0, 800, 800)

class InitialForm(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(int, int, int, int, int, int)

    def __init__(self):
        textFormat = QtGui.QFont()
        textFormat.setBold(True)
        textFormat.setPointSize(20)

        QtWidgets.QWidget.__init__(self)
        self.centralLayout = QtWidgets.QHBoxLayout()
        self.layout1 = QtWidgets.QVBoxLayout()
        self.layout2 = QtWidgets.QVBoxLayout()
        self.mapSizeLayout = QtWidgets.QHBoxLayout()
        self.startPointLayout = QtWidgets.QHBoxLayout()
        self.hazardLayout = QtWidgets.QHBoxLayout()
        self.targetLayout = QtWidgets.QHBoxLayout()


        #textField설정
        self.mapSizeFieldX = QtWidgets.QLineEdit(self)
        self.mapSizeFieldX.setFixedWidth(35)
        self.mapSizeFieldY = QtWidgets.QLineEdit(self)
        self.mapSizeFieldY.setFixedWidth(35)
        self.startPointFieldX = QtWidgets.QLineEdit(self)
        self.startPointFieldX.setFixedWidth(35)
        self.startPointFieldY = QtWidgets.QLineEdit(self)
        self.startPointFieldY.setFixedWidth(35)
        self.hazardField = QtWidgets.QLineEdit(self)
        self.targetField = QtWidgets.QLineEdit(self)

        #label들 설정
        self.mapSizeLabel = QtWidgets.QLabel('지도의 크기 설정🗺')
        self.mapSizeLabelX = QtWidgets.QLabel('가로크기를 입력하세요')
        self.mapSizeLabelY = QtWidgets.QLabel('세로크기를 입력하세요')
        self.startPointLabel = QtWidgets.QLabel('로봇의 시작위치 설정🏃')
        self.startPointLabelX = QtWidgets.QLabel('x좌표값을 입력하세요')
        self.startPointLabelY = QtWidgets.QLabel('y좌표값을 입력하세요')
        self.hazardLabel = QtWidgets.QLabel('위험지역 설정🩸')
        self.hazardLabel2 = QtWidgets.QLabel('위험지역의 갯수를 입력하세요')
        self.targetLabel = QtWidgets.QLabel('목표지점 설정🎯')
        self.targetLabel2 = QtWidgets.QLabel('목표지점의 갯수를 입력하세요')

        #label의 텍스트에 문자형식 지정.
        self.mapSizeLabel.setFont(textFormat)
        self.startPointLabel.setFont(textFormat)
        self.hazardLabel.setFont(textFormat)
        self.targetLabel.setFont(textFormat)

        #button설정
        self.startB = QtWidgets.QPushButton('시작', self)
        self.startB.clicked.connect(self.startClicked)

        #mapsize 입력하는 layout 설정
        self.layout1.addWidget(self.mapSizeLabel)
        self.mapSizeLayout.addWidget(self.mapSizeLabelX)
        self.mapSizeLayout.addWidget(self.mapSizeFieldX)
        self.mapSizeLayout.addWidget(self.mapSizeLabelY)
        self.mapSizeLayout.addWidget(self.mapSizeFieldY)
        self.layout1.addLayout(self.mapSizeLayout)

        #start point 입력하는 layout 설정
        self.layout1.addWidget(self.startPointLabel)
        self.startPointLayout.addWidget(self.startPointLabelX)
        self.startPointLayout.addWidget(self.startPointFieldX)
        self.startPointLayout.addWidget(self.startPointLabelY)
        self.startPointLayout.addWidget(self.startPointFieldY)
        self.layout1.addLayout(self.startPointLayout)

        #hazard 입력하는 layout 설정
        self.layout1.addWidget(self.hazardLabel)
        self.hazardLayout.addWidget(self.hazardLabel2)
        self.hazardLayout.addWidget(self.hazardField)
        self.layout1.addLayout(self.hazardLayout)

        #target 입력하는 layout 설정
        self.layout1.addWidget(self.targetLabel)
        self.targetLayout.addWidget(self.targetLabel2)
        self.targetLayout.addWidget(self.targetField)
        self.layout1.addLayout(self.targetLayout)

        #layout2(시작버튼 있는 레이아웃) 설정
        self.layout2.addWidget(self.startB)

        self.centralLayout.addLayout(self.layout1)
        self.centralLayout.addLayout(self.layout2)
        self.setLayout(self.centralLayout)

    #시작버튼이 눌렸을때 실행되는 함수.
    def startClicked(self):
        print('버튼이 눌렸습니다.')
        mapX = int(self.mapSizeFieldX.text())
        mapY = int(self.mapSizeFieldY.text())
        startPointX = int(self.startPointFieldX.text())
        startPointY = int(self.startPointFieldY.text())
        hazardNum = int(self.hazardField.text())
        targetNum = int(self.targetField.text())
        self.switch_window.emit(mapX, mapY, startPointX, startPointY, hazardNum, targetNum)


#시작버튼이 눌린후 실제 로봇이 움직이는 화면 정의.
class ViewForm(QtWidgets.QMainWindow):
    def __init__(self, mapX, mapY, positionX, positionY, hazardNum, targetNum):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.__mapX = mapX
        self.__mapY = mapY
        self.__robotX = positionX
        self.__robotY = positionY
        self.__hazardNum = hazardNum
        self.__targetNum = targetNum
        self.manager = Manager(self.__mapX, self.__mapY, (self.__robotX, self.__robotY), self.__targetNum, self.__hazardNum)

        #이미지 설정
        self.robotImage = QtGui.QPixmap()
        self.robotImage.load('./images/r.png')
        self.robotImage = self.robotImage.scaledToHeight(100)

        self.unchecked_hazardImage = QtGui.QPixmap()
        self.unchecked_hazardImage.load('./images/uch.png')
        self.unchecked_hazardImage = self.unchecked_hazardImage.scaledToHeight(70)

        self.checked_hazardImage = QtGui.QPixmap()
        self.checked_hazardImage.load('./images/ch.png')
        self.checked_hazardImage = self.checked_hazardImage.scaledToHeight(70)

        self.unchecked_BlobImage = QtGui.QPixmap()
        self.unchecked_BlobImage.load('./images/ucb.png')
        self.unchecked_BlobImage = self.unchecked_BlobImage.scaledToHeight(50)

        self.checkedBlobImage = QtGui.QPixmap()
        self.checkedBlobImage.load('./images/cb.png')
        self.checkedBlobImage = self.checkedBlobImage.scaledToHeight(50)

        self.unchecked_targetImage = QtGui.QPixmap()
        self.unchecked_targetImage.load('./images/uct.png')
        self.unchecked_targetImage = self.unchecked_targetImage.scaledToHeight(50)

        self.checked_targetImage = QtGui.QPixmap()
        self.checked_targetImage.load('./images/ct.png')
        self.checked_targetImage = self.checked_targetImage.scaledToHeight(50)


        self.backgroundImage = QtGui.QPixmap()
        self.backgroundImage.load('./images/bg.jpg')
        self.backgroundImage = self.backgroundImage.scaledToHeight(1000)


        #배경화면 레이블 설정

        self.backgroundLabel = QtWidgets.QLabel(self)
        self.backgroundLabel.setPixmap(self.backgroundImage)
        self.backgroundLabel.setFixedHeight(800)
        self.backgroundLabel.setFixedWidth(1200)
        self.backgroundLabel.move(0, 0)

        #로봇이미지가 담길 레이블 설정.
        self.robotLabel = QtWidgets.QLabel(self)
        self.robotLabel.setPixmap(self.robotImage)
        self.robotLabel.setFixedHeight(100)
        self.robotLabel.move(self.__robotX, self.__robotY)
        self.robotLabel.hide()

        #로봇의 이동명령을 내리는 버튼 설정.
        self.moveB = QtWidgets.QPushButton('로봇 이동', self)
        self.moveB.clicked.connect(self.moveButtonClicked)
        self.moveB.setFixedWidth(100)
        self.moveB.move(self.frameGeometry().width(), 10)

        #로봇의 현재위치를 표시해주는 레이블 설정.
        self.robotPositionLabel = QtWidgets.QLabel(self)
        self.robotPositionLabel.move(self.frameGeometry().width(),  50)

    #로봇 이동버튼을 눌렀을때 실행되는 함수부분
    #이동버튼이 눌릴때마다 경로를 계산하고 이 경로에 따라 이동한 로봇의 업데이트된 위치, 컬러블롭, 위험지점, 타겟등을 표시해준다.
    def moveButtonClicked(self):
        self.robotLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.robotLabel.show()
        updated_map = self.manager.robotMovement()
        current_position = "로봇의 위치: " + str(updated_map.getRobotLocation())
        self.robotPositionLabel.setText(current_position)
        self.moveLabel(self.robotLabel, updated_map.getRobotLocation()[0], updated_map.getRobotLocation()[1])
        self.repaint()

        #아직 방문하지 않은 목표지점을 표시해준다.
        unchecked_target = updated_map.getAllUnCheckedTarget()
        for i in range(len(unchecked_target)):
            self.unchecked_targetLabel = QtWidgets.QLabel(self)
            self.unchecked_targetLabel.setPixmap(self.unchecked_targetImage)
            self.unchecked_targetLabel.setFixedHeight(100)
            self.unchecked_targetLabel.show()
            self.moveLabel(self.unchecked_targetLabel, unchecked_target[i][0], unchecked_target[i][1])
            self.unchecked_targetLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.unchecked_targetLabel.repaint()

        #방문이 완료된 목표지점을 표시해준다.
        checked_target = updated_map.getAllCheckedTarget()
        for i in range(len(checked_target)):
            self.checked_targetLabel = QtWidgets.QLabel(self)
            self.checked_targetLabel.setPixmap(self.checked_targetImage)
            self.checked_targetLabel.setFixedHeight(100)
            self.checked_targetLabel.show()
            self.moveLabel(self.checked_targetLabel, checked_target[i][0], checked_target[i][1])
            self.checked_targetLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.checked_targetLabel.repaint()

        #아직 탐지하지 못한 컬러블롭을 표시해준다.
        unchecked_blob = updated_map.getAllUnCheckedBlob()
        for i in range(len(unchecked_blob)):
            self.unchecked_blobLabel = QtWidgets.QLabel(self)
            self.unchecked_blobLabel.setPixmap(self.unchecked_BlobImage)
            self.unchecked_blobLabel.setFixedHeight(100)
            self.unchecked_blobLabel.show()
            self.moveLabel(self.unchecked_blobLabel, unchecked_blob[i][0], unchecked_blob[i][1])
            self.unchecked_blobLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.unchecked_blobLabel.repaint()

        #탐지가 완료된 컬러블롭을 표시해준다.
        checkedBlob = updated_map.getAllCheckedBlob()
        for i in range(len(checkedBlob)):
            self.checkedBlobLabel = QtWidgets.QLabel(self)
            self.checkedBlobLabel.setPixmap(self.checkedBlobImage)
            self.checkedBlobLabel.setFixedHeight(100)
            self.checkedBlobLabel.show()
            self.moveLabel(self.checkedBlobLabel, checkedBlob[i][0], checkedBlob[i][1])
            self.checkedBlobLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.checkedBlobLabel.repaint()

        #아직 탐지가 안된 위험지점을 표시해준다.
        unchecked_hazard = updated_map.getAllUnSeenHazard()
        for i in range(len(unchecked_hazard)):
            self.unchecked_hazardLabel = QtWidgets.QLabel(self)
            self.unchecked_hazardLabel.setPixmap(self.unchecked_hazardImage)
            self.unchecked_hazardLabel.setFixedHeight(100)
            self.unchecked_hazardLabel.show()
            self.moveLabel(self.unchecked_hazardLabel, unchecked_hazard[i][0], unchecked_hazard[i][1])
            self.unchecked_hazardLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.unchecked_hazardLabel.repaint()

        #탐지가 완료된 위험지점을 표시해준다.
        checked_hazard = updated_map.getAllSeenHazard()
        for i in range(len(checked_hazard)):
            self.checked_hazardLabel = QtWidgets.QLabel(self)
            self.checked_hazardLabel.setPixmap(self.checked_hazardImage)
            self.checked_hazardLabel.setFixedHeight(100)
            self.checked_hazardLabel.show()
            self.moveLabel(self.checked_hazardLabel, checked_hazard[i][0], checked_hazard[i][1])
            self.checked_hazardLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.checked_hazardLabel.repaint()

        #컬러블롭, 위험지점, 로봇의 위치, 목표지점들의 표시가 완료된 후
        #더이성 방문할 목표지점이 남아있지 않을 경우 경고창을 띄운 후 프로그램을 종료시킨다.
        if updated_map.getAllUnCheckedTarget()==[]:
            buttonReply = QMessageBox.information(
                self, 'Cute Robot Says', "로봇이 최종 목적지에 도달하였습니다!",
                QMessageBox.Close
            )
            if buttonReply == QMessageBox.Close:
                self.close()

    #이미지 레이블들의 이동을 화면에 명확하게 나타내주기 위해 실제 이동한 좌표값보다 80배를 한 후 나타내준다.
    def moveLabel(self, Label, x, y):
        Label.move(x*80, y*80)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = ViewManager()
    ex.show_initialForm()
    sys.exit(app.exec_())

