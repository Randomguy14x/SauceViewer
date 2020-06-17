from tkinter import *
from PIL import ImageTk, Image
from nhentai import nhentai
import urllib.parse
import io
import random


#Main window
window = Tk()
window.title("nHentai Viewer")
window.iconbitmap('icon.ico')

#Labels for Search Bars and Search Bars themselves
title = Label(window, text="nhentai Sauce:")
title.grid(row=0,column=0,columnspan=2)
numBar = Entry(window)
numBar.grid(row=1,column=0,columnspan=2)
title2 = Label(window,text="Tags Filter(WIP)")
title2.grid(row=0,column=3,columnspan=2)
tagBar = Entry(window)
tagBar.grid(row=1,column=3,columnspan=2)

#Default image on startup
#Also sets up doujin vars
images = [Image.open('icon.jpg')]
page = 0
d = None
defPic = ImageTk.PhotoImage(images[page])
defImg = Label(window, image=defPic)
defImg.grid(row=3,column=0,columnspan=5)

#Loads images from doujinURL and stores them
def imgProcess():
    global d
    global images
    global defImg
    global defPic
    raw_data = urllib.request.urlopen(d._images[page]).read()
    pic2 = Image.open(io.BytesIO(raw_data))
    images.append(pic2)

#Broken function kappa

#def resize_image(event):
#    global defPic
#    global defImg
#    global images
#    global page
#    global window
#    defImg.grid_forget()
#    (new_w,new_h) = (int(window.winfo_width()-4),int(window.winfo_height() -96))
#    copy = images[page].resize((new_w,new_h))
#    defPic = ImageTk.PhotoImage(copy)
#    defImg = Label(window, image=defPic)
#    defImg.grid(row=3,column=0,columnspan=5)
    #defOrig.image = defImg
#image = Image.open('icon.png')
#copy_of_image = image.copy()
#photo = ImageTk.PhotoImage(image)
#label = Label(window, image = photo)
#window.bind('<Configure>', resize_image)
#label.grid(row=3,column=0,columnspan=5)

#Displays new/next image and fits to screen
    #width - 4 and height - 96 are req bc the window would continuously shrink or enlargen if they were any other number
    #As the image+border would be larger than the window or something while the window also tries to resize
    #to put the image on the screen
def imgLoad():
    global defImg
    global defPic
    global images
    global page
    global window
    defImg.grid_forget()
    (new_w,new_h) = (int(window.winfo_width()-4),int(window.winfo_height() -96))
    copy = images[page].resize((new_w,new_h))
    defPic = ImageTk.PhotoImage(copy)
    defImg = Label(window, image=defPic)
    defImg.grid(row=3,column=0,columnspan=5)

#Function for inputting your own sauce
def onClick():
    global d
    global page
    global images
    global nextButton
    global backButton
    global tagBar
    #Incase given sauce is invalid
    try:
        d = nhentai.Doujinshi(int(numBar.get()))
    except:
        return
    #Resetting vars incase of multisearching
    tagBar.delete(0, END)
    page = 0
    images = []

    

    imgProcess()
    imgLoad()
    
    #next button is enabled now that images[] isn't empty
    #back is still disabled bc you start the doujin on page 1
    backButton = Button(window,text="<<",command = onBack, state=DISABLED)
    backButton.grid(row=4,column=0,columnspan=2)
    nextButton = Button(window,text=">>",command = onNext,state=ACTIVE)
    nextButton.grid(row=4,column=3,columnspan=2)

    return

#Psuedo-random counter vars
counter = 5000
counter2 = 0
#Random Doujin based on given tag(s)
def onRandom(tags):
    global d
    global page
    global images
    global nextButton
    global backButton
    global numBar
    global counter
    global counter2

    #idk how to get list of all tags so
    #this is default for now
    tags.replace(",", "")
    if tags == "":
        tags = "big-breasts"

    #Max Page number for any given doujin tag set is unknown, so I gave counter=5000
    #because the most popular tag (big-breasts) has 4237 pages so 5000 will
    #mean I'm good for awhile
    #I think this might just be a limitation of the nhentai import
    if counter2 == 5:
        counter = 25
        counter2 = 0
    randomPage = random.randint(1,1+counter)
    results = [x for x in nhentai.search(tags, randomPage)]
    if results == [] and counter >25:
        counter-=1000
        counter2+=1
        onRandom(tags=tags)
        return
    elif results == [] and counter > 0:
        counter-=1
        onRandom(tags=tags)
        return
    counter = 5000
    #Creats doujin now that sauce has FINALLY been found from whatever that thing is above me
    try:
        d = nhentai.Doujinshi(results[random.randint(0,len(results))].magic)
    except:
        return

    #Resets vars and puts Sauce in Sauce bar so you know what you're reading
    numBar.delete(0, END)
    numBar.insert(0, str(d.magic))
    page = 0
    images = []

    
    imgProcess()
    imgLoad()

    #Reactivates buttons again
    backButton = Button(window,text="<<",command = onBack, state=DISABLED)
    backButton.grid(row=4,column=0,columnspan=2)
    nextButton = Button(window,text=">>",command = onNext,state=ACTIVE)
    nextButton.grid(row=4,column=3,columnspan=2)
    return

#Buttons for searching
goButton = Button(window, text="Retrieve my Sauce", command = onClick)
randomButton = Button(window, text="Random Sauce", command = lambda:onRandom(tags=tagBar.get()))
goButton.grid(row=2,column=0,columnspan=2)
randomButton.grid(row=2,column=3,columnspan=2)

#Next button function
def onNext():
    global d
    global page
    global images
    global nextButton
    global backButton

    if page == 1-d.pages:
        page += 1

    #Only re-renders new images to save time
    if len(images) -1 < page:
        imgProcess()

    #Displays image
    imgLoad()

    #Disables next button if on last page
    #Else enables next and back buttons since you'd at least
    #Be on page 2 after clicking
    if page == d.pages - 1:
        nextButton = Button(window,text=">>",command = onNext, state=DISABLED)
        nextButton.grid(row=4,column=3,columnspan=2)
    else:
        nextButton = Button(window,text=">>",command = onNext, state=ACTIVE)
        backButton = Button(window,text="<<",command = onBack, state=ACTIVE)
        backButton.grid(row=4,column=0,columnspan=2)
        nextButton.grid(row=4,column=3,columnspan=2)
    return

#Back Button function
def onBack():
    global d
    global page
    global images
    global nextButton
    global backButton

    page -= 1

    #No need to rerender image since we already saved it previously
    imgLoad()

    #Button enable/disabling again so you don't cause
    #An out of bounds error with num of images
    if page == 0:
        backButton = Button(window,text="<<",command = onBack, state=DISABLED)
        backButton.grid(row=4,column=0,columnspan=2)
    else:
        backButton = Button(window,text="<<",command = onBack, state=ACTIVE)
        nextButton = Button(window,text=">>",command = onNext, state=ACTIVE)
        backButton.grid(row=4,column=0,columnspan=2)
        nextButton.grid(row=4,column=3,columnspan=2)

    return

#Setting up next,back,and reload buttons
nextButton = Button(window,text=">>",command = onNext, state=DISABLED)
backButton = Button(window,text="<<",command = onBack, state=DISABLED)
backButton.grid(row=4,column=0,columnspan=2)
nextButton.grid(row=4,column=3,columnspan=2)

#Reload button to resize current image since I couldn't figure out
#how to resize image on window resize without it crashing lol
imgReloadButton = Button(window,text="Resize Image", command = imgLoad)
imgReloadButton.grid(row=2,column=2)

#Runs this things
window.mainloop()
