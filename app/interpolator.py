import numpy as np
import json
import random
import sympy as sy
#import sympy

svg_x_length = 350
svg_y_length = 350

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

def cart_x_to_svg(x):
    return (x-cart_x_min)*(svg_x_length/cart_x_length)

def cart_y_to_svg(y):
    return (cart_y_max - y)*(svg_y_length/cart_y_length)

def svg_coords_to_cart(pair):
    svg_x = pair[0]
    svg_y = pair[1]
    x = cart_x_min + svg_x/svg_x_length*cart_x_length
    y = cart_y_max - svg_y/svg_y_length*cart_y_length
    return x, y

def frac_str_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        numer, denom = frac_str.split('/')
        try:
            leading, numer = numer.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(numer)/float(denom)
        return whole - frac if whole < 0 else whole + frac

def str_list_to_list_of_floats(str_list):
    a = str_list.replace('[', '')
    a = a.replace(']', '')
    a = a.split(',')
    a = [frac_str_to_float(item) for item in a]
    return a


def poly_points_from_numpy(x_points, y_points):
    x_points = cart_x_to_svg(x_points)
    y_points = cart_y_to_svg(y_points)
    poly_points = ""
    for i in range(len(x_points)):
        poly_points += f"{x_points[i]}, {y_points[i]} "
    return poly_points

def get_dict_for_svg(points):
    # print('get_dict_received ', points)
    i = 0
    # while i < len(points):
    #     if type(points[i]) == str:
    #         points[i] = points[i].replace('(', '[')
    #         # print(f'points[{i}]:', points[i])
    #         points[i] = points[i].replace(')', ']')
    #         points[i] = points[i].replace(' ', '')
    #         print(f'points[{i}]:', points[i])
    #         # exec(f'points[i]={points[i]}')
    #         points[i] = str_list_to_list_of_floats(points[i])
    #         print(f'points[{i}]:', points[i])
    #     i += 1
    if len(points) == 0:
        out = {'shape': 'none'}
    elif len(points) == 1:
        p = points[0]
        x1 = 0
        y1 = (cart_y_max-p[1])*(svg_x_length/cart_x_length)
        x2 = svg_x_length
        y2 = (cart_y_max-p[1])*(svg_y_length/cart_x_length)
        #print('This is the result of the inner dump: ', out)
        data = f"{x1},{y1} {x2},{y2}"
        data = {"points": data}
        data = json.dumps(data)
        out = {'shape': 'polyline', 'data': data}
    elif len(points) == 2:
        v = np.array([ points[1][0] - points[0][0], points[1][1] - points[0][1] ])
        diam = np.sqrt(cart_x_length**2 + cart_y_length**2)
        p = np.array(points[0])
        u0 = p - diam*v
        u1 = p + diam*v
        x1, y1 = cart_coords_to_svg(list(u0))
        x2, y2 = cart_coords_to_svg(list(u1))
        data = f"{x1},{y1} {x2},{y2}"
        data = {"points": data}
        data = json.dumps(data)
        #print('This is the result of the inner dump: ', out)
        out = {'shape': 'polyline', 'data': data}
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
        points.sort(key=lambda x: x[0])
        graph = Graph(points)
        print('piecewise:', graph.piecewise)
        if graph.piecewise == True:
            pieces = []
            x_pieces = graph.x_pieces
            y_pieces = graph.y_pieces
            k = 0
            while k < len(x_pieces):
                data = ""
                x_piece = cart_x_to_svg(x_pieces[k])
                y_piece = cart_y_to_svg(y_pieces[k])
                for i in range(len(x_piece)):
                    data += f"{x_piece[i]}, {y_piece[i]} "
                pieces.append(json.dumps({"points": data}))
                k += 1
            pieces = json.dumps(pieces)
            out = {"shape": "polyline", "pieces": pieces}
        else:
            x_points = graph.x_points
            y_points = graph.y_points
            x_points = cart_x_to_svg(x_points)
            y_points = cart_y_to_svg(y_points)
            data = ""
            for i in range(len(x_points)):
                data += f"{x_points[i]}, {y_points[i]} "
            data = {"points": data}
            data = json.dumps(data)
            out = {"shape": "polyline", "data": data}
    out['return_user_points'] = json.dumps(points)
    try:
        out['piecewise'] = json.dumps(graph.piecewise)
    except UnboundLocalError:
        out['piecewise'] = json.dumps(False)
    return out


