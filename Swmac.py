import tkinter as tk
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
            new = []
            while len(Alst) > 5:
                new.append([Alst[0], Alst[1], Alst[2], Alst[3], Alst[4]])
                for i in range(5):
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
    except:
        raise rowColumnArrangeErr
    
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
    try:
        try:
            with open(uuidEntry.get(),'r') as jsonFile:
                loadDict = json.load(jsonFile)
                for i in loadDict:
                    uuidLst.append(i["uuid"])
        except:
            raise readJsonErr
        try:
            for i in uuidLst:
                # print(i)
                addToChrList(nameID=i)
        except:
            raise printJsonErr
    except readJsonErr:
        print("readJsonErr")

if __name__ == "__main__":
    
    projName = "Server Whitelist to Minecraft Avatars Converter"
    mcFampor = tk.Tk()
    mcFampor.title(projName)
    mcFampor.geometry("500x300")
    
    errorVar = tk.StringVar()
    errorVar.set("")
    playerUuidVar = tk.StringVar()
    playerUuidVar.set("")
    
    picFrame = tk.Frame(mcFampor)
    mainFrame = tk.Frame(mcFampor)
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