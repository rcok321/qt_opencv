import cv2

class opencv_engine(object):

    @staticmethod
    def point_float_to_int(point):
        return (int(point[0]), int(point[1]))

    @staticmethod
    def rgb2rgba(rgb_data):
        return cv2.cvtColor(rgb_data, cv2.COLOR_RGB2RGBA)

    @staticmethod
    def bgr2rgb(rgb_data):
        return cv2.cvtColor(rgb_data,cv2.COLOR_BGR2RGB)

    @staticmethod
    def imblend(img1,alpha,img2,beta,gamma):
        return cv2.addWeighted(img1, alpha, img2, beta, gamma)

    @staticmethod
    def read_image(file_path):
        return cv2.imread(file_path)

    @staticmethod
    def draw_point(img, point=(0, 0), color = (128, 128, 128),point_size = 1,thickness = 4): # red
        point = opencv_engine.point_float_to_int(point)
        return cv2.circle(img, point, point_size, color, thickness)

    @staticmethod
    def draw_line(img, point_begin=(0, 0),point_end=(0, 0), color = (128, 128, 128),point_size = 1,thickness = 4): # red
        point_begin = opencv_engine.point_float_to_int(point_begin)
        point_end = opencv_engine.point_float_to_int(point_end)
        return cv2.line(img, point_begin, point_end, color, thickness)