def constant_in_x(points):
    x = points[0][0]
    i = 1
    while i < len(points) and points[i][0] == x:
        i += 1
    if i == len(points):
        return True
    return False

def repeat_in_x(points):
    x_coords = [point[0] for point in points]
    no_repeats = list(set(x_coords))
    if len(no_repeats) < len(points):
        return True
    else:
        return False

def repeated_pairs(points):
    no_repeats = list(set(points))
    if len(no_repeats) < len(points):
        return True
    else:
        return False

def check(points):
    points = list(set(tuple(point) for point in points))
    if len(points) == 1:
        return lambda x, y: y == points[0][1]
    elif constant_in_x(points):
        return lambda x, y: x == points[0][0]
    elif len(points) == 2:
        x0, y0 = points[0]
        x1, y1 = points[1]
        return lambda x, y: (y - y0)(x1 - x0) == (y1 - y0)(x - x0)
        # not finished

def all_satisfy(f, points):
    for i in range(len(points)):
        x = points[i][0]
        y = points[i][1]
        # try:
        # print(i, x, y, f(x), 'diff', abs(y-f(x)))
        if abs(y-f(x)) > 0.001:
            return False
        # except:
        #     return False
    return True

def try_linear(points):
    # points = list(set(tuple(point) for point in points))
    """Assumes points has two pairs with distinct x coords"""
    x0, y0 = points[0]
    x1, y1 = points[1]
    f = lambda x: (y1 - y0)*((x - x0)/(x1 - x0)) + y0
    x_points = np.linspace(cart_x_min, cart_x_max, 2)
    if all_satisfy(f, points):
        return {"function": f, "x_points": x_points}

def try_abs_value(points):
    # points = list(set(tuple(point) for point in points))
    i = 0
    while i < len(points):
        x0, y0 = points[i]
        if i < len(points) - 1:
            x1, y1 = points[i+1]
        else:
            x1, y1 = points[0]
        # print('try_abs_value', x0, y0, x1, y1)
        f = lambda x: (y1-y0)*abs((x-x0)/(x1-x0)) + y0
        if all_satisfy(f, points):
            x_points = np.linspace(cart_x_min, cart_x_max, 1000)
            return {"function": f, "x_points": x_points}
        i += 1

def try_quadratic(points):
    # points = list(set(tuple(point) for point in points))
    i = 0
    while i < len(points):
        x0, y0 = points[i]
        if i < len(points) - 1:
            x1, y1 = points[i+1]
        else:
            x1, y1 = points[0]
        f = lambda x: (y1-y0)*((x-x0)/(x1-x0))**2 + y0
        if all_satisfy(f, points):
            x_points = np.linspace(cart_x_min, cart_x_max, 1000)
            return {"function": f, "x_points": x_points}
        i += 1

def try_cubic(points):
    # points = list(set(tuple(point) for point in points))
    i = 0
    while i < len(points):
        x0, y0 = points[i]
        if i < len(points) - 1:
            x1, y1 = points[i+1]
        else:
            x1, y1 = points[0]
        f = lambda x: (y1-y0)*((x-x0)/(x1-x0))**3 + y0
        if all_satisfy(f, points):
            x_points = np.linspace(cart_x_min, cart_x_max, 1000)
            return {"function": f, "x_points": x_points}
        i += 1

def try_square_root(points):
    # points = list(set(tuple(point) for point in points))
    points.sort(key=lambda x: x[0])
    x0, y0 = points[0]
    x1, y1 = points[1]
    f = lambda x: (y1-y0)*((x-x0)/(x1-x0))**sy.Rational(1, 2) + y0
    if all_satisfy(f, points):
        x_points = np.linspace(x0, cart_x_max, 1000)
        return {"function": f, "x_points": x_points}
    x0, y0 = points[-1]
    x1, y1 = points[-2]
    f = lambda x: (y1-y0)*np.sqrt((x0-x)/(x0-x1)) + y0
    i = 0
    if all_satisfy(f, points):
        x_points = np.linspace(cart_x_min, x0, 1000)
        return {"function": f, "x_points": x_points}

