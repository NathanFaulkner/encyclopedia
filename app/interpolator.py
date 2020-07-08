import numpy as np
import json

svg_x_length = 500
svg_y_length = 500

cart_x_min = -10
cart_x_max = 10
cart_x_length = cart_x_max - cart_x_min

cart_y_min = -10
cart_y_max = 10
cart_y_length = cart_y_max - cart_y_min

def cart_coords_to_svg(pair):
    x = pair[0]
    y = pair[1]
    svg_x = (x-cart_x_min)*(svg_x_length/cart_x_length)
    svg_y = (cart_y_max - y)*(svg_y_length/cart_y_length)
    return svg_x, svg_y

def svg_coords_to_cart(pair):
    svg_x = pair[0]
    svg_y = pair[1]
    x = x_min + svg_x/svg_x_length*cart_x_length
    y = y_min + svg_y/svg_y_length*cart_y_length
    return x, y


def get_dict_for_svg(points):
    print('get_dict_received ', points)
    if len(points) == 1:
        p = points[0]
        out = json.dumps(dict(x1=0,
                        y1=(cart_y_length/2-p[1])*(svg_x_length/cart_x_length),
                        x2=svg_x_length,
                        y2=(cart_x_length/2-p[1])*(svg_y_length/cart_x_length)))
        #print('This is the result of the inner dump: ', out)
        out = {'shape': 'line', 'data': out}
    elif len(points) == 2:
        v0 = points[1][0] - points[0][0]
        v1 = points[1][1] - points[0][1]

        out = json.dumps(dict(x1=(p0[0]+cart_x_length/2)*(svg_x_length/cart_x_length),
                        y1=(cart_y_length/2-p0[1])*(svg_y_length/cart_y_length),
                        x2=(p0[1]+cart_x_length/2)*(svg_x_length/cart_x_length),
                        y2=(cart_x_length/2-p1[1])*(svg_y_length/cart_y_length)))
        #print('This is the result of the inner dump: ', out)
        out = {'shape': 'line', 'data': out}
    else:
        out = None
    return out


def interpolator(points):
    if len(points) == 1:
        return None
