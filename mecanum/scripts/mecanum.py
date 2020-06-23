import matplotlib.pyplot as plt
from matplotlib.patches import Arc, RegularPolygon
import numpy as np
from numpy import radians as rad
import math

class Mecanum(object):
  def __init__(self, a, b, R):
    self.a = a;
    self.b = b;
    self.R = R;

  def ik(self, vx, vy, vw):
    J = np.array([[1, -1, -1*(self.a + self.b)],
                  [1,  1,  1*(self.a + self.b)],
                  [1,  1, -1*(self.a + self.b)],
                  [1, -1,  1*(self.a + self.b)]])
    V = np.array([vx, vy, vw]).reshape(-1, 1)
    W = 1/self.R * np.dot(J, V).ravel()
    return W[0], W[1], W[2], W[3]

  def plot(self, vx, vy, vw, w1, w2, w3, w4):
    fig, ax = plt.subplots()

    v1 = w1/(2*self.R*math.pi)
    v2 = w2/(2*self.R*math.pi)
    v3 = w3/(2*self.R*math.pi)
    v4 = w4/(2*self.R*math.pi)
    pw = np.array([[self.a *  1, self.b *  1, v1, 0],
                   [self.a *  1, self.b * -1, v2, 0],
                   [self.a * -1, self.b *  1, v3, 0],
                   [self.a * -1, self.b * -1, v4, 0]])
    X, Y, U, V = zip(*pw)
    #ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=10)
    ax.quiver(X, Y, U, V, color="blue")
    ax.quiver(0, 0, vx, vy, color="green")
    self.drawCirc(ax, 0.5, 0, 0, np.degrees(np.arctan2(vy, vx)), np.degrees(vw), "red")

    plt.xticks(np.linspace(-2, 2, 5))
    plt.yticks(np.linspace(-2, 2, 5))
    plt.show()

  def drawCirc(self, ax,radius,centX,centY,angle_,theta2_,color_='black'):
    #========Line
    arc = Arc([centX,centY],radius,radius,angle=angle_,
          theta1=0,theta2=theta2_,capstyle='round',linestyle='-',lw=1,color=color_)
    ax.add_patch(arc)

    #========Create the arrow head
    endX=centX+(radius/2)*np.cos(rad(theta2_+angle_)) #Do trig to determine end position
    endY=centY+(radius/2)*np.sin(rad(theta2_+angle_))

    ax.add_patch(                    #Create triangle as arrow head
      RegularPolygon(
        (endX, endY),            # (x,y)
        1,                       # number of vertices
        radius/9,                # radius
        rad(angle_+theta2_),     # orientation
        color=color_
      )
    )
    #ax.set_xlim([centX-radius,centX+radius]) and ax.set_ylim([centY-radius,centY+radius]) 
    # Make sure you keep the axes scaled or else arrow will distort

if __name__ == '__main__':
  m = Mecanum(0.48544, 0.253, 0.1524)
  vx = 0.2
  vy = 0.2
  vw = 0
  w1, w2, w3, w4 = m.ik(vx, vy, vw)
  print(w1, w2, w3, w4)
  m.plot(vx, vy, vw, w1, w2, w3, w4)
