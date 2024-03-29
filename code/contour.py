import cv2 as cv
import numpy as np
import math
import serial
from picamera2 import Picamera2

point = [] 
global mask
point_detec = 280
point_tron = 230
point_vuong = 145
point_tam_giac = 60
index_point: int = 0
height:int 
width: int

def draw_red_circle(event, x, y, flags, param):
    global point_tron, point_detec, point_vuong, point_tam_giac, index_point
    
    if event == cv.EVENT_LBUTTONDBLCLK:
        center = (x, y)
        print(center)
        radius = 1
        color = (0,0,255)
        thickness = 1
        cv.circle(img, center, radius, color, thickness)
        if index_point == 0:
            point_detec = y
        elif index_point == 1:
            point_tron = y
        elif index_point == 2:
            point_vuong = y
        elif index_point == 3:
            point_tam_giac = y
        cv.line(img, (0, y), (width - 1, y), (255,0, 0), 3) 

    
    elif event == cv.EVENT_RBUTTONDBLCLK:
        index_point = (index_point + 1) % 4
        print(index_point)

class item:
    id: int
    shape: int
    center: list
    
    count_tam_giac = 0
    count_vuong = 0
    count_tron = 0
    count_unknow = 0
    
    count_ignore = 10
    is_update = 0
    
    is_detected = 0
    
    is_push = 0
    def __init__(seft, id, center):
        seft.shape = 0
        seft.is_push = 0
        
        seft.id = id
        
        seft.center = center
    
    def show(seft):
        output = "id: " + str(seft.id)
        output += ", shape: " + str(seft.shape)
        output += ", center: (" + str(seft.center[0]) + ":" + str(seft.center[1]) + ")"
        output += ", ignore: " + str(seft.count_ignore)
        # output += ", is_update: " + str(seft.is_update)
        print(output)
    def detect_object_many_times(seft, shape):
        if seft.is_detected == 1:
            return
        
        if shape == 3:#TAM_GIAC
            seft.count_tam_giac += 1
            seft.count_vuong = 0
            seft.count_tron = 0
            
            if seft.count_tam_giac >= 3:
                if seft.shape == 0:#UNKNOW
                    seft.shape = 3 #TAM GIAC
                    count_unknow = 0
                elif ((seft.shape == 4) | (seft.shape == 5)):
                    seft.count_unknow += 1
                    if seft.count_unknow >= 2:
                        seft.shape = 0 #UNKNOW
                        seft.count_vuong = 0
                        seft.count_tam_giac = 0
                        seft.count_tron = 0
                    
        elif shape == 4:#VUONG
            seft.count_vuong += 1
            seft.count_tam_giac = 0
            seft.count_tron = 0
            
            if seft.count_vuong >= 3:
                if seft.shape == 0: #UNKNOW
                    seft.shape = 4 #VUONG
                    count_unknow = 0
                elif ((seft.shape == 3) | (seft.shape == 5)):
                    seft.count_unknow += 1
                    if seft.count_unknow >= 2:
                        seft.shape = 0 #UNKNOW
                        seft.count_vuong = 0
                        seft.count_tam_giac = 0
                        seft.count_tron = 0
                    
        elif shape == 5:#TRON
            seft.count_tron += 1
            seft.count_vuong = 0
            seft.coung_tam_giac = 0
            
            if seft.count_tron >= 3:
                if seft.shape == 0: #UNKNOW
                    seft.shape = 5 #TRON
                elif ((seft.shape == 3) | (seft.shape == 4)):
                    seft.count_unknow += 1
                    count_unknow = 0
                    if seft.count_unknow >= 2:
                        seft.shape = 0 #UNKNOW
                        seft.count_vuong = 0
                        seft.count_tam_giac = 0
                        seft.count_tron = 0
        
items: list[item] = []
id = 0       


#--------------------------------------------------
    


def convert_approx_to_list(approx) -> list:
    arr = []
    for i in approx:
        x = i[0][0]
        y = i[0][1]
        arr.append((x, y))
    return arr


