from tkinter.colorchooser import askcolor
import tkinter as tk
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from numpy import loadtxt


"""
This code starts GUI which allows you to make your own colormap from scratch and test it!
It is at least a bit faster than typing it by hands ... it helped me
However, it is my first time with tkinter, so it is not perfect for sure :)
"""

given_data = loadtxt('example.txt')


def _from_rgb(rgb):
    """
    This function changes rgb (0-255) to hex which is needed for askcolor
    :param rgb: touple of rgb color (0-255)
    :return: str with hex color
    """
    return "#%02x%02x%02x" % rgb

def hex_to_rgb(value):
    """
    This function changes hex to rgb (0-255)
    :param value: strin with hex color
    :return: touple with rgb (0-255)
    """
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_decimal(rgb):
    """
    This function changes rgb (0-255) to rgb (0-1)
    :param rgb: rgb touple color (0-255)
    :return: rgb touple color (0-1)
    """
    new_rgb = []
    for i in range(3):
        new_rgb.append(rgb[i]/255)
    return tuple(new_rgb)

def prepare_one_row(i, colors = (255,255,255)):
    """
    This function makes one row of widgets in left frame (button, color box, rgb and checkbox)
    """
    checkbox_value[i] = tk.IntVar(root, 1)
    b1 = tk.Checkbutton(frame1, width=1, variable=checkbox_value[i])
    checkbox_list[i] = b1
    b1.grid(row=next_row_frame1 + 1 + i, column=4, sticky='news')

    b2 = tk.Button(frame1, text=i + 1)
    b2['command'] = lambda arg=i: open_color_chooser(arg)
    button_list[i] = b2
    b2.grid(row=next_row_frame1 + 1 + i, column=0, sticky='news', columnspan=1, padx=5)

    color_list[i] = _from_rgb(colors)
    bc = tk.Label(frame1, text='o', bg=color_list[i], fg=color_list[i])
    squere_list[i] = bc
    bc.grid(row=next_row_frame1 + 1 + i, column=1, sticky='news', padx=5, pady=3)

    b3 = tk.Label(frame1, text='%i %i %i'%(colors[0], colors[1],colors[2]))
    entry_list[i] = b3
    b3.grid(row=next_row_frame1 + 1 + i, column=2, sticky='news', columnspan=1)


def labels_rows():
    """
    This funtion labels widgets in left frame
    """
    l1 = tk.Label(frame1, text='Select')
    destruct_them_list[0] = l1
    l1.grid(row=next_row_frame1, column=0, sticky='news')

    l2 = tk.Label(frame1, text='RGB')
    destruct_them_list[1] = l2
    l2.grid(row=next_row_frame1, column=1, sticky='news', columnspan=2)

    l3 = tk.Label(frame1, text='Use')
    destruct_them_list[2] = l3
    l3.grid(row=next_row_frame1, column=3, sticky='news', columnspan=2)

    l4 = tk.Button(frame1, text='Make a colorbar!', command=draw_cmap)
    l4.grid(row=next_row_frame1 + 2 + len(button_list), column=0, columnspan=5, pady=5, sticky='news')
    destruct_them_list[3] = l4

def first_global_variables():
    """
    This function prepares all necessary variables for other functions
    """
    global button_list, entry_list, checkbox_list, checkbox_value, color_list, squere_list, destruct_them_list, first_time
    checkbox_list = {}
    button_list = {}
    squere_list = {}
    checkbox_value = {}
    entry_list = {}
    color_list = {}
    destruct_them_list = {}
    first_time = False

def destroy_some_widgets(i):
    """
    This function destroy unused widgets
    """
    button_list[i].destroy()
    entry_list[i].destroy()
    squere_list[i].destroy()
    checkbox_list[i].destroy()
    del button_list[i], entry_list[i], squere_list[i], checkbox_list[i], color_list[i]

def how_many_colors():
    """
    This function initiate most of the widgets in left frame
    It reads number from entry widget and make a loop over all needed rows
    It also prepares many useful global variables used via other functions
    """
    global new_label, button_list, entry_list, checkbox_list, checkbox_value, color_list
    global squere_list, destruct_them_list, first_time

    if not first_time:
        for i in range(len(destruct_them_list)):
            destruct_them_list[i].destroy()
            del destruct_them_list[i]


        if int(color_number.get()) >= len(button_list):
            remove_only = []
        else:
            remove_only = range(int(color_number.get()), len(button_list))


        for i in remove_only:
            i = int(i)
            destroy_some_widgets(i)


    try:
        if first_time:
            first_global_variables()
            loop_take = range(int(color_number.get()))


        else:
            if len(remove_only) == 0:
                loop_take = range(len(button_list), int(color_number.get()))
            else:
                loop_take = []

        for i in loop_take:
            prepare_one_row(i)
        labels_rows()

        try: new_label.destroy()
        except: pass
    except:
        new_label = tk.Label(frame1, text='This is not a number!')
        new_label.grid(row=2, columnspan=2, column=0)

