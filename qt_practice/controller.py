# -*- coding: utf-8 -*-

from PyQt5 import QtCore 
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QButtonGroup

from UI import Ui_MainWindow
from img_controller import img_controller

class MainWindow_controller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        self.current_imagelayer = ''

    def setup_control(self):
        self.img_controller = img_controller(self.ui)
        self.ui.loadImage1_pushButton.clicked.connect(self.loadImage1) 
        self.ui.loadImage2_pushButton.clicked.connect(self.loadImage2) 

        # display_controller
        self.ui.zoom_slider.valueChanged.connect(self.get_zoomSlider_value_and_zoom)
        self.ui.image1Alpha_slider.valueChanged.connect(self.get_alpha1Slider_value)
        self.ui.image2Alpha_slider.valueChanged.connect(self.get_alpha2Slider_value)

        # imgEditor_controller
        self.ui.image1EditorFreehand_pushButton.clicked.connect(self.image1EditorFreehand_pushButton_callback) 
        self.ui.image1EditorLine_pushButton.clicked.connect(self.image1EditorLine_pushButton_callback) 
        self.ui.image1EditorFill_pushButton.clicked.connect(self.image1EditorFill_pushButton_callback) 
        self.ui.image1EditorColor_lineEdit.textEdited.connect(self.image1EditorColor_lineEdit_callback) 
        self.ui.image1EditorPenPixelSize_lineEdit.textEdited.connect(self.image1EditorPenPixelSize_lineEdit_callback) 

        self.ui.image2EditorFreehand_pushButton.clicked.connect(self.image2EditorFreehand_pushButton_callback) 
        self.ui.image2EditorLine_pushButton.clicked.connect(self.image2EditorLine_pushButton_callback) 
        self.ui.image2EditorFill_pushButton.clicked.connect(self.image2EditorFill_pushButton_callback) 
        self.ui.image2EditorColor_lineEdit.textEdited.connect(self.image2EditorColor_lineEdit_callback) 
        self.ui.image2EditorPenPixelSize_lineEdit.textEdited.connect(self.image2EditorPenPixelSize_lineEdit_callback) 

    def open_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.xpm *.jpg *.bmp *.gif *.pbm *.pgm *.ppm *.xbm *.xpm);;All Files (*)", options=options)
        return filename

    def init_new_picture(self, filename1, filename2):
        self.ui.zoom_slider.setProperty("value", 0)
        self.img_controller.set_path(filename1,filename2)
        
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

    def open_file_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("讀取錯誤...")
        msg.setWindowTitle("未成功讀取影像...")
        msg.setIcon(QMessageBox.Information)


    def get_zoomSlider_value_and_zoom(self):
        self.img_controller.set_zoom(self.ui.zoom_slider.value())

    def get_alpha1Slider_value(self):
        image1Alpha = self.ui.image1Alpha_slider.value()
        self.img_controller.set_alpha(image1Alpha,'')

    def get_alpha2Slider_value(self):
        image2Alpha = self.ui.image2Alpha_slider.value()
        self.img_controller.set_alpha('',image2Alpha)

    def get_text_value(self,ui):
        return int(ui.text())

    def imageEditor_callback(self,
                            image_layer='',
                            mode='',
                            pushButton='',
                            color_lineEdit='',
                            penPixelSize_lineEdit=''):
        self.current_imagelayer = image_layer
        if pushButton and mode:
            self.all_editor_button_enable()
            pushButton.setEnabled(False)
        else:
            pass # raising error neither pushButton or mode is missing
        
        color =        self.get_text_value(color_lineEdit) if color_lineEdit else ''
        penPixelSize = self.get_text_value(penPixelSize_lineEdit) if penPixelSize_lineEdit else ''

        pen_property = {'image_layer':image_layer,
                        'mode':mode,
                        'color':color,
                        'penPixelSize':penPixelSize}

        self.img_controller.editor_mouse_controller.set_pen(pen_property)

    def image1EditorFreehand_pushButton_callback(self):
        arg = {'image_layer':'img1',
                'mode':'Freehand',
                'pushButton':            self.ui.image1EditorFreehand_pushButton,
                'color_lineEdit':        self.ui.image1EditorColor_lineEdit,
                'penPixelSize_lineEdit': self.ui.image1EditorPenPixelSize_lineEdit}
        self.imageEditor_callback(**arg)

    def image1EditorLine_pushButton_callback(self):
        arg = {'image_layer':'img1',
                'mode':'Line',
                'pushButton':            self.ui.image1EditorLine_pushButton,
                'color_lineEdit':        self.ui.image1EditorColor_lineEdit,
                'penPixelSize_lineEdit': self.ui.image1EditorPenPixelSize_lineEdit}
        self.imageEditor_callback(**arg)

    def image1EditorFill_pushButton_callback(self):
        arg = {'image_layer':'img1',
                'mode':'Fill',
                'pushButton':            self.ui.image1EditorFill_pushButton,
                'color_lineEdit':        self.ui.image1EditorColor_lineEdit,
                'penPixelSize_lineEdit': self.ui.image1EditorPenPixelSize_lineEdit}
        self.imageEditor_callback(**arg)

    def image2EditorFreehand_pushButton_callback(self):
        arg = {'image_layer':'img2',
                'mode':'Freehand',
                'pushButton':            self.ui.image2EditorFreehand_pushButton,
                'color_lineEdit':        self.ui.image2EditorColor_lineEdit,
                'penPixelSize_lineEdit': self.ui.image2EditorPenPixelSize_lineEdit}
        self.imageEditor_callback(**arg)

    def image2EditorLine_pushButton_callback(self):
        arg = {'image_layer':'img2',
                'mode':'Line',
                'pushButton':            self.ui.image2EditorLine_pushButton,
                'color_lineEdit':        self.ui.image2EditorColor_lineEdit,
                'penPixelSize_lineEdit': self.ui.image2EditorPenPixelSize_lineEdit}
        self.imageEditor_callback(**arg)

    def image2EditorFill_pushButton_callback(self):
        arg = {'image_layer':'img2',
                'mode':'Fill',
                'pushButton':            self.ui.image2EditorFill_pushButton,
                'color_lineEdit':        self.ui.image2EditorColor_lineEdit,
                'penPixelSize_lineEdit': self.ui.image2EditorPenPixelSize_lineEdit}
        self.imageEditor_callback(**arg)

    def image1EditorColor_lineEdit_callback(self):
        if self.current_imagelayer == 'img1':
            arg = {'image_layer':'img1',
                'mode':'',
                'pushButton':            '',
                'color_lineEdit':        self.ui.image1EditorColor_lineEdit,
                'penPixelSize_lineEdit': ''}
            self.imageEditor_callback(**arg)

    def image1EditorPenPixelSize_lineEdit_callback(self):
        if self.current_imagelayer == 'img1':
            arg = {'image_layer':'img1',
                'mode':'',
                'pushButton':            '',
                'color_lineEdit':        '',
                'penPixelSize_lineEdit': self.ui.image1EditorPenPixelSize_lineEdit}
            self.imageEditor_callback(**arg)

    def image2EditorColor_lineEdit_callback(self):
        if self.current_imagelayer == 'img2':
            arg = {'image_layer':'img2',
                'mode':'',
                'pushButton':            '',
                'color_lineEdit':        self.ui.image2EditorColor_lineEdit,
                'penPixelSize_lineEdit': ''}
            self.imageEditor_callback(**arg)

    def image2EditorPenPixelSize_lineEdit_callback(self):
        if self.current_imagelayer == 'img2':
            arg = {'image_layer':'img2',
                'mode':'',
                'pushButton':            '',
                'color_lineEdit':        '',
                'penPixelSize_lineEdit': self.ui.image2EditorPenPixelSize_lineEdit}
            self.imageEditor_callback(**arg)

    def all_editor_button_enable(self):
        self.ui.image1EditorFreehand_pushButton.setEnabled(True)
        self.ui.image1EditorLine_pushButton.setEnabled(True)
        self.ui.image1EditorFill_pushButton.setEnabled(True)
        self.ui.image2EditorFreehand_pushButton.setEnabled(True)
        self.ui.image2EditorLine_pushButton.setEnabled(True)
        self.ui.image2EditorFill_pushButton.setEnabled(True)

