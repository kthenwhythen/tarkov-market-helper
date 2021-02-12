import pyautogui
import cv2
import numpy as np
import hashlib


class Scan:
    def __init__(self):
        screen_image = pyautogui.screenshot()
        self.screen_image_cv = cv2.cvtColor(np.array(screen_image), cv2.COLOR_RGB2GRAY)
        self.mouse_position_x, self.mouse_position_y = pyautogui.position()
        self.item_hash = None
        self.start_shade = 1
        self.start_position_x, self.start_position_y = (0, 0)
        self.item_image = None

        screen_width, screen_height = pyautogui.size()

        if self.mouse_position_x < (screen_width * 0.98) and self.mouse_position_y > (screen_height * 0.02):
            self.find_start_shade()

        if not self.start_shade:
            self.find_item_image()
            self.hash_item_image()

            # Temp
            # cv2.imwrite("item_image.png", self.item_image)
            # Temp
            # cv2.imwrite("screen_image.png", self.screen_image_cv)

    def find_start_shade(self):
        self.start_position_x, self.start_position_y = self.mouse_position_x + 11, self.mouse_position_y - 11
        self.start_shade = self.screen_image_cv[self.start_position_y, self.start_position_x]

    def find_right_corner(self):
        for pix in range(1, 400):
            shade = self.screen_image_cv[self.start_position_y, self.start_position_x + pix]
            if shade == 0:
                pass
            elif shade == 87:
                return self.start_position_x + pix
            else:
                break

    def find_left_corner(self):
        for pix in range(1, 400):
            shade = self.screen_image_cv[self.start_position_y, self.start_position_x - pix]
            if shade == 0:
                pass
            elif shade == 87:
                return self.start_position_x - pix + 1
            else:
                break

    def find_top_corner(self, left_corner_position_x):
        for pix in range(1, 100):
            shade = self.screen_image_cv[self.start_position_y - pix, left_corner_position_x]
            if shade == 0:
                pass
            elif shade == 87:
                return self.start_position_y - pix + 1
            else:
                break

    def find_item_image(self):
        right_corner_position_x = self.find_right_corner()
        left_corner_position_x = self.find_left_corner()
        if right_corner_position_x and left_corner_position_x:
            top_corner_position_y = self.find_top_corner(left_corner_position_x)
            if top_corner_position_y:

                width = right_corner_position_x - left_corner_position_x
                height = self.start_position_y - top_corner_position_y

                crop_screen_image_cv = self.screen_image_cv[top_corner_position_y:top_corner_position_y + height,
                                       left_corner_position_x:left_corner_position_x + width]

                ret, self.item_image = cv2.threshold(crop_screen_image_cv, 0, 255, 0)

    def hash_item_image(self):
        if self.item_image is not None:
            item_bytes = hashlib.md5(self.item_image.tobytes())
            self.item_hash = item_bytes.hexdigest()
