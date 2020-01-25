
from Data.Map import Map
from Operator.AddOn import AddOn
from Data.Enums import *

class Manager:
    __slots__ = ["__map", "__addon", "__k"]

    __map: Map
    __addon: AddOn
    __k: int

    def __init__(self,xSize,ySize , startLocation, targetNum, hazardNum):
        self.__map = Map(xSize, ySize, startLocation, targetNum, hazardNum)
        self.__map.setRobotDirection(Direction.up)
        self.__k = 0

        #compensate move 기능을 위해 addon을 라이프 타임을 공유하는 변수로 둔다. 처음 초기화할때, 로봇 위치를 저장한다.
        self.__addon = AddOn()
        self.__addon.setRobotPosition(self.__map.getRobotLocation()[0], self.__map.getRobotLocation()[1])

    def robotMovement(self):
        # 로봇이 이전에 오작동 했으면, 원래 위치로 옮기고 함수를 종료한다.
        if(self.__addon.compensateMove(self.__map)):
            return self.__map
        #길찾기 알고리즘 수행하고 path 에 결과를 입력한다.
        if self.__map.getAllTarget().count(self.__map.getRobotLocation()):
            self.__k = self.__k + 1
            path = self.__addon.pathFinding(self.__map, self.__map.getRobotLocation(), self.__map.getAllTarget()[self.__k])
        else:
            path = self.__addon.pathFinding(self.__map, self.__map.getRobotLocation(), self.__map.getAllTarget()[self.__k])
        self.findRobotPath(self.__map.getRobotLocation(), path[1])
        # 길찾기 알고리즘 수행하고 path 에 결과를 입력한다.

        #로봇을 돌리고 직진시킨다. 돌린 위치에 위험지역이 있으면 위험지역만 표시하고 움직이진 않는다.
        self.__addon.followPath(self.__map)
        # 움직인 위치에서 체크되지않은  블롭과 하자드를 찾는다.
        self.__addon.detectHazard(self.__map)
        self.__addon.detectBlob(self.__map)
        return self.__map



    def findRobotPath(self, currentPos, nextPos):
        #왼쪽으로 이동해야 하는 경우
        if currentPos[0] - nextPos[0] == 1 and currentPos[1] == nextPos[1]:
            self.__map.setRobotPath(Direction.left)
        #위쪽으로 이동해야 하는 경우
        elif currentPos[0] == nextPos[0] and currentPos[1] - nextPos[1] == -1:
            self.__map.setRobotPath(Direction.up)
        #오른쪽으로 이동해야 하는 경우
        elif currentPos[0] - nextPos[0] == -1 and currentPos[1] == nextPos[1]:
            self.__map.setRobotPath(Direction.right)
        #아래쪽으로 이동해야 하는 경우
        elif currentPos[0] == nextPos[0] and currentPos[1] - nextPos[1] == 1:
            self.__map.setRobotPath(Direction.down)

