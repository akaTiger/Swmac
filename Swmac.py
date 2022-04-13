from mojang import MojangAPI
from PIL import Image, ImageTk
import requests
import json
import shutil
from pathlib import Path
import tkinter as tk
from tkinter.constants import *
from tkinter.scrolledtext import ScrolledText

class Swmac:
    def __init__(self, allowedExtensions):
        self.root = tk.Tk()
        projName = "Swmac v1.0.0"
        self.root.title(projName)
        self.allowedExtensions = allowedExtensions
        self.windowInit()
        self.frameBuild()
        self.root.mainloop()
        
    def windowInit(self):
        self.root.update_idletasks()
        width = 710
        frm_width = self.root.winfo_rootx() - self.root.winfo_x()
        self.root_width = width + 2 * frm_width
        height = 600
        titlebar_height = self.root.winfo_rooty() - self.root.winfo_y()
        self.root_height = height + titlebar_height + frm_width
        x = self.root.winfo_screenwidth() // 2 - self.root_width // 2
        y = self.root.winfo_screenheight() // 2 - self.root_height // 2
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.root.deiconify()
        self.root.resizable(False, False)

    def frameBuild(self):
        self.errorVar = tk.StringVar()
        self.errorVar.set("Error: None")
        self.playerUuidVar = tk.StringVar()
        self.playerUuidVar.set("")
        self.displayFrame = tk.Frame(self.root, padx=20)
        self.displayFrame.pack(fill="both", expand=True, anchor="n")
        self.userPromptLabelFrame = tk.LabelFrame(self.root, text="Swmac Console", padx=10, pady=10)
        self.userPromptLabelFrame.pack(pady=20)
        self.inputFrame = tk.Frame(self.userPromptLabelFrame)
        self.inputFrame.pack()
        self.additionFrame = tk.Frame(self.userPromptLabelFrame)
        self.additionFrame.pack()
        if True:
            self.mainDisplayArea = ScrolledText(self.displayFrame, wrap=WORD)
            self.mainDisplayArea.pack(fill="both", expand=True)
        if True:
            # userPromptLabelFrame design
            self.instructionLabelA = tk.Label(self.inputFrame, text=".JSON Path:")
            self.instructionLabelA.pack(side="left")
            self.uuidEntryBox = tk.Entry(self.inputFrame, width=52)
            self.uuidEntryBox.insert(0, "/Users/tiger/Downloads/whitelist.json")
            self.uuidEntryBox.pack(side="left")
            self.filePathAutoSearcher = tk.Button(self.inputFrame, text="Execute", command=self.mainFunc, width=5)
            self.filePathAutoSearcher.pack(side="left")
            
            self.instructionLabelB = tk.Label(self.additionFrame, text="Folder Path:")
            self.instructionLabelB.pack(side="left")
            self.projFolderEntryBox = tk.Entry(self.additionFrame, width=52)
            self.projFolderEntryBox.insert(0, "/Users/tiger/Downloads/mapiot")
            self.projFolderEntryBox.pack(side="left")
            self.quitButton = tk.Button(self.additionFrame, text="Quit", command=quit, width=5)
            self.quitButton.pack(side="left")
        if True:
            self.mainDisplayArea.downloadedFiles = []
            self.mainDisplayArea.images = []

    def mainFunc(self):
        self.projFolder = self.projFolderEntryBox.get()
        uuidLst = []
        openF = self.uuidEntryBox.get()
        with open(openF,'r') as jsonFile:
            loadDict = json.load(jsonFile)
            for i in loadDict:
                uuidLst.append(i["uuid"])
        avaUsr = []
        for i in uuidLst:
            try:
                aUselessVar = MojangAPI.get_profile(i).name
                filePath = self.projFolder + "/avaImg_" + str(len(avaUsr)) + ".png"
                with open(filePath, "wb") as outFile:
                    url = "https://crafatar.com/avatars/" + i
                    response = requests.get(url, stream=True)
                    shutil.copyfileobj(response.raw, outFile)
                del response
                avaUsr.append(i)
            except:
                pass
        self.mainDisplayArea.downloadedFiles.clear()
        for filepath in Path(self.projFolder).iterdir():
            if filepath.suffix in self.allowedExtensions:
                self.mainDisplayArea.insert(INSERT, filepath.name+'\n')
                self.mainDisplayArea.downloadedFiles.append(filepath)
        self.mainDisplayArea.delete('1.0', END)
        self.mainDisplayArea.images.clear()
        for avatarImageName in self.mainDisplayArea.downloadedFiles:
            if str(avatarImageName)[-6:-5] == "_":
                idIndex = str(avatarImageName)[-5:-4]
            else:
                idIndex = str(avatarImageName)[-6:-4]
            uuidToPrint = avaUsr[int(idIndex)]
            img = Image.open(avatarImageName).resize((20, 20))
            img = ImageTk.PhotoImage(img)
            idHistory = MojangAPI.get_name_history(uuidToPrint)
            idHistoryLst = []
            for data in idHistory:
                idHistoryLst.append(data['name'])
            idHistoryLst.pop(-1)
            if len(idHistoryLst) == 0:
                idHistoryLst.append("Current")
            else:
                pass
            self.mainDisplayArea.image_create(INSERT, padx=5, pady=5, image=img)
            self.mainDisplayArea.images.append(img)
            self.mainDisplayArea.insert(INSERT, f"{MojangAPI.get_profile(uuidToPrint).name:<20}")
            self.mainDisplayArea.insert(INSERT, f"{str('|'):<3}{uuidToPrint}   ")
            self.mainDisplayArea.insert(INSERT, f"{str('|'):<3}{'>>'.join(idHistoryLst[-1:])} >>")
            self.mainDisplayArea.insert(INSERT, '\n')  

if __name__ == "__main__":
    allowedExtensions = {'.jpg', '.png'}
    Swmac(allowedExtensions)