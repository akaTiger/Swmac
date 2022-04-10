import tkinter as tk
from tkinter import ttk
from mojang import MojangAPI
from PIL import Image, ImageTk
import io
import requests
import json

class inputGetErr(Exception):
    pass
class cantFind(Exception):
    pass
class imageDownloadErr(Exception):
    pass
class rowColumnArrangeErr(Exception):
    pass
class imagePlaceErr(Exception):
    pass
class imageIndiviCanvasErr(Exception):
    pass
class readJsonErr(Exception):
    pass
class printJsonErr(Exception):
    pass

def superAlth(Alst):
    colNumber = 15
    new = []
    while len(Alst) > colNumber:
        innerLst = []
        for i in range(colNumber):
            innerLst.append(Alst[i])
        new.append(innerLst)
        for i in range(colNumber):
            Alst.pop(0)
    lastList = []
    for i in range(len(Alst)):
        lastList.append(Alst[0])
        Alst.pop(0)
    new.append(lastList)
    return new

def addToChrList(nameID="TkinterDefault"):
    try:
        try:
            if nameID == "TkinterDefault":
                usrIn = uuidEntry.get()
            else:
                usrIn = nameID
        except:
            raise inputGetErr
        try:
            profile = MojangAPI.get_profile(usrIn)
            if profile.name != "":
                playerIDLst.append(MojangAPI.get_profile(usrIn).name)
                playerUuidVar.set("\n".join(playerIDLst))
                getPor(usrIn, playerIDLst[:])
                mcFampor.update()
        except:
            try:
                usrName = MojangAPI.get_uuid(usrIn)
                usrIn = usrName
                playerIDLst.append(MojangAPI.get_profile(usrIn).name)
                playerUuidVar.set("\n".join(playerIDLst))
                getPor(usrIn, playerIDLst[:])
                mcFampor.update()
            except:
                raise cantFind
    except inputGetErr:
        errorVar.set("inputGetErr: Check your entry box")
    except cantFind:
        errorVar.set("cantFind: info not found in database")
    except imageDownloadErr:
        errorVar.set("imageDownloadErr: Image Download Error")
    except rowColumnArrangeErr:
        errorVar.set("rowColumnArrangeErr")
    except imagePlaceErr:
        errorVar.set("imagePlaceErr")
    except imageIndiviCanvasErr:
        errorVar.set("imageIndiviCanvasErr")

def canvasPutDownForLst(fiveLst):
    for row in range(len(fiveLst)):
            for col in range(len(fiveLst[row])):
                rowFrame = row
                columnFrame = col
                uuid = fiveLst[row][col]
                
                try:
                    url = "https://crafatar.com/avatars/" + uuid
                    imageTKForm = ImageTk.PhotoImage(Image.open(io.BytesIO(requests.get(url).content)).resize((40, 40)))
                    try:
                        imageIndiviCanvas = tk.Frame(picFrame)
                        imageIndiviCanvas.grid(column=columnFrame, row=rowFrame)
                    except:
                        raise imageIndiviCanvasErr
                        
                    try:
                        
                        imageInfo = tk.Label(imageIndiviCanvas, image=imageTKForm)
                        imageInfo.image = imageTKForm
                        imageInfo.grid(column=0, row=0)
                        
                        try:
                            imageName = tk.Label(imageIndiviCanvas, text=MojangAPI.get_profile(uuid).name, width=10, height=3)
                            imageName.grid(column=0, row=1)
                            mcFampor.update()
                        except:
                            imageName = tk.Label(imageIndiviCanvas, text="Invalid User", width=10, height=3)
                            imageName.grid(column=0, row=1)
                            mcFampor.update()
                            errorVar.set("invalidName")
                        
                    except:
                        raise imagePlaceErr
                except:
                    errorVar.set("imageDownloadErr: Image Download Error")
                
                

