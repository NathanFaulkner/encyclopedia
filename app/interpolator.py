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

def get_parameters():
    out = dict(
    cart_x_min=cart_x_min,
    cart_x_max=cart_x_max,
    cart_x_length=cart_x_length,
    cart_y_min=cart_y_min,
    cart_y_max=cart_y_max,
    cart_y_length=cart_y_length,
    svg_x_length=svg_x_length,
    svg_y_length=svg_y_length,
    )
    #out = json.dumps(out)
    return out

def cart_coords_to_svg(pair):
    x = pair[0]
    y = pair[1]
    svg_x = (x-cart_x_min)*(svg_x_length/cart_x_length)
    svg_y = (cart_y_max - y)*(svg_y_length/cart_y_length)
    return svg_x, svg_y

def svg_coords_to_cart(pair):
    svg_x = pair[0]
    svg_y = pair[1]
    x = cart_x_min + svg_x/svg_x_length*cart_x_length
    y = cart_y_min + svg_y/svg_y_length*cart_y_length
    return x, y


def get_dict_for_svg(points):
    print('get_dict_received ', points)
    if len(points) == 1:
        p = points[0]
        out = json.dumps(dict(x1=0,
                        y1=(cart_y_max-p[1])*(svg_x_length/cart_x_length),
                        x2=svg_x_length,
                        y2=(cart_y_max-p[1])*(svg_y_length/cart_x_length)))
        #print('This is the result of the inner dump: ', out)
        out = {'shape': 'line', 'data': out}
    elif len(points) == 2:
        v = np.array([ points[1][0] - points[0][0], points[1][1] - points[0][1] ])
        diam = np.sqrt(cart_x_length**2 + cart_y_length**2)
        p = np.array(points[0])
        u0 = p - diam*v
        u1 = p + diam*v
        x1, y1 = cart_coords_to_svg(list(u0))
        x2, y2 = cart_coords_to_svg(list(u1))
        out = json.dumps(dict(x1=x1, y1=y1, x2=x2, y2=y2))
        #print('This is the result of the inner dump: ', out)
        out = {'shape': 'line', 'data': out}
    elif len(points) == 3:
        points.sort(key=lambda x: x[0])
        v0 = np.array([ points[0][0] - points[1][0], points[0][1] - points[1][1] ])
        v1 = np.array([ points[2][0] - points[1][0], points[2][1] - points[1][1] ])
        diam = np.sqrt(cart_x_length**2 + cart_y_length**2)
        p = np.array(points[1])
        u0 = p + diam*v0
        u1 = p + diam*v1
        x0, y0 = cart_coords_to_svg(list(u0))
        x1, y1 = cart_coords_to_svg(points[1])
        x2, y2 = cart_coords_to_svg(list(u1))
        data = f"{x0},{y0} {x1},{y1} {x2},{y2}"
        data = {"points": data}
        data = json.dumps(data)
        out = {"shape": "polyline", "data": data}
    else:
        out = None
    return out


def interpolator(points):
    if len(points) == 1:
        return None
