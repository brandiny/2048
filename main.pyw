import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image
import random
import math
import json
import time

# This allows Tkinter to run in high resolution - fixes blurry font
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


class MainProgram(tk.Tk):
    """This class is the program skeleton - the Tk object"""

    def __init__(self):
        # Initialise Tk object
        tk.Tk.__init__(self)

        # Define window constants
        self.GAME_WINDOW_CAPTION = '2048 - Python Version'
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 700

        # Initialise game controls variables
        self.slide_up_control = 'Up'
        self.slide_down_control = 'Down'
        self.slide_left_control = 'Left'
        self.slide_right_control = 'Right'

        # Initialise Window Frame + Spawn the Window
        self.title(self.GAME_WINDOW_CAPTION)
        self.minsize(self.GAME_WIDTH, self.GAME_HEIGHT)
        self.geometry('{}x{}'.format(self.GAME_WIDTH, self.GAME_HEIGHT))
        self.center_screen(self.GAME_WIDTH, self.GAME_HEIGHT)

        # Initialise all program wide fonts
        self.DESCRIPTION_FONT = Font(family="Helvetica", size=12)
        self.BUTTON_FONT = Font(family="Helvetica", size=16)
        self.TITLE_FONT = Font(family="Helvetica", size=28, weight='bold')

        # Initialise the program texts
        with open('2048textassets.json') as f:
            data = json.load(f)

            self.INSTRUCTIONS_TEXT = data['instructions_text']
            self.CONTROLS_TEXT = data['controls_text']
            self.SAVE_TEMPLATE = data['save_template']

        # Create the master frame
        self.container = tk.Frame(self)
        self.container.pack()

        # This variable holds pointer to current frame object
        self.current_frame = None

        # Display the main menu page
        self.show_frame(MainMenu)

        # Initialise colors for the 2048 game;
        # Label is the text, and tile is the background.
        self.TILE_COLORS = {
            2: "#daeddf", 4: "#9ae3ae", 8: "#6ce68d", 16: "#42ed71",
            32: "#17e650", 64: "#17c246", 128: "#149938",
            256: "#107d2e", 512: "#0e6325", 1024: "#0b4a1c",
            2048: "#031f0a", 4096: "#000000", 8192: "#000000"
        }

        self.LABEL_COLORS = {
            2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
            32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
            256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0",
            2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0"
        }

    def center_screen(self, window_width, window_height):
        """Centers the program window, within the whole screen"""
        offset_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        offset_down = int(
            (self.winfo_screenheight() - 40) / 2 - window_height / 2)

        self.geometry('+{}+{}'.format(offset_right, offset_down))

    def show_frame(self, frame_class, new_game=True):
        """
        Switches to the frame class passed as argument
        e.g. show_frame(MainMenu) ==> switches to main menu
        """
        if self.current_frame is not None:
            self.current_frame.destroy()

        if frame_class == MainGame and not new_game:
            frame = frame_class(self.container, self, new_game=False)
        else:
            frame = frame_class(self.container, self)

        frame.grid(row=0, column=0, sticky='news')
        self.current_frame = frame


class MainMenu(tk.Frame):
    """Main menu Frame Object"""

    def __init__(self, parent, controller):
        # Initialise frame
        tk.Frame.__init__(
            self,
            parent,
            width=controller.GAME_WIDTH,
            height=controller.GAME_HEIGHT)
        self.controller = controller

        # Create frame canvas
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Display background onto the canvas
        self.display_background('images/mainmenubackground.png')

        # Create button frame - menu button container
        button_frame = tk.Frame(self, width=250, height=300)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_propagate(False)

        # Initialise menu button objects
        menu_button1 = tk.Button(
            button_frame,
            text='New Game',
            command=lambda: controller.show_frame(MainGame))
        menu_button2 = tk.Button(
            button_frame,
            text='Load Game',
            command=lambda: controller.show_frame(
                MainGame,
                new_game=False))
        menu_button3 = tk.Button(
            button_frame,
            text='Instructions',
            command=lambda: controller.show_frame(Instructions))
        menu_button4 = tk.Button(
            button_frame,
            text='Controls',
            command=lambda: controller.show_frame(Controls))
        menu_button5 = tk.Button(
            button_frame,
            text='High Scores',
            command=lambda: controller.show_frame(HighScores))

        # If there is no save file (or it's empty) - grey out the Load Button
        try:
            with open('2048save.json') as f:
                content = f.readlines()
                if len(content) == 0:
                    menu_button2['state'] = tk.DISABLED
                    menu_button2['bg'] = '#cccccc'
                else:
                    pass
        except FileNotFoundError:
            menu_button2['state'] = tk.DISABLED
            menu_button2['bg'] = '#cccccc'

        buttons = [
            menu_button1,
            menu_button2,
            menu_button3,
            menu_button4,
            menu_button5]

        # Grid buttons into the button container
        for index, button in enumerate(buttons):
            button_frame.grid_rowconfigure(index, weight=1)
            button.config(font=controller.BUTTON_FONT)
            button.config(borderwidth=3)
            button.grid(row=index, column=0, sticky='news')

        # Render button container onto canvas
        # pixels_below_center: position of the buttons on the vertical axis
        pixels_below_center = 150
        self.display_object_on_canvas(
            button_frame,
            controller.GAME_WIDTH //
            2 -
            0.5 *
            button_frame['width'],
            controller.GAME_HEIGHT //
            2 -
            0.5 *
            button_frame['height'] +
            pixels_below_center)

    def display_background(self, image_path):
        """
        Given a relative path to an image (any image format),
        the image is drawn on frame canvas.
        """
        background_image = Image.open(image_path)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        """
        Given a tkinter object            (e.g. frame, button, label),
        X, Y coordinates                (measured from top left corner),

        The object is drawn onto the frame canvas.
        """
        self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)


