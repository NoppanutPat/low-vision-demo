#!/usr/bin/env python3

import cv2
import numpy as np

class LowVisionDemo(object):
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)
        self.image = None
        self.zoom_factor = 1.5
        self.offset = 40
    
    def update(self) -> None:
        _, self.image = self.cap.read()
        self.image = cv2.resize(self.image, None, fx=self.zoom_factor, fy=self.zoom_factor)  # type: ignore
    
    def show_image(self) -> None:
        if self.image is None:
            return None
    
        # print(self.image.shape)
        img_size_y = 1000
        img_size_x = 1000
        ori_x = 960
        ori_y = 540

        print([ori_y - (img_size_y//2),ori_y + (img_size_y//2),ori_x - (img_size_x//2),ori_x + (img_size_x//2)])
        print([ori_y - (img_size_y//2) + self.offset,ori_y + (img_size_y//2), ori_x - (img_size_x//2) + self.offset,ori_x + (img_size_x//2) + self.offset])

        image1 = self.image[ori_y - (img_size_y//2):ori_y + (img_size_y//2),ori_x - (img_size_x//2):ori_x + (img_size_x//2)]
        image2 = self.image[ori_y - (img_size_y//2):ori_y + (img_size_y//2), ori_x - (img_size_x//2) + self.offset:ori_x + (img_size_x//2) + self.offset]
        print(f"image 1 shape: {image1.shape}")
        print(f"image 2 shape: {image2.shape}")
        vr_image = cv2.hconcat([image1, image2])  # type: ignore
        # print(vr_image.shape)
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
            text = f"Mode: test",
            org = (1900, 30),
            fontFace = cv2.FONT_HERSHEY_DUPLEX,
            fontScale = 1.0,
            color = (125, 246, 55),
            thickness = 2
        )
        cv2.imshow("frame", vr_image)
        key = cv2.waitKey(1)

        # cv2.imshow("frame", image2)
        ### For debugging 
        # key = cv2.waitKey(0)
        # print(key)

        if key == 119:
            self.zoom_factor += 0.1
        elif key == 115:
            self.zoom_factor -= 0.1
            if self.zoom_factor < 1.0:
                self.zoom_factor = 1.0
        elif key == 114:
            self.zoom_factor = 1.0
        elif key == 97:
            self.offset -= 1
        elif key == 100:
            self.offset += 1

    def main(self) -> None:
        while True:
            self.update()
            self.show_image()


if __name__ == "__main__":
    demo = LowVisionDemo()
    demo.main()

