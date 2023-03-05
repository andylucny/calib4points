import numpy as np
import cv2

img = np.zeros((480,640,3),np.uint8)

ideal = [(0,0),(200,0),(200,200),(0,200)]
real = [(300,100),(600,200),(500,400),(350,300)]

for i in range(4):
    cv2.line(img,ideal[i],ideal[(i+1)%4],(0,0,255),1)
    cv2.line(img,real[i],real[(i+1)%4],(0,255,0),1)

ideal = np.array(ideal,np.float32)
idealavg = np.average(ideal,axis=0)
idealstd = np.std(ideal,axis=0)
ideal = (ideal - idealavg)/idealstd

real = np.array(real,np.float32)
realavg = np.average(real,axis=0)
realstd = np.std(real,axis=0)
real = (real - realavg)/realstd

def softmax(v):
    ev = np.exp(v)
    return ev / np.sum(ev)
       
def project(x,y):
    q = (np.array([x,y],np.float32)-realavg)/realstd
    d = 0.5
    c = softmax(q@real.T/d)
    p = c@ideal
    return tuple(np.asarray(p*idealstd+idealavg,np.int32))

x = 0
y = 0
def mouseHandler(event, _x, _y, flags, param):
    global x, y
    x = _x
    y = _y
    
cv2.namedWindow("projection")
cv2.setMouseCallback("projection", mouseHandler)

while True:
    disp = np.copy(img)
    x2, y2 = project(x,y)
    cv2.circle(disp,(x,y),2,(0,255,0),cv2.FILLED)
    cv2.circle(disp,(x2,y2),2,(0,0,255),cv2.FILLED)
    
    cv2.imshow("projection",disp)
    if cv2.waitKey(10) == 27:
        break
    
cv2.destroyAllWindows()