class Instructions(tk.Frame):
    """This class is the instructions frame"""

    def __init__(self, parent, controller):
        # Initialise the frame object
        tk.Frame.__init__(
            self,
            parent,
            bg='white',
            width=controller.GAME_WIDTH,
            height=controller.GAME_HEIGHT)
        self.pack_propagate(False)
        self.controller = controller

        # Create frame canvas
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Draw and render background image
        self.display_background('images/instructionsbackground.png')

        # Display the main instructions text
        instructions_label = tk.Label(
            self,
            bg='white',
            wrap=600,
            anchor=tk.W,
            justify=tk.LEFT,
            text=controller.INSTRUCTIONS_TEXT,
            font=controller.DESCRIPTION_FONT)

        self.display_object_on_canvas(
            instructions_label,
            controller.GAME_WIDTH //
            2 -
            0.5 *
            instructions_label.winfo_reqwidth(),
            controller.GAME_HEIGHT //
            2 -
            0.5 *
            instructions_label.winfo_reqheight() +
            120)

        # Display the back button
        back_button_instructions = tk.Button(
            self,
            text='Back to menu',
            font=controller.BUTTON_FONT,
            command=lambda: controller.show_frame(MainMenu)
        )

        self.display_object_on_canvas(
            back_button_instructions,
            controller.GAME_WIDTH -
            back_button_instructions.winfo_reqwidth() -
            30,
            controller.GAME_HEIGHT -
            back_button_instructions.winfo_reqheight() -
            30)

    def display_background(self, image_path):
        """
        Given a relative path to an image (any image format),
        the image is drawn on frame canvas.
        """
        background_image = Image.open(image_path)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        """
        Given a tkinter object            (e.g. frame, button, label),
        X, Y coordinates                (measured from top left corner),

        The object is drawn onto the frame canvas.
        """
        self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)