def try_cube_root(points):
    # points = list(set(tuple(point) for point in points))
    i = 0
    while i < len(points):
        x0, y0 = points[i]
        if i < len(points) - 1:
            x1, y1 = points[i+1]
        else:
            x1, y1 = points[0]
        f = lambda x: (y1-y0)*np.cbrt((x-x0)/(x1-x0)) + y0
        if all_satisfy(f, points):
            x_points = np.linspace(cart_x_min, cart_x_max, 1000)
            return {"function": f, "x_points": x_points}
        i += 1

def try_inverse_x(points):
    # points = list(set(tuple(point) for point in points))
    points.sort(key=lambda x: x[0])
    # print('points', points)
    i = 0
    while i < len(points):
        x0, y0 = points[i]
        if i < len(points) - 1:
            x1, y1 = points[i+1]
        else:
            x1, y1 = points[0]
        a = (y1-y0)/(x0-x1)*(x1-x0+1)
        f = lambda x: a/(x-x0+1) + y0 - a
        if all_satisfy(f, points) and (x0 - 2, y0 - 2*a) in points:
            x_points = np.linspace(cart_x_min, cart_x_max, 1001)
            return {"function": f, "x_points": x_points, "horiz_shift": x0-1}
        i += 1

def try_factored_polynomial(points):
    zeroes = [p[0] for p in points if p[1] == 0]
    other_points = [p for p in points if p[1] != 0]
    if zeroes == []:
        return None
    if other_points == []:
        return None
    x = sy.Symbol('x')
    expr = 1
    for z in zeroes:
        expr *= (x-z)
    x0, y0 = other_points[0]
    try:
        a = y0/expr.subs(x, x0)
    except ZeroDivisionError:
        return None
    expr = a*expr
    f = sy.lambdify(x, expr)
    if all_satisfy(f, points):
        x_points = np.linspace(cart_x_min, cart_x_max, 1000)
        # print('points:', points)
        return {"function": f, "x_points": x_points}


# I don't think I am actually using this function....
def interpolate(points):
    points = list(set(tuple(point) for point in points))
    if repeat_in_x(points):
        return None
    if len(points) == 1:
        return lambda x: points[0][1]
    if len(points) > 1:
        if try_linear(points):
            return try_linear(points)
        if try_abs_value(points):
            return try_abs_value(points)
        if try_quadratic(points):
            return try_quadratic(points)
        if try_cubic(points):
            return try_cubic(points)
        if try_square_root(points):
            return try_square_root(points)
        if try_cube_root(points):
            return try_cube_root(points)
        if try_inverse_x(points):
            return try_inverse_x(points)
        if try_factored_polynomial(points):
            return try_inverse_x(points)

