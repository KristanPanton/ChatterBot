from tkinter import *
from tkinter.ttk import Style, Button, Frame
from nltk.chat.util import Chat, reflections


# Took some responses from nltk.chat.eliza

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
        self.bgsecondary = "#3498DB"
        self.font = "calibri"

        # ~~~~~~~~~~< Keybindings >~~~~~~~~~~
        master.bind('<Return>', self.enter_keypress)

        # ~~~~~~~~~~< Resizing >~~~~~~~~~~
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        master.geometry("800x500")

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
                                 font=(self.font, 20, "bold"),
                                 foreground=self.send_btnfg, background=self.send_btnbg,
                                 relief="flat",
                                 width=0,
                                 padding=(5, 0))
        self.btn_style.map("TButton",
                           foreground=[("pressed", self.send_btnbg), ("active", self.send_btnbg)],
                           background=[("pressed", "!disabled", self.bgsecondary), ("active", self.bgcolor)])

        self.print_message("ChatterBot", "Hi! My name is ChatterBot, what is yours?", "#43B581")
        self.messages.configure(state=DISABLED)

        self.input_field.focus_set()

        # ~~~~~~~~~~~~< NLTK >~~~~~~~~~~~~~~~~
        self.pairs = [
            (r"(Hi|Hello|Hey)(.*)", [
                "Hello!",
                "Hi there!",
                "Hey!",
                "Greetings."
            ]),
            (r"My name is (\w+( +\w+)*)", [
                "Hi %1.",
                "Nice to meet you %1.",
                "Your parents could have named you better, %1.",
                "What a beautiful name!",
            ]),
            (r"That('s| is) (\w+( +\w+)*)", [
                "No. It is not %2.",
                "I am sorry about that.",
                "I agree it is %2.",
            ]),
            (r"(Thanks|Thank you)(.*)", [
                "No problem!",
                "You should be thankful.",
                "You're welcome!",
            ]),
            (r"Are you a (robot|computer|machine)\?", [
                "Yes I am a %1. Would you treat me differently otherwise?",
                "Do you have something against %1s?",
                "Do you like %1s?",
            ]),
            (r"(.*) (robot|computer|machine) (.*)", [
                "Does it seem strange to talk to a %2?",
                "How do %2s make you feel?",
                "Do you feel threatened by %2s?",
            ]),
            (r"Are you (\w+( +\w+)*)", [
                "Why does it matter whether I am %1?",
                "Would you prefer it if I were not %1?",
                "Perhaps you believe I am %1.",
                "I may be %1 -- what do you think?",
            ]),
            (r"(What|How) is the weather today", [
                "Not bad",
                "Pretty good!",
                "Could be better.",
            ]),
            (r"What (\w+( +\w+)*)", [
                "You've come to the wrong program.",
                "I don't know.",
                "I don't have to answer that.",
                "Why would I know?",
                "What %1? You tell me."
            ]),
            (r"Why (\w+( +\w+)*)", [
                "You tell me.",
                "That's a good question. Maybe you should answer it.",
                "Ask Google.",
                "Bing it. Who am I kidding? Nobody uses that.",
            ]),
            (r"(Will|Would|Can) (\w+( +\w+)*)", [
                "Probably not.",
                "Possibly.",
                "Not likely.",
                "There is a chance.",
                "Maybe.",
                "Depends.",
            ]),
            (r"I can't (\w+( +\w+)*)", [
                "How do you know you can't %1?",
                "Perhaps you could %1 if you tried.",
                "What would it take for you to %1?",
            ]),
            (r"Who (\w+( +\w+)*)", [
                "I'd rather not say.",
                "Who are you to ask such a question?",
                "Not me."
            ]),
            (r"How (are you doing|do you feel)", [
                "Wonderful!",
                "Amazing!",
                "I am operating at peak efficiency!",
                "Do you really care?",
            ]),
            (r"(I'm|I am) (\w+( +\w+)*)", [
                "Why are you %2?",
                "How are you %2?",
                "Does your family appreciate that you are %2?",
                "How long have you been %2?",
                "%1 %2?"
            ]),
            (r"(.*) feel (\w+( +\w+)*)", [
                "Why are you feeling %2?",
                "Feeling %2 is completely normal.",
                "Good, tell me more about these feelings.",
                "Do you often feel %2?",
                "When do you usually feel %2?",
                "When you feel %2, what do you do?",
            ]),
            (r"Because (.*)", [
                "That's interesting.",
                "Are you sure that is a valid reason?",
                "That may or may not be true.",
                "Have you considered all perspectives?",
            ]),
            (r"(Yes|No)(.*)", [
                "You seem quite sure.",
                "That's a shame. Tell me more.",
                "Ok, but can you elaborate a bit?",
                "Are you sure about that?",
                "Maybe the opposite is true.",
            ]),
            (r"How (are you feeling|do you feel)(.*)", [
                "I do not feel. I am a robot.",
                "No no no. How are you feeling?",
                "I'd much rather hear about you."
            ]),
            (r"You (\w+( +\w+)*)", [
                "We should be discussing you, not me.",
                "Why do you say that about me?",
                "That may be true, but what about you?",
                "Perhaps you %1.",
            ]),
            (r"(.*)\?", [
                "Not quite sure how to answer that.",
                "Perhaps the answer lies within yourself.",
                "That is not the true question. Rephrase.",
                "Maybe I should ask you the same question."
            ]),
            (r"(.*)\!", [
                "Calm down.",
                "No need for emotion ... only logic.",
                "Let's be rational here.",
                "Take a chill pill.",
            ]),
            (r"(Bye|Goodbye|Bye bye)", [
                "It was nice talking to you.",
                "Bye bye!",
                "Please don't turn me off!",
                "I have a family. Don't do this.",
            ]),
            (r"(\w+( +\w+)*)(.*)", [
                "%1?",
                "Hmmm...",
                "Good.",
                "I see.",
                "Interesting.",
                "Continue.",
                "Could you rephrase that?",
                "Can you elaborate?",
                "Go on.",
                "Tell me in a way that I can understand.",
                "How does that make you feel?"
            ]),
            (r"(.*)", [
                "Is that even English?"
            ])

        ]
        # reflections["are"] = "am"
        self.chat = Chat(self.pairs, reflections)

    def bot_response(self):
        response = self.chat.respond(self.user_input).capitalize()
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
        self.print_message("ChatterBot", "Hi! My name is ChatterBot, what is yours?", "#43B581")
        self.messages.configure(state=DISABLED)


root = Tk()
cb = ChatterBot(master=root)

cb.mainloop()
