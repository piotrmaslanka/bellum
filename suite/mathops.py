from random import gauss
from math import sin, cos, radians, sqrt, pow
def polar_to_cartesian(r, theta):
    return (r * cos(radians(theta)), r * sin(radians(theta)))

def getStandarizedGauss():
    while True:
        x = gauss(0, 1)
        if (x < 2) and (x > -2): break
    return x / 2

def distance(x1, y1, x2, y2):
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def polarcs_distance(r1, theta1, r2, theta2):
    x1, y1 = polar_to_cartesian(r1, theta1)
    x2, y2 = polar_to_cartesian(r2, theta2)
    return distance(x1, y1, x2, y2)
def minmax(a, b):
    '''A is min, B is max'''
    if a > b: return (b, a)
    else: return (a, b)

def det33(a, b, c, d, e, f, g, h, i):
    return a * e * i + b * f * g + d * h * c - c * e * g - b * d * i - f * h * a
def sgn(x):
    if x >= 0: return 1
    else: return -1
def sgnz(x):
    if x > 0: return 1
    elif x < 0: return -1
    return 0
def do_segments_intersect(x11, y11, x21, y21, x12, y12, x22, y22):
    a = (x11, y11)
    b = (x21, y21)
    c = (x12, y12)
    d = (x22, y22)
    if (a == c) and not (b == d):
        return False
    if (b == d) and not (a == c):
        return False
    if sgnz(det33(x12, y12, 1, x22, y22, 1, x11, y11, 1)) <> sgnz(det33(x12, y12, 1, x22, y22, 1, x21, y21, 1)):
        if sgnz(det33(x11, y11, 1, x21, y21, 1, x12, y12, 1)) <> sgnz(det33(x11, y11, 1, x21, y21, 1, x22, y22, 1)):
            return True
    return False