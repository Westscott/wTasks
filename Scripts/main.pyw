import os
import json 
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import config as cf

class AppMain:
    def __init__(self):
        super().__init__()
        self.activeFont = (cf._selectedTypeface, cf._fontSize)
        
        # Frame & Widget Arrays
        self.totalFrames = []
        self.totalWidgets = []
        
        self.secondaryFrames = []
        
        self.catFrameList = []
        self.secondaryWidgets = []

        # Command line in/out variables
        self.clOutText = ""
        self.clOutIndex = 0
        self.isWriting = False
        self.breakLoop = False

        # Root Frame
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("wTasks")
        self.root.eval('tk::PlaceWindow . center')
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.totalFrames.append(self.root)
        
        # Init UI
        self.initBaseUI()
        self.initContentUI()
        
        self.changeColorTheme(0)
        
        # Setup Keybinds
        self.root.bind("<Control-space>", lambda event: self.clInput.focus())
        self.clInput.bind("<KeyRelease>", self.checkInput)
        self.clInput.bind("<Return>", self.runCommand)
        
        self.LoadData()
        # Run Main UI Loop
        self.root.mainloop()



    def initBaseUI(self):
        #! COMMAND FRAME
        self.commandFrame = tk.Frame(self.root)
        self.commandFrame.pack(side=tk.BOTTOM, fill=tk.X)
        self.secondaryFrames.append(self.commandFrame)
        
        self.clInput = tk.Entry(self.commandFrame, width=15, font=self.activeFont)
        self.clInput.pack(side=tk.LEFT)
        self.clInput.insert(tk.END, "/")
        self.totalWidgets.append(self.clInput)
        
        self.clOutput = tk.Entry(self.commandFrame, font=self.activeFont)
        self.clOutput.insert(tk.END, ">>")
        self.clOutput.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.totalWidgets.append(self.clOutput)

        #! NOTEBOOK / TAB FRAME
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        self.nstyle = ttk.Style()
        self.nstyle.theme_use('default')

        self.mainFrame = tk.Frame(self.notebook)
        self.notebook.add(self.mainFrame, text="[Tasks]")
        self.totalFrames.append(self.mainFrame)

        self.configFrame = tk.Frame(self.notebook)
        self.notebook.add(self.configFrame, text="[CONFIG]")
        self.totalFrames.append(self.configFrame)

        #!----- CONTENT -----!#
        
        #?--- CONFIG BASE ---?#
        self.themeValue = tk.StringVar()
        self.themeValue.set(cf._themeOptions[0])
        self.themeComboBox = tk.OptionMenu(self.configFrame, self.themeValue, *cf._themeOptions, command= lambda event: self.changeColorTheme(0, 3))
        self.themeComboBox.configure(font=self.activeFont)
        menu = self.root.nametowidget(self.themeComboBox.menuname)
        menu.configure(font=self.activeFont)
        self.themeComboBox.pack()
        self.totalWidgets.append(self.themeComboBox)

    def initContentUI(self):
        self.itemDisplayArray = []
        self.itemNameArray = []
        self.itemDisplayFrameArray = []
        
        self.activeItemFrame = tk.Frame(self.mainFrame)
        self.activeItemFrame.pack(side=tk.LEFT, fill=tk.Y)
        self.totalFrames.append(self.activeItemFrame)
        
        self.taskCatFrame = tk.Frame(self.mainFrame)
        self.taskCatFrame.pack(side=tk.LEFT, fill=tk.Y)
        self.totalFrames.append(self.activeItemFrame)
        
        self.activeItemsList = tk.Listbox(self.activeItemFrame)
        self.activeItemsList.pack(fill=tk.Y, expand=1)
        self.totalWidgets.append(self.activeItemsList)
        
        self.addCatBtn = tk.Button(self.activeItemFrame, text="Add Category", command=self.addTaskCategory)
        self.addCatBtn.pack(side=tk.LEFT)
        self.totalWidgets.append(self.addCatBtn)


    def LoadData(self):
        if not os.path.isfile('wTaskData.json'):
            self.SaveData()
            
        with open('wTaskData.json', 'r') as _file:
            data = json.load(_file)
        settings = data['settings']
        
        categories = data['categories']
        for cats in categories:
            self.addTaskCategory(cats['name'])
            #! Another loop for items 
                


    def SaveData(self):
        _settingData = {
            'appTheme': f"{cf._themeOptions.index(self.themeValue.get())}"
        }
        
        _catNum = len(self.itemDisplayFrameArray)
        
        _cats = []
        for x in range(_catNum):
            # init loop for list items
            _cats.append({
                'id': str(x),
                'name': f"{self.itemNameArray[x]}"
            })
        _data = {
            'settings': _settingData,
            'categories': _cats
        }
        with open('wTaskData.json', 'w') as _file:
            json.dump(_data, _file, indent=4)
            
            

    def addTaskCategory(self, _catName=None):
        
        _sIndex = cf._themeOptions.index(self.themeValue.get())
        
        self.itemDisplayFrameArray.append(tk.Frame(self.mainFrame))
        _fIndex = len(self.itemDisplayFrameArray)-1
        self.itemDisplayFrameArray[_fIndex].pack(side=tk.LEFT, fill=tk.Y)
        self.catFrameList.append(self.itemDisplayFrameArray[_fIndex])
        
        if _catName == None:
            _catName = f"Category {_fIndex}"
        
        self.secondaryWidgets.append(tk.Label(self.itemDisplayFrameArray[_fIndex], text=f"{_catName}"))
        _swIndex = len(self.secondaryWidgets)-1
        self.secondaryWidgets[_swIndex].pack(side=tk.TOP)
        self.itemNameArray.append(f"{_catName}")
        
        
        self.itemDisplayArray.append(tk.Listbox(self.itemDisplayFrameArray[_fIndex]))
        _wIndex = len(self.itemDisplayArray)-1
        self.itemDisplayArray[_wIndex].pack(side=tk.LEFT, fill=tk.Y, expand=1)
        self.itemDisplayArray[_wIndex].configure(background=cf._backgroundColors[_sIndex], fg=cf._typefaceColors[_sIndex])



    def on_close(self):
        self.SaveData()
        self.root.destroy()

    def changeColorTheme(self, event=None, tIndex=None):
        
        if tIndex == 3:
            _index = cf._themeOptions.index(self.themeValue.get())
        elif tIndex != None: 
            _index = tIndex
        else:
            _index = 0
        
        if tIndex != None:
            if _index == 0:
                self.clOutText=">> Color theme change to dark"
            else:
                self.clOutText=">> Color theme change to light"
            self.clOutIndex = 0
            self.clOutput.delete(0, tk.END)
            self.writingOut = 1
            if self.isWriting:
                self.breakLoop = True
            self.outputTyper()


        for _frame in self.totalFrames:
            _frame.configure(bg=cf._backgroundColors[_index])
        for _frame in self.catFrameList:
            _frame.configure(bg=cf._backgroundColors[_index])
        for _widget in self.totalWidgets:
            _widget.configure(
                bg=cf._backgroundColors[_index], 
                fg=cf._typefaceColors[_index], 
                highlightcolor=cf._backgroundColors[_index]
            )
        for _widget in self.itemDisplayArray:
            _widget.configure(
                bg=cf._backgroundColors[_index], 
                fg=cf._typefaceColors[_index], 
                highlightcolor=cf._backgroundColors[_index]
            )
        for _widget in self.secondaryWidgets:
            _widget.configure(
                bg=cf._backgroundColors[_index], 
                fg=cf._typefaceColors[_index], 
                highlightcolor=cf._backgroundColors[_index]
            )
            
        self.nstyle.configure('TNotebook.Tab',
            background=cf._tabColors[_index][1],
            foreground=cf._backgroundColors[_index],
            bordercolor=cf._backgroundColors[_index],
            borderwidth=0, 
            tabmargins=0
        )
        self.nstyle.map("TNotebook.Tab", background=[("selected", cf._tabColors[_index][0])])
        self.nstyle.configure('TNotebook', 
            background=cf._backgroundColors[_index],
            highlightbackground=cf._backgroundColors[_index],
            bordercolor=cf._backgroundColors[_index],
            borderwidth=0, 
            tabmargins=0
        )
        self.clInput.configure(insertbackground=cf._typefaceColors[_index])
        self.clOutput.configure(insertbackground=cf._typefaceColors[_index])

    def checkInput(self, event=None):
        _input = str(self.clInput.get()[1:])
        self.clInput.delete(0, tk.END)
        self.clInput.insert(0, f"/{_input}")

    def runCommand(self, event=None):
        _input = str(self.clInput.get()[1:])

        if _input == "1":
            self.notebook.select(0)
            self.clOutText=">> Main Page Loaded"
        elif _input == "2":
            self.notebook.select(1)
            self.clOutText=">> Settings Page Loaded"
        elif "help" in _input.lower():
            self.popupWindow("", "BASIC COMMANDS\n'help' - Basic command list\ninfo - General info on app & pc\n[1,2] - Change active tab")
            self.clOutText=">> help, info, 1, 2"
        elif "light" in _input.lower():
            self.changeColorTheme(0, 1)
        elif "dark" in _input.lower():
            self.changeColorTheme(0, 0)
        elif "exit" in _input.lower():
            self.clOutText=">> Goodbye < 3 "
        elif "ca" in _input.lower():
            cName = None
            if len(_input) > 2:
                cName = f"{_input[3:]}"
            self.addTaskCategory(cName)
            self.clOutText=f">> New Category added '{cName}'"
        elif "cd" in _input.lower():
            _index = int(_input[3:])
            self.itemDisplayFrameArray[_index].destroy()
            self.itemDisplayFrameArray.pop(_index)
            self.itemDisplayArray.pop(_index)
            self.itemNameArray.pop(_index)
            self.catFrameList.pop(_index)
            self.secondaryWidgets.pop(_index)
            self.clOutText=f">> New Category deleted at index '{_index}'"
            
        else:
            self.clOutText=f">> Command '{_input}' not found"

        self.clInput.delete(0, tk.END)
        self.clOutIndex = 0
        self.clOutput.delete(0, tk.END)
        self.writingOut = 1
        if self.isWriting:
            self.breakLoop = True
        self.outputTyper()

    def outputTyper(self):
        self.isWriting = True
        if self.breakLoop:
            self.breakLoop = False
            self.clOutIndex = 0
            return
        self.clOutput.insert(tk.END, self.clOutText[self.clOutIndex])
        self.clOutIndex += 1 
        if self.clOutIndex < len(self.clOutText):
            typeDelay = random.randint(5, 50)
            if typeDelay >= 40:
                typeDelay = random.randint(75, 200)
            self.root.after(typeDelay, self.outputTyper)
        else:
            self.clOutIndex = 0
            self.isWriting = False
            if ">> Goodbye < 3 " in self.clOutText: self.on_close()

    def popupWindow(self, type, msg):
        if type == "alert":
            mb.showinfo("", f"{msg}")
        else:
            _index = cf._themeOptions.index(self.themeValue.get())
            _tempWindow = tk.Toplevel(self.root)
            _tempWindow.geometry("200x175")
            _tempWindow.title("INFO")
            _tempWindow.configure(background=cf._backgroundColors[_index])
            _tempLbl = tk.Label(_tempWindow, text=f"{msg}", font=self.activeFont, background=cf._backgroundColors[_index], fg=cf._typefaceColors[_index])
            _tempLbl.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, pady=15)
            
if __name__ == "__main__":
    AppMain();