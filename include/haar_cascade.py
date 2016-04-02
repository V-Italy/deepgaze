#!/usr/bin/env python

## @package haar_cascade.py
#
# Massimiliano Patacchiola, Plymouth University 2016
#
# This module use the opencv haar cascade classifier
# to find frontal and profile faces in a frame.

import numpy
import cv2
import sys
import os.path


class haarCascade:


    def __init__(self, frontalFacePath, profileFacePath):

        self.is_face_present = False

        #Represent the face type found
        #0- no face
        #1- frontal face
        #2- left face
        #3- right face
        self.face_type = 0

        self.face_x = 0
        self.face_y = 0
        self.face_h = 0
        self.face_w = 0

        if(os.path.isfile(frontalFacePath) == False and os.path.isfile(profileFacePath)==False):
            raise ValueError('haarCascade: the files specified do not exist.') 

        self._frontalFacePath = frontalFacePath
        self._profileFacePath = profileFacePath

        self._frontalCascade = cv2.CascadeClassifier(frontalFacePath)
        self._profileCascade = cv2.CascadeClassifier(profileFacePath)


    ##
    # Find a face (frontal or profile) in the input image
    # To find the right profile the input image is vertically flipped,
    # this is done because the training file for profile faces was 
    # trained only on left profile.
    # @param inputImg the image where the cascade will be called
    # @param runLeft if True it look for left profile faces
    # @param runRight if True it looks for right profile faces
    #
    def findFace(self, inputImg, runLeft=True, runRight=True, scaleFactor=1.1, minSizeX=30, minSizeY=30):

        #Cascade: frontal faces
        self._findFrontalFace(inputImg)
        if(self.is_face_present == True):
            self.face_type = 1
            return (self.face_x, self.face_y, self.face_w, self.face_h)

        #Cascade: left profiles
        if(runLeft==True):
            self._findProfileFace(inputImg)
            if(self.is_face_present == True):
                self.face_type = 2
                return (self.face_x, self.face_y, self.face_w, self.face_h)

        #Cascade: right profiles
        if(runRight==True):
            flipped_inputImg = cv2.flip(inputImg,1) 
            self._findProfileFace(flipped_inputImg)
            if(self.is_face_present == True):
                self.face_type = 3
                f_w, f_h = flipped_inputImg.shape[::-1] #finding the max dimensions
                self.face_x = f_w - (self.face_x + self.face_w) #reshape the x to unfold the mirroring
                return (self.face_x, self.face_y, self.face_w, self.face_h)

        #It returns zeros if anything is found
        self.face_type = 0    
        self.is_face_present = False 
        return (0, 0, 0, 0)


    ##
    # Find a frontalface in the input image
    # @param inputImg the image where the cascade will be called
    #
    def _findFrontalFace(self, inputImg, scaleFactor=1.1, minSizeX=30, minSizeY=30):

        #Cascade: frontal faces
        faces = self._frontalCascade.detectMultiScale(
            inputImg,
            scaleFactor=scaleFactor,
            minNeighbors=5,
            minSize=(minSizeX, minSizeY),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        if(len(faces) == 0):
            self.face_x = 0
            self.face_y = 0
            self.face_w = 0
            self.face_h = 0
            self.is_face_present = False
            return (0, 0, 0, 0)

        if(len(faces) == 1): 
            self.face_x = faces[0][0]
            self.face_y = faces[0][1]
            self.face_w = faces[0][2]
            self.face_h = faces[0][3]
            self.is_face_present = True
            return (faces[0][0], faces[0][1], faces[0][2], faces[0][3])
        #for x,y,h,w in faces:

    ##
    # Find a profile face in the input image
    # @param inputImg the image where the cascade will be called
    #           
    def _findProfileFace(self, inputImg, scaleFactor=1.1, minSizeX=30, minSizeY=30):

        #Cascade: left profile
        faces = self._profileCascade.detectMultiScale(
            inputImg,
            scaleFactor=scaleFactor,
            minNeighbors=5,
            minSize=(minSizeX, minSizeY),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        if(len(faces) == 0):
            self.face_x = 0
            self.face_y = 0
            self.face_w = 0
            self.face_h = 0
            self.is_face_present = False
            return (0, 0, 0, 0)

        if(len(faces) == 1): 
            self.face_x = faces[0][0]
            self.face_y = faces[0][1]
            self.face_w = faces[0][2]
            self.face_h = faces[0][3]
            self.is_face_present = True
            return (faces[0][0], faces[0][1], faces[0][2], faces[0][3])
        #for x,y,h,w in faces:




