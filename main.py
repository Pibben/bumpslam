import math
import numpy as np
import cv2


class Agent:
    def __init__(self, x, y, angle):
        self.position = np.array([x,y])
        self.heading = angle
        self.width = 25
        self.height = 40
        self.speed = np.zeros((1, 2))

    def draw_box(self, canvas):
        box = (self.position, (self.width, self.height), self.heading)
        box2 = cv2.boxPoints(box)
        box3 = np.int0(box2)
        cv2.drawContours(canvas, [box3], 0, (0, 191, 255), 1)

    def draw_point(self, canvas):
        pass

    def move(self):
        self.position += self.speed

    def rotate(self, angle_offset):
        self.heading = (self.heading + angle_offset) % math.pi


class Environment:
    def __init__(self):
        self.width = 768
        self.height = 512

        self.cells = np.zeros((self.width, self.height))

    def draw(self, canvas):
        pass

    def get(self, box):
        pass

    def set(self, box, value):
        pass

    def increase(self, box, amount):
        pass

    def decrease(self, box, amount):
        pass


def main():
    img = np.zeros((512, 768, 3), np.int8)

    a = Agent(100, 100, 0)

    a.draw_box(img)

    cv2.imshow('Draw01', img)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