def retrive_old_cmap():
    """
    This function reads values from big textbox in right frame in order to retrive old colormap
    It makes all necessary global viariables as well, and make sure there is no old widgets on the lists
    """
    global button_list, entry_list, checkbox_list, checkbox_value, color_list, squere_list, first_time, destruct_them_list

    if first_time:
        first_global_variables()
    else:
        for i in range(len(destruct_them_list)):
            destruct_them_list[i].destroy()
            del destruct_them_list[i]
        for i in range(len(button_list)):
            destroy_some_widgets(i)

    old = result_cmap.get('1.0', 'end').split(')')
    old_color_list = []
    for i in range(len(old)):
        if len(old[i])>2:
            color = old[i].split('(')
            for j in range(len(color)):
                if len(color[j])>2:
                    old_one = list(map(float,color[j].split(',')))
                    old_one = [int(o*255) for o in old_one]
                    old_color_list.append(tuple(old_one))
    del old_one, old, color


    for i in range(len(old_color_list)):
        prepare_one_row(i, old_color_list[i])
    labels_rows()

def open_color_chooser(i):
    """
    This function opens new window for choosing color
    Then it changes the values in dictionaries, to make the color appear
    :param i: is the key in dictionary
    """
    color_i = askcolor()
    if color_i[0] != None and color_i[1] != None:
        color_list[i] = _from_rgb(color_i[0])

        bc = tk.Label(frame1, text='o', bg=color_list[i], fg=color_list[i])
        squere_list[i] = bc
        bc.grid(row=next_row_frame1 + 1 + i, column=1, sticky='news', padx=5, pady=3)

        b3 = tk.Label(frame1, text=color_i[0])
        entry_list[i] = b3
        b3.grid(row=next_row_frame1 + 1 + i, column=2, sticky='news', columnspan=1)

def draw_cmap():
    """
    This function prepares new color map and draws examplary data in middle frame
    """
    cols = []
    for i in range(len(color_list)):
        if checkbox_value[i].get():
            cols.append(rgb_to_decimal(hex_to_rgb(color_list[i])))
    cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list("",
        cols)
    norm = matplotlib.colors.Normalize(vmin = 0, vmax = 1)
    cb = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap1, norm=norm)
    ax.pcolor(given_data,cmap = cmap1)
    ax2.set_yticks([], [])
    canvas.draw()
    result_cmap.delete("1.0","end")
    cols = ['(%s, %s, %s)'%(c[0],c[1],c[2]) for c in cols]
    cols = ', '.join(cols)
    result_cmap.insert('end',cols)


first_time = True

# Initiate the GUI
root = tk.Tk()
root.title('Colormap chooser')

# Left frame (basic entry and rows of widgets)
frame1 = tk.Frame(root)
frame1.columnconfigure(0, weight = 1)

text_colors = tk.Label(frame1, text='How many colors do you want to use?')
text_colors.grid(row = 0, column = 0, sticky='news', columnspan=5)

color_number = tk.Entry(frame1)
color_number.grid(row=1, column=0,  sticky='news', padx = 10, pady = 10, columnspan=3)


button1_main_grid = tk.Button(frame1, text='Show them!', command= how_many_colors)
button1_main_grid.grid(row=1, column= 3, sticky='news', padx = 10, pady = 10, columnspan=2)

frame1.pack(side=tk.LEFT, anchor=tk.NW)

next_row_frame1 = 2

# Middle frame (examplary plot and colorbar)
frame2 = tk.Frame(root)

frame2.pack(side=tk.LEFT, anchor=tk.N, padx=20)

fig = Figure(figsize=(3,3), dpi = 300)
ax = fig.add_subplot(111)
ax.set_title('Examplary data')
ax.set_position(pos=[0., 0.01, 0.9, 0.9])
ax.set_yticks([],[])
ax.set_xticks([],[])
ax2 = fig.add_axes([0.91,0.01,0.08,0.9])
ax2.set_yticks([],[])
ax2.set_xticks([],[])


canvas = FigureCanvasTkAgg(fig, master=frame2)
canvas.get_tk_widget().pack()

# Right frame (textbox with result cmap and retriving option)

frame3 = tk.Frame(root)
frame3.pack(side=tk.LEFT, anchor=tk.N, padx=10)

text_retrive = tk.Label(frame3, text='Here is your result cmap!')
text_retrive.grid(row = 0, column = 0, sticky='news', columnspan=5,padx = 10)

text_retrive = tk.Label(frame3, text='You can also paste here old cmap to retrive it: (r,g,b), (r,g,b), (r,g,b)...')
text_retrive.grid(row = 1, column = 0, sticky='news', columnspan=5,padx = 10)


button2_main_grid = tk.Button(frame3, text='Retrive old cmap!', command= retrive_old_cmap)
button2_main_grid.grid(row=2, column= 0, sticky='news', padx = 10, pady = 3, columnspan=5)

result_cmap = tk.Text(frame3,width=15, height=13)
result_cmap.insert('end','(1.0, 1.0, 1.0), (0.5882352941176471, 0.5882352941176471, 0.5882352941176471), (0.3254901960784314, 0.25882352941176473, 0.9176470588235294),'
                         '(0.08235294117647059, 0.047058823529411764, 0.4117647058823529), (0.01568627450980392, 0.00784313725490196, 0.09019607843137255), (0.0, 0.0, 0.0)')
result_cmap.grid(row=3, column=0, columnspan=5, sticky='news',pady=10, padx=10)

root.mainloop()
