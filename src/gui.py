import PySimpleGUI as sg
import time
import stone_class as sc
import player_class as pc
import random



# SIZE OF BOARD
MAX_ROWS = MAX_COL = 19


# Import assets :

st_black = './assets/stone_black2.png'
st_white = './assets/stone_white.png'
board_dots = './assets/board_dot_big.png'
exit_button = './assets/exit_button.png'
stone_white_UI = './assets/stone_white_UI.png'
stone_black_UI = './assets/stone_black_UI.png'
board_dot = './assets/board_dot.png'

layout = []

# Exit button :
# This is stupid bad, haha 
layout += [[sg.Text("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", background_color='white')] \
          + [sg.Button(image_filename=exit_button, button_color=('white', 'white'),border_width=0, key='Exit')]]

# Bigger dot board positions
board_dot_pos = [( 3,3), (3,9), (3,15), (9,3), (9,9), (9,15), (15,3), (15,9), (15,15)]


# Initialize GUI board :
b = []
for i in range(MAX_ROWS):
    a = []

    # 2 choices for display :
    # grid : " | \n-----|-----\n | "
    # interpunct : u"\xb7"

    for j in range(MAX_COL):
        if (i,j) in board_dot_pos:
            a += [sg.Button("", button_color=('black', 'white'), 
                            image_filename=board_dots, border_width=0,
                            size=(4,2), key=(i,j), pad=(0,0))]
        else:
            a += [sg.Button("", image_filename=board_dot, button_color=('black', 'white'),
                            border_width=0 ,size=(4,2), key=(i,j), pad=(0,0))]
    b += [a]

layout += b


# Captured UI elements :

layout[14] += [sg.Text("\t", background_color='white')] \
              + [sg.Button(image_filename=stone_black_UI, border_width=0)] \
              + [sg.Text("   Captured : ", background_color='white', text_color='black', font='lato')] \
              + [sg.Text("",key='-UI1-', background_color='white',text_color='black', font='lato')]


layout[15] += [sg.Text("\t", background_color='white')] \
               + [sg.Button(image_filename=stone_white_UI, border_width=0)] \
               + [sg.Text("   Captured : ", background_color='white', text_color='black', font='lato')] \
               + [sg.Text("", background_color='white', key='-UI2-', text_color='black', font='lato')]

# Debug window :
layout2 = [[sg.Multiline("Debug initialized", key='-MULTILINE KEY-', size=(60,40))]]


# Initialize windows :

window = sg.Window('GO', layout, background_color='white', no_titlebar=True,
                    grab_anywhere=True, resizable=True).Finalize()

window2 = sg.Window("Debugger", layout2, resizable=True, grab_anywhere=True,
                    keep_on_top=True, alpha_channel=0.7, background_color='white').Finalize()


# Initialize players :
white = pc.player('w')
black = pc.player('b')

# Capture stones
def capture_stones(group):
    if group is not None:
        if len(group[2]) > 1:
            for nb in group[2]:
                window[(nb.x, nb.y)].Update(image_filename=board_dot) 
            if group[0]=='w' : white.captured += group[1]
            elif group[0]=='b' : black.captured += group[1]
        elif len(group[2]) == 1:
            window[(group[2][0].x, group[2][0].y)].Update(image_filename=board_dot) 
            if group[0]=='w' : white.captured += group[1]
            elif group[0]=='b' : black.captured += group[1]



# Make the keys in the matrix indexes and than access them.
move_idx = 1

# Event loop
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if window[event]:
        if move_idx % 2 == 0:
            a = time.time()

            if window[event].Key not in sc._pl_st:
                # If a stone is not already played in that spot. 
                window[event].update(button_color=('white', 'white'), image_filename=st_white)

                # Play stone :
                st = white.play(window[event].Key)

                # Search for capture in self and neighbours :
                temp = white.capture(st)
                for group in temp:
                    capture_stones(group) 

                # Update the capture UI element :
                window['-UI1-'].update(str(white.captured))

                # Update debugger :
                window2['-MULTILINE KEY-'].print("------------------------")

                from stone_class import debug_buffer
                for i in debug_buffer:
                    window2['-MULTILINE KEY-'].print(i)
                
                move_idx += 1

            else:
                window2['-MULTILINE KEY-'].print("Illigal move.")

            # Calculate and display time elapsed.
            b = time.time()
            window2['-MULTILINE KEY-'].print("\nTime Elapsed :" + str(b-a))
            debug_buffer.clear()


        else:
            a = time.time()

            if window[event].Key not in sc._pl_st:
                window[event].update("", button_color=('white', 'white'), image_filename=st_black)

                # Play stone :
                st = black.play(window[event].Key)

                # Search for capture in self and neighbours :
                temp = black.capture(st)
                for group in temp:
                    capture_stones(group)
        
                # Update the capture UI element :
                window['-UI2-'].update(str(black.captured))

               # Update debugger :
                window2['-MULTILINE KEY-'].print("------------------------")

                from stone_class import debug_buffer
                for i in debug_buffer:
                    window2['-MULTILINE KEY-'].print(i)
                
                move_idx += 1

            elif move_idx == 1:
                window[event].update("", button_color=('white', 'white'), image_filename=st_black)

                # Play stone :
                st = black.play(window[event].Key)

                # Search for capture in self and neighbours :
                temp = black.capture(st)
                for group in temp:
                    capture_stones(group)
        
                # Update the capture UI element :
                window['-UI2-'].update(str(black.captured))

               # Update debugger :
                window2['-MULTILINE KEY-'].print("------------------------")

                from stone_class import debug_buffer
                for i in debug_buffer:
                    window2['-MULTILINE KEY-'].print(i)
                
                move_idx += 1

            else:
                window2['-MULTILINE KEY-'].print("Illigal move.")


            # Calculate and display time elapsed :
            b = time.time()
            window2['-MULTILINE KEY-'].print("\nTime Elapsed :" + str(b-a))
            debug_buffer.clear()




window.close()
