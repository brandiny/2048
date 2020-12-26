import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image
import random
import math

# fix blurry font
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


class MainProgram(tk.Tk):
    """This class is the program skeleton - the Tk object"""
    def __init__(self):
        # initialise Tk object
        tk.Tk.__init__(self)

        # program window variables
        self.GAME_WINDOW_CAPTION = '2048 - Python Version'
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 700

        # system wide controls
        self.slide_up_control = 'Up'
        self.slide_down_control = 'Down'
        self.slide_left_control = 'Left'
        self.slide_right_control = 'Right'

        # initialise window frame and spawn window
        self.title(self.GAME_WINDOW_CAPTION)
        self.minsize(self.GAME_WIDTH, self.GAME_HEIGHT)
        self.geometry('{}x{}'.format(self.GAME_WIDTH, self.GAME_HEIGHT))
        self.center_screen(self.GAME_WIDTH, self.GAME_HEIGHT)

        # initialise all program wide fonts
        self.DESCRIPTION_FONT = Font(family="Helvetica", size=12)
        self.BUTTON_FONT = Font(family="Helvetica", size=16)
        self.TITLE_FONT = Font(family="Helvetica", size=28, weight='bold')

        # create the master frame
        self.GAME_MARGIN_X = 0
        self.GAME_MARGIN_Y = 0
        self.container = tk.Frame(self)
        self.container.pack(padx=self.GAME_MARGIN_X, pady=self.GAME_MARGIN_Y)

        # memory to hold the pointer to the current frame rendered
        self.current_frame = None

        # initialise by showing the main menu page
        self.show_frame(MainMenu)

    def center_screen(self, window_width, window_height):
        """centers the spawned screen"""
        offset_right = int(self.winfo_screenwidth()/2 - window_width/2)
        offset_down = int((self.winfo_screenheight()-40)/2 - window_height / 2)

        self.geometry('+{}+{}'.format(offset_right, offset_down))

    def show_frame(self, frame_class):
        """displays given frame class in parameter: e.g. show_frame(MainMenu)"""
        if self.current_frame is not None:
            self.current_frame.destroy()

        frame = frame_class(self.container, self)
        frame.grid(row=0, column=0, sticky='news')
        self.current_frame = frame


