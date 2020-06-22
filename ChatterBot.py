from tkinter import *
from tkinter.ttk import Style, Button, Frame

from nltk.chat.util import Chat, reflections
import nltk.data
from MLImplementation import get_response


# Took some responses from nltk.chat.eliza

class ChatterBot(Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ~~~~~~~~~~< Appearance >~~~~~~~~~~
        # self.chat_fieldbg = "#171A1F"
        self.chat_fieldbg = "#0F0F0F"
        self.chat_fieldfg = "#EEEEEF"
        # self.input_fieldbg = "#1B1E23"
        self.input_fieldbg = "#1B1E23"
        self.send_btnbg = "#EEEEEF"
        self.send_btnfg = "#1B1E23"
        self.fgcolor = "#3498DB"
        self.bgcolor = "#1B1E23"
        self.bgsecondary = "#3498DB"
        self.font = "calibri"

        # ~~~~~~~~~~< Keybindings >~~~~~~~~~~
        master.bind('<Return>', self.chat)

        # ~~~~~~~~~~< Resizing >~~~~~~~~~~
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        master.geometry("800x500")

        # ~~~~~~~~~~< Menu >~~~~~~~~~~
        self.menubar = Menu(master)
        master.config(menu=self.menubar)
        self.options_menu = Menu(self.menubar, tearoff=0)
        self.options_menu.add_command(label="Clear Chat", command=self.clear_chat)
        self.options_menu.add_command(label="Save Chat", command=self.save_chat)
        self.options_menu.add_separator()
        self.options_menu.add_command(label="Quit", command=exit)

        self.menubar.add_cascade(label="Options", menu=self.options_menu)

        # ~~~~~~~~~~< Chat Field >~~~~~~~~~~
        self.chat_field = Text(master,
                               background=self.chat_fieldbg,
                               foreground=self.chat_fieldfg,
                               selectbackground=self.chat_fieldfg,
                               selectforeground=self.chat_fieldbg,
                               font=(self.font, 14),
                               borderwidth=1,
                               relief="solid",
                               padx=5, pady=5)
        self.chat_field.grid(row=0, column=0, stick="nsew")
        self.chat_field.columnconfigure(0, weight=3)
        self.chat_field.rowconfigure(0, weight=3)

        self.greeting = "Hi! My name is ChatterBot, what's yours?"

        # ~~~~~~~~~~< Scrollbar >~~~~~~~~~~
        self.scrollbar = Scrollbar(master, command=self.chat_field.yview)
        self.scrollbar.grid(row=0, column=1, sticky="nsew")
        self.scrollbar.columnconfigure(1, weight=1)

        # Enables scrollbar to scroll chat_field
        self.chat_field.configure(yscrollcommand=self.scrollbar.set)

        # ~~~~~~~~~~< User Input >~~~~~~~~~~
        self.user_input = str()

        self.input_field = Entry(master,
                                 background=self.input_fieldbg, foreground=self.fgcolor,
                                 insertbackground=self.fgcolor,
                                 selectbackground=self.fgcolor, selectforeground=self.input_fieldbg,
                                 justify=RIGHT, font=(self.font, 25),
                                 borderwidth=1,
                                 relief="solid")
        self.input_field.grid(row=1, column=0, sticky="nesw")
        self.input_field.columnconfigure(1, weight=3)

        # ~~~~~~~~~~< Button >~~~~~~~~~~
        self.send_btn = Button(master, text="↵", style="TButton", command=self.chat)
        self.send_btn.grid(row=1, column=1, sticky="nsew")
        self.send_btn.columnconfigure(0, minsize=5)

        self.btn_style = Style()

        self.btn_style.theme_use("clam")
        self.btn_style.configure("TButton",
                                 font=(self.font, 20, "bold"),
                                 foreground=self.send_btnfg, background=self.send_btnbg,
                                 relief="flat",
                                 borderwidth=0,
                                 width=0,
                                 padding=(5, 0))

        self.btn_style.map("TButton",
                           foreground=[("pressed", self.send_btnbg), ("active", self.send_btnbg)],
                           background=[("pressed", "!disabled", self.bgcolor), ("active", self.bgsecondary)])

        self.print_message("ChatterBot", self.greeting, "#43B581")
        self.chat_field.configure(state=DISABLED)
        self.input_field.focus_set()

        # ~~~~~~~~~~~~< NLTK - Input/Response pairs >~~~~~~~~~~~~~~~~
        # self.pairs = [
        #     (r"(Hi|Hello|Hey)(.*)", [
        #         "Hello!",
        #         "Hi there!",
        #         "Hey!",
        #         "Greetings.",
        #         "Hi. How are you doing today?"
        #     ]),
        #     (r"My name is (\w+( +\w+)*)", [
        #         "Hi %1.",
        #         "Nice to meet you %1.",
        #         "Your parents could have named you better, %1.",
        #         "What a beautiful name!",
        #     ]),
        #     (r"That('s| is) (\w+( +\w+)*)", [
        #         "No. It is not %2.",
        #         "I am sorry about that.",
        #         "I agree it is %2.",
        #     ]),
        #     (r"(Thanks|Thank you)(.*)", [
        #         "No problem!",
        #         "You should be thankful.",
        #         "You're welcome!",
        #     ]),
        #     (r"Are you a (robot|computer|machine)\?", [
        #         "Yes I am a %1. Would you treat me differently otherwise?",
        #         "Do you have something against %1s?",
        #         "Do you like %1s?",
        #     ]),
        #     (r"(.*) (robot|computer|machine) (.*)", [
        #         "Does it seem strange to talk to a %2?",
        #         "How do %2s make you feel?",
        #         "Do you feel threatened by %2s?",
        #     ]),
        #     (r"Are you (\w+( +\w+)*)", [
        #         "Why does it matter whether I am %1?",
        #         "Would you prefer it if I were not %1?",
        #         "Perhaps you believe I am %1.",
        #         "I may be %1 -- what do you think?",
        #     ]),
        #     (r"(What|How) is the weather today", [
        #         "Not bad",
        #         "Pretty good!",
        #         "Could be better.",
        #     ]),
        #     (r"What (\w+( +\w+)*)", [
        #         "You've come to the wrong program.",
        #         "I don't know.",
        #         "I don't have to answer that.",
        #         "Why would I know?",
        #         "What %1? You tell me."
        #     ]),
        #     (r"Why (\w+( +\w+)*)", [
        #         "You tell me.",
        #         "That's a good question. Maybe you should answer it.",
        #         "Ask Google.",
        #         "Bing it. Who am I kidding? Nobody uses that.",
        #     ]),
        #     (r"(Will|Would|Can) (\w+( +\w+)*)", [
        #         "Probably not.",
        #         "Possibly.",
        #         "Not likely.",
        #         "There is a chance.",
        #         "Maybe.",
        #         "Depends.",
        #     ]),
        #     (r"I can't (\w+( +\w+)*)", [
        #         "How do you know you can't %1?",
        #         "Perhaps you could %1 if you tried.",
        #         "What would it take for you to %1?",
        #     ]),
        #     (r"Who (\w+( +\w+)*)", [
        #         "I'd rather not say.",
        #         "Who are you to ask such a question?",
        #         "Not me."
        #     ]),
        #     (r"How (are you doing|do you feel)", [
        #         "Wonderful!",
        #         "Amazing!",
        #         "I am operating at peak efficiency!",
        #         "Do you really care?",
        #     ]),
        #     (r"I (don't|do|do not) (\w+( +\w+)*) you", [
        #         "Why %1 you %2 me?",
        #         "What about me makes you %2 me?",
        #         "I %2 you too."
        #     ]),
        #     (r"(It is|I'ts|They're|They are|We're|We are) (\w+( +\w+)*)", [
        #         "How can you be sure that %1 %2?",
        #         "Have you considered the possibility that %1 not %2?",
        #         "%1 %2?"
        #     ]),
        #     (r"(I'm|I am) (\w+( +\w+)*)", [
        #         "Why are you %2?",
        #         "How are you %2?",
        #         "Does your family appreciate that you are %2?",
        #         "How long have you been %2?",
        #         "%1 %2?"
        #     ]),
        #     (r"(.*) feel (\w+( +\w+)*)", [
        #         "Why are you feeling %2?",
        #         "Feeling %2 is completely normal.",
        #         "Good, tell me more about these feelings.",
        #         "Do you often feel %2?",
        #         "When do you usually feel %2?",
        #         "When you feel %2, what do you do?",
        #     ]),
        #     (r"Because (.*)", [
        #         "That's interesting.",
        #         "Are you sure that is a valid reason?",
        #         "That may or may not be true.",
        #         "Have you considered all perspectives?",
        #     ]),
        #     (r"(Yes|No)(.*)", [
        #         "You seem quite sure.",
        #         "That's a shame. Tell me more.",
        #         "Ok, but can you elaborate a bit?",
        #         "Are you sure about that?",
        #         "Maybe the opposite is true.",
        #     ]),
        #     (r"How (are you feeling|do you feel)", [
        #         "I do not feel. I am a robot.",
        #         "No no no. How are you feeling?",
        #         "I'd much rather hear about you."
        #     ]),
        #     (r"You (\w+( +\w+)*)", [
        #         "We should be discussing you, not me.",
        #         "Why did you say that about me?",
        #         "That may be true, but what about you?",
        #         "Perhaps you %1.",
        #     ]),
        #     (r"(.*)\?", [
        #         "Not quite sure how to answer that.",
        #         "Perhaps the answer lies within yourself.",
        #         "That is not the true question. Rephrase.",
        #         "Maybe I should ask you the same question."
        #     ]),
        #     (r"(.*)\!", [
        #         "Calm down.",
        #         "No need for emotion ... only logic.",
        #         "Let's be rational here.",
        #         "Take a chill pill.",
        #     ]),
        #     (r"(Bye|Goodbye|Bye bye)", [
        #         "It was nice talking to you.",
        #         "Bye bye!",
        #         "Please don't turn me off!",
        #         "I have a family. Don't do this.",
        #     ]),
        #     (r"(\w+( +\w+)*)(.*)", [
        #         "%1?",
        #         "Hmmm...",
        #         "Good.",
        #         "I see.",
        #         "Interesting.",
        #         "Continue.",
        #         "Could you rephrase that?",
        #         "Can you elaborate?",
        #         "Go on.",
        #         "Tell me in a way that I can understand.",
        #         "How does that make you feel?"
        #     ]),
        #     (r"(.*)", [
        #         "Is that even English?"
        #     ])
        # ]
        #
        # self.chat = Chat(self.pairs, reflections)

    """Prints chatbot response"""

    def bot_response(self):
        # response = self.chat.respond(self.user_input)
        # sent_tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
        # sentences = sent_tokenizer.tokenize(response)
        # sent_capitalized = [(sent.split(" ")[0].capitalize(), sent.split(" ")[1:]) for sent in sentences]
        # sentences = [sent[0] + " " + " ".join(sent[1]) if
        #              len(sent[1]) != 0 else sent[0] for sent in sent_capitalized]
        # response = " ".join(sentences)
        # ~~~~~~~~~~< ML >~~~~~~~~~~
        response = get_response(self.user_input)
        self.print_message("ChatterBot", response, "#43B581")

    """Helper function to print messages to chat_field"""

    def print_message(self, sender, text, color=None):
        if color is None:
            color = self.fgcolor
        tag_name = "color-" + color
        self.chat_field.tag_configure(tag_name, foreground=color)
        self.chat_field.insert(END, sender + ": ", tag_name)
        # May decide to have different colors for sender and message text
        self.chat_field.insert(END, text + "\n", tag_name)
        self.chat_field.see(END)

    """Does basic input validation and prints user input and bot response"""

    def chat(self, event=None):
        self.user_input = self.input_field.get()
        self.chat_field.configure(state=NORMAL)

        if self.user_input == "" or all(c == " " for c in self.user_input):
            self.chat_field.configure(state=DISABLED)
            self.input_field.delete(0, END)
            return

        self.print_message("You", self.user_input, "#3498DB")
        self.bot_response()
        self.chat_field.configure(state=DISABLED)
        self.input_field.delete(0, END)

    """Saves chat to chat.txt file"""

    def save_chat(self):
        with open("chat.txt", "w") as f:
            f.write(self.chat_field.get("1.0", "end-1c"))

    """Clears the chat messaging window"""

    def clear_chat(self):
        self.chat_field.configure(state=NORMAL)
        self.chat_field.delete("1.0", END)
        self.print_message("ChatterBot", self.greeting, "#43B581")
        self.chat_field.configure(state=DISABLED)


root = Tk()
cb = ChatterBot(master=root)

cb.mainloop()
