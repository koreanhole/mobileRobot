import random
from Data.Point import Point as P
from Data.Enums import Direction as D
from Data.Enums import State as S


class Map:
    # 격자 크기, 시작 위치,타겟 지역,  위험 지역 을 입력 받는다.... 시작위치는 튜플, 타겟,위험 지역은 튜플의 리스트로 받는다.
    __slots__ = ["__xSize", "__ySize", "__seenHazardP", "__unseenHazardP", "__HazardP", "avoidRedundance", "__blobP",
                 "__unchecked_blobP", "__checked_blobP", "__targetP", "__unchecked_targetP", "__checked_targetP",
                 "__robot"]

    __xSize: int
    __ySize: int
    __seenHazardP: list
    __HazardP: list
    __unseenHazard: list
    __avoidRedundance : list
    __blobP: list
    __unchecked_blobP: list
    __checked_blobP: list
    __targetP: list
    __unchecked_targetP: list
    __checked_targetP: list
    __robot: P


    def __init__(self, xSize, ySize, startLocation, targetNum, hazardNum):
        self.__xSize = xSize
        self.__ySize = ySize

        self.__seenHazardP = []
        self.__unseenHazardP = []
        self.__HazardP = []
        self.avoidRedundance = []

        self.__blobP = []
        self.__unchecked_blobP = []
        self.__checked_blobP = []

        self.__targetP = []
        self.__unchecked_targetP = []
        self.__checked_targetP = []

        # initialize robot
        tmpX, tmpY = startLocation
        self.__robot = P(tmpX, tmpY, S.robot)
        self.__robot.setPath(D.up)
        self.__robot.setDirection(D.up)
        self.avoidRedundance.append((tmpX, tmpY))

        # 입력받은 위험 지역에서 홀수번쨰는 안보이는 위험, 짝수번째는 보이는 위험으로 설정.
        for i in range(0, targetNum):
            tmpX, tmpY = self.getNewPoint()
            self.__targetP.append(P(tmpX, tmpY, S.unchecked_target))
            self.__unchecked_targetP.append(P(tmpX, tmpY, S.unchecked_target))
            self.avoidRedundance.append((tmpX, tmpY))

        # 하자드 포인트 생성. 홀수 번째는 보이지 않는 위험으로 한다.
        for i in range(0, hazardNum):
            tmpX, tmpY = self.getNewPoint()
            self.__HazardP.append(P(tmpX, tmpY, S.hazard))
            self.avoidRedundance.append((tmpX,tmpY))
            if i % 2 == 0:
                self.__seenHazardP.append(P(tmpX, tmpY, S.seen_hazard))
            else:
                self.__unseenHazardP.append(P(tmpX, tmpY, S.unseen_hazard))

        # 블롭 생성, 처음엔 모두 unchecked blob 으로 한다.
        for i in range(0, 3):
            tmpX, tmpY = self.getNewPoint()
            self.avoidRedundance.append((tmpX, tmpY))
            self.__blobP.append(P(tmpX, tmpY, S.unchecked_blob))
            self.__unchecked_blobP.append(P(tmpX, tmpY, S.unchecked_blob))


    # 초기화에 사용된다. 겹치지 않는 점의 좌표를 리턴한다.
    def getNewPoint(self):
        tmpX, tmpY = random.randint(0, self.__xSize - 1), random.randint(0, self.__ySize - 1)
        while (tmpX, tmpY) in self.avoidRedundance:
            tmpX, tmpY = random.randint(0, self.__xSize - 1), random.randint(0, self.__ySize - 1)
        return (tmpX, tmpY)

    # blob 상태의 점의 위치를 튜플의 배열로 리턴한다.
    # 나머지 getAll 함수들도 모두 마찬 가지이다.
    def getAllBlob(self):
        pointTupleArr = []
        for tmpPoint in self.__blobP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    def getAllCheckedBlob(self):
        pointTupleArr = []
        for tmpPoint in self.__checked_blobP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    def getAllUnCheckedBlob(self):
        pointTupleArr = []
        for tmpPoint in self.__unchecked_blobP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    # 위험 상태의 점의 위치를 튜플의 배열로 리턴한다..... 처음에 길찾기 경로 확인.
    def getAllHazard(self):
        pointTupleArr = []
        for tmpPoint in self.__HazardP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    def getAllSeenHazard(self):
        pointTupleArr = []
        for tmpPoint in self.__seenHazardP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    def getAllUnSeenHazard(self):
        pointTupleArr = []
        for tmpPoint in self.__unseenHazardP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    def getAllTarget(self):
        pointTupleArr = []
        for tmpPoint in self.__targetP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    def getAllCheckedTarget(self):
        pointTupleArr = []
        for tmpPoint in self.__checked_targetP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    def getAllUnCheckedTarget(self):
        pointTupleArr = []
        for tmpPoint in self.__unchecked_targetP:
            pointTupleArr.append(tmpPoint.getLocation())
        return pointTupleArr

    # 맵 크기를 튜플로 리턴
    def getMapSize(self):
        return (self.__xSize, self.__ySize)

    # find_unseen~ 함수
    # 좌표를 입력받아 unseen_hazard,unchecked_target, unchecked_blob 이면 체크된 블롭,위험,타겟으로 상태를 바꾼다.
    # find_unseenHazard의 경우, 찾아서 수정했는지의 여부를 리턴한다.
    def find_unseenHazard(self, x, y):
        for tmpPoint in self.__unseenHazardP:
            tmpTuple = tmpPoint.getLocation()
            if tmpTuple == (x, y):
                tmpPoint.setState(S.seen_hazard)
                self.__seenHazardP.append(tmpPoint)
                self.__unseenHazardP.remove(tmpPoint)
                return 1
        return 0


    # 입력받은 좌표를 갖는 블롭을 타겟으로
    def find_blob(self, x, y):
        for tmpPoint in self.__unchecked_blobP:
            tmpTuple = tmpPoint.getLocation()
            if tmpTuple == (x, y):
                tmpPoint.setState(S.checked_blob)
                self.__checked_blobP.append(tmpPoint)
                self.__unchecked_blobP.remove(tmpPoint)

    def find_target(self, x, y):
        for tmpPoint in self.__unchecked_targetP:
            tmpTuple = tmpPoint.getLocation()
            if tmpTuple == (x, y):
                tmpPoint.setState(S.checked_target)
                self.__checked_targetP.append(tmpPoint)
                self.__unchecked_targetP.remove(tmpPoint)

    # map 의 로봇 상태를 바꾸는 get,set 함수들이다.
    def getRobotLocation(self):
        return self.__robot.getLocation()

    def moveRobot(self, x, y):
        self.__robot.move(x, y)

    def setRobotPath(self, path):
        self.__robot.setPath(path)

    def getRobotPath(self):
        return self.__robot.getPath()

    def getRobotDirection(self):
        return self.__robot.getDirection()

    def setRobotDirection(self, newDirection):
        self.__robot.setDirection(newDirection)


        # 맵의 크기를 리턴한다.
    def getY(self):
        return self.__ySize

    def getX(self):
        return self.__xSize