def expression_of_line(point1: tuple, point2: tuple) -> tuple:
    #ax + by + c = 0
    u_vector = (point2[0] - point1[0], point2[1] - point1[1])
    n_vector = (-u_vector[1], u_vector[0])
    a = n_vector[0]
    b = n_vector[1]
    #ax + by + c = 0
    # -> c = -ax - by
    c = -a*point1[0] - b*point1[1]
    return (a, b, c)


def distance_from_point_to_line(point: tuple, expression_line: tuple) -> float:
    a = expression_line[0]
    b = expression_line[1]
    c = expression_line[2]
    
    tu = a*point[0] + b*point[1] + c
    if tu < 0:
        tu = -tu
    mau_square = a*a + b*b
    mau = math.sqrt(mau_square)
    
    return tu/mau


        
def distance_from_middle_point_to_line(point1:tuple, point2:tuple, point3:tuple) -> float:
    line = expression_of_line(point1, point3)
    distance = distance_from_point_to_line(point2, line)
    return distance


def filter_for_remove_vectecx(arr: list) -> int:
    
    # print(f"Array input in function filter_for_remove_vectecx is: {arr}")
    
    number_of_vertecx = len(arr)
    
    for i in range(number_of_vertecx):
        
        before = i - 1
        after = (i + 1) % len(arr)
        distance = distance_from_middle_point_to_line(arr[before], arr[i], arr[after])
        
        distance_bound = 10
        if distance < distance_bound:
            #print(f"Distance from {arr[i]} to line {arr[before]} -> {arr[after]} is: {distance}")
            #print(f"Remove {arr[i]} because distace small less than {distance_bound}")
            arr.remove(arr[i])
            
            return filter_for_remove_vectecx(arr)
    
    return number_of_vertecx
        

#getContours according area
def getContours(img, img_contour):
    global items
    global id
    
    contours, _ = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    #print("##############################")
    
    list_contours_object = []
    list_contours_shape = []
    for cnt in contours:
        area = cv.contourArea(cnt)
        if ((area > 200) & (area < 5000)):
            cv.drawContours(img_contour, cnt, -1, (255, 0, 0), 2)
            
            peri = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.02*peri, True)
            
            x, y, w, h = cv.boundingRect(approx)
            cv.rectangle(img_contour, (x, y), (x+w, y+h), (0,0,255), 2)
            
            center = [x+int(w/2), y+int(h/2)]
            cv.circle(img_contour, tuple(center), 1, (0,0,255), 2)
 
            shape: int = 0
            
            if len(approx) >= 8:  shape = 5
            else: 
                arr = convert_approx_to_list(approx)
                # print(f"List of points: {arr}")
                shape = filter_for_remove_vectecx(arr)
            
            new_object = item(id, center)
            list_contours_object.append(new_object)
            list_contours_shape.append(shape)
            
   # if len(list_contours_object) != 0:
   #     print("-------------")
   #     print(f"Len of list_countours_object: {len(list_contours_object)}")
    
    for object in items:
        min_distance:int = 9999
        index_min_distance: int = 9999
    #    print(f"ITEM: {object.center}")
        
        for i in range(len(list_contours_object)):
            
            distance =  object.center[1] - list_contours_object[i].center[1]
    #        print(f"\tDistance: {distance}")
            if distance < 0:
                continue
            if min_distance >= distance:
                index_min_distance = i
                min_distance = distance
                
     #   print(f"index_min_distance: {index_min_distance}")
        if min_distance < 20:
            min_object = list_contours_object[index_min_distance]
            
     #       print(f"\tUpdate with new object: {min_object.center}")
            if object.is_detected == 0:
                shape = list_contours_shape[index_min_distance]
                object.detect_object_many_times(shape)
                
            object.center = min_object.center
            object.is_update = 1
            cv.putText(img_contour, f"{object.shape}, {object.id}",
                   tuple(object.center), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1)
            list_contours_object.remove(min_object)
            
            
    
    #if len(items) != 0:
    #    print(f"Len of items: {len(items)}")
    
    for new_object in list_contours_object:
        #add item into list       
        #if new_object.center[1] > point_detec:
        #    print(f"In region detected: {new_object.center[1]}")
        if new_object.center[1] < point_detec:
            #print(f"New Object {new_object.center[1]} out region detect")
            continue
        new_object.is_update = 1
        id += 1
        items.append(new_object)
        # print(f"Put text in {(x,y)} with id: {new_object.id}")
        cv.putText(img_contour, f"{new_object.shape}, {new_object.id}",
                       tuple(new_object.center), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0,0,0), 1)
        #else:
        #    print(f"Out region detected: {new_object.center[1]}")
    
    items_remove = []
    for i in range(len(items)):
        object = items[i]
        if object.is_update == 0:
            items[i].count_ignore -= 1
            if items[i].count_ignore <= 0:
                items_remove.append(object)
        else:
            items[i].count_ignore = 10
            items[i].is_update = 0
            
    for i in items_remove:
        items.remove(i)
    #if len(items) == 0:
    #    return
    #print("Contours")
    #for i in items:
    #    print(f"shape: {i.shape}, center: {i.center[1]}, is_detected: {i.is_detected}, ignore: {i.count_ignore}")
    #print("------------------")
    #for i in items:
    #    i.show()    
            
    #print("##############################")
    