class MainMenu(tk.Frame):
    """Main menu frame object"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=controller.GAME_WIDTH, height=controller.GAME_HEIGHT)
        self.controller = controller

        # create canvas
        self.create_canvas()

        # display background onto the canvas
        self.display_background('background.png')

        # create button frame which holds menu buttons
        button_frame = tk.Frame(self, width=250, height=250)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_propagate(False)

        # create menu buttons
        menu_button1 = tk.Button(button_frame, text='New Game', command=lambda: controller.show_frame(MainGame))
        menu_button2 = tk.Button(button_frame, text='Load Game', command=lambda: controller.show_frame(MainGame))
        menu_button3 = tk.Button(button_frame, text='Instructions', command=lambda: controller.show_frame(Instructions))
        menu_button4 = tk.Button(button_frame, text='Controls', command=lambda: controller.show_frame(Controls))
        buttons = [menu_button1, menu_button2, menu_button3, menu_button4]

        # grid buttons into the button frame
        for index, button in enumerate(buttons):
            button_frame.grid_rowconfigure(index, weight=1)
            button.config(font=controller.BUTTON_FONT)
            button.config(borderwidth=3)
            button.grid(row=index, column=0, sticky='news')

        # display button frame on canvas
        # increase pixels_below_center: push the menu buttons lower on the GUI
        pixels_below_center = 130
        self.display_object_on_canvas(
            button_frame,
            controller.GAME_WIDTH // 2 - 0.5*button_frame['width'],
            controller.GAME_HEIGHT // 2 - 0.5*button_frame['height'] + pixels_below_center)

    def create_canvas(self):
        """Renders a canvas onto the frame - covering the whole frame"""
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def display_background(self, image_path):
        """Given a path to an image - it draws this image onto the frame canvas"""
        # draws and paints the background with image of given path
        background_image = Image.open(image_path)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        """Given object and X,Y coordinates, it draws it onto the frame canvas"""
        button1_window = self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)


class Instructions(tk.Frame):
    """This class is the instructions frame"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white', width=controller.GAME_WIDTH, height=controller.GAME_HEIGHT)
        self.pack_propagate(False)
        self.controller = controller

        # create canvas
        self.create_canvas()

        # display background
        self.display_background('instructionsbackground.png')

        # display the main instructions
        instructions_label = tk.Label(
            self,
            bg='white',
            wrap=600,
            anchor=tk.W,
            justify=tk.LEFT,
            text="""2048 is a game where you combine numbered tiles in order to gain a higher numbered tile. In this game you start with two tiles, the lowest possible number available is two. Then you will play by combining the tiles with the same number to have a tile with the sum of the number on the two tiles.

The default controls for the game are the arrow keys, however this can be changed in the controls section of the game.
            """,
            font=controller.DESCRIPTION_FONT)

        self.display_object_on_canvas(
            instructions_label,
            controller.GAME_WIDTH // 2 - 0.5 * instructions_label.winfo_reqwidth(),
            controller.GAME_HEIGHT // 2 - 0.5 * instructions_label.winfo_reqheight() + 120)

        # display the back button
        back_button_instructions = tk.Button(
            self,
            text='Back to menu',
            font=controller.BUTTON_FONT,
            command=lambda: controller.show_frame(MainMenu)
        )

        self.display_object_on_canvas(
            back_button_instructions,
            controller.GAME_WIDTH - back_button_instructions.winfo_reqwidth() - 30,
            controller.GAME_HEIGHT - back_button_instructions.winfo_reqheight() - 30
        )

    def create_canvas(self):
        """Renders a canvas onto the frame - covering the whole frame"""
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def display_background(self, imagepath):
        """Given a path to an image - it draws this image onto the frame canvas"""
        background_image = Image.open(imagepath)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        """Given object and X,Y coordinates, it draws it onto the frame canvas"""
        button1_window = self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)


