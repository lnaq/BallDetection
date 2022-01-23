import numpy as np
import cv2
from mss import mss
import time
from imutils import resize

class DetectBall:   # Aim Lab SETTINGS - PARAM2 - 23 OR LOWER (EXPERIMENT MORE) MAXRADIOUS 45 - 50 (NOT SURE)

    def __init__(self,
                 monitor = {'top':int(1080/4),'left':int(1920/4),
                            'width':int(1920/2),'height':int(1080/2)},
                 minDist=100,param1=30,param2=45,minRadius=10,maxRadius=115):

        self.monitor = monitor

        self.minDist = minDist
        self.param1 = param1
        self.param2 = param2
        self.minRadius = minRadius
        self.maxRadius = maxRadius

        self.color = (123, 204, 15)
        self.line_thickness = 3

        self.end_point = (int(round(self.monitor['width'] / 2)),
                           int(round(self.monitor['height'] / 2)))


    def draw_on_screen(self, img: str, blurred:str) -> None:
        ''' The following function draws circles around objects'''
        circles = cv2.HoughCircles(blurred,cv2.HOUGH_GRADIENT,1,self.minDist,
                                   param1=self.param1,param2=self.param2,
                                   minRadius=self.minRadius,maxRadius=self.maxRadius)
        # Line thickness
        thickness = 3

        # Draw
        if circles is not None:
            circles = np.uint16(np.around(circles))

            for i in circles[0,:]:
                cv2.circle(img, (i[0], i[1]), i[2], self.color, 2)

                # Draw Lines
                cv2.line(img, (i[0], i[1]), self.end_point,
                         self.color, self.line_thickness)


    @staticmethod
    def convert_img(img: str) -> list: # The list is a bunch of lists of numbers
        '''
            converts an image into gray, and the it blurs
            in order to find objects
        '''
        # Convert img into grey
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Blur Img Out
        blurred = cv2.medianBlur(gray, 25) #cv2.bilateralFilter(gray,10,50,50)

        return (gray, blurred)

    def get_image(self) -> None:
        ''' Records the screen by taking a bunch of screenshots '''
        sct = mss()
        while True:
            last_time = time.time()
            # Get img
            sct_img = sct.grab(self.monitor)
            # Read igm
            img = np.array(sct_img)
            # Convert img
            gray, blur_img = DetectBall.convert_img(img)
            # Draw Circle
            self.draw_on_screen(img, blur_img)
            # Display Text On Img
            cv2.putText(img, f'fps: {1 / (time.time() - last_time)}'[0:9],
		               (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.0, self.color, 2)

            # Show Final Card
            cv2.imshow('screen', resize(img, width=1000))

            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                cv2.destroyAllWindows()
                break

def main():
    det = DetectBall()
    det.get_image()

if __name__ == '__main__':
    main()
