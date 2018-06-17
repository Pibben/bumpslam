import math
import numpy as np
import cv2


def draw_box(box, canvas, color, thickness):
    box2 = cv2.boxPoints(box)
    box3 = np.int0(box2)
    cv2.drawContours(canvas, [box3], 0, color, thickness)


def calc_roi_and_mask(points, img):
    bb = cv2.boundingRect(points)
    roi = img[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]]
    mask = np.full_like(roi, 0)

    adjusted_box = points - (bb[0], bb[1])

    cv2.drawContours(mask, [np.int0(adjusted_box)], 0, 1.0, -1)

    return roi, mask


class Agent:
    def __init__(self, x, y, angle):
        self.position = np.array([x, y])
        self.heading = angle
        self.width = 25
        self.height = 40
        self.speed = 5

    def get_box(self):
        return self.position, (self.height, self.width), np.degrees(self.heading)

    def get_front_corners(self):
        points = cv2.boxPoints(self.get_box())
        return points[2:]

    def draw_box(self, canvas):
        box = self.get_box()
        draw_box(box, canvas, (0, 191, 255), 1)
        points = self.get_front_corners()

        cv2.circle(canvas, tuple(points[0]), 5, (0, 0, 255), -1)
        cv2.circle(canvas, tuple(points[1]), 5, (0, 0, 255), -1)

    def draw_point(self, canvas):
        cv2.circle(canvas, tuple(np.int0(self.position)), 2, (255, 255, 255), -1)

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
        cv2.circle(self.cells, (150, 250), 50, 1.0)

    def draw(self, canvas):
        color_img = cv2.cvtColor((255.0 * self.cells).astype(np.uint8), cv2.COLOR_GRAY2RGB)
        canvas[:] = np.maximum(color_img, canvas)

    def get(self, points):
        roi, mask = calc_roi_and_mask(points, self.cells)

        return np.sum(np.multiply(roi, mask))


class Estimation:
    def __init__(self):
        self.width = 768
        self.height = 512

        self.cells = 0.5*np.ones((self.height, self.width))

    def draw(self, canvas):
        color_img = cv2.cvtColor((255.0 * self.cells).astype(np.uint8), cv2.COLOR_GRAY2RGB)
        canvas[:] = np.maximum(color_img, canvas)

    def get(self, points):
        roi, mask = calc_roi_and_mask(points, self.cells)

        return np.sum(np.multiply(roi, mask))

    def set(self, box, value):
        pass

    def increase(self, box, amount):
        roi, mask = calc_roi_and_mask(box, self.cells)

        roi += mask * amount
        roi[:] = np.clip(roi, 0.0, 1.0)

    def decrease(self, box, amount):
        roi, mask = calc_roi_and_mask(box, self.cells)

        roi -= mask * amount
        roi[:] = np.clip(roi, 0.0, 1.0)


def main():
    img = np.ones((512, 768, 3), np.uint8)

    e = Environment()
    ee = Estimation()

    a_s = [Agent(768 / 2, 512 / 2, np.random.uniform(0, 2*np.pi)) for _ in range(1000)]

    while True:
        img.fill(0)

        for a in a_s:
            last_corners = a.get_front_corners()
            a.move()
            new_corners = a.get_front_corners()

            contour = np.concatenate((last_corners, new_corners[::-1]))

            if e.get(contour) > 0:
                ee.increase(contour, 0.02)
                a.reverse()
                for r in range(int(45.0 / abs(a.speed))):
                    a.move()
                a.rotate(np.random.uniform(np.radians(135), np.radians(135+90)))
                a.reverse()
            else:
                ee.decrease(contour, 0.02)

            a.draw_point(img)
        ee.draw(img)

        #e.draw(img)

        cv2.imshow('Draw01', img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