def nothing(x):
    pass


def checkThrough(data_serial):
    #if len(items) == 0:
    #    return
    #print(f"Len items: {len(items)}")
    for item in items:
        if item.is_detected == 1:
            if item.is_push == 1:
                continue
            
            if item.shape == 3:
                if ((item.center[1] <= point_tam_giac + 10) & (item.center[1] >= point_tam_giac - 10)):
                    item.is_push = 1
                    print("Day tam giac")
                    data_serial.write("3\r".encode())
                    item.show()    
            elif item.shape == 4:
                if ((item.center[1] <= point_vuong + 10) & (item.center[1] >= point_vuong - 10)):
                    item.is_push = 1
                    print("Day vuong")
                    data_serial.write("2\r".encode())
                    item.show()    
            elif item.shape == 5:
                if ((item.center[1] <= point_tron + 10) & (item.center[1] >= point_tron - 10)):
                    item.is_push = 1
                    print("Day tron")
                    data_serial.write("1\r".encode())
                    item.show()    
        else:#item hasn't detected
            if ((item.center[1] <= point_detec + 10) & (item.center[1] >= point_detec - 10)):
                item.is_detected = 1
                print("Detected item: ")
                item.show()    
            
if __name__ == "__main__":
    #init camera
    cap = Picamera2()
    cap.preview_configuration.main.size = (640,480)
    cap.preview_configuration.main.format = "RGB888"
    cap.preview_configuration.controls.FrameRate = 30
    cap.preview_configuration.align()
    cap.configure("preview")
    cap.start()

    #init uart
    data_serial = serial.Serial("/dev/ttyUSB0", 9600)
    
    img = cap.capture_array()[50:450:, 250:320]
    height, width, _ = img.shape
    
    #object_detector = cv.createBackgroundSubtractorMOG2()
    object_detector = cv.createBackgroundSubtractorKNN()
    
    while True:

        img = cap.capture_array()[50:450:, 250:320]

        img_contour = img.copy()
        detec = object_detector.apply(img)
        _, detec = cv.threshold(detec,190,255,cv.THRESH_BINARY)
        blur = cv.GaussianBlur(detec,(5,5),0)
        ret3,detec = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)


        cv.imshow("Anh Detec", detec)
        
        getContours(detec, img_contour)
        checkThrough(data_serial)
        
        cv.line(img_contour, (0, point_detec), (width - 1, point_detec), (255,0, 0), 3) 
        cv.line(img_contour, (0, point_tron), (width - 1, point_tron), (255,0, 0), 3) 
        cv.line(img_contour, (0, point_vuong), (width - 1, point_vuong), (255,0, 0), 3) 
        cv.line(img_contour, (0, point_tam_giac), (width - 1, point_tam_giac), (255,0, 0), 3) 
        
        cv.imshow("Anh Contour", img_contour)
        
        if cv.waitKey(1) == ord('q'):
            break
    cv.destroyAllWindows()
        
