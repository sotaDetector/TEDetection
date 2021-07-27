from LOTcommunication.SerialConnector import serialCommu
from tedCore.objectTracking.sot.sot_siameseRPN import SiameseRPNModule
import threading
import cv2
import time
serialCom = serialCommu()

object_th=0

base_change_tag=0
up_change_tag=0
commandFlag=-1
counter=0
def calServoAngle():
    global now_base_servo, now_up_servo,window_center_x,window_center_y,base_change_tag,up_change_tag,commandFlag

    while True:
        time.sleep(0.05)
        if object_th > 0.5:
            offset_x = window_center_x - object_center_x
            offset_y = window_center_y - object_center_y
            if offset_x>40:
                base_change_tag=1

            if offset_x<-40:
                base_change_tag=-1

            if offset_y>40:
                up_change_tag=-1

            if offset_y<-40:
                up_change_tag=1

            if base_change_tag==1 and up_change_tag==1:
                commandFlag=1
            elif base_change_tag==1 and up_change_tag==0:
                commandFlag=2
            elif base_change_tag==1 and up_change_tag==-1:
                commandFlag=3
            elif base_change_tag==0 and up_change_tag==1:
                commandFlag=4
            elif base_change_tag==0 and up_change_tag==-1:
                commandFlag=6
            elif base_change_tag==-1 and up_change_tag==1:
                commandFlag=7
            elif base_change_tag==-1 and up_change_tag==0:
                commandFlag=8
            elif base_change_tag==-1 and up_change_tag==-1:
                commandFlag=9

            if commandFlag!=-1:
                serialCom.sendData(commandFlag)
                print("servo update", commandFlag);
            commandFlag = -1
            base_change_tag = 0
            up_change_tag = 0




counter=0
if __name__ == "__main__":
    serialCom.sendData(0)

    configPath = "../../excellentDependency/mmtracking/configs/sot/siamese_rpn/siamese_rpn_r50_1x_lasot.py"
    weightPath = "../../resources/modelWeights/siamese_rpn_r50_1x_lasot_20201218_051019-3c522eff.pth"
    siameseSot = SiameseRPNModule(configPath, weightPath)
    siameseSot.setupDatasource(1, 0)

    siameseSot.startTracking()
    threading.Thread(target=calServoAngle).start()

    frame_width,frame_height=siameseSot.getCapSize()
    window_center_x=int(frame_width/2)
    window_center_y=int(frame_height/2)
    while True:
        detResult=siameseSot.getDctFrameData()
        if detResult is not None:
            box_tracking = detResult.dctResult["bbox"]
            object_th=detResult.dctResult["score"]

            if object_th==None:
                object_th=0

            left_top_x=int(box_tracking[0])
            left_top_y=int(box_tracking[1])
            rigth_buttom_x=int(box_tracking[2])
            rigth_buttom_y=int(box_tracking[3])
            object_center_x=left_top_x+int((rigth_buttom_x-left_top_x)/2)
            object_center_y=left_top_y+int((rigth_buttom_y-left_top_y)/2)

            showImg=detResult.dctImg
            cv2.circle(showImg,(window_center_x,window_center_y), 4, (0, 255, 255), cv2.FILLED)
            cv2.circle(showImg,(object_center_x,object_center_y),3,(0,0,255),cv2.FILLED)
            cv2.imshow("tracking", showImg)


        if cv2.waitKey(1) & 0xFF == ord('s'):
            siameseSot.reselectTracking()
