from Data.Map import Map
from Data.Enums import Direction as D
from random import randint


class Sim(object):

    # map 을 인풋 받아 map의 robot을 direction 방향으로 1칸 이동 시킵니다.
    # 10프로 확률로 2 칸을 갑니다. 맵의 경계를 넘거나, 2칸 움직임시 하자드를 밟지 않도록 if문으로 조치합니다.
    def moveForward(self, map):

        robotDirection = map.getRobotDirection()
        if robotDirection == D.closed:
            print(" error on Function Sim- moveForward: Direction is closed")
        elif robotDirection == D.up:
            map.moveRobot(0, 1)
        elif robotDirection == D.right:
            map.moveRobot(1, 0)
        elif robotDirection == D.down:
            map.moveRobot(0, -1)
        elif robotDirection == D.left:
            map.moveRobot(-1, 0)
        else:
            print(" error on Function Sim- moveForward: direction is not defined")

            # 10프로의 확률.
        if randint(1, 10) == 1:
            # if 1:
            robotLocation = map.getRobotLocation()

            if robotDirection == D.closed:
                print(" error on Function Sim- moveForward: Direction is closed")
            elif robotDirection == D.up and robotLocation[1] + 1 < map.getY() and not self.hazardSensor(
                    map.getAllHazard(), (robotLocation[0], robotLocation[1] + 1)):
                map.moveRobot(0, 1)
            elif robotDirection == D.right and robotLocation[0] + 1 < map.getX() and not self.hazardSensor(
                    map.getAllHazard(), (robotLocation[0] + 1, robotLocation[1])):
                map.moveRobot(1, 0)
            elif robotDirection == D.down and robotLocation[1] - 1 >= 0 and not self.hazardSensor(map.getAllHazard(), (
            robotLocation[0], robotLocation[1] - 1)):
                map.moveRobot(0, -1)
            elif robotDirection == D.left and robotLocation[0] - 1 >= 0 and not self.hazardSensor(map.getAllHazard(), (
            robotLocation[0] - 1, robotLocation[1])):
                map.moveRobot(-1, 0)

    # 로봇을 오른쪽 90도 회전시킵니다.
    def turnRight(self, map):

        robotDirection = map.getRobotDirection()
        if robotDirection == D.closed:
            print(" error on Function Sim- turn right: Direction is closed")
        elif robotDirection == D.up:
            map.setRobotDirection(D.right)
        elif robotDirection == D.right:
            map.setRobotDirection(D.down)
        elif robotDirection == D.down:
            map.setRobotDirection(D.left)
        elif robotDirection == D.left:
            map.setRobotDirection(D.up)
        else:
            print(" error on Function Sim- turn right: direction is not defined")

    # 점 좌표를 받아 해당 좌표가 blop,hazard 점인지 확인합니다.
    #  첫번째 인자는 map의 getAll~ () 함수로 리턴되는 튜플 어레이를 받을 수 있도록 제작하였습니다.
    def blobSensor(self, blobP, location):
        if location in blobP:
            return 1
        else:
            return 0

    def hazardSensor(self, unseenHazardP, location):
        if location in unseenHazardP:
            return 1
        else:
            return 0

    # 로봇이 오작동했는지 확인하는 함수 입니다.
    # 입력된 튜플값이 다르면 1을 리턴합니다. ADDON의 COMPENSATE MOVE 에서 사용합니다.
    def positioningSensor(self, rightPos, currentPos):
        if currentPos != rightPos:
            return 1
        else:
            return 0
