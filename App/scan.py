from mouse import get_position
from cv2 import cvtColor, threshold, COLOR_RGB2GRAY
from numpy import array
from hashlib import md5
from PIL import ImageGrab


class Scan:
    def __init__(self):
        """
        Scan that taking screenshot every time when MainFrame is updating and then set item_hash
        """
        try:
            screen_image = ImageGrab.grab()
            self.screen_image = cvtColor(array(screen_image), COLOR_RGB2GRAY)
            self.mouse_position_x, self.mouse_position_y = get_position()
            self.item_hash = None
            self.start_shade = 1
            self.start_position_x, self.start_position_y = (0, 0)
            self.item_image = None

            screen_width, screen_height = (1920, 1080)

            if self.mouse_position_x < (screen_width * 0.98) and self.mouse_position_y > (screen_height * 0.02):
                self.find_start_shade()

            if not self.start_shade:
                self.find_item_image()
                self.hash_item_image()

        except OSError as error:
            print(error)

    def find_start_shade(self):
        """
        Find shade that will be remembered like start position
        """
        self.start_position_x, self.start_position_y = self.mouse_position_x + 11, self.mouse_position_y - 11
        self.start_shade = self.screen_image[self.start_position_y, self.start_position_x]

    def find_right_corner(self):
        """
        Will search right border that equal to 87
        """
        for pix in range(1, 400):
            try:
                shade = self.screen_image[self.start_position_y, self.start_position_x + pix]
                if shade == 0:
                    pass

                elif shade == 87:
                    return self.start_position_x + pix

                else:
                    break

            except IndexError as error:
                print(error)
                print(self.start_position_y, self.start_position_x, pix)

    def find_top_corner(self, left_corner_position_x):
        """
        Will search top border that equal to 87
        """
        for pix in range(1, 100):
            shade = self.screen_image[self.start_position_y - pix, left_corner_position_x]

            if shade == 0:
                pass

            elif shade == 87:
                return self.start_position_y - pix + 1

            else:
                break

    def find_item_image(self):
        """
        Method search right_corner and top_corner that needed for finding item_image
        """
        right_corner_position_x = self.find_right_corner()
        if right_corner_position_x:
            top_corner_position_y = self.find_top_corner(self.start_position_x)

            if top_corner_position_y:
                width = right_corner_position_x - self.start_position_x
                height = self.start_position_y - top_corner_position_y
                crop_screen_image = self.screen_image[top_corner_position_y:top_corner_position_y + height,
                                    self.start_position_x:self.start_position_x + width]
                ret, self.item_image = threshold(crop_screen_image, 0, 255, 0)

    def hash_item_image(self):
        """
        Set item_hash for item_image
        """
        if self.item_image is not None:
            item_bytes = md5(self.item_image.tobytes())
            self.item_hash = item_bytes.hexdigest()
