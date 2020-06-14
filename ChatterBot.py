from tkinter import *
from tkinter.ttk import Style, Button, Frame
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

        # self.messagesbg = "#111218"
        self.messagesbg = "#F0F0F0"
        self.messagesfg = "black"
        self.input_fieldbg = "firebrick4"
        self.send_btnbg = "firebrick3"
        self.fgcolor = "white"
        self.bgcolor = "grey5"
        self.bgsecondary = "firebrick4"

        master.bind('<Return>', self.enter_keypress)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        # self.menu_bar = Menu(master)
        # self.menu_bar.add_command(label="File")
        # self.menu_bar.add_command(label="Edit")
        # self.menu_bar.add_command(label="Quit")

        self.messages = Text(master,
                             state=DISABLED,
                             background=self.messagesbg,
                             foreground=self.messagesfg,
                             selectbackground=self.messagesfg,
                             selectforeground=self.messagesbg,
                             font=("calibri", 14, "bold"),
                             borderwidth=0
                             )

        self.messages.grid(row=0, column=0, stick="nsew")
        self.messages.columnconfigure(0, weight=3)
        self.messages.rowconfigure(0, weight=3)

        self.scrollbar = Scrollbar(master, command=self.messages.yview, borderwidth=0)
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        self.scrollbar.columnconfigure(1, weight=1)

        self.messages.configure(yscrollcommand=self.scrollbar.set)

        self.input_field = Entry(master,
                                 insertbackground=self.fgcolor,
                                 background=self.input_fieldbg,
                                 foreground=self.fgcolor,
                                 selectbackground=self.fgcolor,
                                 selectforeground=self.input_fieldbg,
                                 justify=RIGHT,
                                 font=("calibri", 30),
                                 borderwidth=0
                                 )

        self.input_field.grid(row=1, column=0, sticky="nesw")
        self.input_field.columnconfigure(1, weight=3)

        self.send_btn = Button(master, text="Send", style="TButton", command=self.enter_keypress)

        self.send_btn.grid(row=1, column=1, sticky="nsew")
        self.send_btn.columnconfigure(0, minsize=5)

        # master.config(menu=self.menu_bar)
        self.master = master

        self.user_input = str()

        self.btn_style = Style()
        self.input_field_style = Style()

        self.btn_style.theme_use("clam")
        self.btn_style.configure("TButton",
                                 font=("calibri", 18, "bold"),
                                 foreground=self.fgcolor,
                                 background=self.send_btnbg,
                                 relief="flat",
                                 width=0,
                                 borderwidth=0,
                                 padding=(10, 0)
                                 )

        self.btn_style.map("TButton",
                           foreground=[("pressed", self.fgcolor), ("active", self.input_fieldbg)],
                           background=[("pressed", "!disabled", self.bgsecondary), ("active", self.fgcolor)],
                           )

        self.input_field.focus_set()

    def print_message(self, sender, text, color=None):
        if color is None:
            color = self.fgcolor
        tag_name = "color-" + color
        self.messages.tag_configure(tag_name, foreground=color)
        self.messages.insert(END, sender + ": ", tag_name)
        self.messages.insert(END, text + "\n", )
        self.messages.see(END)

    def enter_keypress(self, event=None):
        self.user_input = self.input_field.get()
        self.messages.configure(state=NORMAL)

        if self.user_input == "" or all(c == " " for c in self.user_input):
            self.messages.configure(state=DISABLED)
            self.input_field.delete(0, END)
            return

        self.print_message("You", self.user_input, self.input_fieldbg)
        # self.messages.insert(END, "You: " + self.user_input + "\n")
        self.messages.configure(state=DISABLED)
        self.input_field.delete(0, END)
        return "break"


root = Tk()
cb = ChatterBot(master=root)
cb.mainloop()
