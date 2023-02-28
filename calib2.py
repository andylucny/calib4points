# dedicated to be rewritten into C#
import numpy as np
import cv2

img = np.zeros((480,640,3),np.uint8)

ideal = [(0,0),(200,0),(200,200),(0,200)]
real = [(300,100),(600,200),(500,400),(350,300)]

for i in range(4):
    cv2.line(img,ideal[i],ideal[(i+1)%4],(0,0,255),1)
    cv2.line(img,real[i],real[(i+1)%4],(0,255,0),1)

def determinant(a1,a2,a3,a4):
    return a1*a4 - a2*a3
    
def solve(A,B):
    det = determinant(A[0][0],A[1][0],A[0][1],A[1][1])
    x = determinant(B[0],A[1][0],B[1],A[1][1])/det
    y = determinant(A[0][0],B[0],A[0][1],B[1])/det
    return x, y

def triangle(pts,p):
    a = (pts[1][0]-pts[0][0],pts[1][1]-pts[0][1])
    b = (pts[2][0]-pts[0][0],pts[2][1]-pts[0][1])
    c = (p[0]-pts[0][0],p[1]-pts[0][1])
    d = solve([a,b],c)
    return (1-d[0]-d[1],d[0],d[1])
    
def dot(pts,k):
    return (pts[0][0]*k[0]+pts[1][0]*k[1]+pts[2][0]*k[2],pts[0][1]*k[0]+pts[1][1]*k[1]+pts[2][1]*k[2])
    
def round(t):
    return (int(t[0]),int(t[1]))
       
def project(x,y):
    n = ([real[0][1]-real[2][1],real[2][0]-real[0][0]])
    q = - (n[0]*real[0][0]+n[1]*real[0][1])
    if n[0]*x+n[1]*y+q <= 0:
        k = triangle([real[0],real[1],real[2]],(x,y))
        return round(dot([ideal[0],ideal[1],ideal[2]],k))
    else:
        k = triangle([real[2],real[3],real[0]],(x,y))
        return round(dot([ideal[2],ideal[3],ideal[0]],k))

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
