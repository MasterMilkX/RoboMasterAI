from __future__ import print_function 
import visilibity as vis

# Used to plot the example
import matplotlib.pylab as plt

# Used in the create_cone function
import math

ym = 28
y_size = 28


#build the outer boundary of the polygon
def outer(y_up, y_down, x_left, x_right): ## use arena coordinates

    #list points ccw
    a = vis.Point(x_left, y_size - (y_down - 1))    
    b = vis.Point(x_right, y_size - (y_down - 1))
    c = vis.Point(x_right, y_size - (y_up - 1))
    d = vis.Point(x_left, y_size - (y_up - 1))

    # Values for graph
    wall_x = [a.x(), b.x(), c.x(), d.x(), a.x()]
    wall_y = [a.y(), b.y(), c.y(), d.y(), a.y()]
    
    # Create the outer boundary polygon
    walls = vis.Polygon([a, b, c, d])
    
    return wall_x, wall_y, walls
    

#build the polygon holes
def hole(y_up, y_down, x_left, x_right): ## use arena coordinates
    
    #points are listed in cc order
    #list points cw
    a = vis.Point(x_left, y_size - (y_down-1))
    b = vis.Point(x_left, y_size - (y_up-1))
    c = vis.Point(x_right, y_size - (y_up-1))
    d = vis.Point(x_right, y_size - (y_down-1))
        
    # values for graph\
    hole_x = [a.x(), b.x(), c.x(), d.x(), a.x()]
    hole_y = [a.y(), b.y(), c.y(), d.y(), a.y()]
    
   # Create the hole polygon
    hole = vis.Polygon([a, b, c, d])
    
    return hole_x, hole_y, hole


#point location (for robots)
def a_point(x,y): #input arena coordinates
    return vis.Point(x, y_size - (y - 1))   

def make_arena_polygon():
    #build center diamond polygon
    #list points cw
    p1 =vis.Point(23, ym-16)
    p2 =vis.Point(22, ym-15)
    p3 =vis.Point(22, ym-13)
    p4 =vis.Point(23, ym-12)
    p5 =vis.Point(25, ym-12)
    p6 =vis.Point(26, ym-13)
    p7 =vis.Point(26, ym-15)
    p8 =vis.Point(25, ym-16)


    # Load the values of the hole polygon in order to draw it later
    diam_x = [p2.x(), p3.x(), p4.x(), p5.x(), p6.x(), p7.x(), p8.x(), p1.x(), p2.x()]
    diam_y = [p2.y(), p3.y(), p4.y(), p5.y(), p6.y(), p7.y(), p8.y(), p1.y(), p2.y()]

    # Create the hole polygon
    diam = vis.Polygon([p2, p3, p4, p5, p6, p7, p8, p1])

    #build the arena
    wall_x, wall_y, walls = outer(28,2,1,47)  #y_up, y_down, x_left, x_right, use arena format


    #format y_up, y_down, x_left, x_right, use arena format
    huecos_input = [[ ym-6,  ym-7,  1,  7],     #
                    [ym-12,   ym-14, 10, 14],   #
                    [ym-20,   ym-26, 9, 11],    #
                    [ ym-5,    ym-7, 21, 27],   #
                    [ym-19,   ym-21, 21, 27],  #
                    [ym-12,   ym-14, 34, 38], 
                    [ym-19, ym-20, 41, 47],  #
                    [ ym,    ym-6, 37, 39],  #
                   ]
    huecos = []
    for item in huecos_input:
        huecos.append(hole(item[0], item[1], item[2], item[3]))


    # Create environment, wall will be the outer boundary because
    # is the first polygon in the list. The other polygons will be holes

    arena_poly = vis.Environment([walls, 
                           huecos[0][2], 
                           huecos[1][2], 
                           huecos[2][2], 
                           huecos[3][2], 
                           huecos[4][2], 
                           huecos[5][2], 
                           huecos[6][2], 
                           huecos[7][2], 
                           diam])


    return arena_poly, [[wall_x,wall_y],[huecos[0][0], huecos[0][1]],[huecos[1][0], huecos[1][1]],[huecos[2][0], huecos[2][1]],[huecos[3][0], huecos[3][1]],[huecos[4][0], huecos[4][1]],[huecos[5][0], huecos[5][1]],[huecos[6][0], huecos[6][1]],[huecos[7][0], huecos[7][1]],[diam_x, diam_y]]
