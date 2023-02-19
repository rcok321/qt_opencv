import abc
from PyQt5.QtCore import Qt

class mouseEvent_library(object):
    def __init__(self):
        self.method = {'Freehand':Freehand,
                    'Line':Line,
                    'Fill':Fill}

class mouseEvent_interface(abc.ABC):
    def __init__(self,img_controller):
        self.drawing = False
        self.lastPoint = (0,0)
        self.img_controller = img_controller

        self.pen_property = {'image_layer':'',
                            'color':128,
                            'penPixelSize':1}
        self.__set_pen()

    def __set_img(self,image_layer):
        if image_layer == 'img1':
            self.img = self.img_controller.origin_img1
        elif image_layer == 'img2':
            self.img = self.img_controller.origin_img2
        else:
            pass
            
    def __set_color(self,color):
        if color:
            self.color = [color]*3

    def __set_penPixelSize(self,penPixelSize):
        if penPixelSize:
            self.penPixelSize = penPixelSize

    def __set_pen(self):
        self.__set_img(self.pen_property.get('image_layer',''))
        self.__set_color(self.pen_property.get('color',''))
        self.__set_penPixelSize(self.pen_property.get('penPixelSize',''))

    def set_property(self,pen_property):
        self.pen_property = pen_property
        self.__set_pen()

    @abc.abstractmethod
    def mousePressEvent(self):
        return NotImplemented

    @abc.abstractmethod
    def mouseMoveEvent(self):
        return NotImplemented

    @abc.abstractmethod
    def mouseReleaseEvent(self):
        return NotImplemented

class Freehand(mouseEvent_interface):
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = (event.pos().x(),event.pos().y())
            self.drawing = True
    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            currentPoint = (event.pos().x(),event.pos().y())
            self.image = self.img_controller.draw_line(self.img,self.lastPoint,currentPoint,self.color,self.penPixelSize)
            self.img_controller.update_img()
            self.lastPoint = currentPoint
    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

class Line(mouseEvent_interface):
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            if self.drawing:
                currentPoint = (event.pos().x(),event.pos().y())
                self.image = self.img_controller.draw_line(self.img,self.lastPoint,currentPoint,self.color,self.penPixelSize)
                self.img_controller.update_img()
                self.drawing = False
            else:
                self.drawing = True
                self.lastPoint = (event.pos().x(),event.pos().y())
    def mouseMoveEvent(self, event):
        pass
    def mouseReleaseEvent(self, event):
        pass

class Fill(mouseEvent_interface):
    def mousePressEvent(self, event):
        currentPoint = (event.pos().x(),event.pos().y())
        self.image = self.img_controller.draw_bucket(self.img,currentPoint,self.color)
        self.img_controller.update_img()
    def mouseMoveEvent(self, event):
        pass
    def mouseReleaseEvent(self, event):
        pass
