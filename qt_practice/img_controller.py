from PyQt5 import QtCore 
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint
from opencv_engine import opencv_engine

class img_controller(object):
    def __init__(self, img1_path='',img2_path='', imagelayer='', label_img='', init_height=500, init_width=500, alpha=128,color=128,penpixelsize=5,editor_mode=''):
        self.img1_path = img1_path
        self.img2_path = img2_path
        self.imagelayer = imagelayer #img1 or img2
        self.editor_mode = editor_mode
        self.color = color
        self.penpixelsize = penpixelsize
        self.label_img = label_img
        self.line_counter = 0
        self.init_height = init_height
        self.init_width = init_width
        self.alpha = alpha
        self.read_file_and_init()
        self.drawing = False
        self.lastPoint = QPoint()
        if self.img1_path or self.img2_path:
            self.__update_img()

    def read_file_and_init(self):
        if self.img1_path:
            self.origin_img1 = opencv_engine.read_image(self.img1_path)
            self.origin_height, self.origin_width, self.origin_channel = self.origin_img1.shape

        if self.img2_path:
            self.origin_img2 = opencv_engine.read_image(self.img2_path)
            self.origin_height, self.origin_width, self.origin_channel = self.origin_img2.shape

        if self.img1_path and self.img2_path:
            if self.origin_img1.shape != self.origin_img2.shape:
                pass # raise error
            self.qpixmap_height = max(self.origin_height,self.init_height)
            self.__update_img()
        elif self.img1_path or self.img2_path:
            self.qpixmap_height = max(self.origin_height,self.init_height)
            self.__update_img()
        else:
            pass

    def set_path(self, img1_path, img2_path):
        if img1_path: 
            self.img1_path = img1_path
        if img2_path: 
            self.img2_path = img2_path
        self.read_file_and_init()
        self.__update_img()

    def __update_img_height(self):
        self.qpixmap = self.qpixmap.scaledToHeight(self.qpixmap_height)

    def __update_img(self):
        if self.img1_path and self.img2_path:
            alpha = self.alpha/255
            self.display_img = opencv_engine.imblend(self.origin_img1,(1-alpha),self.origin_img2,alpha,0.0)
            height, width, channel = self.display_img.shape
            bytesPerline = channel * width
            self.qimg = QImage(self.display_img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        elif self.img1_path:
            self.display_img = opencv_engine.bgr2rgb(self.origin_img1)
            self.display_img = opencv_engine.rgb2rgba(self.display_img)
            self.display_img[:,:,3] = 255-self.alpha
            height, width, channel = self.display_img.shape
            bytesPerline = channel * width
            self.qimg = QImage(self.display_img, width, height, bytesPerline, QImage.Format_RGBA8888)
        elif self.img2_path:
            self.display_img = opencv_engine.bgr2rgb(self.origin_img2)
            self.display_img = opencv_engine.rgb2rgba(self.display_img)
            self.display_img[:,:,3] = self.alpha
            height, width, channel = self.display_img.shape
            bytesPerline = channel * width
            self.qimg = QImage(self.display_img, width, height, bytesPerline, QImage.Format_RGBA8888)
        else:
            pass # raising error
        self.qpixmap = QPixmap.fromImage(self.qimg)
        self.__update_img_height()
        self.label_img.setPixmap(self.qpixmap)
        self.label_img.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_img.mousePressEvent = self.mousePressEvent
        self.label_img.mouseMoveEvent = self.mouseMoveEvent
        self.label_img.mouseReleaseEvent = self.mouseReleaseEvent

    def set_zoom(self, value, step=35):
        self.qpixmap_height = self.init_height+step*value
        if self.img1_path or self.img2_path:
            self.__update_img()

    def set_alpha(self, value):
        self.alpha = value
        if self.img1_path or self.img2_path:
            self.__update_img()

    def set_imagelayer(self, value):
        self.imagelayer = value #img1 or img2

    def set_editor_mode(self, value):
        self.editor_mode = value # Freehand, Line, Fill

    def set_color(self,layer, value):
        if self.imagelayer == layer:
            self.color = value

    def set_penpixelsize(self,layer, value):
        if self.imagelayer == layer:
            self.penpixelsize = value

    def get_clicked_position(self, event):
        x = event.pos().x()
        y = event.pos().y()
        norm_x = x/self.qpixmap.width()
        norm_y = y/self.qpixmap.height()
        self.draw_point((norm_x, norm_y))

    def draw_point(self, point):
        # give me normalized point, i will help you to transform to origin cv image position
        cv_image_x = point[0]*self.origin_width
        cv_image_y = point[1]*self.origin_height
        if self.imagelayer == 'img1':
            self.origin_img1 = opencv_engine.draw_point(self.origin_img1, (cv_image_x, cv_image_y),color = (self.color,self.color,self.color),thickness = self.penpixelsize)
        elif self.imagelayer == 'img2':
            self.origin_img2 = opencv_engine.draw_point(self.origin_img2, (cv_image_x, cv_image_y),color = (self.color,self.color,self.color),thickness = self.penpixelsize)
        else:
            pass # raising error
        self.__update_img()

    def draw_line(self, point_begin, point_end):
        # give me normalized point, i will help you to transform to origin cv image position
        cv_image_x_begin = point_begin[0]*self.origin_width
        cv_image_y_begin = point_begin[1]*self.origin_height
        cv_image_x_end = point_end[0]*self.origin_width
        cv_image_y_end = point_end[1]*self.origin_height
        if self.imagelayer == 'img1':
            self.origin_img1 = opencv_engine.draw_line(self.origin_img1, (cv_image_x_begin, cv_image_y_begin),(cv_image_x_end,cv_image_y_end),color = (self.color,self.color,self.color),thickness = self.penpixelsize)
        elif self.imagelayer == 'img2':
            self.origin_img2 = opencv_engine.draw_line(self.origin_img2, (cv_image_x_begin, cv_image_y_begin),(cv_image_x_end,cv_image_y_end),color = (self.color,self.color,self.color),thickness = self.penpixelsize)
        else:
            pass # raising error
        self.__update_img()

# mouse control should be OOP
# class mouse_controller(object):
#     def __init__(self,)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            if self.editor_mode == 'Freehand':
                next
            elif (self.line_counter == 1) and (self.editor_mode == 'Line'):
                x = event.pos().x()
                y = event.pos().y()
                norm_lastPoint_x = self.lastPoint[0]/self.qpixmap.width()
                norm_lastPoint_y = self.lastPoint[1]/self.qpixmap.height()
                norm_x = x/self.qpixmap.width()
                norm_y = y/self.qpixmap.height()
                self.draw_line((norm_lastPoint_x,norm_lastPoint_y),(norm_x, norm_y))
                self.line_counter = 0
            elif (self.line_counter == 0) and (self.editor_mode == 'Line'):
                self.line_counter = 1
            else:
                pass

            self.lastPoint = (event.pos().x(),event.pos().y())

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing and (self.editor_mode == 'Freehand'):
            # painter = QPainter(self.image)
            # painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            # painter.drawLine(self.lastPoint, event.pos())
            x = event.pos().x()
            y = event.pos().y()
            norm_lastPoint_x = self.lastPoint[0]/self.qpixmap.width()
            norm_lastPoint_y = self.lastPoint[1]/self.qpixmap.height()
            norm_x = x/self.qpixmap.width()
            norm_y = y/self.qpixmap.height()
            self.draw_line((norm_lastPoint_x,norm_lastPoint_y),(norm_x, norm_y))
            self.lastPoint = (event.pos().x(),event.pos().y())

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False
