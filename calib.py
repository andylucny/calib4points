import numpy as np
import cv2

img = np.zeros((480,640,3),np.uint8)

ideal = [(0,0),(200,0),(200,200),(0,200)]
real = [(300,100),(600,200),(500,400),(350,300)]

for i in range(4):
    cv2.line(img,ideal[i],ideal[(i+1)%4],(0,0,255),1)
    cv2.line(img,real[i],real[(i+1)%4],(0,255,0),1)

ideal = np.array(ideal,np.float32)
real = np.array(real,np.float32)

def triangle(pts,p):
    global pt, pp, a, b, c, d
    pt = pts
    pp = p
    a = pts[1]-pts[0]
    b = pts[2]-pts[0]
    c = np.linalg.solve(np.array([a,b]).T,p-pts[0])
    d = np.array([1-c[0]-c[1],c[0],c[1]])
    #print(pts.T@d.T,p) # == 
    return d
       
def project(x,y):
    global q, n, k
    n = (real[2]-real[0])[::-1]*np.array([-1,1])
    q = - n@real[0]
    if n@np.array([x,y])+q <= 0:
        k = triangle(real[:3],np.array([x,y]))
        #print(real[:3].T@k.T,np.array([x,y])) # ==
        return tuple(np.asarray(ideal[:3].T@k.T,np.int32))
    else:
        k = triangle(real[[2,3,0]],np.array([x,y]))
        #print(real[1:].T@k.T,np.array([x,y])) # ==
        return tuple(np.asarray(ideal[[2,3,0]].T@k.T,np.int32))

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
