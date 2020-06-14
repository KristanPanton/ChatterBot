from tkinter import *
from tkinter.ttk import *
from nltk.chat.util import Chat, reflections


# pairs = [
#     ['my name is (.*)', ['hi %1']],
#     ['how are you doing?', ["i'm doing fine. You?"],
#      [f""]
#      ]
# ]

# chat = Chat(pairs, reflections)
# chat.converse()


# Creates menu bar
class ChatterBot(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.bgcolor = "#111218"
        self.fgcolor = "#7699E5"
        self.bgsecondary = "#2C3858"

        master.bind('<Return>', self.enter_keypress)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.menu_bar = Menu(master)
        self.menu_bar.add_command(label="File")
        self.menu_bar.add_command(label="Edit")
        self.menu_bar.add_command(label="Quit")

        self.messages = Text(master,
                             state=DISABLED,
                             background=self.bgcolor,
                             foreground=self.fgcolor,
                             selectbackground=self.fgcolor,
                             selectforeground=self.bgcolor,
                             font=("calibri", 14, "bold")
                             )

        self.input_field = Entry(master, style="TEntry", justify=RIGHT, font=("calibri", 30))
        # self.input_field.configure(insertbackground=self.fgcolor)

        self.send_btn = Button(master, text="Send", style="TButton", command=self.enter_keypress)

        self.send_btn.grid(row=1, column=1, sticky="nsew")
        self.send_btn.columnconfigure(0, minsize=5)

        self.messages.grid(row=0, column=0, columnspan=2, stick="nsew")
        self.messages.columnconfigure(0, weight=3)
        self.messages.rowconfigure(0, weight=3)

        master.config(menu=self.menu_bar)
        self.master = master

        self.user_input = str()

        self.btn_style = Style()
        self.input_field_style = Style()

        self.btn_style.theme_use("clam")
        self.btn_style.configure("TButton",
                                 font=("calibri", 18, "bold"),
                                 foreground=self.fgcolor,
                                 background=self.bgcolor,
                                 relief="flat",
                                 width=0,
                                 borderwidth=0
                                 )

        self.btn_style.map("TButton",
                           foreground=[("pressed", self.fgcolor), ("active", self.bgcolor)],
                           background=[("pressed", "!disabled", self.bgsecondary), ("active", self.fgcolor)],
                           )

        self.input_field_style.configure("TEntry",
                                         background=self.bgcolor,
                                         foreground=self.fgcolor,
                                         fieldbackground=self.bgcolor,
                                         selectbackground=self.fgcolor,
                                         selectforeground=self.bgcolor,
                                         )

        self.input_field.grid(row=1, column=0, sticky="nesw")
        self.input_field.columnconfigure(1, weight=3)

        self.input_field.focus_set()

    def enter_keypress(self, event=None):
        self.user_input = self.input_field.get()
        self.messages.configure(state=NORMAL)

        if self.user_input == "" or all(c == " " for     c in self.user_input):
            self.messages.configure(state=DISABLED)
            self.input_field.delete(0, END)
            return

        self.messages.insert(END, "You: " + self.user_input + "\n")
        self.messages.configure(state=DISABLED)
        self.input_field.delete(0, END)
        return "break"


root = Tk()
cb = ChatterBot(master=root)
cb.mainloop()
