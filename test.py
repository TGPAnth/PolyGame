import math
from math import pi

def gradus2rad(a):
  return a*pi/180

def rad2gradus(a):
  return a*180/pi

a = -50
b = -130

c = math.asin(math.sin(gradus2rad(a)))
d = math.asin(math.sin(gradus2rad(a)))
print rad2gradus(c)
print rad2gradus(d)

print 