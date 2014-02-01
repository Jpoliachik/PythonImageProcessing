################################################
# Image Processing GUI
# Performs several image processing functions on
# an imported image
# using Python, Pyside, Qt, PIL
# 
# Justin Poliachik
# 10 December 2013
################################################


#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide import QtGui
from PySide import QtCore
from PIL import Image
from random import randint

class MainWindow(QtGui.QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        print "Initializing"
        
        # File Pick Layout
        filePick = QtGui.QHBoxLayout()

        # Create a label which displays the path to our chosen file
        self.fileLabel = QtGui.QLabel('No file selected')
        filePick.addWidget(self.fileLabel)

        # Create a push button labelled 'choose' and add it to our layout
        fileBtn = QtGui.QPushButton('Choose file', self)
        filePick.addWidget(fileBtn)
        
        # Connect the clicked signal to the get_fname handler
        self.connect(fileBtn, QtCore.SIGNAL('clicked()'), self.get_fname)
        
        #Set the image to be blank at first
        pixmap = QtGui.QPixmap()
        self.imageLabel = QtGui.QLabel()
        self.imageLabel.setPixmap(pixmap)
        self.imageString = ""
        self.sliderValue = 0
        
        #Define layout boxes
        bottomBox = QtGui.QHBoxLayout()
        topBox = QtGui.QHBoxLayout()
        sideBox = QtGui.QVBoxLayout()
        sideBoxPad = QtGui.QHBoxLayout()
        
        #File picker on top
        topBox.addStretch(1)
        topBox.addLayout(filePick)
        topBox.addStretch(1)
        
        #Image in middle/right
        bottomBox.addStretch(1)
        bottomBox.addWidget(self.imageLabel)
        bottomBox.addStretch(1)
        
        #Buttons on left
        normalButton = QtGui.QPushButton("Normal")
        self.connect(normalButton, QtCore.SIGNAL('clicked()'), self.normal_image)
        addButton = QtGui.QPushButton("Add")
        self.connect(addButton, QtCore.SIGNAL('clicked()'), self.add)
        blurButton = QtGui.QPushButton("Blur")
        self.connect(blurButton, QtCore.SIGNAL('clicked()'), self.blur)
        contrastButton = QtGui.QPushButton("Contrast")
        self.connect(contrastButton, QtCore.SIGNAL('clicked()'), self.contrast)
        edgeDetectButton = QtGui.QPushButton("Edge Detect")
        self.connect(edgeDetectButton, QtCore.SIGNAL('clicked()'), self.edge_detect)
        invertButton = QtGui.QPushButton("Invert")
        self.connect(invertButton, QtCore.SIGNAL('clicked()'), self.invert)
        multiplyButton = QtGui.QPushButton("Multiply")
        self.connect(multiplyButton, QtCore.SIGNAL('clicked()'), self.multiply)
        sharpenButton = QtGui.QPushButton("Sharpen")
        self.connect(sharpenButton, QtCore.SIGNAL('clicked()'), self.sharpen)
        twoToneButton = QtGui.QPushButton("Two Tone")
        self.connect(twoToneButton, QtCore.SIGNAL('clicked()'), self.two_tone)
        
        #Slider
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld.setFocusPolicy(QtCore.Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 50)
        sld.valueChanged[int].connect(self.change_slider)
        
        sideBox.addStretch(1)
        sideBox.addWidget(normalButton)
        sideBox.addStretch(1)
        sideBox.addWidget(addButton)
        sideBox.addWidget(blurButton)
        sideBox.addWidget(contrastButton)
        sideBox.addWidget(edgeDetectButton)
        sideBox.addWidget(invertButton)
        sideBox.addWidget(multiplyButton)
        sideBox.addWidget(sharpenButton)
        sideBox.addWidget(twoToneButton)
        sideBox.addWidget(sld)
        sideBox.addStretch(1)
        sideBoxPad.addStretch(1)
        sideBoxPad.addLayout(sideBox)
        sideBoxPad.addStretch(1)
        
        #Set grid layout
        grid = QtGui.QGridLayout()
        grid.addLayout(topBox, 0, 1)
        grid.addLayout(sideBoxPad, 1, 0)
        grid.addLayout(bottomBox, 1, 1)
        self.setLayout(grid)  
        
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Image Processing Functions')
        
        self.show()
      
    #File Picker Function    
    def get_fname(self):
        """
        Handler called when 'choose file' is clicked
        """
        # When you call getOpenFileName, a file picker dialog is created
        # and if the user selects a file, it's path is returned, and if not
        # (ie, the user cancels the operation) None is returned
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Select file')
        print fname
        if fname:
            self.fileLabel.setText(fname[0])
            self.load_image(fname[0])
        else:
            self.fileLabel.setText("No file selected")
            
    #Load new image function        
    def load_image(self, filepath):
        #Load the image into the label
        print "Loading Image"
        pixmap = QtGui.QPixmap(filepath)
        self.imageLabel.setPixmap(pixmap)
        self.imageString = filepath
        
    #Load new image function        
    def set_image(self, image):
        #Load the image into the label
        self.imageLabel.setPixmap(image)
        
     #Load normal image       
    def normal_image(self):
        #Load the image into the label
        print "Loading Image"
        pixmap = QtGui.QPixmap(self.imageString)
        self.imageLabel.setPixmap(pixmap)
        
     #Slider Changed     
    def change_slider(self, value):
        self.sliderValue = value
        
    #----------------------------------------------------------------------
    #Image Processing Functions
    #----------------------------------------------------------------
    def add(self):
        print self.imageString
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]
                    
                    addValue = self.sliderValue
                    pixelR += addValue
                    pixelG += addValue
                    pixelB += addValue
              
                    if pixelR > 255:
                        pixelR = 255
                    if pixelG > 255:
                        pixelG = 255
                    if pixelB > 255:
                        pixelB = 255
                        
                    if pixelR < 0:
                        pixelR = 0
                    if pixelG < 0:
                        pixelG = 0
                    if pixelB < 0:
                        pixelB = 0
                    
                    copiedValue = QtGui.qRgb(pixelR, pixelG, pixelB)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)
            
                #newqim.save('result.jpg')

                # Put image data in a pixmap for display.
                # PIL Images and QImages may be used for read, write, manipulate.
                # QPixmaps are used for Qt GUI display.
                ################################################
                #pix = QPixmap.fromImage(qim) # Pixmap for display using QImage
            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)
        
        
        
    #Blur    
    def blur(self):
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]
                    
                    averageR = 0
                    averageG = 0
                    averageB = 0
                    
                    # Ignore pixels on top and left borders
                    if(xstep > 0 and xstep < imWidth-1):
                       if(ystep > 0 and ystep < imHeight-1):
                          averageR = pixelR*.11111
                          averageG = pixelG*.11111
                          averageB = pixelB*.11111
                          #top left
                          offsetpixel = im.getpixel((xstep-1,ystep-1))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          #top center
                          offsetpixel = im.getpixel((xstep,ystep-1))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          #top right
                          offsetpixel = im.getpixel((xstep+1,ystep-1))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          #center left
                          offsetpixel = im.getpixel((xstep-1,ystep))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          #center right
                          offsetpixel = im.getpixel((xstep+1,ystep))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          #bottom left
                          offsetpixel = im.getpixel((xstep-1,ystep+1))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          #bottom center
                          offsetpixel = im.getpixel((xstep,ystep+1))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          #bottom right
                          offsetpixel = im.getpixel((xstep+1,ystep+1))
                          averageR = averageR + (offsetpixel[0]*.11111)
                          averageG = averageG + (offsetpixel[1]*.11111)
                          averageB = averageB + (offsetpixel[2]*.11111)
                          
                    pixelR = averageR
                    pixelG = averageG
                    pixelB = averageB
              
                    if pixelR > 255:
                        pixelR = 255
                    if pixelG > 255:
                        pixelG = 255
                    if pixelB > 255:
                        pixelB = 255
                        
                    if pixelR < 0:
                        pixelR = 0
                    if pixelG < 0:
                        pixelG = 0
                    if pixelB < 0:
                        pixelB = 0
                    
                    copiedValue = QtGui.qRgb(pixelR, pixelG, pixelB)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)

            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)
    
    
    
    #Contrast
    def contrast(self):
        print self.imageString
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]
            
            factor = (self.sliderValue*2.0)/100.0

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]
                    
                    pixelR = (factor * (pixelR - 128)) + 128
                    pixelG = (factor * (pixelG - 128)) + 128
                    pixelB = (factor * (pixelB - 128)) + 128
              
                    if pixelR > 255:
                        pixelR = 255
                    if pixelG > 255:
                        pixelG = 255
                    if pixelB > 255:
                        pixelB = 255
                        
                    if pixelR < 0:
                        pixelR = 0
                    if pixelG < 0:
                        pixelG = 0
                    if pixelB < 0:
                        pixelB = 0
                    
                    copiedValue = QtGui.qRgb(pixelR, pixelG, pixelB)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)
            
            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)                
        
        
        
    #Edge Detect
    def edge_detect(self):
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]
                    
                    averageR = 0
                    averageG = 0
                    averageB = 0
                    
                    # Ignore pixels on top and left borders
                    if(xstep > 0 and xstep < imWidth-1):
                       if(ystep > 0 and ystep < imHeight-1):
                          averageR = pixelR*8
                          averageG = pixelG*8
                          averageB = pixelB*8
                          #top left
                          offsetpixel = im.getpixel((xstep-1,ystep-1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #top center
                          offsetpixel = im.getpixel((xstep,ystep-1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #top right
                          offsetpixel = im.getpixel((xstep+1,ystep-1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #center left
                          offsetpixel = im.getpixel((xstep-1,ystep))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #center right
                          offsetpixel = im.getpixel((xstep+1,ystep))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #bottom left
                          offsetpixel = im.getpixel((xstep-1,ystep+1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #bottom center
                          offsetpixel = im.getpixel((xstep,ystep+1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #bottom right
                          offsetpixel = im.getpixel((xstep+1,ystep+1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          
                    pixelR = averageR
                    pixelG = averageG
                    pixelB = averageB
              
                    if pixelR > 255:
                        pixelR = 255
                    if pixelG > 255:
                        pixelG = 255
                    if pixelB > 255:
                        pixelB = 255
              
                    if pixelR < 0:
                        pixelR = 0
                    if pixelG < 0:
                        pixelG = 0
                    if pixelB < 0:
                        pixelB = 0
                    
                    copiedValue = QtGui.qRgb(pixelR, pixelG, pixelB)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)
            
            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)
                
                
    #Invert
    def invert(self):
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]
                    
                    pixelR = 255-pixelR
                    pixelG = 255-pixelG
                    pixelB = 255-pixelB
              
                    if pixelR > 255:
                        pixelR = 255
                    if pixelG > 255:
                        pixelG = 255
                    if pixelB > 255:
                        pixelB = 255
                        
                    if pixelR < 0:
                        pixelR = 0
                    if pixelG < 0:
                        pixelG = 0
                    if pixelB < 0:
                        pixelB = 0
                    
                    copiedValue = QtGui.qRgb(pixelR, pixelG, pixelB)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)
            
            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)
                
    
    
    #Multiply
    def multiply(self):
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]
            
            multValue = (self.sliderValue*2.0)/100.0

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]

                    pixelR *= multValue
                    pixelG *= multValue
                    pixelB *= multValue
              
                    if pixelR > 255:
                        pixelR = 255
                    if pixelG > 255:
                        pixelG = 255
                    if pixelB > 255:
                        pixelB = 255
                        
                    if pixelR < 0:
                        pixelR = 0
                    if pixelG < 0:
                        pixelG = 0
                    if pixelB < 0:
                        pixelB = 0
                    
                    copiedValue = QtGui.qRgb(pixelR, pixelG, pixelB)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)
            
            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)            
                
    
    
    
    #Sharpen
    def sharpen(self):
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]
                    
                    averageR = 0
                    averageG = 0
                    averageB = 0
                    
                    # Ignore pixels on top and left borders
                    if(xstep > 0 and xstep < imWidth-1):
                       if(ystep > 0 and ystep < imHeight-1):
                          averageR = pixelR*9
                          averageG = pixelG*9
                          averageB = pixelB*9
                          #top left
                          offsetpixel = im.getpixel((xstep-1,ystep-1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #top center
                          offsetpixel = im.getpixel((xstep,ystep-1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #top right
                          offsetpixel = im.getpixel((xstep+1,ystep-1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #center left
                          offsetpixel = im.getpixel((xstep-1,ystep))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #center right
                          offsetpixel = im.getpixel((xstep+1,ystep))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #bottom left
                          offsetpixel = im.getpixel((xstep-1,ystep+1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #bottom center
                          offsetpixel = im.getpixel((xstep,ystep+1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          #bottom right
                          offsetpixel = im.getpixel((xstep+1,ystep+1))
                          averageR = averageR + (offsetpixel[0]*-1)
                          averageG = averageG + (offsetpixel[1]*-1)
                          averageB = averageB + (offsetpixel[2]*-1)
                          
                    pixelR = averageR
                    pixelG = averageG
                    pixelB = averageB
              
                    if pixelR > 255:
                        pixelR = 255
                    if pixelG > 255:
                        pixelG = 255
                    if pixelB > 255:
                        pixelB = 255
              
                    if pixelR < 0:
                        pixelR = 0
                    if pixelG < 0:
                        pixelG = 0
                    if pixelB < 0:
                        pixelB = 0
                    
                    copiedValue = QtGui.qRgb(pixelR, pixelG, pixelB)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)
            
            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)
                
    
     #Custom Function two_tone
     #Converts the image to grayscale using the luminosity formula
     #Determines a cutoff point based off the slider value
     #Pixels are either white or black based on the cutoff point
    def two_tone(self):
        if self.imageString:
            print "Processing"
            im = Image.open(self.imageString)
            imdata = im.tostring()
            imWidth = im.size[0]
            imHeight = im.size[1]
            
            cutoffValue = self.sliderValue*2.55

            # Convert image data from PIL image into a QImage
            ################################################
            newqim = QtGui.QImage(imWidth, imHeight, QtGui.QImage.Format_ARGB32)
            for xstep in range(0,imWidth-1):
                for ystep in range(0,imHeight-1):
                    # PIL uses getpixel and putpixel
                    pixelValueTuple = im.getpixel((xstep,ystep))
                    pixelR = pixelValueTuple[0]
                    pixelG = pixelValueTuple[1]
                    pixelB = pixelValueTuple[2]
                    
                    #Using luminosity formula
                    grayPixel = (pixelR*.21) + (pixelG*.71) + (pixelB*.07)
              
                    if(grayPixel > cutoffValue):
                        grayPixel = 255
                    else:
                        grayPixel = 1
                        
                    if grayPixel > 255:
                        grayPixel = 255
                    if grayPixel < 0:
                        grayPixel = 0
                    
                    copiedValue = QtGui.qRgb(grayPixel, grayPixel, grayPixel)
                    # QImage uses pixel and setpixel
                    newqim.setPixel(xstep, ystep, copiedValue)
            
            pix = QtGui.QPixmap.fromImage(newqim)
            self.set_image(pix)
                
               
               
                
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()