from tkinter import *
import tkinter.font as tkFont
import random


class UiLogger:
    LEVEL_VERBOSE = 0
    LEVEL_DEBUG = 1
    LEVEL_INFO = 2
    LEVEL_WARNING = 3
    LEVEL_ERROR = 4
    LEVELS = ['VERBOSE', 'DEBUG', 'INFO', 'WARNING', 'ERROR']
    COLORS = ['BLACK', 'GREY', 'GREEN', 'ORANGE', 'RED']
    FONT = 'Yahei Mono'

    class Item:
        LEN_LEVEL = 7
        LEN_LABEL = 10
        LEN_TEXT = 64

        def __init__(self, level: int, label: str, text: str):
            self.level = level
            self.label = label
            self.text = text
            self.var = self.form_var()
            self.res = self.var.get()
            self.simple = self.form_simple()

        def form_var(self):
            res_level = ("%-" + str(self.LEN_LEVEL) + "s") % UiLogger.LEVELS[self.level]
            res_label = ("%-" + str(self.LEN_LABEL) + "s") % self.label
            res_text = ("%-" + str(self.LEN_TEXT) + "s") % self.text
            var = StringVar()
            var.set("[{level}][{label}]{text}".format(level=res_level, label=res_label, text=res_text))
            return var

        def form_simple(self):
            res_text = ("%-" + str(self.LEN_TEXT) + "s") % self.text
            return "{text}".format(text=res_text)

        def __str__(self):
            return self.res

    def __init__(self, root,
                 label_frame: bool=True, title: str='Logger',
                 max_height: int=8,
                 simplify: bool=False,
                 # 没有用处。。。
                 width: int=None, height: int=None):
        self.root = root
        self.title = title
        self.max_height = max_height
        self.simplify = simplify
        if width is not None and height is not None:
            if label_frame:
                self.frame = LabelFrame(self.root, text=self.title, width=width, height=height)
            else:
                self.frame = Frame(self.root, width=width, height=height)
        else:
            if label_frame:
                self.frame = LabelFrame(self.root, text=self.title)
            else:
                self.frame = Frame(self.root)

        self.queue = []
        self.vars = [StringVar() for i in range(self.max_height)]
        ft = tkFont.Font(family=self.FONT, size=10, weight=tkFont.NORMAL)
        self.labels = [Label(self.frame, textvariable=self.vars[i], font=ft) for i in range(self.max_height)]
        # self.labels = [Label(self.frame, font=ft) for i in range(self.max_height)]
        for i in range(self.max_height):
            self.labels[i].grid(row=i, column=0, sticky=W+E)

    def logger(self):
        return self.frame

    def push(self, item: Item):
        if len(self.queue) >= self.max_height:
            self.queue.remove(self.queue[0])
            # self.queue = self.queue[:1]
            # self.queue = []
            self.queue.append(item)
            self.update()
            return
        self.queue.append(item)

        self.update()

    def update(self):
        for index in range(len(self.queue)):
            item = self.queue[index]
            label = self.labels[index]
            var = self.vars[index]

            if self.simplify:
                var.set(item.simple)
            else:
                var.set(item.res)
            label.configure(fg=self.COLORS[item.level])




