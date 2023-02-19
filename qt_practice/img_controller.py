from PyQt5 import QtCore 
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint
from opencv_engine import opencv_engine

from mouseEvent_library import mouseEvent_library

class editor_mouse_controller(object):    
    def __init__(self,img_controller):
        self.img_controller = img_controller

    def __set_mode(self,pen_property):
        self.editor_mode = pen_property.get('mode')
        if self.editor_mode:
            self.method = mouseEvent_library().method.get(self.editor_mode)(self.img_controller)

    def set_pen(self,pen_property): # pen_property = {imagelayer,editor_mode,color,penpixelsize} 
        self.__set_mode(pen_property)
        self.method.set_property(pen_property)
        self.set_editor_mouse_event()

    def set_editor_mouse_event(self):
        self.img_controller.label_img.mousePressEvent =  self.method.mousePressEvent
        self.img_controller.label_img.mouseReleaseEvent = self.method.mouseReleaseEvent
        self.img_controller.label_img.mouseMoveEvent = self.method.mouseMoveEvent

class label_img_controller(object): 
    def __init__(self,img_controller):
        self.img_controller = img_controller
    
    def set_zoom(self, value, step=35):
        self.qpixmap_height = self.init_height+step*value
        if self.img1_path or self.img2_path:
            self.update_img()

    def set_alpha(self, alpha1, alpha2):
        if alpha1: self.alpha1 = alpha1
        if alpha2: self.alpha2 = alpha2
        if self.origin_img1 or self.origin_img2:
            self.update_img()

class img_controller(object):
    def __init__(self, ui,
                img1_path='',img2_path='',
                alpha1=128,alpha2=128,
                origin_img1='',origin_img2='',
                init_height=500, init_width=500):
        self.ui = ui
        self.label_img = ui.imageArea_QLabel
        self.img1_path = img1_path
        self.img2_path = img2_path
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        self.origin_img1 = origin_img1
        self.origin_img2 = origin_img2
        self.init_height = init_height
        self.init_width = init_width
        self.editor_mouse_controller = editor_mouse_controller(self)

    def read_file_and_init(self):
        if self.img1_path:
            self.origin_img1 = opencv_engine.read_image(self.img1_path)
            self.origin_height, self.origin_width, self.origin_channel = self.origin_img1.shape
        if self.img2_path:
            self.origin_img2 = opencv_engine.read_image(self.img2_path)
            self.origin_height, self.origin_width, self.origin_channel = self.origin_img2.shape

        if self.img1_path and self.img2_path and (self.origin_img1.shape != self.origin_img2.shape):
            pass # raising error: The size of the two images does not match.

        self.qpixmap_height = max(self.origin_height,self.init_height)

    def set_path(self, img1_path, img2_path):
        if img1_path: self.img1_path = img1_path
        if img2_path: self.img2_path = img2_path
        self.read_file_and_init()
        self.update_img()


    def __update_img_height(self):
        self.qpixmap = self.qpixmap.scaledToHeight(self.qpixmap_height)

    def __update_label_img(self):
        height, width, channel = self.display_img.shape
        bytesPerline = channel * width
        self.qimg = QImage(self.display_img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        self.qpixmap = QPixmap.fromImage(self.qimg)
        self.__update_img_height()
        self.label_img.setPixmap(self.qpixmap)
        self.label_img.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

    def update_img(self):
        if self.img1_path and self.img2_path:
            self.display_img = opencv_engine.imblend(self.origin_img1,self.alpha1/255,self.origin_img2,self.alpha2/255,0.0)
        elif self.img1_path:
            self.display_img = self.origin_img1
        elif self.img2_path:
            self.display_img = self.origin_img2
        else:
            pass # raising error plz read image first
        self.__update_label_img()

    def trans_labelimage2img(self,point,labelimage_shape,img_shape):
        # give me label img point, i will help you to transform to origin cv image position
        return (point[0]/labelimage_shape[0]*img_shape[0],point[1]/labelimage_shape[1]*img_shape[1])

    def draw_line(self, img, point_begin, point_end, color, thickness):
        point_begin = self.trans_labelimage2img(point_begin,(self.qpixmap.width(),self.qpixmap.height()),(self.origin_width,self.origin_height))
        point_end = self.trans_labelimage2img(point_end,(self.qpixmap.width(),self.qpixmap.height()),(self.origin_width,self.origin_height))
        return opencv_engine.draw_line(img, point_begin,point_end,color = color,thickness = thickness)

    def draw_point(self, img, point, color, thickness):
        point = self.trans_labelimage2img(point,(self.qpixmap.width(),self.qpixmap.height()),(self.origin_width,self.origin_height))
        return opencv_engine.draw_point(img, point,color = color,thickness = thickness)

    def draw_bucket(self, img, point, color):
        point = self.trans_labelimage2img(point,(self.qpixmap.width(),self.qpixmap.height()),(self.origin_width,self.origin_height))
        return opencv_engine.floodfill(img, point, color = color)

    def set_zoom(self, value, step=35):
        self.qpixmap_height = self.init_height+step*value
        if self.img1_path or self.img2_path:
            self.update_img()

    def set_alpha(self, alpha1, alpha2):
        if alpha1: self.alpha1 = alpha1
        if alpha2: self.alpha2 = alpha2
        if self.img1_path or self.img2_path:
            self.update_img()