class Graph():
    def __init__(self, user_input, piecewise=False):
        self.user_input = user_input # user_input just means the user's points in Cartesian coordinates
        self.piecewise = piecewise
        self.setup()

    def setup(self):
        self.vert = False
        # points = list(set(tuple(point) for point in self.user_input))
        points = list(tuple(point) for point in self.user_input)
        # print('user points in cartesian', points)
        if (repeat_in_x(points) and len(points) == 2):
            self.vert = True
            self.as_lambda = None
        if len(points) == 1:
            f = lambda x: points[0][1]
            self.as_lambda = f
            self.x_points = np.linspace(cart_x_min, cart_x_max, 2)
            self.y_points = f(self.x_points)
        if len(points) > 1:
            if repeated_pairs(points):
                things_to_try = [try_factored_polynomial]
            else:
                things_to_try = [try_linear,
                                try_abs_value,
                                try_quadratic,
                                try_cubic,
                                try_square_root,
                                try_cube_root,
                                try_inverse_x,
                                try_factored_polynomial]
            one_of_the_things_worked_out = False
            for thing_to_try in things_to_try:
                print('I am trying ', thing_to_try)
                try:
                    if thing_to_try(points):
                        info = thing_to_try(points)
                        f = info["function"]
                        self.as_lambda = f
                        if thing_to_try == try_inverse_x:
                            a = info["horiz_shift"]
                            self.piecewise = True
                            self.x_pieces = []
                            self.y_pieces = []
                            self.x_pieces.append(np.linspace(cart_x_min, a-0.001, 500))
                            self.x_pieces.append(np.linspace(a+0.001, cart_x_max, 500))
                            print(self.x_pieces)
                            self.y_pieces.append(f(self.x_pieces[0]))
                            self.y_pieces.append(f(self.x_pieces[1]))
                            one_of_the_things_worked_out = True
                            break
                        self.x_points = info["x_points"]
                        self.y_points = f(self.x_points)
                        one_of_the_things_worked_out = True
                        break
                except:
                    pass
            if not one_of_the_things_worked_out and not self.vert:
                deg = 4
                user_x = [a[0] for a in points]
                user_y = [a[1] for a in points]
                polyinfo = np.polyfit(user_x, user_y, deg, full=True)
                p = polyinfo[0]
                R2 = polyinfo[-1]
                self.x_points = np.linspace(-10, 10, 1000)
                self.y_points = np.polyval(p, self.x_points)
                self.as_lambda = lambda x: np.polyval(p, x)

    def gen_dict_for_svg(self):
        # print('get_dict_received ', points)
        points = self.user_input
        i = 0
        # while i < len(points):
        #     if type(points[i]) == str:
        #         points[i] = points[i].replace('(', '[')
        #         # print(f'points[{i}]:', points[i])
        #         points[i] = points[i].replace(')', ']')
        #         points[i] = points[i].replace(' ', '')
        #         print(f'points[{i}]:', points[i])
        #         # exec(f'points[i]={points[i]}')
        #         points[i] = str_list_to_list_of_floats(points[i])
        #         print(f'points[{i}]:', points[i])
        #     i += 1
        if len(points) == 0:
            out = {'shape': 'none'}
            self.poly_points = ''
        elif len(points) == 1:
            p = points[0]
            x1 = 0
            y1 = (cart_y_max-p[1])*(svg_x_length/cart_x_length)
            x2 = svg_x_length
            y2 = (cart_y_max-p[1])*(svg_y_length/cart_x_length)
            #print('This is the result of the inner dump: ', out)
            data = f"{x1},{y1} {x2},{y2}"
            self.poly_points = data
            data = {"points": data}
            data = json.dumps(data)
            out = {'shape': 'polyline', 'data': data}
        elif len(points) == 2:
            v = np.array([ points[1][0] - points[0][0], points[1][1] - points[0][1] ])
            diam = np.sqrt(cart_x_length**2 + cart_y_length**2)
            p = np.array(points[0])
            u0 = p - diam*v
            u1 = p + diam*v
            x1, y1 = cart_coords_to_svg(list(u0))
            x2, y2 = cart_coords_to_svg(list(u1))
            data = f"{x1},{y1} {x2},{y2}"
            self.poly_points = data
            data = {"points": data}
            data = json.dumps(data)
            #print('This is the result of the inner dump: ', out)
            out = {'shape': 'polyline', 'data': data}
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
            self.poly_points = data
            data = {"points": data}
            data = json.dumps(data)
            out = {"shape": "polyline", "data": data}
        else:
            points.sort(key=lambda x: x[0])
            # graph = Graph(points)
            # print('piecewise:', graph.piecewise)
            if self.piecewise == True:
                pieces = []
                x_pieces = self.x_pieces
                y_pieces = self.y_pieces
                k = 0
                self.poly_points = []
                while k < len(x_pieces):
                    data = ""
                    x_piece = cart_x_to_svg(x_pieces[k])
                    y_piece = cart_y_to_svg(y_pieces[k])
                    for i in range(len(x_piece)):
                        data += f"{x_piece[i]}, {y_piece[i]} "
                    pieces.append(json.dumps({"points": data}))
                    self.poly_points.append(data)
                    k += 1
                pieces = json.dumps(pieces)
                out = {"shape": "polyline", "pieces": pieces}
            else:
                x_points = self.x_points
                y_points = self.y_points
                x_points = cart_x_to_svg(x_points)
                y_points = cart_y_to_svg(y_points)
                data = ""
                for i in range(len(x_points)):
                    data += f"{x_points[i]}, {y_points[i]} "
                self.poly_points = data
                data = {"points": data}
                data = json.dumps(data)
                out = {"shape": "polyline", "data": data}
        out['return_user_points'] = json.dumps(points)
        try:
            out['piecewise'] = json.dumps(self.piecewise)
        except UnboundLocalError:
            out['piecewise'] = json.dumps(False)
        self.svg_data = out
