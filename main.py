#!/usr/bin/env python3

import cv2
import numpy as np

class LowVision(object):
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(1)
        self.zoom_factor = 1.0
        self.offset = 40
        self.image = None
        self.proc_image = None
        self.mode = ["normal", "high_contrast","show_black","change_to_yellow"]
        self.mode_index = 0
    def load_image(self):
        ret = False
        while not ret:
            ret, self.image = self.cap.read()
        if self.zoom_factor < 1.0:
            self.image = cv2.resize(self.image, None, fx=self.zoom_factor, fy=self.zoom_factor)  # type: ignore
        else:
            width = int(self.image.shape[1] * self.zoom_factor)
            height = int(self.image.shape[0] * self.zoom_factor)
            dim = (width, height)
            print(dim)
        
            # resize image
            resized = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)
            self.image = resized[(resized.shape[0]-1080)//2:(resized.shape[0]+1080)//2, (resized.shape[1]-1920)//2:(resized.shape[1]+1920)//2]

    def process_image(self):
        if self.image is None:
            return None
        if self.mode[self.mode_index] == "normal":
            self.proc_image = self.image
        elif self.mode[self.mode_index] == "high_contrast":
            contrast = 65
            shadow = 20
            highlight = 255
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow
            buf = cv2.addWeighted(self.image, alpha_b, self.image, 0, gamma_b)
            f = 131*(contrast + 127)/(127*(131-contrast))
            alpha_c = f
            gamma_c = 127*(1-f)
            self.proc_image = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
            # tmp = self.image
            # # tmp[0] = tmp[0] * 2.55
            # tmp[1] = tmp[1] * 2.55
            # self.proc_image = tmp
        elif self.mode[self.mode_index] == "show_black":
            # self.proc_image = cv2.Canny(self.image,100,200)
            contrast = 65
            shadow = 20
            highlight = 255
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow
            buf = cv2.addWeighted(self.image, alpha_b, self.image, 0, gamma_b)
            f = 131*(contrast + 127)/(127*(131-contrast))
            alpha_c = f
            gamma_c = 127*(1-f)
            tmp = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)   
            lower_black = np.array([0, 0, 0], dtype = "uint16")
            upper_black = np.array([80, 80, 80], dtype = "uint16")
            black_mask = cv2.inRange(tmp, lower_black, upper_black)
            tmp = cv2.cvtColor(black_mask, cv2.COLOR_GRAY2RGB)
            tmp[np.all(tmp == (255,255,255), axis=-1)] = (0,255,255)
            self.proc_image = tmp

        elif self.mode[self.mode_index] == "change_to_yellow":
            tmp = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            invert = cv2.bitwise_not(tmp)
            image = np.zeros_like(self.image)
            image[:,:,0] = invert
            image[:,:,1] = invert
            image[:,:,2] = invert
            alpha = 0.4
            beta = 1.0 - alpha
            yellow = np.zeros((tmp.shape[0], tmp.shape[1],3), dtype=np.uint8)
            yellow[:] = (0,255,255)
            final = cv2.addWeighted(image, alpha, yellow, beta, 0.0)
            self.proc_image = final

    def render_image(self):
        
        if self.proc_image is None:
            return None

        img_size_y = 1000
        img_size_x = 1000
        ori_x = 960
        ori_y = 540

        if self.zoom_factor < 1.0:
            top = (1080 - self.proc_image.shape[0])//2
            bottom = top
            left = (1920 - self.proc_image.shape[1])//2
            right = left
            self.proc_image = cv2.copyMakeBorder(self.proc_image, top, bottom, left, right, cv2.BORDER_CONSTANT, None, [0, 0, 0])

        image1 = self.proc_image[ori_y - (img_size_y//2):ori_y + (img_size_y//2),ori_x - (img_size_x//2):ori_x + (img_size_x//2)]
        image2 = self.proc_image[ori_y - (img_size_y//2):ori_y + (img_size_y//2), ori_x - (img_size_x//2) + self.offset:ori_x + (img_size_x//2) + self.offset]
        
        vr_image = cv2.hconcat([image1, image2])  # type: ignore
        vr_image = cv2.putText(
            img = vr_image,
            text = f"Zoom: {round(self.zoom_factor,2)}",
            org = (10, 30),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 1.0,
            color = (125, 246, 55),
            thickness = 2
        )
        vr_image = cv2.putText(
            img = vr_image,
            text = f"Mode: {self.mode[self.mode_index]}",
            org = (1000, 30),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 1.0,
            color = (125, 246, 55),
            thickness = 2
        )
        
        cv2.imshow("frame", vr_image)

        ## Find key
        # key = cv2.waitKey(0)
        # print(key)
        
        ## Key check
        key = cv2.waitKey(1)
        zoom_scale = 0.05
        if key == 119:
            self.zoom_factor += zoom_scale
        elif key == 115:
            self.zoom_factor -= zoom_scale
            if self.zoom_factor <= zoom_scale:
                self.zoom_factor = zoom_scale
        elif key == 114:
            self.zoom_factor = 1.0
        elif key == 97:
            self.offset -= 1
        elif key == 100:
            self.offset += 1
        elif key == 32:
            self.mode_index += 1
            self.mode_index = self.mode_index % len(self.mode)
        elif key == 113:
            exit()

    def main(self):
        while True:
            self.load_image()
            self.process_image()
            self.render_image()

if __name__ == "__main__":
    lowVision = LowVision()
    lowVision.main()