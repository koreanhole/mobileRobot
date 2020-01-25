from Operator.Sim import Sim
from Data.Map import Map as M
from Data.Enums import Direction as D
from Operator.Node import Node



class AddOn(object):
    # 객체 변수와 자료형을 미리 설정했습니다.
    __slots__ = ["__currentX", "__currentY", "isHazard"]
    sim = Sim()
    __currentX: int
    __currentY: int
    __sim: Sim

    #map 을 인자로, 현재 위치가 , unchecked_target이면 target으로 바꾸고 맵에 저장합니다.
    def checkTarget(self, map):
        tmpX = map.getRobotLocation()[0]
        tmpY = map.getRobotLocation()[1]
        map.find_target(tmpX, tmpY)


    # map, 시작점, 도착지점을 인자로 받아서, 에이 스타 알고리즘을 사용, 다음가야 할 좌표를 입력 받습니다.
    def pathFinding(self, map, start, end):

        # 지도를 만드는 전처리 과정
        maze = [[0 for col in range(map.getMapSize()[0])] for row in range(map.getMapSize()[1])]
        for i in range(len(map.getAllSeenHazard())):
            maze[map.getAllSeenHazard()[i][0]][map.getAllSeenHazard()[i][1]] = 1
        start = start
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = []
        closed_list = []

        open_list.append(start_node)

        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            open_list.pop(current_index)
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Adjacent squares

                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                new_node = Node(current_node, node_position)

                children.append(new_node)

            for child in children:

                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                child.g = current_node.g
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)

    # 맵을 입력받아서, 로봇의 사방을 검사, 블롭이 있으면 타겟으로 바꾼다.
    def detectBlob(self, map):
        robotLocation = map.getRobotLocation()
        blobTuples = map.getAllBlob()
        if map.getY() > robotLocation[1] + 1 and self.sim.blobSensor(blobTuples,
                                                                     (robotLocation[0], robotLocation[1] + 1)):
            map.find_blob(robotLocation[0], robotLocation[1] + 1)

        if map.getX() > robotLocation[0] + 1 and self.sim.blobSensor(blobTuples,
                                                                     (robotLocation[0] + 1, robotLocation[1])):
            map.find_blob(robotLocation[0] + 1, robotLocation[1])

        if 0 <= robotLocation[1] - 1 and self.sim.blobSensor(blobTuples, (robotLocation[0], robotLocation[1] - 1)):
            map.find_blob(robotLocation[0], robotLocation[1] - 1)

        if 0 <= robotLocation[0] - 1 and self.sim.blobSensor(blobTuples, (robotLocation[0] - 1, robotLocation[1])):
            map.find_blob(robotLocation[0] - 1, robotLocation[1])

    # 맵 입력. 로봇이 보는 방향으로 하자드 검사./ unseen_hazard 가 있다면 seen_hazard 로 바꿈.
    def detectHazard(self, map):
        robotLocation = map.getRobotLocation()
        unSeenHazardTuples = map.getAllUnSeenHazard()
        robotDirection = map.getRobotDirection()
        isHazard = 0
        if robotDirection == D.up and map.getY() > robotLocation[1] + 1:
            isHazard = map.find_unseenHazard(robotLocation[0], robotLocation[1] + 1)


        if robotDirection == D.right and map.getX() > robotLocation[0] + 1 :
            isHazard = map.find_unseenHazard(robotLocation[0] + 1, robotLocation[1])

        if robotDirection == D.down and 0 <= robotLocation[1] - 1 :
            isHazard =  map.find_unseenHazard(robotLocation[0], robotLocation[1] - 1)

        if robotDirection == D.left and 0 <= robotLocation[0] - 1 :
            isHazard = map.find_unseenHazard(robotLocation[0] - 1, robotLocation[1])
        return isHazard

    # 객체가 초기화 될때 실행, 로봇의 위치를 저장한다. 로봇움직임 오작동 감지에 사용된다.
    def setRobotPosition(self, x, y):
       self.__currentX = x
       self.__currentY = y

    # SET ROBOT LOCATION 에서 저장된 값이 현재 로봇값과 다르다면, 원래 있어야하는 곳으로 로봇을 움직이고, 오류여부를 리턴한다.
    def compensateMove(self, map):
        robotLocation = map.getRobotLocation()
        rightLocation = (self.__currentX, self.__currentY)

        if self.sim.positioningSensor(rightLocation, robotLocation):
            map.moveRobot(rightLocation[0] - robotLocation[0], rightLocation[1] - robotLocation[1])

            self.checkTarget(map)
            return 1
        return 0

    # 로봇의 direction을 path로 맞추고 돌린 위치에서 위험검사를 한다. 만약 있다면 unseen hazard 를 seen hazard 로 바꾸고 함수를 리턴한다.
    # 위험지역이 없으면 sim의 moveForward로 직진 시킨다.
    # 저장된 CURRENTX, CURRENTY 의 값을 로봇이 한칸 움직인 위치로 하여 저장한다. 이 값들은 나중에 COMPENSATE MOVE 함수의 인자로 쓰인다.

    def followPath(self, map):
        print("start follow path: ", map.getRobotLocation())

        path = map.getRobotPath()
        direction = map.getRobotDirection()

        while path != direction:
            self.sim.turnRight(map)
            direction = map.getRobotDirection()

        if(self.detectHazard(map)):
            return

        self.sim.moveForward(map)
        self.checkTarget(map)

        if direction == D.up:
            self.__currentY = self.__currentY + 1
        elif direction == D.right:
            self.__currentX = self.__currentX + 1
        elif direction == D.down:
            self.__currentY = self.__currentY - 1
        elif direction == D.left:
            self.__currentX = self.__currentX - 1