class Controls(tk.Frame):
    """This class is the controls frame"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=controller.GAME_WIDTH, height=controller.GAME_HEIGHT)
        self.controller = controller
        self.pack_propagate(False)

        # boolean showing if the user in the process of binding?
        self.is_binding = False

        # create canvas
        self.create_canvas()

        # display background
        self.display_background('controlsbackground.png')

        # display the main instructions
        instructions_label = tk.Label(
            self,
            bg='white',
            wrap=600,
            anchor=tk.W,
            justify=tk.LEFT,
            text="""To change a control, click on the current value and input a key. To cancel the process, re-click it.""",
            font=controller.DESCRIPTION_FONT)

        self.display_object_on_canvas(
            instructions_label,
            controller.GAME_WIDTH // 2 - 0.5 * instructions_label.winfo_reqwidth(),
            instructions_label.winfo_reqheight() + 220)

        # display the input field grid 2x4 table (columns, rows)
        table_border_width = 2
        table_border_color = 'black'
        table_2x4 = tk.Frame(self, width=550, height=220, bg=table_border_color)
        table_2x4.grid_columnconfigure(0, weight=1)
        table_2x4.grid_columnconfigure(1, weight=1)
        table_2x4.grid_propagate(0)

        # create the LEFT HAND COLUMN labels: which show which column the user is changing
        control_up_label = tk.Label(table_2x4, text='Slide tiles up')
        control_down_label = tk.Label(table_2x4, text='Slide tiles down')
        control_left_label = tk.Label(table_2x4, text='Slide tiles left')
        control_right_label = tk.Label(table_2x4, text='Slide tiles right')

        # grid the LEFT HAND COLUMN
        control_labels = [control_up_label, control_down_label, control_left_label, control_right_label]
        for index, label in enumerate(control_labels):
            table_2x4.grid_rowconfigure(index, weight=1)
            label.config(
                bg='white',
                anchor=tk.W,
                justify=tk.LEFT,
                font=controller.DESCRIPTION_FONT
            )

            if index == 0:
                label.grid(row=index, column=0, sticky='news', pady=(table_border_width, table_border_width), padx=(table_border_width, 0))

            else:
                label.grid(row=index, column=0, sticky='news', pady=(0, table_border_width), padx=(table_border_width, 0))

        def initialise_control_button(button, button_save_string):
            """
            Given a button object, and its purpose (left, right, up, down),
            Change the text on the button back to normal and,
            Exit the binding state
            """

            # change the text back to black (from red)
            button['fg'] = 'black'

            # for each case of control, change its text back to what was stored.
            if button_save_string == 'left':
                if controller.slide_left_control in ('Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_left_control + ' arrow key'

                else:
                    button['text'] = controller.slide_left_control

            elif button_save_string == 'right':
                if controller.slide_right_control in ('Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_right_control + ' arrow key'

                else:
                    button['text'] = controller.slide_right_control

            elif button_save_string == 'up':
                if controller.slide_up_control in ('Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_up_control + ' arrow key'

                else:
                    button['text'] = controller.slide_up_control

            elif button_save_string == 'down':
                if controller.slide_down_control in ('Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_down_control + ' arrow key'

                else:
                    button['text'] = controller.slide_down_control

        # given button and which KEY it controls, it changes self variable storage
        def switch_keys(button, button_save_string):
            """
            Given a button,
            and which command it controls
            """

            def unbind_keys(button):
                """Stop collecting keystrokes for this button by unbinding arrow keys + letter keys"""
                button.unbind('<Key>')
                button.unbind('<Left>')
                button.unbind('<Up>')
                button.unbind('<Right>')
                button.unbind('<Down>')

            def set_command_for(string, command):
                """
                Given a command direction (left, right, up, down),
                and a keystroke symbol (a, b, return, up, down ... etc)
                It saves this command to the MainProgram variables
                """

                button['fg'] = 'black'
                if string == 'left':
                    controller.slide_left_control = command

                elif string == 'right':
                    controller.slide_right_control = command

                elif string == 'up':
                    controller.slide_up_control = command

                elif string == 'down':
                    controller.slide_down_control = command

            # given a key event, it sets the commands to it and changes button text
            def key(event):
                """
                Given a key event (collecting from tk.bind method)
                THAT IS NOT AN ARROW KEY
                and this key is not SPACE
                change text on BUTTON
                save EVENT
                stop COLLECTING, and exit BINDING
                """
                nonlocal button_save_string
                self.is_binding = False
                try:
                    if event.keysym == 'space':
                        initialise_control_button(button, button_save_string)
                        return
                    button['text'] = str(event.keysym)
                    set_command_for(button_save_string, event.keysym)

                except Exception:
                    if event.char == 'space':
                        initialise_control_button(button, button_save_string)
                        return
                    button['text'] = str(event.char)
                    set_command_for(button_save_string, event)

                unbind_keys(button)


            def arrow_key(event):
                """
                Given a key event (collecting from tk.bind method)
                that is an ARROW KEY
                and this key is not SPACE
                change text on BUTTON
                save EVENT
                stop COLLECTING, and exit BINDING
                """
                set_command_for(button_save_string, event.keysym)
                button['text'] = event.keysym + ' arrow key'
                unbind_keys(button)


            def set_to_current_value():
                """
                Exits binding and resets the text on the button to the original key
                """
                self.is_binding = False
                button['fg'] = 'black'
                nonlocal button_save_string
                if button_save_string == 'left':
                    if controller.slide_left_control in ('Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_left_control + ' arrow key'

                    else:
                        button['text'] = controller.slide_left_control

                elif button_save_string == 'right':
                    if controller.slide_right_control in ('Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_right_control + ' arrow key'

                    else:
                        button['text'] = controller.slide_right_control

                elif button_save_string == 'up':
                    if controller.slide_up_control in ('Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_up_control + ' arrow key'

                    else:
                        button['text'] = controller.slide_up_control

                elif button_save_string == 'down':
                    if controller.slide_down_control in ('Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_down_control + ' arrow key'

                    else:
                        button['text'] = controller.slide_down_control

            """
            BEGIN MAIN LOGIC FLOW FOR THIS FUNCTION - after all nested functions declared
            """

            # If clicked and already in binding state, untoggle the button and exit binding.
            if button['text'] == 'Enter new key':
                set_to_current_value()
                unbind_keys(button)
                self.is_binding = False
                return

            # If clicked and another command is already in binding state, don't do anything
            elif self.is_binding:
                return

            # Otherwise, display the 'enter new key' option in red and begin binding
            else:
                button['text'] = 'Enter new key'
                button['fg'] = 'red'
                self.is_binding = True

            # Move the focus of the program to the button and start collecting button clicks
            button.focus_set()
            button.bind('<Key>', key)
            button.bind('<Left>', arrow_key)
            button.bind('<Up>', arrow_key)
            button.bind('<Right>', arrow_key)
            button.bind('<Down>', arrow_key)

            def useless_function(event):
                pass

            # Ignore any space key presses.
            button.bind('<space>', useless_function)

        # Allow all the inputs to have this switch_key function on click
        # Initialise buttons with any saved buttons.
        control_up_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_up_input, 'up'))
        initialise_control_button(control_up_input, 'up')

        control_down_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_down_input, 'down'))
        initialise_control_button(control_down_input, 'down')

        control_left_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_left_input, 'left'))
        initialise_control_button(control_left_input, 'left')

        control_right_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_right_input, 'right'))
        initialise_control_button(control_right_input, 'right')

        # Grid the RIGHT HAND COLUMN of the 2x4 grid
        control_inputs = [control_up_input, control_down_input, control_left_input, control_right_input]
        for index, item in enumerate(control_inputs):
            table_2x4.grid_rowconfigure(index, weight=1)

            item.config(
                bg='white',
                borderwidth=0,
                font=controller.DESCRIPTION_FONT,
                justify='center'
            )

            if index == 0:
                item.grid(row=index, column=1, sticky='news', pady=(table_border_width, table_border_width), padx=(table_border_width, table_border_width))

            else:
                item.grid(row=index, column=1, sticky='news', pady=(0, table_border_width), padx=(table_border_width, table_border_width))

        # display the packed canvas
        self.display_object_on_canvas(
            table_2x4,
            controller.GAME_WIDTH // 2 - 0.5*table_2x4.winfo_reqwidth(),
            table_2x4.winfo_reqheight() + 140)

        # display the back button
        back_button_instructions = tk.Button(
            self,
            text='Save and go back to menu',
            font=controller.BUTTON_FONT,
            command=lambda: self.preliminary_check_controls()
        )

        self.display_object_on_canvas(
            back_button_instructions,
            controller.GAME_WIDTH - back_button_instructions.winfo_reqwidth() - 30,
            controller.GAME_HEIGHT - back_button_instructions.winfo_reqheight() - 30
        )

        # declare the error msg empty
        self.error_msg = tk.Label(
            self,
            text='',
            wraplength=200,
            width=20,
            height=3,
            justify=tk.LEFT,
            bg='white',
            fg='red'
        )

    def preliminary_check_controls(self):
        """
        Perform checks on the validity of keys entered,
        and if all checks passed -
        exit and show_frame(MainMenu)
        """

        # is the program still in a binding state?
        if self.is_binding:
            self.error_msg['text'] = 'You are still binding'
            self.display_object_on_canvas(
                self.error_msg,
                50,
                self.controller.GAME_HEIGHT - self.error_msg.winfo_reqheight() - 15
            )

        # are the controls set all unique?
        elif len({
            self.controller.slide_up_control,
            self.controller.slide_down_control,
            self.controller.slide_left_control,
            self.controller.slide_right_control
        }) != 4:
            self.error_msg['text'] = 'All controls must be unique'
            self.display_object_on_canvas(
                self.error_msg,
                50,
                self.controller.GAME_HEIGHT - self.error_msg.winfo_reqheight() - 15
            )

        # all tests passed?
        else:
            # save to file - do this

            # move to main menu frame
            self.controller.show_frame(MainMenu)

    def create_canvas(self):
        """Renders a canvas onto the frame - covering the whole frame"""
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def display_background(self, imagepath):
        """Given a path to an image - it draws this image onto the frame canvas"""
        background_image = Image.open(imagepath)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        """Given object and X,Y coordinates, it draws it onto the frame canvas"""
        button1_window = self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)

    def remove_object_from_canvas(self, tk_object):
        """Given object memory pointer, it DELETES it from the frame canvas"""
        self.canvas.delete(tk_object)


class MainGame(tk.Frame):
    """This class is the 2048 game frame"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=controller.GAME_WIDTH, height=controller.GAME_HEIGHT)
        self.controller = controller

        # create the grid frame
        self.GRID_WIDTH = 600
        self.TILES_PER_ROW = 4

        self.main_grid = tk.Frame(self, width=self.GRID_WIDTH, height=self.GRID_WIDTH, bg='black')
        self.main_grid.grid_propagate(0)

        # set the width of each row and column
        for i in range(self.TILES_PER_ROW):
            # document bug weight 1: do this
            self.main_grid.grid_columnconfigure(i, minsize=self.GRID_WIDTH // 4)
            self.main_grid.grid_rowconfigure(i, minsize=self.GRID_WIDTH // 4)

        # place it on screen
        self.main_grid.place(
            x=controller.GAME_WIDTH // 2 - self.main_grid.winfo_reqwidth() * 0.5,
            y=0)

        # generate the grid values (matrix of values)
        self.main_grid_values = [
            [0]*self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)
        ]

        # initiate by spawning 2 two's and rendering the frame
        self.add_two()
        self.add_two()
        self.update_grid()

        # set the focus onto the game frame, and bind the controls
        self.focus_set()
        self.bind('<{}>'.format(controller.slide_left_control), self.push_left)
        self.bind('<{}>'.format(controller.slide_right_control), self.push_right)
        self.bind('<{}>'.format(controller.slide_up_control), self.push_up)
        self.bind('<{}>'.format(controller.slide_down_control), self.push_down)

        # add the score text
        self.score_text = tk.Label(self, text='SCORE:', font=controller.BUTTON_FONT)
        self.score_text.place(
            x=30,
            y=controller.GAME_HEIGHT - self.score_text.winfo_reqheight() - 30)

        # add score value
        self.score_value = tk.StringVar(value='0')
        self.score_value_label = tk.Label(self, textvariable=self.score_value, font=controller.BUTTON_FONT)
        self.score_value_label.place(
            x=self.score_text.winfo_reqwidth() + 30,
            y=controller.GAME_HEIGHT - self.score_value_label.winfo_reqheight() - 30)

        # add the back button
        self.back_button_game = tk.Button(self, text='Back to main menu', font=controller.DESCRIPTION_FONT, command=lambda: controller.show_frame(MainMenu))
        self.back_button_game.place(x=controller.GAME_WIDTH - self.back_button_game.winfo_reqwidth() - 20, y=controller.GAME_HEIGHT - self.back_button_game.winfo_reqheight() - 20)


        # add the restart button
        self.restart_button = tk.Button(self, text='Restart game', font=controller.DESCRIPTION_FONT, command=self.restart)
        self.restart_button.place(
            x=controller.GAME_WIDTH - self.restart_button.winfo_reqwidth() - 30 - self.back_button_game.winfo_reqwidth(),
            y=controller.GAME_HEIGHT - self.back_button_game.winfo_reqheight() - 20)

    def update_grid(self):
        """
        Redraws the game grid, from the matrix of main_grid_values
        """
        def rgb_color(rgb):
            """RGB to HEX"""
            return '#%02x%02x%02x' % rgb

        # clear on widgets preexisting on frame
        for widget in self.main_grid.winfo_children():
            widget.destroy()

        BORDER_WIDTH = 8

        # draw tiles
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values[i])):
                if self.main_grid_values[i][j] == 0:
                    # ignore 0 tiles for text
                    tile = tk.Label(self.main_grid, bg='red', text='', font=('Arial', 18))
                else:
                    # give tiles a different color
                    exponent = int(math.log(int(self.main_grid_values[i][j]), 2))
                    tile = tk.Label(
                        self.main_grid,
                        bg=rgb_color((255, 255 - exponent*31, 0)),
                        text=self.main_grid_values[i][j],
                        font=('Arial', 20)
                    )

                # color the 0 tiles with grey
                if tile['text'] == '':
                    tile.config(bg=rgb_color((210, 210, 210)))

                # border configuration - so that all borders are not overlapping
                if j == len(self.main_grid_values) - 1 and i == len(self.main_grid_values) - 1:
                    tile.grid(row=i, column=j, padx=BORDER_WIDTH, pady=BORDER_WIDTH, sticky='news')

                elif j == len(self.main_grid_values) - 1:
                    tile.grid(row=i, column=j, padx=BORDER_WIDTH, pady=(BORDER_WIDTH, 0), sticky='news')

                elif i == len(self.main_grid_values) - 1:
                    tile.grid(row=i, column=j, padx=(BORDER_WIDTH, 0), pady=BORDER_WIDTH, sticky='news')

                else:
                    tile.grid(row=i, column=j, padx=(BORDER_WIDTH, 0), pady=(BORDER_WIDTH, 0), sticky='news')

    def add_two(self):
        """Adds a randomly placed two onto the game matrix"""
        i = random.randint(0, self.TILES_PER_ROW - 1)
        j = random.randint(0, self.TILES_PER_ROW - 1)

        # regenerate positions until empty one is found
        while self.main_grid_values[i][j] != 0:
            i = random.randint(0, self.TILES_PER_ROW - 1)
            j = random.randint(0, self.TILES_PER_ROW - 1)

        self.main_grid_values[i][j] = 2

    def stack(self):
        """Stacks all tiles to the left (removes 0 tiles in between"""

        # create temporary matrix
        temp_matrix = [[0] * self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)]

        # for each row in actual matrix
        for i in range(len(self.main_grid_values)):
            empty_spot = 0
            # for each value in actual matrix
            for j in range(len(self.main_grid_values)):
                # if non zero, copy into optimal position into temporary matrix
                if self.main_grid_values[i][j] != 0:
                    temp_matrix[i][empty_spot] = self.main_grid_values[i][j]
                    empty_spot += 1

        # copy temp matrix to actual
        self.main_grid_values = temp_matrix

    def merge(self):
        """Merges all adjacent congruent tiles in a leftwards direction"""
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values) - 1):
                if self.main_grid_values[i][j] == self.main_grid_values[i][j+1]:
                    self.score_value.set(str(int(self.score_value.get()) + self.main_grid_values[i][j]*2))
                    self.main_grid_values[i][j] *= 2
                    self.main_grid_values[i][j+1] = 0

    def transpose(self):
        """Transposes the game matrix"""
        temp_matrix = [[0] * self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)]
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values)):
                temp_matrix[j][i] = self.main_grid_values[i][j]

        self.main_grid_values = temp_matrix

    def reverse(self):
        """Reverses the game matrix in horizontal direction"""
        temp_matrix = [[0] * self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)]
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values)):
                temp_matrix[i][self.TILES_PER_ROW - 1 - j] = self.main_grid_values[i][j]

        self.main_grid_values = temp_matrix

    def any_empty_tiles(self):
        """
        False if NO tiles remaining
        True if empty tiles exist
        """
        for i in range(self.TILES_PER_ROW):
            for j in range(self.TILES_PER_ROW):
                if self.main_grid_values[i][j] == 0:
                    return True

        return False

    def any_possible_moves_horizontal(self):
        """
        False if NO moves possible left to right
        True if merges possible on the horizontal
        """
        for i in range(self.TILES_PER_ROW):
            for j in range(self.TILES_PER_ROW - 1):
                if self.main_grid_values[i][j] == self.main_grid_values[i][j+1]:
                    return True

        return False

    def any_possible_moves_vertical(self):
        """
        False if NO moves possible up and down
        True if merges possible on the vertical
        """
        for i in range(self.TILES_PER_ROW - 1):
            for j in range(self.TILES_PER_ROW):
                if self.main_grid_values[i][j] == self.main_grid_values[i+1][j]:
                    return True

        return False

    def is_game_finished(self):
        """
        Checks if game finished:
            if not, do nothing
            otherwise, it is, and UNBIND controls, and DISPLAY GAME OVER
        """
        if not self.any_possible_moves_horizontal() and not self.any_possible_moves_vertical() and not self.any_empty_tiles():
            self.game_over_button = tk.Label(self, text='Game Over', padx=20, pady=20, font=self.controller.TITLE_FONT)
            self.game_over_button.place(
                x=self.controller.GAME_WIDTH // 2 - 0.5 * self.game_over_button.winfo_reqwidth() ,
                y=self.controller.GAME_HEIGHT // 2 - 0.5 * self.game_over_button.winfo_reqheight()- 40)

            self.unbind('<{}>'.format(self.controller.slide_left_control))
            self.unbind('<{}>'.format(self.controller.slide_right_control))
            self.unbind('<{}>'.format(self.controller.slide_up_control))
            self.unbind('<{}>'.format(self.controller.slide_down_control))

    def restart(self):
        """Clear game matrix, score, and rebind the controls, and recreate new board"""
        self.main_grid_values = [
            [0] * self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)
        ]

        self.score_value.set('0')
        self.add_two()
        self.add_two()
        self.update_grid()

        self.bind('<{}>'.format(self.controller.slide_left_control), self.push_left)
        self.bind('<{}>'.format(self.controller.slide_right_control), self.push_right)
        self.bind('<{}>'.format(self.controller.slide_up_control), self.push_up)
        self.bind('<{}>'.format(self.controller.slide_down_control), self.push_down)

        self.game_over_button.destroy()

    def push_left(self, event):
        """Control to swipe tiles left"""
        self.stack()
        self.merge()

        if self.any_empty_tiles():
            self.add_two()

        self.update_grid()
        self.is_game_finished()

    def push_up(self, event):
        """Control to swipe tiles up"""
        self.transpose()
        self.stack()
        self.merge()
        self.transpose()

        if self.any_empty_tiles():
            self.add_two()

        self.update_grid()
        self.is_game_finished()

    def push_right(self, event):
        """Control to swipe tiles right"""
        self.reverse()
        self.stack()
        self.merge()
        self.reverse()

        if self.any_empty_tiles():
            self.add_two()

        self.update_grid()
        self.is_game_finished()

    def push_down(self, event):
        """Control to swipe tiles down"""
        self.transpose()
        self.reverse()
        self.stack()
        self.merge()
        self.reverse()
        self.transpose()

        if self.any_empty_tiles():
            self.add_two()

        self.update_grid()
        self.is_game_finished()


if __name__ == '__main__':
    app = MainProgram()
    app.mainloop()