import tkinter as tk
from tkinter.font import Font
from PIL import ImageTk, Image

# fix blurry font
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


class MainProgram(tk.Tk):
    """This class drives the program"""
    def __init__(self):
        tk.Tk.__init__(self)

        # program window variables
        self.GAME_WINDOW_CAPTION = '2048 - Python Version'
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 700

        # controls
        self.slide_up_control = 'Up'
        self.slide_down_control = 'Down'
        self.slide_left_control = 'Left'
        self.slide_right_control = 'Right'

        # intialise window
        self.title(self.GAME_WINDOW_CAPTION)
        self.minsize(self.GAME_WIDTH, self.GAME_HEIGHT)
        self.geometry('{}x{}'.format(self.GAME_WIDTH, self.GAME_HEIGHT))
        self.center_screen(self.GAME_WIDTH, self.GAME_HEIGHT)

        # initialise all program wide fonts
        self.DESCRIPTION_FONT = Font(family="Helvetica", size=12)
        self.BUTTON_FONT = Font(family="Helvetica", size=16)
        self.TITLE_FONT = Font(family="Helvetica", size=28, weight='bold')

        # declare master frame
        self.GAME_MARGIN_X = 0
        self.GAME_MARGIN_Y = 0
        self.container = tk.Frame(self)
        self.container.pack(padx=self.GAME_MARGIN_X, pady=self.GAME_MARGIN_Y)

        # current frame used
        self.current_frame = None

        # initialise by showing the main menu page
        self.show_frame(MainMenu)

    def center_screen(self, window_width, window_height):
        """centers the spawned screen"""
        offset_right = int(self.winfo_screenwidth()/2 - window_width/2)
        offset_down = int((self.winfo_screenheight()-40)/2 - window_height / 2)

        self.geometry('+{}+{}'.format(offset_right, offset_down))

    def show_frame(self, frame_class):
        """displays given frame"""
        if self.current_frame is not None:
            self.current_frame.destroy()

        frame = frame_class(self.container, self)
        frame.grid(row=0, column=0, sticky='news')
        self.current_frame = frame


class MainMenu(tk.Frame):
    """This class is the main menu frame"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=controller.GAME_WIDTH, height=controller.GAME_HEIGHT)
        self.controller = controller

        # create canvas
        self.create_canvas()

        # display background
        self.display_background('mainmenubackground.png')

        # create button frame
        button_frame = tk.Frame(self, width=250, height=250)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_propagate(False)

        # create buttons
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
        # change pixels_below_center to push the menu buttons lower
        pixels_below_center = 130
        self.display_object_on_canvas(
            button_frame,
            controller.GAME_WIDTH // 2 - 0.5*button_frame['width'],
            controller.GAME_HEIGHT // 2 - 0.5*button_frame['height'] + pixels_below_center)

    def create_canvas(self):
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def display_background(self, imagepath):
        # draws and paints the background with image of given path
        background_image = Image.open(imagepath)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
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
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def display_background(self, imagepath):
        # draws and paints the background with image of given path
        background_image = Image.open(imagepath)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
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

        # is in the process of binding
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

        # display the input field grid 2x4 table (width, height)
        # the background color determines the border color
        table_2x4 = tk.Frame(self, width=550, height=220, bg='black')
        table_2x4.grid_propagate(0)
        table_2x4.grid_columnconfigure(0, weight=1)
        table_2x4.grid_columnconfigure(1, weight=1)
        table_border_width = 2

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

        # Initialse button, set button to what it was saved to
        def intialise_control_button(button, button_save_string):
            button['fg'] = 'black'
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
            # UNBIND all keys to given buttons
            def unbind_keys(button):
                button.unbind('<Key>')
                button.unbind('<Left>')
                button.unbind('<Up>')
                button.unbind('<Right>')
                button.unbind('<Down>')

            # given which self variable control string to change, it changes it.
            def set_command_for(string, command):
                self.is_binding = False
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
                try:
                    button['text'] = str(event.keysym)
                    set_command_for(button_save_string, event.keysym)

                except Exception:
                    button['text'] = str(event.char)
                    set_command_for(button_save_string, event)

                unbind_keys(button)

            # given an arrow key event, it sets the commands to it and changes button text
            def arrow_key(event):
                set_command_for(button_save_string, event.keysym)
                button['text'] = event.keysym + ' arrow key'
                unbind_keys(button)

            # sets is binding to false and the button to the current value it has (removes 'enter your key')
            def set_to_current_value():
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
                    if self.slide_up_control in ('Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_up_control + ' arrow key'

                    else:
                        button['text'] = controller.slide_up_control

                elif button_save_string == 'down':
                    if controller.slide_down_control in ('Left', 'Right', 'Up', 'Down'):
                        button['text'] = controller.slide_down_control + ' arrow key'

                    else:
                        button['text'] = controller.slide_down_control

            # BEGIN MAIN FUNCTION CONTENT

            # If clicked and already asking for a key, un toggle this option and exit function
            if button['text'] == 'Enter new key':
                set_to_current_value()
                unbind_keys(button)
                self.is_binding = False
                return

            # If clicked and another option already in action, don't do anything
            elif self.is_binding:
                return

            # Otherwise, display the 'enter new key' option in red
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

        # Allow all the inputs to have this switch_key ability on click
        control_up_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_up_input, 'up'))
        intialise_control_button(control_up_input, 'up')

        control_down_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_down_input, 'down'))
        intialise_control_button(control_down_input, 'down')

        control_left_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_left_input, 'left'))
        intialise_control_button(control_left_input, 'left')

        control_right_input = tk.Button(table_2x4, text='', command=lambda: switch_keys(control_right_input, 'right'))
        intialise_control_button(control_right_input, 'right')

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
        # is the table still asking for a key
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
        self.canvas = tk.Canvas(
            self,
            bd=-2,
            height=self.controller.GAME_HEIGHT,
            width=self.controller.GAME_WIDTH)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

    def display_background(self, imagepath):
        # draws and paints the background with image of given path
        background_image = Image.open(imagepath)
        self.canvas.image = ImageTk.PhotoImage(background_image)
        self.canvas.create_image((0, 0), image=self.canvas.image, anchor='nw')

    def display_object_on_canvas(self, tk_object, x, y):
        button1_window = self.canvas.create_window(
            x,
            y,
            anchor='nw',
            window=tk_object)

    def remove_object_from_canvas(self, tk_object):
        self.canvas.delete(tk_object)

class MainGame(tk.Frame):
    """This class is the 2048 game frame"""
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=controller.GAME_WIDTH, height=controller.GAME_HEIGHT)
        self.controller = controller

        temp_label = tk.Label(self, text='this is the game page')
        temp_label.pack()

        temp_button = tk.Button(self, text='go back', command=lambda: controller.show_frame(MainMenu))
        temp_button.pack()


if __name__ == '__main__':
    app = MainProgram()
    app.mainloop()