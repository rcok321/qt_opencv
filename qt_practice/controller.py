# -*- coding: utf-8 -*-

from PyQt5 import QtCore 
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from UI import Ui_MainWindow
from img_controller import img_controller

class MainWindow_controller(QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        self.img_controller = img_controller(label_img=self.ui.imageArea_QLabel)
        self.ui.loadImage1_pushButton.clicked.connect(self.loadImage1) 
        self.ui.loadImage2_pushButton.clicked.connect(self.loadImage2) 
        self.ui.zoom_slider.valueChanged.connect(self.get_zoomSlider_value_and_zoom)
        self.ui.imageAlpha_slider.valueChanged.connect(self.get_alphaSlider_value)

        self.ui.image1EditorFreehand_pushButton.clicked.connect(self.image1EditorFreehand_pushButton_callback) 
        self.ui.image1EditorLine_pushButton.clicked.connect(self.image1EditorLine_pushButton_callback) 
        # self.ui.image1EditorFill_pushButton.clicked.connect(self.image1EditorFill_pushButton_callback) 
        self.ui.image1EditorFill_pushButton.setEnabled(False)

        self.ui.image2EditorFreehand_pushButton.clicked.connect(self.image2EditorFreehand_pushButton_callback) 
        self.ui.image2EditorLine_pushButton.clicked.connect(self.image2EditorLine_pushButton_callback) 
        # self.ui.image2EditorFill_pushButton.clicked.connect(self.image2EditorFill_pushButton_callback) 
        self.ui.image2EditorFill_pushButton.setEnabled(False)

        self.ui.image1EditorColor_lineEdit.textEdited.connect(self.image1EditorColor_lineEdit_callback) 
        self.ui.image1EditorPenPixelSize_lineEdit.textEdited.connect(self.image1EditorPenPixelSize_lineEdit_callback) 

        self.ui.image2EditorColor_lineEdit.textEdited.connect(self.image2EditorColor_lineEdit_callback) 
        self.ui.image2EditorPenPixelSize_lineEdit.textEdited.connect(self.image2EditorPenPixelSize_lineEdit_callback) 
        
    def loadImage1(self):
        filename = self.open_file()
        if filename:
            self.init_new_picture(filename,'')
        else:
            self.open_file_error()            

    def loadImage2(self):
        filename = self.open_file()
        if filename:
            self.init_new_picture('',filename)
        else:
            self.open_file_error()            

    def open_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.xpm *.jpg *.bmp *.gif *.pbm *.pgm *.ppm *.xbm *.xpm);;All Files (*)", options=options)
        return filename

    def open_file_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("讀取錯誤...")
        msg.setWindowTitle("未成功讀取影像...")
        msg.setIcon(QMessageBox.Information)

    def get_zoomSlider_value_and_zoom(self):
        self.img_controller.set_zoom(self.ui.zoom_slider.value())
    
    def get_alphaSlider_value(self):
        imageAlpha = self.ui.imageAlpha_slider.value()
        self.img_controller.set_alpha(imageAlpha)

    def init_new_picture(self, filename1, filename2):
        self.ui.zoom_slider.setProperty("value", 0)
        self.img_controller.set_path(filename1,filename2)

    def image1EditorFreehand_pushButton_callback(self):
        self.all_editor_button_enable()
        self.ui.image1EditorFreehand_pushButton.setEnabled(False)
        self.set_pen('img1','Freehand',int(self.ui.image1EditorColor_lineEdit.text()),int(self.ui.image1EditorPenPixelSize_lineEdit.text()))
    def image1EditorLine_pushButton_callback(self):
        self.all_editor_button_enable()
        self.ui.image1EditorLine_pushButton.setEnabled(False)
        self.set_pen('img1','Line',int(self.ui.image1EditorColor_lineEdit.text()),int(self.ui.image1EditorPenPixelSize_lineEdit.text()))
    def image1EditorFill_pushButton_callback(self):
        self.all_editor_button_enable()
        self.ui.image1EditorFill_pushButton.setEnabled(False)
        self.set_pen('img1','Fill',int(self.ui.image1EditorColor_lineEdit.text()),int(self.ui.image1EditorPenPixelSize_lineEdit.text()))

    def image2EditorFreehand_pushButton_callback(self):
        self.all_editor_button_enable()
        self.ui.image2EditorFreehand_pushButton.setEnabled(False)
        self.set_pen('img2','Freehand',int(self.ui.image2EditorColor_lineEdit.text()),int(self.ui.image2EditorPenPixelSize_lineEdit.text()))

    def image2EditorLine_pushButton_callback(self):
        self.all_editor_button_enable()
        self.ui.image2EditorLine_pushButton.setEnabled(False)
        self.set_pen('img2','Line',int(self.ui.image2EditorColor_lineEdit.text()),int(self.ui.image2EditorPenPixelSize_lineEdit.text()))

    def image2EditorFill_pushButton_callback(self):
        self.all_editor_button_enable()
        self.ui.image2EditorFill_pushButton.setEnabled(False)
        self.set_pen('img2','Fill',int(self.ui.image2EditorColor_lineEdit.text()),int(self.ui.image2EditorPenPixelSize_lineEdit.text()))

    def image1EditorColor_lineEdit_callback(self):
        self.img_controller.set_color('img1',int(self.ui.image1EditorColor_lineEdit.text()))

    def image1EditorPenPixelSize_lineEdit_callback(self):
        self.img_controller.set_penpixelsize('img1',int(self.ui.image1EditorPenPixelSize_lineEdit.text()))

    def image2EditorColor_lineEdit_callback(self):
        self.img_controller.set_color('img2',int(self.ui.image1EditorColor_lineEdit.text()))

    def image2EditorPenPixelSize_lineEdit_callback(self):
        self.img_controller.set_penpixelsize('img2',int(self.ui.image2EditorPenPixelSize_lineEdit.text()))

    def all_editor_button_enable(self):
        self.ui.image1EditorFreehand_pushButton.setEnabled(True)
        self.ui.image1EditorLine_pushButton.setEnabled(True)
        # self.ui.image1EditorFill_pushButton.setEnabled(True)
        self.ui.image2EditorFreehand_pushButton.setEnabled(True)
        self.ui.image2EditorLine_pushButton.setEnabled(True)
        # self.ui.image2EditorFill_pushButton.setEnabled(True)

    def set_pen(self,layer,mode,color,penpixelsize):
        self.img_controller.set_imagelayer(layer)
        self.img_controller.set_editor_mode(mode)
        self.img_controller.set_color(layer,color)
        self.img_controller.set_penpixelsize(layer,penpixelsize)