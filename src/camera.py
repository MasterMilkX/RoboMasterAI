from __future__ import print_function 
import visilibity as vis
from arena_builder import a_point

# Used to plot the example
import matplotlib.pylab as plt

# Used in the create_cone function
import math


# build and validate environment
# Define an epsilon value (should be != 0.0)
epsilon = 0.0000001

scale = 1
px = 10
pixels = px*scale     #size of pixels relative to the game arena


# create cone polygon representing robot camp of vision
# five inputs(robot, radius, angle, opening, resolution).
#   'robot': is the location of robot
#   'radius': is the longitude from 'robot' camp of vision
#   'angle': is the direcction of the cone. 0 = ->
#   'resolution': is the number of degrees one point and the next in the arc.
def create_cone(robot, radio, angle, opening, resolution=1):

	# Define the list for the points of the cone-shape polygon
	p=[]
	
	# The fisrt point will be the vertex of the cone
	p.append(robot)

	# Define the start and end of the arc
	start = angle - opening
	end = angle + opening
	
	for i in range(start, end, resolution):
		
		# Convert start angle from degrees to radians
		rad = math.radians(i)
		
		# Calculate the off-set of the first point of the arc
		x = radio*math.cos(rad)
		y = radio*math.sin(rad)
		
		# Add the off-set to the vertex point
		new_x = robot.x() + x
		new_y = robot.y() + y
		
		# Add the first point of the arc to the list
		p.append( vis.Point(new_x, new_y) )
	
	# Add the last point of the arc
	rad = math.radians(end)
	x = int(radio*math.cos(rad))
	y = int(radio*math.sin(rad))
	new_x = robot.x() + x
	new_y = robot.y() + y
	p.append( vis.Point(new_x, new_y) )
	
	return vis.Polygon(p)

#make a cone with points without any offset
def base_cone(radio, angle, opening,resolution=1):
	p = [(0,0)]

	# Define the start and end of the arc
	start = angle - opening
	end = angle + opening
	
	for i in range(start, end, resolution):
		
		# Convert start angle from degrees to radians
		rad = math.radians(i)
		
		# Calculate the off-set of the first point of the arc
		x = int(radio*math.cos(rad))
		y = int(radio*math.sin(rad))
		
		# Add the first point of the arc to the list
		p.append((x,y))

	return p

def make_base_cone(angle):
	return base_cone(25*pixels,(angle-90)%360,40,20)

def make_robot_cone(robot):
	return create_cone(a_point(robot.x,robot.y),25*pixels,(robot.rot-90)%360,40,20)

def make_robot_360(robot,env):
	return vis.Visibility_Polygon(a_point(robot.x,robot.y), env, epsilon)


#robot can see another robot with its camera/cone
def i_see_you(enemy, vision360, cone):
	enemypt = a_point(enemy.x,enemy.y)
	if enemypt._in(vision360, epsilon) and enemypt._in(cone, epsilon):
		return True
	
#enemy robot can see this robot from its positioning
def you_see_me(enemy, vision360):
	enemypt = a_point(enemy.x,enemy.y)
	if enemypt._in(vision360, epsilon):
		return True
	