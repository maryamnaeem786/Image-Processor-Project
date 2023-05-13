"""MyImage.py: Base class implementation to manage PGM and PPM images file. """

__author__ = "Shishir Shah"
__version__ = "1.0.0"
__copyright__ = "Copyright 2023 by Shishir Shah, Quantitative Imaging Laboratory (QIL), Department of Computer  \
                Science, University of Houston.  All rights reserved.  This software is property of the QIL, and  \
                should not be distributed, reproduced, or shared online, without the permission of the author."

__Student__Name__= 'Maryam Naeem'
__student__ID__= '1945670'


import math
import numpy as np


class MyImage:
    ''' Constructor that initializes the values for the
    data items necessary to represent an image.'''
    def __init__(self):
        '''This is the n-d array that stores the image intensity values.'''
        self.data = None
        '''This defines the size of the image as [width, height].'''
        self.size = [0, 0]
        '''This defines the number of image channels and should be 1 for gray scale and 3 for color image.'''
        self.channels = None
        '''This defines the maximum intensity values.  
        In our case, since we will restrict to 8-bit images, this will be 255.'''
        self.bitdepth = None
        '''This specifies if the image is PGM or PPM, hence would take values of 'P2' or 'P3', respectively.'''
        self.category = None
        # '''This  defines the array that will maintain the gray level image histogram'''
        # self.gray_hist = np.zeros((256,), dtype=int)
        # self.rotated_img = None
        # self.history = []

    ''' Method to read either a PGM or PPM files given the filename as the argument.  
    All the defined data attributes in the constructor should have appropriate values after reading the file.'''
    def load_image(self, filename):
        values = []
        with open(filename, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                elif line.startswith('#'):
                    pass
                else:
                    temp = line.split()
                    for i in range(len(temp)):
                        values.append(temp[i])

        self.category = values[0]
        self.size = [int(values[1]), int(values[2])]
        self.bitdepth = values[3]
        nvals = list(map(int, values[4:]))
        if self.category == 'P2':
            self.channels = 1
        elif self.category == 'P3':
            self.channels = 3
        else:
            print('File type not supported\n')
            return
        self.data = np.reshape(nvals, (self.size[1], self.size[0], self.channels))
        return

    ''' Method to save either a PGM or PPM files given the filename as the argument.'''
    def save_image(self, filename):
        if self.category == None:
            print('Image does not exist so cannot be saved\n')
        else:
            fp = open(filename, 'w')
            fp.write(self.category + '\n')
            img_size = str(self.get_width()) + ' ' + str(self.get_height())
            fp.write(img_size + '\n')
            fp.write(str(self.bitdepth) + '\n')
            for x in self.data:
                for y in x:
                    fp.write(" ".join(map(str, y)))
                    fp.write('\n')
            fp.close()
        return

    ''' Method to create a new image of dimension 'width' by 'height' and 
    with all pixels having intensity values provided by the argument 'value'.'''
    def new_image(self, width, height, value):
        self.size = [width, height]
        self.channels = len(value)
        self.bitdepth = 255
        if self.channels == 1:
            self.data = np.zeros([height, width, 1], dtype=np.uint8)
            self.category = 'P2'
        elif self.channels == 3:
            self.data = np.zeros([height, width, 3], dtype=np.uint8)
            self.category = 'P3'
        self.data[:, :] = value

    ''' Method that returns the number of channels an image has.  
    Recall that this value is 1 for gray scale images and 3 for color images.'''
    def get_channels(self):
        return self.channels

    ''' Method that sets the number of channels of an image.  
     Recall that this value is 1 for gray scale images and 3 for color images.'''
    def set_channels(self, chn):
        self.channels = chn
        return

    ''' Method that returns the n-d array having the intensity values of the image.'''
    def get_image_data(self):
        return self.data

    ''' Method that return the width of the image.'''
    def get_width(self):
        return self.size[0]

    ''' Method that return the height of the image.'''
    def get_height(self):
        return self.size[1]

    '''' Method that assigns intensity value of a range of image pixels to 
    that given by the argument 'value' where the range of pixel locations is specified 
    as a bounding box in the format [x, y, width, height].'''
    def set_image_pixels(self, bbox, value):
        startx = bbox[0]
        starty = bbox[1]
        endx = startx + bbox[2]
        endy = starty + bbox[3]
        self.data[starty:endy, startx:endx] = value
        return

    '''' Method that return an n-d array of intensity values for a range of image pixels
    where the range is specified as a bounding box in the format [x, y, width, height].'''
    def get_image_pixels(self, bbox):
        startx = bbox[0]
        starty = bbox[1]
        endx = startx + bbox[2]
        endy = starty + bbox[3]
        return self.data[starty:endy, startx:endx]

    ''' Method that assigns the pixel value in the image at 
    location 'x', 'y' to the intensity given by argument 'value'.'''
    def set_image_pixel(self, x, y, value):
        self.data[y, x] = value
        return

    ''' Method that returns the pixel value in the image at 
    location 'x', 'y'.'''
    def get_image_pixel(self, x, y):
        return self.data[y, x]

    ''' Write method that converts a color image to a gray scale image 
    by computing the average of the red, green, and blue intensity value 
    at each pixel of the color image.  Please note that this should only 
    happen if the image is a color image. Return a gray scale image if 
    the image is already gray scale'''
    def color_to_gray(self):
        big_image_lst = []
        if self.channels == 1:
            return self.data
        else:
            for line in self.data:
                newline_lst = []
                for pixel in line:
                    gray_value = [(pixel[0] + pixel[1] + pixel[2]) // 3]  # creates list of gray values
                    newline_lst.append(gray_value)
                big_image_lst.append(newline_lst)
            print(big_image_lst)
            gray_img = MyImage()
            width = self.get_width()
            height = self.get_height()
            gray_img.new_image(width, height, [0])
            gray_img.set_image_pixels([0, 0, width, height], big_image_lst)
            return gray_img


    ''' Write method to threshold a gray scale image such that all 
    intensity values less than or equal to N are assigned a value of 0
    and values greater than N are assigned to 255.  The method also 
    computes the optimal value of N as the mean of means of estimated 
    bimodal distribution of image intensities.  The method should return
    the estimated threshold value and the thresholded image as a tuple.  
    The threshold value should be a float.'''
    def threshold(self):
        # Checks to see if the input image is a gray image
        #print("in the threshold")
        thr_epsilon = 0.5
        if self.channels != 1:
            val_er = "The input image needs be a gray image"
            raise ValueError(val_er)

        # sets a threshold value
        threshold_value = 128
        threshold_diff = 256  # the difference is 256 so it executes the loop at least once

        # will iterate through segmenting the image to 2 groups until we find the optimal value of the threshold
        while threshold_diff >= thr_epsilon:  # t_epsilon is the pre-defined T0
            threshold_prev = threshold_value
            big_image_lst = []  # the final image that gets displayed
            g1, g2 = [], []  # the 2 groups of pixels based on threshold

            for line in self.data:
                newline_lst = []
                for pixel in line:
                    if pixel[0] > threshold_value:
                        g1.append(pixel[0])  # pixel that belongs to group 1
                        newline_lst.append([255])
                    else:
                        g2.append(pixel[0])  # pixel that belongs to group 2
                        newline_lst.append([0])
                big_image_lst.append(newline_lst)  # add the line/row of pixels to the final image

            threshold_value = 0.5 * ((sum(g1) / len(g1)) + (sum(g2) / len(
                g2)))  # updating threshold to find the mean of means, can use int() as well since these are pixel intensities
            threshold_diff = abs(
                threshold_prev - threshold_value)  # taking the absolute of the difference to ignore sign
        #print("after loop")
        # Create a new image object for the thresholded image
        threshold_img = MyImage()
        width = self.get_width()
        height = self.get_height()
        threshold_img.new_image(width, height, [0])
        threshold_img.set_image_pixels([0, 0, width, height], big_image_lst)

        # Returns the computed threshold value and the thresholded image as a tuple
        return threshold_value, threshold_img


    ''' Write a method for rotating the image where the amount of rotation 
    is provided as an angle in degrees.  Positive value of the angle should 
    indicate anti-clockwise rotation around the center of the image.  Method 
    should perform a mapping of each pixel position in the original image 
    to the position in the rotated image.  Method should return the rotated image.'''
    def rotate_image(self,degrees):
        theta = math.radians(degrees)

        # Calculating trigonometric functions of the angle
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        # Getting the dimensions of the original image
        width, height = self.size

        # Calculating the center point of the image
        center_x = width // 2
        center_y = height // 2

        # Creating a new image object for the rotated image we will make
        rotated_img = MyImage()
        if self.get_channels() == 1:
            rotated_img.new_image(width, height, [0])
        else:
            rotated_img.new_image(width, height, [0, 0, 0])

        for y in range(height):
            for x in range(width):
                # Translating the pixel position to the center of the image
                x_trans = x - center_x
                y_trans = y - center_y

                # Rotating the pixel position around the center of the image
                x_rotate = x_trans * cos_theta - y_trans * sin_theta
                y_rotate = x_trans * sin_theta + y_trans * cos_theta

                # Translating the rotated pixel position back to the original position
                x_rotate += center_x
                y_rotate += center_y

                # Here it rounds the pixel positions to integers
                x_rotate, y_rotate = int(round(x_rotate)), int(round(y_rotate))

                # This Checks if the rotated pixel position is within the range of the image
                if 0 <= x_rotate < width and 0 <= y_rotate < height:
                    # Gets the pixel intensity value at the rotated position
                    pixel_value = self.data[y_rotate][x_rotate]

                    # Sets the corresponding pixel in the rotated image
                    rotated_img.data[y][x] = pixel_value
        return rotated_img


    def rotate_image_inv(self, degrees):
        # Convert from degrees to radians
        theta = math.radians(degrees)

        # Calculating trigonometric functions of the angle
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        # Getting the dimensions of the original image
        width, height = self.get_width(), self.get_height()

        # Calculating the center point of the image
        center_x = width // 2
        center_y = height // 2

        # Calculating the rotation matrix using the trigonometric functions
        rotation_matrix = np.array([[cos_theta, -sin_theta],
                                    [sin_theta, cos_theta]])

        # This Calculates the inverse of the rotation matrix
        det = rotation_matrix[0][0] * rotation_matrix[1][1] - rotation_matrix[0][1] * rotation_matrix[1][0]
        inv_rotation_matrix = [[rotation_matrix[1][1] / det, -rotation_matrix[0][1] / det],
                               [-rotation_matrix[1][0] / det, rotation_matrix[0][0] / det]]

        # Creates a new image object for the rotated image
        rotated_img = MyImage()
        if self.get_channels() == 1:
            rotated_img.new_image(width, height, [0])
        else:
            rotated_img.new_image(width, height, [0, 0, 0])

        for y in range(height):
            for x in range(width):
                # Here is translates pixel position to the center of the image
                x_trans = x - center_x
                y_trans = y - center_y

                # This calculates the position of the corresponding pixel in the original image using the inverse of the rotation matrix
                x_rotate, y_rotate = np.dot(inv_rotation_matrix, [x_trans, y_trans])

                # Translates the rotated pixel position back to its original position
                x_rotate += center_x
                y_rotate += center_y

                # Rounds the pixel positions to integers
                x_rotate, y_rotate = int(round(x_rotate)), int(round(y_rotate))

                # Checks if the rotated pixel position is within the range of the image
                if 0 <= x_rotate < width and 0 <= y_rotate < height:
                    # Getting the pixel intensity value at the rotated position
                    pixel_value = self.data[y_rotate][x_rotate]

                    # Sets the corresponding pixel in the rotated image
                    rotated_img.data[y][x] = pixel_value

        return rotated_img