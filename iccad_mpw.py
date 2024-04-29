#!/usr/bin/env python
"""For IC fabrication demo showing dice projection on wafer,
also with demos on Python basic elements and using GUI in Python
"""
# I used 'autopep8' to convert code to be PEP8 compliant,
# but some places look not so concise as before, so modified a little
# for github re-post in 03/18/2024

# use Tkinter in Python 2, but tkinter in Python 3
import tkinter as tk
import turtle


def sdist(x, y):
    '''Return squared distance with respect to the (0, 0) origin,
    which is the center of wafer
    '''
    return x * x + y * y

def fully_outside(x, y, w, h, radius):
    '''Judge whether a rectangle is fully outside a circle;
    the circle's center is on (0,0), and has a radius.
    '''
    R2 = radius * radius
    # can we remove '\' here?
    if sdist(x, y) > R2 and sdist(x + w - 1, y) > R2 \
            and sdist(x, y + h - 1) > R2 \
            and sdist(x + w - 1, y + h - 1) > R2:
        return True
    else:
        return False

def filed_size(plan):
    max_length = 0 
    max_height = 0
    for t in plan:
        if(t[0]+t[2]>max_length):
            max_length = t[0]+t[2]
        if(t[1]+t[3]>max_height):
            max_height = t[1]+t[3]
    return (max_length,max_height)

def touch_edge(x,y,w,h,x_c,y_c,radius):
    dot_list = ((x-x_c,y-y_c),(x-x_c,y-y_c+h),(x-x_c+w,y-y_c),(x-x_c+w,y-y_c+h))
    out_circle = 0
    for dot in dot_list:
        if(sdist(dot[0],dot[1])>radius**2):
            if(out_circle * 1 == -1):
                return True
            out_circle = 1
        else:
            if(out_circle * -1 == -1):
                return True
            out_circle = -1
    return False

def on_button_click():
    # 这里定义按钮被点击时要执行的函数
    label.config(text="按钮被点击了!")


def mpw(l):
    ''' Return the desired field width and height in a tuple 'wrap',
    and return all dice's x/y/w/h information in list l.
    the information in list 'planned' could be automatically generated
    by a die placement optimizer, but here we just give a plan for demo.
    wrap has the dimensions of boundary box of all planned dice.
    '''
    planned = [(0, 0, 15, 15),
               (15, 0, 15, 10),
               (15, 10, 8, 8),
               (0, 15, 4, 5),
               (5, 15, 4, 5),
               (10, 15, 5, 5),
               (25, 12, 5, 7)]
    wrap = filed_size(planned) #what does wrap mean here,wrap has the dimensions of boundary box of all planned dice. 
    # let us try to automatically generate 'wrap' in homework
    for t in planned:
        l.append(t)
    # would you try use 'l = planned' to replace the 2 lines above?

    return wrap

def field(width=30, height=30, diameter=300, detail=False):
    '''Expose many fields on wafer by stepper,
    each field has width, height; each wafer has a specified diameter
    the default diameter value=300 indicates a 12 inch wafer
    when setting argument detail=True:
        argument width and height have no meanings in this case.
        mpw() returns a list of die positions and dimensions,
        then each die inside each field is finely drawn 
    the wafer center might be on a field center or on field corner
    but here to demonstrate Python list, we just implement the latter
    '''
    root = tk.Tk()
    radius = int(diameter / 2)
    x_c = 1.5 * radius
    y_c = 1.25 * radius
    cv = tk.Canvas(root, bg='white', width=2*x_c, height=2*y_c) # 指定背景框

    # draw a wafer, its center is on canvas center, r=radius
    cv.create_oval(x_c - radius, y_c - radius,
                   x_c + radius, y_c + radius, outline='red')  #通过四个点创建一个椭圆
    cv.pack()

    if detail:
        dice_list = []
        # # when detail is True, field width and height are over-set by mpw()
        (width, height) = mpw(dice_list)

    # expose all fields below. first generate a list of tuples,
    # which contains 4 quadrants' field left-bottom corners x/y
    # copying from one quadrant can easily keep field placement symmetry
    x_list = [x for x in range(0, radius, width)]
    y_list = [y for y in range(0, radius, height)]

    xy_list = [(x, y) for x in x_list for y in y_list] \
        + [(-x - width, y) for x in x_list for y in y_list] \
        + [(-x - width, -y - height) for x in x_list for y in y_list] \
        + [(x, -y - height) for x in x_list for y in y_list]

    field_count = 0
    for (x, y) in xy_list:
        if not fully_outside(x, y, width, height, radius):
            cv.create_rectangle(x_c + x, y_c + y,
                                x_c + x + width, y_c + y + height, width=1)
            field_count += 1

            # next, draw all mpw dice in detail. for each field,
            # the given x/y coordinates from mpw() are drawn
            if detail:
                for (xx, yy, ww, hh) in dice_list:
                    x1 = x_c + x + xx
                    y1 = y_c + y + yy
                    if(touch_edge(x1,y1,ww,hh,x_c,y_c,radius)):
                        cv.create_rectangle(x1, y1, x1 + ww, y1 + hh,outline="red")
                    else:
                        cv.create_rectangle(x1, y1, x1 + ww, y1 + hh)

    print("Actual field width and height = %d, %d;" % (width, height))
    print("Total actually stepping fields = %d;" % field_count)
    # However, there might be some fields barely-touched wafer edge,
    # and which could be left for fine tuning in homework later

    root.mainloop()


def show_mpw(n=10):
    ''' Show the MPW arrangement in detail with adjusting scale 'n'
    Usage: show_mpw() or show_mpw(n=value)
    '''
    # get mpw information
    singleMPW = []
    (w, h) = mpw(singleMPW)

    root = tk.Tk()
    cv = tk.Canvas(root, bg='white', width=20+w*n, height=20+h*n)# 指定显示框大小
    cv.pack()

    # initialize position setting
    xcor = 10
    ycor = 10

    cv.create_rectangle(xcor, ycor,
                        xcor + w * n, ycor + h * n, fill='lightgrey') # create the rectangle

    for (x, y, w, h) in singleMPW:
        x1 = xcor + x * n
        y1 = ycor + y * n
        cv.create_rectangle(x1, y1, x1+w*n, y1+h*n, width=3)

    # 创建标签，用于显示按钮点击后的信息
    label = tk.Label(root, text="点击按钮!")
    label.pack()

    # 创建按钮，指定点击时调用的函数
    button = tk.Button(root, text="点击我", command=on_button_click)
    button.pack()

    # 进入主事件循环，这使得窗口可以实时响应用户的交互
    root.mainloop()

# Let us try all commands below, one by one
# It is easier in an interactive environment to run commands together

# show_mpw()
# field()
# field(24,28,200)
# field(30,20)
field(detail=True)
# 创建标签，用于显示按钮点击后的信息
label = tk.Label(root, text="点击按钮!")
label.pack()
# field(detail=True, diameter=450)
# Let us try another dice floor plan
# (try using vim to copy them up and remove # signs on line beginnings)
#    planned = [(0, 0, 15, 15), \
#         (15, 0, 10, 15), \
#         (0, 15, 8, 8), \
#         (8, 15, 5, 4), \
#         (8, 19, 5, 4), \
#         (13, 15, 5, 5), \
#         (18, 15, 7, 5)]
#
#    wrap = (25, 23)
# also try to automatically generate 'wrap' as required in homework
