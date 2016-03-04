#!/usr/bin/env python
# .. -*- coding: utf-8 -*-
#
# Library imports
# ---------------
import time
#
# Local imports
# -------------
from bertha_bot_base import ButtonGui
from bertha_bot_base import main
from bertha_bot_controller import RobotController
#
# Must import after ``bertha_bot_base`` to get SIP API set
# correctly.
from PyQt4.QtCore import QElapsedTimer, pyqtSlot
#
# ROS Imports
# -----------
import rospy


class BotControl(ButtonGui):

    #__________________________________________________________________________
    #
    # Autonomous mode state machine
    #__________________________________________________________________________

    # def updateState(self, nextState):
    #     # State 1: IDLE
    #     if nextState == 1:
    #         self.controller.SetNavCommand(46)
    #         self.controller.SetNavCommand(76)
    #         # Wait for bump
    #         if self.controller.bumpSwitchPressed == True:
    #             self.state = 2

    #     # State 2: LOOK_FOR_BLOCKS
    #     if nextState == 2:
    #         self.controller.SetNavCommand(46)
    #         self.controller.SetNavCommand(108)
    #         time.sleep(1.0)
    #         self.state = 3

    #     # State 3: STOP
    #     if nextState == 3:
    #         self.controller.SetNavCommand(46)
        
    #     print nextState



    #__________________________________________________________________________
    #
    # Rail cart aligment testing
    #__________________________________________________________________________

    def updateState(self, nextState):
        
        if nextState == 1:
            self.count = 0
            print "State 1"
            self.controller.SetNavCommand(108)
            time.sleep(1.5)
            self.controller.SetNavCommand(46)
            time.sleep(0.5)
            self.controller.SetNavCommand(204)
            time.sleep(1.8)
            self.controller.SetNavCommand(46)
            time.sleep(0.5)
            self.controller.SetNavCommand(108)
            time.sleep(0.5)
            self.controller.SetNavCommand(46)
            time.sleep(0.5)

            self.state = 2

        # State 2: SET TRACKING COLOR
        elif nextState == 2:
            print "STATE 2"
            time.sleep(3.0)
            if self.count == 0:
                # Red Rail Cart
                self.setTrackingColor(self.railCartColorMatrix[0])
            elif self.count == 1:    
                # Blue Rail Cart
                self.setTrackingColor(self.railCartColorMatrix[1])
            elif self.count == 2:
                # Green Rail Cart
                self.setTrackingColor(self.railCartColorMatrix[2])
            elif self.count == 3:
                # Yellow Rail Cart
                self.setTrackingColor(self.railCartColorMatrix[3])

            elif self.count >= 4:  
                self.state = 4 

            self.state = 3

        # State 2: CREATE CART ARRAY
        elif nextState == 3:
            print "STATE 3"
            print self.x_center

            for color in xrange(4):
                if (self.x_center > self.firstCart_x_Position[0] and self.x_center < self.firstCart_x_Position[1]):
                    self.railCartArray[0] = self.count

                elif (self.x_center > self.secondCart_x_Position[0] and self.x_center < self.secondCart_x_Position[1]):
                    self.railCartArray[1] = self.count

                elif (self.x_center > self.thirdCart_x_Position[0] and self.x_center < self.thirdCart_x_Position[1]):
                    self.railCartArray[2] = self.count

                elif (self.x_center > self.fourthCart_x_Position[0] and self.x_center < self.fourthCart_x_Position[1]):
                    self.railCartArray[3] = self.count

                else:
                    print "ERROR"

            self.count += 1
            print self.railCartArray

            self.state = 2

        # State 2: CREATE CART ARRAY
        elif nextState == 4:
            print "State 4"
            time.sleep(1.0)
            self.count = 0
            self.state = 2
        


    #__________________________________________________________________________
    #
    # Vision parameters for GUI
    #__________________________________________________________________________

    def on_hsThreshold_valueChanged(self, value):
        print(value)

    # Show current tracking color
    def updateTrackingColorLabel(self, s):
        self.lbAuto_2.setText(s)

    def updateCenterPositions(self, x, y):
        self.lbAuto_3.setText(x)
        self.lbAuto_4.setText(y)


    #__________________________________________________________________________
    #
    # Color Sensing Functions for GUI
    #__________________________________________________________________________

    def on_pbScan_pressed(self):
        print("Scanning Blocks")
        sensorData = self.controller.scanBlocks()
        self.setColorGui(sensorData)
        print("Blocks have been scanned")

    def on_pbScan_released(self):
        print("Scan Released")
        
    def setColorGui(self, data):
        sensorArray = ['error','error','error','error','error','error','error','error']

        for i in xrange(len(data)):
            if(data[i] == 0):
                sensorArray[i] = 'error'
            elif(data[i] == 1):
                sensorArray[i] = 'blue'
            elif(data[i] == 2):
                sensorArray[i] = 'green'
            elif(data[i] == 3):
                sensorArray[i] = 'red'
            elif(data[i] == 4):
                sensorArray[i] = 'yellow'

        self.lef1.setText("F: "+str(sensorArray[0]))
        self.leb1.setText("B: "+str(sensorArray[1]))
        self.lef2.setText("F: "+str(sensorArray[2]))
        self.leb2.setText("B: "+str(sensorArray[3]))
        self.lef3.setText("F: "+str(sensorArray[4]))
        self.leb3.setText("B: "+str(sensorArray[5]))
        self.lef4.setText("F: "+str(sensorArray[6]))
        self.leb4.setText("B: "+str(sensorArray[7]))


    #__________________________________________________________________________
    #
    # Navigation Commands for GUI
    #__________________________________________________________________________
    def on_pbForward_pressed(self):
        print("Forward Pressed")
        self.controller.SetNavCommand(0x50)
    def on_pbForward_released(self):
        print("Forward Released")
        self.controller.SetNavCommand(0x2e)

    def on_pbBack_pressed(self):
        print("Backward Pressed")
        self.controller.SetNavCommand(108)
    def on_pbBack_released(self):
        print("Backward Released")
        self.controller.SetNavCommand(0x2e)

    def on_pbLeft_pressed(self):
        print("Left Pressed")
        self.controller.SetNavCommand(0x90)
    def on_pbLeft_released(self):
        print("Left Released")
        self.controller.SetNavCommand(0x2e)

    def on_pbRight_pressed(self):
        print("Right Pressed")
        self.controller.SetNavCommand(0xb0)
    def on_pbRight_released(self):
        print("Right Released")
        self.controller.SetNavCommand(0x2e)

    def on_pbRLeft_pressed(self):
        print("Rotate Left Pressed")
        self.controller.SetNavCommand(0xf0)
    def on_pbRLeft_released(self):
        print("Rotate Left Released")
        self.controller.SetNavCommand(0x2e)

    def on_pbRRight_pressed(self):
        print("Rotate Right Pressed")
        self.controller.SetNavCommand(204)
    def on_pbRRight_released(self):
        print("Rotate Right Released")
        self.controller.SetNavCommand(0x2e)

    def on_pbRaisePlatform_pressed(self):
        print("Raise Platform Pressed")
        self.controller.SetNavCommand(50)
    def on_pbRaisePlatform_released(self):
        print("Raise Platform Released")
        self.controller.SetNavCommand(0x2e)

    def on_pbLowerPlatform_pressed(self):
        print("Lower Platform Pressed")
        self.controller.SetNavCommand(58)
    def on_pbLowerPlatform_released(self):
        print("Lower Platform Released")
        self.controller.SetNavCommand(0x2e)


    #__________________________________________________________________________
    #
    # Gate and Arm Functions for GUI
    #__________________________________________________________________________

    def on_pbArmExtend_pressed(self):
        print("Arm is Extending")
        self.controller.SetSortCommand(3)
    def on_pbArmExtend_released(self):
        self.controller.SetSortCommand(40)

    def on_pbArmRetract_pressed(self):
        print("Arm is Retracting")
        self.controller.SetSortCommand(4)
    def on_pbArmRetract_released(self):
        self.controller.SetSortCommand(40)

    def on_pbGateLift_pressed(self):
        print("Gate is Lifting")
        self.controller.SetSortCommand(5)
    def on_pbGateLift_released(self):
        self.controller.SetSortCommand(40)

    def on_pbGateLower_pressed(self):
        print("Gate is Lowering")
        self.controller.SetSortCommand(6)
    def on_pbGateLower_released(self):
        self.controller.SetSortCommand(40)

    # Explain what the robot is doing
    def updateAutoLabel(self, s):
        self.lbAuto.setText(s)


    #__________________________________________________________________________
    #
    # Block Handling Commands for GUI
    #__________________________________________________________________________

    def on_pbClearCommand_pressed(self):
        self.controller.SetSortCommand(40)

    def on_rbFullBlock_clicked(self):
        self.rbHalfBlock.setChecked(False)

    def on_rbHalfBlock_clicked(self):
        self.rbFullBlock.setChecked(False)

    def on_pbRetractAll_pressed(self):
        print("Retracting All Rows")
        if self.rbFullBlock.isChecked() == True:
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(2)
        elif self.rbHalfBlock.isChecked() == True:
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(39)
        
    def on_pbC1TE_pressed(self):
        print("Ejecting Top Row of Channel 1")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            self.controller.SetSortCommand(13)
            print("Full Block")
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(29)

    def on_pbC1TR_pressed(self):
        print("Retracting Top Row of Channel 1")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(14)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(30)

    def on_pbC1BE_pressed(self):
        print("Ejecting Bottom Row of Channel 1")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            print("Full Block")
            self.controller.SetSortCommand(21)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(37)

    def on_pbC1BR_pressed(self):
        print("Retracting Bottom Row of Channel 1")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(22)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(38)



    def on_pbC2TE_pressed(self):
        print("Ejecting Top Row of Channel 2")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            print("Full Block")
            self.controller.SetSortCommand(11)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(27)

    def on_pbC2TR_pressed(self):
        print("Retracting Top Row of Channel 2")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(12)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(28)

    def on_pbC2BE_pressed(self):
        print("Ejecting Bottom Row of Channel 2")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            print("Full Block")
            self.controller.SetSortCommand(19)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(35)

    def on_pbC2BR_pressed(self):
        print("Retracting Bottom Row of Channel 2")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(20)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(36)



    def on_pbC3TE_pressed(self):
        print("Ejecting Top Row of Channel 3")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            print("Full Block")
            self.controller.SetSortCommand(9)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(25)

    def on_pbC3TR_pressed(self):
        print("Retracting Top Row of Channel 3")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(10)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(26)

    def on_pbC3BE_pressed(self):
        print("Ejecting Bottom Row of Channel 3")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            print("Full Block")
            self.controller.SetSortCommand(17)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(33)

    def on_pbC3BR_pressed(self):
        print("Retracting Bottom Row of Channel 3")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(18)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(34)



    def on_pbC4TE_pressed(self):
        print("Ejecting Top Row of Channel 4")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            print("Full Block")
            self.controller.SetSortCommand(7)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(23)

    def on_pbC4TR_pressed(self):
        print("Retracting Top Row of Channel 4")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(8)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(24)

    def on_pbC4BE_pressed(self):
        print("Ejecting Bottom Row of Channel 4")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to eject a full block
            print("Full Block")
            self.controller.SetSortCommand(15)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to eject a half block
            print("Half Block")
            self.controller.SetSortCommand(31)

    def on_pbC4BR_pressed(self):
        print("Retracting Bottom Row of Channel 4")
        if (self.rbFullBlock.isChecked() == True):
            # Do command to retract a full block
            print("Full Block")
            self.controller.SetSortCommand(16)
        elif (self.rbHalfBlock.isChecked() == True):
            # Do command to retract a half block
            print("Half Block")
            self.controller.SetSortCommand(32)


if __name__=='__main__':
    main(BotControl)