class Controls(tk.Frame):
    """User controls Frame object"""

    def __init__(self, parent, controller):
        # Initialise inherited Frame object
        tk.Frame.__init__(
            self,
            parent,
            width=controller.GAME_WIDTH,
            height=controller.GAME_HEIGHT)
        self.controller = controller
        self.pack_propagate(False)

        # Is the user in the process of choosing a key?
        self.is_binding = False

        # Create frame canvas
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Render and draw background image on canvas
        self.display_background('images/controlsbackground.png')

        # Display the instructions for changing user controls
        instructions_label = tk.Label(
            self,
            bg='white',
            wrap=600,
            anchor=tk.W,
            justify=tk.LEFT,
            text=controller.CONTROLS_TEXT,
            font=controller.DESCRIPTION_FONT)

        self.display_object_on_canvas(
            instructions_label,
            controller.GAME_WIDTH //
            2 -
            0.5 *
            instructions_label.winfo_reqwidth(),
            instructions_label.winfo_reqheight() +
            220)

        # Display the input field grid - the 2x4 table (columns, rows)
        table_border_width = 2
        table_border_color = 'black'
        table_2x4 = tk.Frame(
            self,
            width=550,
            height=220,
            bg=table_border_color)
        table_2x4.grid_columnconfigure(0, weight=1)
        table_2x4.grid_columnconfigure(1, weight=1)
        table_2x4.grid_propagate(0)

        # Create the LEFT HAND COLUMN labels
        # Each label shows which control the user is changing
        control_up_label = tk.Label(table_2x4, text='Slide tiles up')
        control_down_label = tk.Label(table_2x4, text='Slide tiles down')
        control_left_label = tk.Label(table_2x4, text='Slide tiles left')
        control_right_label = tk.Label(table_2x4, text='Slide tiles right')

        # Grid the LEFT HAND COLUMN labels
        control_labels = [
            control_up_label,
            control_down_label,
            control_left_label,
            control_right_label
        ]
        for index, label in enumerate(control_labels):
            table_2x4.grid_rowconfigure(index, weight=1)
            label.config(
                bg='white',
                anchor=tk.W,
                justify=tk.LEFT,
                font=controller.DESCRIPTION_FONT
            )

            if index == 0:
                label.grid(
                    row=index,
                    column=0,
                    sticky='news',
                    pady=(table_border_width, table_border_width),
                    padx=(table_border_width, 0))

            else:
                label.grid(
                    row=index,
                    column=0,
                    sticky='news',
                    pady=(0, table_border_width),
                    padx=(table_border_width, 0))

        def initialise_control_button(button, button_save_string):
            """
            !!Use this function to CANCEL a key selection process!!

            Given a button object, and its purpose (left, right, up, down),
            Change the text on the button from

            from: "Enter a key"
            to: original control before entering a binding state

            And, let the frame know, the binding state is false
            """

            # Change the text back to black (from red)
            button['fg'] = 'black'
            suffix = ' arrow key'

            # Given a button, set its text back to str(control)
            if button_save_string == 'left':
                if controller.slide_left_control in (
                        'Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_left_control + suffix

                else:
                    button['text'] = controller.slide_left_control

            elif button_save_string == 'right':
                if controller.slide_right_control in (
                        'Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_right_control + \
                        suffix

                else:
                    button['text'] = controller.slide_right_control

            elif button_save_string == 'up':
                if controller.slide_up_control in (
                        'Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_up_control + suffix

                else:
                    button['text'] = controller.slide_up_control

            elif button_save_string == 'down':
                if controller.slide_down_control in (
                        'Left', 'Right', 'Up', 'Down'):
                    button['text'] = controller.slide_down_control + suffix

                else:
                    button['text'] = controller.slide_down_control

        def switch_keys(button, button_save_string):
            """
            Given a button,
            and which command it controls

            Collect one key, and store it in the Main Program master object
            """

            def unbind_keys(btn):
                """
                Stop collecting keystrokes for this button,
                unbinding arrow keys,
                and letter keys
                """
                btn.unbind('<Key>')
                btn.unbind('<Left>')
                btn.unbind('<Up>')
                btn.unbind('<Right>')
                btn.unbind('<Down>')

            def set_command_for(string, command):
                """
                Given a command direction (left, right, up, down),
                and a keystroke symbol (a, b, return, up, /, shift ... etc)
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

            def key(event):
                """
                Given a key event (collecting from tk.bind method)
                THAT IS NOT AN ARROW KEY nor SPACE
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
                that is an ARROW KEY but not SPACE
                change text on BUTTON
                save EVENT
                stop COLLECTING, and exit BINDING
                """
                set_command_for(button_save_string, event.keysym)
                button['text'] = event.keysym + ' arrow key'
                unbind_keys(button)
                self.is_binding = False

            def set_to_current_value():
                """
                Exits binding and resets the text on button
                """
                self.is_binding = False
                button['fg'] = 'black'
                nonlocal button_save_string
                if button_save_string == 'left':
                    if controller.slide_left_control in (
                            'Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_left_control + \
                            ' arrow key'

                    else:
                        button['text'] = controller.slide_left_control

                elif button_save_string == 'right':
                    if controller.slide_right_control in (
                            'Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_right_control + \
                            ' arrow key'

                    else:
                        button['text'] = controller.slide_right_control

                elif button_save_string == 'up':
                    if controller.slide_up_control in (
                            'Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_up_control + \
                            ' arrow key'

                    else:
                        button['text'] = controller.slide_up_control

                elif button_save_string == 'down':
                    if controller.slide_down_control in (
                            'Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_down_control + \
                            ' arrow key'

                    else:
                        button['text'] = controller.slide_down_control

            """
            BEGIN MAIN LOGIC FLOW FOR THIS FUNCTION
            ** all nested 
            functions declared **
            """
            # If clicked and already in binding state,
            # Untoggle the button and exit binding
            if button['text'] == 'Enter new key':
                set_to_current_value()
                unbind_keys(button)
                self.is_binding = False
                return

            # If clicked and another command is already in binding state,
            # don't do anything
            elif self.is_binding:
                return

            # Otherwise,
            # Display the 'enter new key' option in red and set binding = True
            else:
                button['text'] = 'Enter new key'
                button['fg'] = 'red'
                self.is_binding = True

            # Move the focus of the program to the button and,
            # start collecting button clicks
            button.focus_set()
            button.bind('<Key>', key)
            button.bind('<Left>', arrow_key)
            button.bind('<Up>', arrow_key)
            button.bind('<Right>', arrow_key)
            button.bind('<Down>', arrow_key)

            def do_nothing_when_pressed(event):
                pass

            # Ignore key presses from SPACE KEY
            # Over rides binding from <Key> bind in above section
            button.bind('<space>', do_nothing_when_pressed)

        # Initialise key collecting buttons with any saved controls.
        control_up_input = tk.Button(
            table_2x4, text='', command=lambda: switch_keys(
                control_up_input, 'up'))
        initialise_control_button(control_up_input, 'up')

        control_down_input = tk.Button(
            table_2x4, text='', command=lambda: switch_keys(
                control_down_input, 'down'))
        initialise_control_button(control_down_input, 'down')

        control_left_input = tk.Button(
            table_2x4, text='', command=lambda: switch_keys(
                control_left_input, 'left'))
        initialise_control_button(control_left_input, 'left')

        control_right_input = tk.Button(
            table_2x4, text='', command=lambda: switch_keys(
                control_right_input, 'right'))
        initialise_control_button(control_right_input, 'right')

        # Grid the RIGHT HAND COLUMN (key collecting buttons) of the 2x4 grid
        control_inputs = [
            control_up_input,
            control_down_input,
            control_left_input,
            control_right_input]
        for index, item in enumerate(control_inputs):
            table_2x4.grid_rowconfigure(index, weight=1)

            item.config(
                bg='white',
                borderwidth=0,
                font=controller.DESCRIPTION_FONT,
                justify='center'
            )

            if index == 0:
                item.grid(
                    row=index,
                    column=1,
                    sticky='news',
                    pady=(table_border_width, table_border_width),
                    padx=(table_border_width, table_border_width))

            else:
                item.grid(
                    row=index,
                    column=1,
                    sticky='news',
                    pady=(0, table_border_width),
                    padx=(table_border_width, table_border_width))

        # Display the packed table
        self.display_object_on_canvas(
            table_2x4,
            controller.GAME_WIDTH // 2 - 0.5 * table_2x4.winfo_reqwidth(),
            table_2x4.winfo_reqheight() + 140)

        # Display the back button
        back_button_instructions = tk.Button(
            self,
            text='Save and go back to menu',
            font=controller.BUTTON_FONT,
            command=lambda: self.preliminary_check_controls()
        )

        self.display_object_on_canvas(
            back_button_instructions,
            controller.GAME_WIDTH -
            back_button_instructions.winfo_reqwidth() -
            30,
            controller.GAME_HEIGHT -
            back_button_instructions.winfo_reqheight() -
            30)

        # Create the red error msg - which will be empty at first
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

        # Is the program still in a binding state? If yes, do not allow exit
        if self.is_binding:
            self.error_msg['text'] = 'You are still binding'
            self.display_object_on_canvas(
                self.error_msg,
                50,
                self.controller.GAME_HEIGHT -
                self.error_msg.winfo_reqheight() -
                15)

        # Are the controls set all unique? If yes, do not allow exit
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
                self.controller.GAME_HEIGHT -
                self.error_msg.winfo_reqheight() -
                15)

        # All tests passed? If yes, allow exit
        else:
            self.controller.show_frame(MainMenu)

    def display_background(self, image_path):
        """
        Given a relative path to an image (any image format),
        the image is drawn on frame canvas.
        """
        background_image = Image.open(image_path)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        """
        Given a tkinter object            (e.g. frame, button, label),
        X, Y coordinates                (measured from top left corner),

        The object is drawn onto the frame canvas.
        """
        self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)

    def remove_object_from_canvas(self, tk_object):
        """
        Given a tkinter object            (e.g. frame, button, label),

        Delete object from frame canvas.
        """
        self.canvas.delete(tk_object)


class MainGame(tk.Frame):
    """This class is the 2048 game frame"""

    def __init__(self, parent, controller, new_game=True):
        # Initialise the inherited frame object
        tk.Frame.__init__(
            self,
            parent,
            width=controller.GAME_WIDTH,
            height=controller.GAME_HEIGHT)
        self.controller = controller

        # Create the game grid frame
        self.GRID_WIDTH = 600
        self.TILES_PER_ROW = 4

        self.main_grid = tk.Frame(
            self,
            width=self.GRID_WIDTH,
            height=self.GRID_WIDTH,
            bg='black')
        self.main_grid.grid_propagate(0)

        # Set the width of each row and column
        for i in range(self.TILES_PER_ROW):
            self.main_grid.grid_columnconfigure(
                i, minsize=self.GRID_WIDTH // self.TILES_PER_ROW)
            self.main_grid.grid_rowconfigure(
                i, minsize=self.GRID_WIDTH // self.TILES_PER_ROW)

        # Place it on screen
        self.main_grid.place(
            x=controller.GAME_WIDTH //
            2 -
            self.main_grid.winfo_reqwidth() *
            0.5,
            y=0)

        # Initialise the time variable
        self.runtime = None

        # Generate the grid matrix (matrix of values)
        self.main_grid_values = [
            [0] * self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)
        ]

        # Initiate by spawning 2 two's and rendering the frame
        self.add_two()
        self.add_two()
        self.update_grid()

        # Add the score text
        self.score_text = tk.Label(
            self, text='SCORE:', font=controller.BUTTON_FONT)
        self.score_text.place(
            x=30,
            y=controller.GAME_HEIGHT - self.score_text.winfo_reqheight() - 30)

        # Add score value
        self.score_value = tk.StringVar(value='0')
        self.score_value_label = tk.Label(
            self,
            textvariable=self.score_value,
            font=controller.BUTTON_FONT)
        self.score_value_label.place(
            x=self.score_text.winfo_reqwidth() +
            30,
            y=controller.GAME_HEIGHT -
            self.score_value_label.winfo_reqheight() -
            30)

        # Add the back button
        self.back_button = tk.Button(
            self,
            text='Go Back',
            font=controller.DESCRIPTION_FONT,
            command=lambda: self.controller.show_frame(MainMenu))
        self.back_button.place(
            x=controller.GAME_WIDTH - self.back_button.winfo_reqwidth() - 20,
            y=controller.GAME_HEIGHT - self.back_button.winfo_reqheight() - 20)

        # Add the restart button
        self.save_button = tk.Button(
            self,
            text='Save',
            bg='blue',
            fg='white',
            font=controller.DESCRIPTION_FONT,
            command=self.save_game)
        self.save_button.place(
            x=controller.GAME_WIDTH - self.save_button.winfo_reqwidth()
            - 30 - self.back_button.winfo_reqwidth(),
            y=controller.GAME_HEIGHT - self.save_button.winfo_reqheight() - 20)

        # Initialise name and prediction value
        self.name = ''
        self.predicted_value = -1

        # Load game if there is a save file
        if not new_game:
            self.load_game()
            self.bind(
                '<{}>'.format(
                    self.controller.slide_left_control),
                self.push_left)
            self.bind(
                '<{}>'.format(
                    self.controller.slide_right_control),
                self.push_right)
            self.bind(
                '<{}>'.format(
                    self.controller.slide_up_control),
                self.push_up)
            self.bind(
                '<{}>'.format(
                    self.controller.slide_down_control),
                self.push_down)
            self.focus_set()

        # If name and prediction not set, ask for them
        if not self.name or self.predicted_value == -1:
            # Create the prompt frame
            self.details_grid = tk.Frame(
                self,
                width=485,
                height=340,
                bg='white',
                highlightbackground="#bbbbbb",
                highlightthickness=8,
                padx=40,
                pady=40
            )
            self.details_grid.grid_propagate(0)

            # Fill the frame
            name_label = tk.Label(
                self.details_grid,
                text='What is your name?',
                bg='white',
                anchor=tk.W,
                justify=tk.LEFT,
                font=controller.DESCRIPTION_FONT
            )
            name_label.grid(row=0, sticky='we')

            self.name_entry_temp = tk.StringVar()
            name_entry = tk.Entry(
                self.details_grid,
                borderwidth=2,
                textvariable=self.name_entry_temp
            )
            name_entry.grid(row=1, sticky='we', pady=(5, 0))

            predict_label = tk.Label(
                self.details_grid,
                text='What score do you think you\'ll get?',
                bg='white',
                font=controller.DESCRIPTION_FONT,
                anchor=tk.W,
                justify=tk.LEFT
            )
            predict_label.grid(row=2, sticky='we')

            self.predict_entry_temp = tk.StringVar()
            predict_entry = tk.Entry(
                self.details_grid,
                borderwidth=2,
                textvariable=self.predict_entry_temp
            )
            predict_entry.grid(row=3, sticky='we', pady=(5, 0))

            submit_button = tk.Button(
                self.details_grid,
                text='Play Game',
                padx=10,
                pady=0,
                command=self.clear_details_box
            )
            submit_button.grid(row=4, pady=(10, 0), sticky='we')

            # Initialise the error message thing
            self.error_msg_details = tk.Label(
                self.details_grid, text='', fg='red', bg='white')
            self.error_msg_details.grid(row=5, pady=(10, 0), sticky='we')

            # Place it on the screen
            self.details_grid.place(
                x=self.controller.GAME_WIDTH //
                2 -
                0.5 *
                self.details_grid.winfo_reqwidth(),
                y=self.controller.GAME_HEIGHT //
                2 -
                0.5 *
                self.details_grid.winfo_reqheight() -
                40)

    def clear_details_box(self):
        """
        Removes the details box,

        If, and only if,
            - Both fields filled out
            - len(name) < 50 characters
            - Prediction is a number and non-negative, and < 10^8
        """

        name = self.name_entry_temp.get()
        prediction = self.predict_entry_temp.get()

        # Are both fields filled out? If not, return
        if not name and not prediction:
            self.error_msg_details.config(
                text='Make sure both fields are filled out')
            return

        # Is name field < 50 characters? If not, return
        if len(name) > 50:
            self.error_msg_details.config(
                text='Name must be below 50 characters')
            return
        else:
            self.name = name

        # Is the number entry ACTUALLY a number? If not, return
        try:
            self.predicted_value = int(prediction)
        except Exception as e:
            self.error_msg_details.config(
                text='Please enter a number for prediction')
            return

        # If prediction is greater than 10^8, exit
        if self.predicted_value > 1 * 10 ** 8:
            self.error_msg_details.config(text='Your number is too big')
            return

        # If prediction is negative, exit
        elif self.predicted_value < 0:
            self.error_msg_details.config(
                text='Please enter a non-negative number')
            return

        # Else everything is met, and destroy the prompt box
        self.details_grid.destroy()
        self.focus_set()
        self.bind(
            '<{}>'.format(
                self.controller.slide_left_control),
            self.push_left)
        self.bind(
            '<{}>'.format(
                self.controller.slide_right_control),
            self.push_right)
        self.bind(
            '<{}>'.format(
                self.controller.slide_up_control),
            self.push_up)
        self.bind(
            '<{}>'.format(
                self.controller.slide_down_control),
            self.push_down)
        self.bind('a', self.run_ai)

        self.runtime = time.time()

    def load_game(self):
        """Load the game file, and start the game"""

        with open('2048save.json', 'r') as f:
            data = json.load(f)
            self.main_grid_values = data['game_matrix']
            self.score_value.set(str(data['score']))
            self.predicted_value = data['predicted_score']
            self.name = str(data['name'])

        self.update_grid()

        self.bind(
            '<{}>'.format(
                self.controller.slide_left_control),
            self.push_left)
        self.bind(
            '<{}>'.format(
                self.controller.slide_right_control),
            self.push_right)
        self.bind(
            '<{}>'.format(
                self.controller.slide_up_control),
            self.push_up)
        self.bind(
            '<{}>'.format(
                self.controller.slide_down_control),
            self.push_down)
        self.bind(
            '<a>', self.run_ai)

    def save_game(self):
        """Save the game matrix into 2048save.json - overwriting last save"""

        with open('2048save.json', 'w+') as f:
            results = {
                'game_matrix': self.main_grid_values,
                'score': self.score_value.get(),
                'name': self.name,
                'predicted_score': self.predicted_value
            }
            json.dump(results, f)

    def update_grid(self):
        """
        Redraws the game grid,
        using the matrix: self.main_grid_values
        """

        def rgb_color(rgb):
            """RGB to HEX"""
            return '#%02x%02x%02x' % rgb

        # Clear the on widgets preexisting on frame
        for widget in self.main_grid.winfo_children():
            widget.destroy()

        BORDER_WIDTH = 8

        # Draw the tiles.
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values[i])):
                # If the tile is 0: it must be blank,
                # Therefore, render a blank grey tile.
                if self.main_grid_values[i][j] == 0:
                    tile = tk.Label(
                        self.main_grid,
                        text='',
                        font=('Arial', 18),
                        bg=rgb_color((210, 210, 210)))

                # Otherwise, it must be non-empty and therefore,
                # We add the number into the label - and color it accordingly
                else:
                    number = int(self.main_grid_values[i][j])
                    tile = tk.Label(
                        self.main_grid,
                        bg=self.controller.TILE_COLORS[number],
                        fg=self.controller.LABEL_COLORS[number],
                        text=self.main_grid_values[i][j],
                        font=('Arial', 20)
                    )

                # Border configuration
                # This is so that no borders are overlapping
                if j == len(self.main_grid_values) - \
                        1 and i == len(self.main_grid_values) - 1:
                    tile.grid(
                        row=i,
                        column=j,
                        padx=BORDER_WIDTH,
                        pady=BORDER_WIDTH,
                        sticky='news')

                elif j == len(self.main_grid_values) - 1:
                    tile.grid(
                        row=i, column=j, padx=BORDER_WIDTH, pady=(
                            BORDER_WIDTH, 0), sticky='news')

                elif i == len(self.main_grid_values) - 1:
                    tile.grid(
                        row=i,
                        column=j,
                        padx=(
                            BORDER_WIDTH,
                            0),
                        pady=BORDER_WIDTH,
                        sticky='news')

                else:
                    tile.grid(
                        row=i, column=j, padx=(
                            BORDER_WIDTH, 0), pady=(
                            BORDER_WIDTH, 0), sticky='news')

    def add_two(self):
        """
        Adds a randomly placed two or four onto the game matrix,
        P(x=2) = 0.75,
        P(x=4) = 0.25
        """

        i = random.randint(0, self.TILES_PER_ROW - 1)
        j = random.randint(0, self.TILES_PER_ROW - 1)

        # Regenerate positions until empty one is found
        # This doesn't create an infinite loop,
        # As matrix has GUARANTEE of possible move
        while self.main_grid_values[i][j] != 0:
            i = random.randint(0, self.TILES_PER_ROW - 1)
            j = random.randint(0, self.TILES_PER_ROW - 1)

        self.main_grid_values[i][j] = random.choice([2, 2, 2, 4])

    def stack(self):
        """
        Stacks all tiles to the LEFT (removes 0 tiles in between)
        e.g

        2 0 2 0                     2 2 0 0
        0 0 2 0        ---->        2 0 0 2
        2 0 0 2     stack left      2 2 0 0
        0 2 2 0                     2 2 0 0

        Note, it does NOT merge the tiles. This is in self.merge()
        """

        # Create temporary matrix
        temp_matrix = [
            [0] *
            self.TILES_PER_ROW for _ in range(
                self.TILES_PER_ROW)]

        for i in range(len(self.main_grid_values)):
            # Empty spot maintains the optimal position for the tile
            empty_spot = 0
            for j in range(len(self.main_grid_values)):
                # If non zero, copy into optimal position into temporary matrix
                # And increment the optimal position (as its full now)
                if self.main_grid_values[i][j] != 0:
                    temp_matrix[i][empty_spot] = self.main_grid_values[i][j]
                    empty_spot += 1

        # Copy temporary matrix to real matrix
        self.main_grid_values = temp_matrix

    def merge(self):
        """
        Merges all adjacent congruent tiles in a LEFT-wards direction

        2 2 0 0                     4 0 0 0
        2 0 0 0       ---->         2 0 0 0
        2 2 0 0     stack left      4 0 0 0
        2 2 0 0                     4 0 0 0

        """
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values) - 1):
                # If adjacent tiles are equal,
                # Merge them into the leftwards term
                value = self.main_grid_values[i][j]
                right_adjacent_value = self.main_grid_values[i][j + 1]
                if value == right_adjacent_value:
                    self.score_value.set(
                        str(int(self.score_value.get()) + value * 2))
                    self.main_grid_values[i][j] *= 2
                    self.main_grid_values[i][j + 1] = 0

    def transpose(self):
        """
        Transposes the game matrix

        where if F(X, Y) = item in row X, column Y is mapped to F(Y, X)
        F(X, Y) --> F(Y, X)

        The geometric equivalent of a matrix transposition,
        is a 90 degree counter-clock wise rotation / mirror with line Y = X
        """

        temp_matrix = [
            [0] *
            self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)]
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values)):
                temp_matrix[j][i] = self.main_grid_values[i][j]

        self.main_grid_values = temp_matrix

    def reverse(self):
        """
        Reverses the game matrix in horizontal direction
        """

        temp_matrix = [
            [0] *
            self.TILES_PER_ROW for _ in range(
                self.TILES_PER_ROW)]
        for i in range(len(self.main_grid_values)):
            for j in range(len(self.main_grid_values)):
                temp_matrix[i][self.TILES_PER_ROW -
                               1 - j] = self.main_grid_values[i][j]

        self.main_grid_values = temp_matrix

    def any_empty_tiles(self):
        """
        Returns False if NO tiles remaining
        Returns True if empty tiles exist
        """
        for i in range(self.TILES_PER_ROW):
            for j in range(self.TILES_PER_ROW):
                if self.main_grid_values[i][j] == 0:
                    return True

        return False

    def any_possible_moves_horizontal(self):
        """
        Returns False if NO merges possible left to right
        Returns True if merges possible on the horizontal
        """
        for i in range(self.TILES_PER_ROW):
            for j in range(self.TILES_PER_ROW - 1):
                value = self.main_grid_values[i][j]
                right_adjacent_value = self.main_grid_values[i][j + 1]
                if value == right_adjacent_value:
                    return True

        return False

    def any_possible_moves_vertical(self):
        """
        Returns False if NO merges possible up and down
        Returns True if merges possible on the vertical axis
        """
        for i in range(self.TILES_PER_ROW - 1):
            for j in range(self.TILES_PER_ROW):
                value = self.main_grid_values[i][j]
                down_adjacent_value = self.main_grid_values[i + 1][j]
                if value == down_adjacent_value:
                    return True

        return False

    def is_game_finished(self):
        """
        Checks if game finished (no moves, or merges in XY directions):
            if not, do nothing
            otherwise, it is, and UNBIND controls, and DISPLAY GAME OVER
        """
        if not self.any_possible_moves_horizontal() and \
                not self.any_possible_moves_vertical() and \
                not self.any_empty_tiles():

            # Create frame
            self.game_over_frame = tk.Frame(
                self,
                padx=40,
                pady=40,
                highlightbackground="#bbbbbb",
                highlightthickness=8
            )

            # Create the large game over label
            game_over_label = tk.Label(
                self.game_over_frame,
                text='Game Over',
                padx=20,
                pady=20,
                font=self.controller.TITLE_FONT, justify=tk.CENTER, anchor=tk.W
            )
            game_over_label.grid(row=0, sticky='we')

            # Render the game details (i.e name, score, prediction)
            name = self.name
            score = str(self.score_value.get())
            score_second = int(self.score_value.get()) // (time.time() -
                                                           self.runtime)
            int(self.score_value.get()) - int(self.predicted_value),
            if int(self.predicted_value) - int(self.score_value.get()) >= 0:
                prediction = '+' + str(
                    abs(
                        int(self.predicted_value)
                        - int(self.score_value.get())
                    )
                )
            else:
                prediction = '-' + str(self.score_value.get())

            game_over_description = tk.Label(
                self.game_over_frame,
                wrap=350,
                font=self.controller.DESCRIPTION_FONT,
                text=self.controller.SAVE_TEMPLATE.format(
                    name=name,
                    score=score,
                    prediction=prediction,
                    score_second=str(score_second) + ' pts / s'
                ),
                justify=tk.LEFT,
                anchor=tk.W)
            game_over_description.grid(row=1, sticky='we')

            # Display the restart button
            game_over_restart_button = tk.Button(
                self.game_over_frame,
                font=self.controller.DESCRIPTION_FONT,
                text='Restart Game',
                command=self.restart,
                bg='blue',
                fg='white'
            )
            game_over_restart_button.grid(row=2, sticky='we', pady=(10, 0))

            # Show the game over frame
            self.game_over_frame.place(
                x=self.game_over_frame.winfo_reqwidth() + 130,
                y=self.game_over_frame.winfo_reqheight() + 80
            )

            # Unbind the controls - so the user can't play anymore
            self.unbind('<{}>'.format(self.controller.slide_left_control))
            self.unbind('<{}>'.format(self.controller.slide_right_control))
            self.unbind('<{}>'.format(self.controller.slide_up_control))
            self.unbind('<{}>'.format(self.controller.slide_down_control))

            # Save this entry as a highscore
            with open('2048highscores.json', 'r') as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = json.loads('[]')

                p_int = int(self.score_value.get()) - int(self.predicted_value)
                data.append({
                    'name': self.name,
                    'score': int(self.score_value.get()),
                    'prediction': p_int,
                    'score / s': score_second
                })

            with open('2048highscores.json', 'w') as f:
                json.dump(data, f)

            # Clear the save file
            with open('2048save.json', 'w+') as f:
                pass

            # Grey out the save button (as you can't save if you've lost :O)
            self.save_button['state'] = tk.DISABLED
            self.save_button['bg'] = '#cccccc'

    def restart(self):
        """
        Restarts the game

        Clear game matrix,
        rest score,
        rebind the controls,
        redraw board
        """

        # Clear matrix
        self.main_grid_values = [
            [0] * self.TILES_PER_ROW for _ in range(self.TILES_PER_ROW)
        ]

        # Reset score and add new twos to board
        self.score_value.set('0')
        self.add_two()
        self.add_two()
        self.update_grid()

        # Rebind keys
        self.bind(
            '<{}>'.format(
                self.controller.slide_left_control),
            self.push_left)
        self.bind(
            '<{}>'.format(
                self.controller.slide_right_control),
            self.push_right)
        self.bind(
            '<{}>'.format(
                self.controller.slide_up_control),
            self.push_up)
        self.bind(
            '<{}>'.format(
                self.controller.slide_down_control),
            self.push_down)

        # Remove the ending message
        try:
            self.game_over_frame.destroy()
        except Exception:
            pass

        # Ungrey save
        self.save_button['state'] = tk.NORMAL
        self.save_button['bg'] = 'blue'
        self.save_button['fg'] = 'white'

        # Restart time
        self.time = time.time()

    def push_left(self, event):
        """Swipe tiles left"""
        pre_matrix = self.main_grid_values

        self.stack()
        self.merge()

        if self.any_empty_tiles() and pre_matrix != self.main_grid_values:
            self.add_two()

        self.update_grid()
        self.is_game_finished()

    def push_up(self, event):
        """Swipe tiles up"""
        pre_matrix = self.main_grid_values

        self.transpose()
        self.stack()
        self.merge()
        self.transpose()

        if self.any_empty_tiles() and pre_matrix != self.main_grid_values:
            self.add_two()

        self.update_grid()
        self.is_game_finished()

    def push_right(self, event):
        """Swipe tiles right"""
        pre_matrix = self.main_grid_values

        self.reverse()
        self.stack()
        self.merge()
        self.reverse()

        if self.any_empty_tiles() and pre_matrix != self.main_grid_values:
            self.add_two()

        self.update_grid()
        self.is_game_finished()

    def push_down(self, event):
        """Swipe tiles down"""
        pre_matrix = self.main_grid_values

        self.transpose()
        self.reverse()
        self.stack()
        self.merge()
        self.reverse()
        self.transpose()

        if self.any_empty_tiles() and pre_matrix != self.main_grid_values:
            self.add_two()

        self.update_grid()
        self.is_game_finished()

    def run_ai(self, event, move='right'):
        """
        Bonus rudimentary AI included:

        press A to run
        """

        # If the game is done, climb and exit call stack
        if not self.any_possible_moves_horizontal() and \
                not self.any_possible_moves_vertical() and \
                not self.any_empty_tiles():
            return

        # Copy the matrix
        copy_matrix = self.main_grid_values

        # Choose control
        next_move = None
        if move == 'right':
            self.push_right('a')
            next_move = 'down'

        elif move == 'down':
            self.push_down('a')
            next_move = 'right'

        elif move == 'left':
            self.push_left('a')
            next_move = 'right'

        elif move == 'up':
            self.push_up('a')
            next_move = 'down'

        # No changes
        if self.main_grid_values == copy_matrix:
            if move == 'down':
                next_move = 'right'

            elif move == 'right':
                next_move = 'left'

            elif move == 'left':
                next_move = 'up'

        # Draw grid and call next recursive call
        self.update_grid()
        self.controller.after(50, lambda: self.run_ai('a', move=next_move))


class HighScores(tk.Frame):
    """This class handles the high scores page of the game"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create the frame canvas
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Display background image of title
        self.display_background('images/highscoresbackground.png')

        # Display "sort by" label
        self.sort_by_label = tk.Label(
            self,
            text='Sort By: ',
            font=controller.BUTTON_FONT,
            bg='white'
        )

        # THESE ARE THE MARGINS FOR THE SORT BUTTON BAR (pixels)
        LEFT_MARGIN = 30
        BOTTOM_MARGIN = 360
        self.display_object_on_canvas(
            self.sort_by_label,
            x=LEFT_MARGIN,
            y=controller.GAME_HEIGHT -
            self.sort_by_label.winfo_reqheight() -
            BOTTOM_MARGIN)

        # THIS CONTROLS THE GAP BETWEEN THE SORT BUTTONS (pixels)
        GAP = 10
        self.sort_by1 = tk.Button(
            self,
            text='High score',
            font=controller.DESCRIPTION_FONT,
            command=self.update_textmatrix_score
        )
        self.display_object_on_canvas(
            self.sort_by1,
            x=LEFT_MARGIN +
            GAP +
            self.sort_by_label.winfo_reqwidth(),
            y=controller.GAME_HEIGHT -
            self.sort_by_label.winfo_reqheight() -
            BOTTOM_MARGIN)

        self.sort_by2 = tk.Button(
            self,
            text='Prediction',
            font=controller.DESCRIPTION_FONT,
            command=self.update_textmatrix_prediction
        )
        self.display_object_on_canvas(
            self.sort_by2,
            x=LEFT_MARGIN +
            2 *
            GAP +
            self.sort_by_label.winfo_reqwidth() +
            self.sort_by1.winfo_reqwidth(),
            y=controller.GAME_HEIGHT -
            self.sort_by_label.winfo_reqheight() -
            BOTTOM_MARGIN)

        self.sort_by3 = tk.Button(
            self,
            text='Score per second',
            font=controller.DESCRIPTION_FONT,
            command=self.update_textmatrix_scoresecond
        )

        self.display_object_on_canvas(
            self.sort_by3,
            x=LEFT_MARGIN +
            3 *
            GAP +
            self.sort_by2.winfo_reqwidth() +
            self.sort_by_label.winfo_reqwidth() +
            self.sort_by1.winfo_reqwidth(),
            y=controller.GAME_HEIGHT -
            self.sort_by_label.winfo_reqheight() -
            BOTTOM_MARGIN)

        # Displays back button
        back_button_instructions = tk.Button(
            self,
            text='Back to menu',
            font=controller.BUTTON_FONT,
            command=lambda: controller.show_frame(MainMenu)
        )

        self.display_object_on_canvas(
            back_button_instructions,
            controller.GAME_WIDTH -
            back_button_instructions.winfo_reqwidth() -
            30,
            controller.GAME_HEIGHT -
            back_button_instructions.winfo_reqheight() -
            30)

        # The START and FINISH pointers that the program will render between
        # from text_matrix
        self.a = 0
        self.b = 4

        # Matrix (2d-array) that holds the values of the scoreboard
        # Must be initialised by self.load_textmatrix
        self.text_matrix = []

        # Load the high score matrix,
        # Sort it via score,
        # Draw it
        self.load_textmatrix()
        self.update_textmatrix_score()

        # Displays next page and previous page buttons
        self.previous_page = tk.Button(
            self,
            text='Previous',
            font=controller.DESCRIPTION_FONT,
            command=self.previous_page
        )

        self.display_object_on_canvas(
            self.previous_page,
            x=20,
            y=self.previous_page.winfo_reqheight() + 570
        )

        self.next_page = tk.Button(
            self,
            text='Next',
            font=controller.DESCRIPTION_FONT,
            command=self.next_page
        )

        self.display_object_on_canvas(
            self.next_page,
            x=20 + GAP + self.previous_page.winfo_reqwidth(),
            y=self.previous_page.winfo_reqheight() + 570
        )

        self.page_label = tk.Label(
            self,
            text='Page: ',
            font=controller.BUTTON_FONT,
            bg='white'
        )

        self.display_object_on_canvas(
            self.page_label,
            x=20 +
            3 *
            GAP +
            self.next_page.winfo_reqwidth() +
            self.previous_page.winfo_reqwidth(),
            y=self.previous_page.winfo_reqheight() +
            572)

        # Initialise the page_number label at the bottom of page.
        self.page_number = tk.StringVar()
        self.page_number.set('1')
        self.page_number_label = tk.Label(
            self,
            textvariable=self.page_number,
            font=controller.BUTTON_FONT,
            bg='white'
        )

        self.display_object_on_canvas(
            self.page_number_label,
            x=20 + 5 * GAP + 40
            + self.next_page.winfo_reqwidth()
            + self.previous_page.winfo_reqwidth()
            + self.page_number_label.winfo_reqwidth(),
            y=self.previous_page.winfo_reqheight() + 572
        )

    def display_background(self, image_path):
        """
        Given a relative path to an image (any image format),
        the image is drawn on frame canvas.
        """
        background_image = Image.open(image_path)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        """
        Given a tkinter object            (e.g. frame, button, label),
        X, Y coordinates                (measured from top left corner),

        The object is drawn onto the frame canvas.
        """
        self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)

    def update_scoreboard(self):
        """Clears and draws the high score table from self.text_matrix"""

        # clear board if not cleared.
        try:
            self.table_4x5.destroy()
        except Exception:
            pass

        # create frame
        self.table_border_width = 2
        self.table_border_color = 'black'
        self.table_4x5 = tk.Frame(
            self,
            width=640,
            height=220,
            bg=self.table_border_color)
        self.table_4x5.grid_columnconfigure(0, weight=1)
        self.table_4x5.grid_columnconfigure(1, weight=1)
        self.table_4x5.grid_columnconfigure(2, weight=1)
        self.table_4x5.grid_columnconfigure(3, weight=1)
        self.table_4x5.grid_propagate(0)

        # check self.textmatrix for emptiness, if so, fill them
        if len(self.text_matrix) < 5:
            J = 5 - len(self.text_matrix)
            for iteration in range(J):
                self.text_matrix.append(['' for i in range(5)])

        # set up columns
        for i in range(0, 5):
            self.table_4x5.grid_rowconfigure(i, weight=1)

        # insert title labels
        labels = ['Rank', 'Name', 'Score', 'Prediction', 'Score / second']
        for jndex, text in enumerate(labels):
            label = tk.Label(self.table_4x5, text=text)
            label.config(
                bg='white',
                anchor=tk.W,
                justify=tk.LEFT
            )

            if jndex == 4:
                label.grid(
                    row=0,
                    column=jndex,
                    sticky='news',
                    pady=(self.table_border_width, self.table_border_width),
                    padx=(self.table_border_width, self.table_border_width))

            else:
                label.grid(
                    row=0,
                    column=jndex,
                    sticky='news',
                    pady=(self.table_border_width, self.table_border_width),
                    padx=(self.table_border_width, 0))

        # column_index stores the column pointer for each entry.
        # e.g column_index = 2 means read the NAME column for this entry.
        column_index = 0
        for index in range(self.a, self.b):
            column_index += 1

            # INDEX NOT EXIST:
            # A boolean that allows for the loop to default to blank values
            # Iff the matrix index doesnt exist.
            index_not_exist = False

            # Check to see if this index exists in text_matrix.
            # If so, go ahead and draw,
            # Else use blanks.
            try:
                if self.text_matrix[index][0] != '':
                    self.text_matrix[index][0] = index + 1
            except IndexError:
                index_not_exist = True

            # Grid the labels.
            for jndex in range(5):
                if index_not_exist:
                    text = ''
                else:
                    text = self.text_matrix[index][jndex]

                label = tk.Label(self.table_4x5, text=text)
                label.config(
                    bg='white',
                    anchor=tk.W,
                    justify=tk.LEFT
                )

                if jndex == 0:
                    label.config(justify=tk.RIGHT, anchor=tk.E)

                if column_index == 0:
                    if jndex == 4:
                        label.grid(
                            row=column_index,
                            column=jndex,
                            sticky='news',
                            pady=(
                                self.table_border_width,
                                self.table_border_width),
                            padx=(
                                self.table_border_width,
                                self.table_border_width)
                        )

                    else:
                        label.grid(
                            row=column_index,
                            column=jndex,
                            sticky='news',
                            pady=(
                                self.table_border_width,
                                self.table_border_width),
                            padx=(
                                self.table_border_width,
                                0)
                        )

                else:
                    if jndex == 4:
                        label.grid(
                            row=column_index,
                            column=jndex,
                            sticky='news',
                            pady=(
                                0, self.table_border_width),
                            padx=(
                                self.table_border_width,
                                self.table_border_width)
                        )

                    else:
                        label.grid(
                            row=column_index,
                            column=jndex,
                            sticky='news',
                            pady=(0, self.table_border_width),
                            padx=(self.table_border_width, 0))

        # Display the packed table
        self.display_object_on_canvas(
            self.table_4x5,
            30,
            self.table_4x5.winfo_reqheight() + 150)

    def load_textmatrix(self):
        """
        This method reads from 2048highscores.json,
        and copies values over to self.text_matrix
        """

        # Load the file up
        try:
            f = open('2048highscores.json', 'r')
            data = json.load(f)

            # Append the values into the self.text_matrix variable
            for index, entry in enumerate(data):
                self.text_matrix.append([
                    index + 1,
                    entry['name'],
                    entry['score'],
                    entry['prediction'],
                    entry['score / s']
                ])

        except Exception:
            # If file blank, or file not existent, do nothing.
            pass

    def update_textmatrix_score(self):
        """Sorts text_matrix and by highest score, and redraws the table"""
        data = []
        for line in self.text_matrix:
            if not isinstance(line[0], type(0)):
                continue
            else:
                data.append(line)

        data.sort(reverse=True, key=lambda x: int(x[2]))
        self.text_matrix = []
        for line in data:
            self.text_matrix.append(line)

        self.update_scoreboard()

    def update_textmatrix_prediction(self):
        """
        Sorts text_matrix and by smallest absolute prediction,
        and redraws the table
        """
        data = []
        for line in self.text_matrix:
            if not isinstance(line[0], type(0)):
                continue
            else:
                data.append(line)

        data.sort(key=lambda x: abs(int(x[3])))

        self.text_matrix = []
        for line in data:
            self.text_matrix.append(line)

        self.update_scoreboard()

    def update_textmatrix_scoresecond(self):
        """
        Sorts text_matrix and by highest score second, and redraws the table
        """
        data = []
        for line in self.text_matrix:
            if not isinstance(line[0], type(0)):
                continue
            else:
                data.append(line)

        data.sort(reverse=True, key=lambda x: int(x[4]))
        self.text_matrix = []

        for line in data:
            self.text_matrix.append(line)

        self.update_scoreboard()

    def next_page(self):
        """
        Increments the matrix pointers, and redraws the table accordingly
        """
        if self.b >= len(self.text_matrix) or len(self.text_matrix) == 5:
            return

        self.page_number.set(str(int(self.page_number.get()) + 1))
        self.a += 4
        self.b += 4
        self.update_scoreboard()

    def previous_page(self):
        """
        Decrements the matrix pointers, and redraws the table accordingly
        """
        if self.a <= 0:
            return

        self.page_number.set(str(int(self.page_number.get()) - 1))
        self.a -= 4
        self.b -= 4
        self.update_scoreboard()


if __name__ == '__main__':
    app = MainProgram()
    app.mainloop()
