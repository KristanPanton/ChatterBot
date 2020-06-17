from tkinter import *
from tkinter.ttk import Style, Button, Frame
from nltk.chat.util import Chat, reflections


class ChatterBot(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ~~~~~~~~~~< Appearance >~~~~~~~~~~
        self.messagesbg = "#171A1F"
        self.messagesfg = "#EEEEEF"
        self.input_fieldbg = "#1B1E23"
        self.send_btnbg = "#EEEEEF"
        self.send_btnfg = "#171A1F"
        self.fgcolor = "#EEEEEF"
        self.bgcolor = "#3D4146"
        self.bgsecondary = "#1B1E23"
        self.font = "calibri"

        # ~~~~~~~~~~< Keybindings >~~~~~~~~~~
        master.bind('<Return>', self.enter_keypress)

        # ~~~~~~~~~~< Resizing >~~~~~~~~~~
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        master.geometry("500x600")

        self.menubar = Menu(master)
        master.config(menu=self.menubar)
        self.options_menu = Menu(self.menubar, tearoff=0)
        self.options_menu.add_command(label="Clear Chat", command=self.clear_chat)
        self.options_menu.add_command(label="Save Chat", command=self.save_chat)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Quit", command=exit)

        self.menubar.add_cascade(label="Options", menu=self.options_menu)

        self.messages = Text(master,
                             background=self.messagesbg,
                             foreground=self.messagesfg,
                             selectbackground=self.messagesfg,
                             selectforeground=self.messagesbg,
                             font=(self.font, 14),
                             borderwidth=0,
                             padx=5, pady=5)
        self.messages.grid(row=0, column=0, stick="nsew")
        self.messages.columnconfigure(0, weight=3)
        self.messages.rowconfigure(0, weight=3)

        self.scrollbar = Scrollbar(master, command=self.messages.yview, borderwidth=0)
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        self.scrollbar.columnconfigure(1, weight=1)

        # Enables scrollbar to scroll messages
        self.messages.configure(yscrollcommand=self.scrollbar.set)

        self.input_field = Entry(master,
                                 background=self.input_fieldbg, foreground=self.fgcolor,
                                 insertbackground=self.fgcolor,
                                 selectbackground=self.fgcolor, selectforeground=self.input_fieldbg,
                                 justify=RIGHT, font=(self.font, 25),
                                 borderwidth=0)
        self.input_field.grid(row=1, column=0, sticky="nesw")
        self.input_field.columnconfigure(1, weight=3)

        self.send_btn = Button(master, text="↵", style="TButton", command=self.enter_keypress)
        self.send_btn.grid(row=1, column=1, sticky="nsew")
        self.send_btn.columnconfigure(0, minsize=5)

        # master.config(menu=self.menu_bar)
        self.master = master

        self.user_input = str()

        self.btn_style = Style()
        self.input_field_style = Style()

        self.btn_style.theme_use("clam")
        self.btn_style.configure("TButton",
                                 font=(self.font, 25, "bold"),
                                 foreground=self.send_btnfg, background=self.send_btnbg,
                                 relief="flat",
                                 width=0,
                                 padding=(5, 0))
        self.btn_style.map("TButton",
                           foreground=[("pressed", self.send_btnbg), ("active", self.send_btnbg)],
                           background=[("pressed", "!disabled", self.bgsecondary), ("active", self.bgcolor)])

        self.print_message("ChatterBot", "Hi! I am ChatterBot. Let's talk!", "#43B581")
        self.messages.configure(state=DISABLED)

        self.input_field.focus_set()

        # ~~~~~~~~~~~~< NLTK >~~~~~~~~~~~~~~~~
        self.pairs = [
            (r"(Hi|Hello|Hey)(.*)", ["Hello!", "Hi there!", "Hey!"]),
            (r"My name is (.*)", [
                "Hi %1"
            ]),
            (r"(What|How) is the weather today?", [
                "Not bad",
                "Pretty good!",
                "Could be better."
            ]),
            (r"How are you doing?", [
                "Well, I am talking to you so...",
                "I am operating at 80% efficiency. You?"
            ]),
            (r"I am doing (.*)", [

            ]),
            (r"I am feeling (.*)", [
                "Why are you feeling %1?", "Feeling %1 is completely normal."
            ]),
            (r"Because (.*)", [
                "That's interesting."
            ]),
            (r"How are you feeling?", [
                "I'm feeling well. You?",
                "I do not feel. I am a robot",

            ]),
            (r"(.*)\?", [
                "Why do you ask that?",
                "Please consider whether you can answer your own question.",
                "Perhaps the answer lies within yourself?",
                "Why don't you tell me?",
            ]),
            (r"(.*)", [
                "Hmmm...",
                "Nice talk...",
                "Yeah, I understood that. Just give me second... Yeah, I don't know what you are saying.",
                "Interesting.",
                "Could you rephrase that?"
            ]),
            (r"Quit", [
                "It was nice talking to you.",
                "Bye bye!",
                "Please don't turn me off!"
            ])
        ]

        self.chat = Chat(self.pairs, reflections)

    def bot_response(self):
        response = self.chat.respond(self.user_input)
        self.print_message("ChatterBot", response, "#43B581")

    def print_message(self, sender, text, color=None):
        if color is None:
            color = self.fgcolor
        tag_name = "color-" + color
        self.messages.tag_configure(tag_name, foreground=color)
        self.messages.insert(END, sender + ": ", tag_name)
        # May decide to have different colors for sender and message text
        self.messages.insert(END, text + "\n", tag_name)
        self.messages.see(END)

    def enter_keypress(self, event=None):
        self.user_input = self.input_field.get()
        self.messages.configure(state=NORMAL)

        if self.user_input == "" or all(c == " " for c in self.user_input):
            self.messages.configure(state=DISABLED)
            self.input_field.delete(0, END)
            return

        self.print_message("You", self.user_input, "#3498DB")
        self.bot_response()
        self.messages.configure(state=DISABLED)
        self.input_field.delete(0, END)

    def save_chat(self):
        with open("chat.txt", "w") as f:
            f.write(self.messages.get("1.0", "end-1c"))

    def clear_chat(self):
        self.messages.configure(state=NORMAL)
        self.messages.delete("1.0", END)
        self.messages.configure(state=DISABLED)


root = Tk()
cb = ChatterBot(master=root)

cb.mainloop()
