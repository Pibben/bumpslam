import math
import numpy as np
import cv2


def draw_box(box, canvas, color, thickness):
    box2 = cv2.boxPoints(box)
    box3 = np.int0(box2)
    cv2.drawContours(canvas, [box3], 0, color, thickness)


class Agent:
    def __init__(self, x, y, angle):
        self.position = np.array([x, y])
        self.heading = angle
        self.width = 25
        self.height = 40
        self.speed = 15

    def get_box(self):
        return self.position, (self.height, self.width), np.degrees(self.heading)

    def draw_box(self, canvas):
        box = self.get_box()
        draw_box(box, canvas, (0, 191, 255), 1)

    def draw_point(self, canvas):
        pass

    def move(self):
        self.position += self.speed * np.array([math.cos(self.heading), math.sin(self.heading)])

    def rotate(self, angle_offset):
        self.heading = (self.heading + angle_offset) % (2.0 * math.pi)

    def reverse(self):
        self.speed = -self.speed

    def set_speed(self, speed):
        self.speed = speed


class Environment:
    def __init__(self):
        self.width = 768
        self.height = 512

        self.cells = np.zeros((self.height, self.width))
        cv2.rectangle(self.cells, (20, 20), (self.width - 20, self.height - 20), 1.0)

    def draw(self, canvas):
        color_img = cv2.cvtColor((255.0 * self.cells).astype(np.uint8), cv2.COLOR_GRAY2RGB)
        canvas[:] = np.maximum(color_img, canvas)

    def get(self, box):
        points = cv2.boxPoints(box)
        bb = cv2.boundingRect(points)
        roi = self.cells[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]
        mask = np.full_like(roi, 0)
        adjusted_box = ((box[0][0] - bb[0], box[0][1] - bb[1]), box[1], box[2])

        draw_box(adjusted_box, mask, 1.0, -1)

        return np.sum(np.multiply(roi, mask))


class Estimation:
    def __init__(self):
        self.width = 768
        self.height = 512

        self.cells = np.zeros((self.height, self.width))

    def draw(self, canvas):
        color_img = cv2.cvtColor((255.0 * self.cells).astype(np.uint8), cv2.COLOR_GRAY2RGB)
        canvas[:] = np.maximum(color_img, canvas)

    def get(self, box):
        points = cv2.boxPoints(box)
        bb = cv2.boundingRect(points)
        roi = self.cells[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]
        mask = np.full_like(roi, 0)
        adjusted_box = ((box[0][0] - bb[0], box[0][1] - bb[1]), box[1], box[2])

        draw_box(adjusted_box, mask, 1.0, -1)

        return np.sum(np.multiply(roi, mask))

    def set(self, box, value):
        pass

    def increase(self, box, amount):
        pass

    def decrease(self, box, amount):
        pass


def main():
    img = np.ones((512, 768, 3), np.uint8)

    e = Environment()
    a = Agent(100.0, 100.0, np.radians(135))

    for i in range(200):
        img.fill(0)
        e.draw(img)
        a.move()
        a.draw_box(img)

        cv2.imshow('Draw01', img)
        cv2.waitKey(100)

        if e.get(a.get_box()) > 0:
            a.reverse()
            for r in range(int(45.0 / abs(a.speed))):
                a.move()
            a.rotate(np.random.uniform(np.radians(135), np.radians(135+90)))
            a.reverse()


if __name__ == "__main__":
    main()