def getPor(uuid, playerLst):
    try:
        url = "https://crafatar.com/avatars/" + uuid
        imageTKForm = ImageTk.PhotoImage(Image.open(io.BytesIO(requests.get(url).content)).resize((40, 40)))
    except:
        raise imageDownloadErr
    
    try:
        # print(playerLst)
        fiveLst = superAlth(playerLst)
        # print(fiveLst)
        for row in range(len(fiveLst)):
            for col in range(len(fiveLst[row])):
                if fiveLst[row][col] == MojangAPI.get_profile(uuid).name:
                    rowFrame = row
                    columnFrame = col
    except imageDownloadErr:
        print("imageDownloadErr")
    except imagePlaceErr:
        print("imagePlaceErr")
    except imageIndiviCanvasErr:
        print("imageIndiviCanvasErr")
    except:
        raise printJsonErr
    
    try:
        imageIndiviCanvas = tk.Frame(picFrame)
        imageIndiviCanvas.grid(column=columnFrame, row=rowFrame)
    except:
        raise imageIndiviCanvasErr
        
    try:
        imageInfo = tk.Label(imageIndiviCanvas, image=imageTKForm)
        imageInfo.image = imageTKForm
        imageInfo.grid(column=0, row=0)
        imageName = tk.Label(imageIndiviCanvas, text=MojangAPI.get_profile(uuid).name, width=10, height=3)
        imageName.grid(column=0, row=1)
    except:
        raise imagePlaceErr
    

def jsonSearch():
    uuidLst = []
    openF = "/Users/tiger/Downloads/whitelist.json"
    # openF = uuidEntry.get()
    try:
        try:
            with open(openF,'r') as jsonFile:
                loadDict = json.load(jsonFile)
                for i in loadDict:
                    uuidLst.append(i["uuid"])
        except:
            raise readJsonErr
        try:
            finalA = superAlth(uuidLst)
            canvasPutDownForLst(finalA)
        except:
            raise printJsonErr
    except readJsonErr:
        print("readJsonErr")

if __name__ == "__main__":
    
    projName = "Server Whitelist to Minecraft Avatars Converter"
    mcFampor = tk.Tk()
    mcFampor.title(projName)
    mcFampor.geometry("1920x1080")
    
    bigFrame = tk.Frame(mcFampor)
    bigFrame.pack(fill="both", expand=1)
    scrollCan = tk.Canvas(bigFrame)
    scrollCan.pack(side="left", fill="both", expand=1)
    scrollMain = ttk.Scrollbar(bigFrame, orient="vertical", command=scrollCan.yview)
    scrollMain.pack(side="right", fill="y")
    scrollCan.configure(yscrollcommand=scrollMain.set)
    scrollCan.bind("<Configure>", lambda e: scrollCan.configure(scrollregion=scrollCan.bbox("all")))
    secondFrame = tk.Frame(scrollCan)
    scrollCan.create_window((950,0), window=secondFrame, anchor="n")
    
    errorVar = tk.StringVar()
    errorVar.set("")
    playerUuidVar = tk.StringVar()
    playerUuidVar.set("")
    
    picFrame = tk.Frame(secondFrame)
    mainFrame = tk.Frame(secondFrame)
    picFrame.pack()
    mainFrame.pack()
    
    playerIDLst = []
    
    uuidEntry = tk.Entry(mainFrame, text="Enter UUID")
    addToCharacterList = tk.Button(mainFrame, text="Add to List", command=addToChrList)
    errorLabel = tk.Label(mainFrame, textvariable=errorVar)
    playerLabel = tk.Label(mainFrame, textvariable=playerUuidVar)
    quitButton = tk.Button(mainFrame, text="Quit", command=quit)
    filePathAutoSearcher = tk.Button(mainFrame, text="Json Whitelist Search", command=jsonSearch)
    
    # playerLabel.pack()
    errorLabel.pack()
    uuidEntry.pack()
    addToCharacterList.pack()
    filePathAutoSearcher.pack()
    
    quitButton.pack()
    
    mcFampor.mainloop()