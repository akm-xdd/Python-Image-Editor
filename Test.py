'''
A simple walkthrough to edit the files and contribute

Step 1: Import all the new libraries (if any)

Step 2: Define the function

Step 3: Create button and assign the function created in step 2 as a lamda

Step 4: Run the code and test
'''


from tkinter import *
from collections import deque
import PIL.Image
from tkinter import filedialog as fd, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFilter, ImageOps

Font_tuple = ("Sans Serif", 12, "bold")

#defining the buttons as global scope variables

save_button = None
export_button = None
undo_button = None
redo_button = None
clear_button = None
crop_button = None
brightness_button = None
contrast_button = None
RGB_button = None
flip_button = None
mirror_button = None
rotate_button = None
draw_button = None
gray_button = None
filter_button = None

#function definitions go below

def grayscale(canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    check_deque(canvas)

    canvas.data.image = ImageOps.grayscale(canvas.data.image)

    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)


def save(canvas):
    im = canvas.data.image
    im.save(canvas.data.imageLocation)


def export(canvas):
    pass


def check_deque(canvas):
    global undo_button
    global redo_button
    if len(canvas.data.undoQueue) > 0:
        undo_button.config(state=NORMAL)
    else:
        undo_button.config(state=DISABLED)

    if len(canvas.data.redoQueue) > 0:
        redo_button.config(state=NORMAL)
    else:
        redo_button.config(state=DISABLED)


def undo(canvas):
    canvas.data.redoQueue.append(canvas.data.image.copy())
    canvas.data.image = canvas.data.undoQueue.pop()
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)
    check_deque(canvas)


def redo(canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.image = canvas.data.redoQueue.pop()
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)
    check_deque(canvas)


def clear(canvas):

    canvas.data.undoQueue.clear()
    canvas.data.redoQueue.clear()
    canvas.data.image = img
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)
    check_deque(canvas)


def closeRGBWindow(canvas, state=1):
    if state == 0:
        canvas.data.image = canvas.data.recentBeforeChange
        canvas.data.imageForTk = drawImageForTk(canvas)
        drawImageOnCanvas(canvas)
    else:
        canvas.data.undoQueue.append(canvas.data.recentBeforeChange.copy())
        check_deque(canvas)
    canvas.data.RGBWindowClose = True


def RGB(canvas):
    canvas.data.recentBeforeChange = canvas.data.image
    RGBWindow = Toplevel(canvas.data.mainWindow)
    RGBWindow.attributes('-toolwindow', True)
    RGBWindow.protocol('WM_DELETE_WINDOW', lambda: closeRGBWindow(canvas, 0))
    RGBWindow.title("RGB")
    redSlider = Scale(RGBWindow, from_=-100, to=100, orient=HORIZONTAL, label="R")
    redSlider.pack()
    blueSlider = Scale(RGBWindow, from_=-100, to=100, orient=HORIZONTAL, label="B")
    blueSlider.pack()
    greenSlider = Scale(RGBWindow, from_=-100, to=100, orient=HORIZONTAL, label="G")
    greenSlider.pack()
    OkRGBFrame = Frame(RGBWindow)
    OkRGBButton = Button(OkRGBFrame, text="OK", command=lambda: closeRGBWindow(canvas))
    OkRGBButton.grid(row=0, column=0)
    OkRGBFrame.pack(side=BOTTOM)
    initialRGB = (0, 0, 0)
    changeColours(canvas, redSlider, blueSlider, greenSlider, RGBWindow, initialRGB)


def changeColours(canvas, redSlider, blueSlider, greenSlider, RGBWindow, previousRGB):
    if canvas.data.RGBWindowClose == True:
        RGBWindow.destroy()
        canvas.data.RGBWindowClose = False
    else:
        if canvas.data.image != None and RGBWindow.winfo_exists():
            sliderValR = redSlider.get()
            sliderValG = greenSlider.get()
            sliderValB = blueSlider.get()
            currentRGB = (sliderValR, sliderValG, sliderValB)
            if currentRGB != previousRGB:
                R, G, B = canvas.data.recentBeforeChange.split()
                R = R.point(lambda i: i + int(round(i * sliderValR / 100.0)))
                G = G.point(lambda i: i + int(round(i * sliderValG / 100.0)))
                B = B.point(lambda i: i + int(round(i * sliderValB / 100.0)))
                canvas.data.image = Image.merge(canvas.data.recentBeforeChange.mode, (R, G, B))
                canvas.data.imageForTk = drawImageForTk(canvas)
                drawImageOnCanvas(canvas)
            canvas.after(200, lambda: changeColours(canvas, redSlider, blueSlider, greenSlider, RGBWindow, currentRGB))


def rotate90CW(canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.image = canvas.data.image.rotate(90, PIL.Image.NEAREST, expand = 1)
    check_deque(canvas)
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)


def crop(canvas, crop_button):
    if not hasattr(canvas.data, 'cropEnable') or canvas.data.cropEnable == False:
        crop_button.config(text="Stop Crop", fg="black", background="white")
        canvas.data.cropEnable = True
        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>", lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>", lambda event: endCrop(event, canvas))
    else:
        crop_button.config(text="Crop", fg="black", background="white")
        canvas.data.cropEnable = False


def startCrop(event, canvas):
    if canvas.data.cropEnable == True:
        canvas.data.startCropX = event.x
        canvas.data.startCropY = event.y


def drawCrop(event, canvas):
    if canvas.data.cropEnable == True:
        canvas.data.tempCropX = event.x
        canvas.data.tempCropY = event.y
        print(str(canvas.data.startCropX) + " " + str(canvas.data.startCropY) + " " + str(
            canvas.data.tempCropX) + " " + str(canvas.data.tempCropY))
        canvas.create_rectangle(canvas.data.startCropX, canvas.data.startCropY, canvas.data.tempCropX,
                                canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)


def endCrop(event, canvas):
    if canvas.data.cropEnable is True:
        canvas.data.endCropX = event.x
        canvas.data.endCropY = event.y
        canvas.create_rectangle(canvas.data.startCropX, canvas.data.startCropY, canvas.data.endCropX,
                                canvas.data.endCropY, fill="gray", stipple="gray12", width=0)
        canvas.data.mainWindow.bind("<Return>", lambda event: performCrop(event, canvas))


def performCrop(event, canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.image = \
        canvas.data.image.crop(
            (int(round((canvas.data.startCropX - canvas.data.imageTopX) * canvas.data.imageScale)),
             int(round((canvas.data.startCropY - canvas.data.imageTopY) * canvas.data.imageScale)),
             int(round((canvas.data.endCropX - canvas.data.imageTopX) * canvas.data.imageScale)),
             int(round((canvas.data.endCropY - canvas.data.imageTopY) * canvas.data.imageScale))))
    check_deque(canvas)
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)


def colorPallette(canvas):
    drawWindow = Toplevel(canvas.data.mainWindow)
    drawWindow.title = "Draw"
    drawFrame = Frame(drawWindow)
    redButton = Button(drawFrame, bg="red", width=2, command=lambda: colourChosen(drawWindow, canvas, "red"))
    redButton.grid(row=0, column=0)
    blueButton = Button(drawFrame, bg="blue", width=2, command=lambda: colourChosen(drawWindow, canvas, "blue"))
    blueButton.grid(row=0, column=1)
    greenButton = Button(drawFrame, bg="green", width=2, command=lambda: colourChosen(drawWindow, canvas, "green"))
    greenButton.grid(row=0, column=2)
    magentaButton = Button(drawFrame, bg="magenta", width=2,
                           command=lambda: colourChosen(drawWindow, canvas, "magenta"))
    magentaButton.grid(row=1, column=0)
    cyanButton = Button(drawFrame, bg="cyan", width=2, command=lambda: colourChosen(drawWindow, canvas, "cyan"))
    cyanButton.grid(row=1, column=1)
    yellowButton = Button(drawFrame, bg="yellow", width=2, command=lambda: colourChosen(drawWindow, canvas, "yellow"))
    yellowButton.grid(row=1, column=2)
    orangeButton = Button(drawFrame, bg="orange", width=2, command=lambda: colourChosen(drawWindow, canvas, "orange"))
    orangeButton.grid(row=2, column=0)
    purpleButton = Button(drawFrame, bg="purple", width=2, command=lambda: colourChosen(drawWindow, canvas, "purple"))
    purpleButton.grid(row=2, column=1)
    brownButton = Button(drawFrame, bg="brown", width=2, command=lambda: colourChosen(drawWindow, canvas, "brown"))
    brownButton.grid(row=2, column=2)
    blackButton = Button(drawFrame, bg="black", width=2, command=lambda: colourChosen(drawWindow, canvas, "black"))
    blackButton.grid(row=3, column=0)
    whiteButton = Button(drawFrame, bg="white", width=2, command=lambda: colourChosen(drawWindow, canvas, "white"))
    whiteButton.grid(row=3, column=1)
    grayButton = Button(drawFrame, bg="gray", width=2, command=lambda: colourChosen(drawWindow, canvas, "gray"))
    grayButton.grid(row=3, column=2)
    drawFrame.pack(side=BOTTOM)


def colourChosen(drawWindow, canvas, colour):
    canvas.data.drawColour = colour
    canvas.data.mainWindow.bind("<B1-Motion>", lambda event: drawDraw(event, canvas))
    drawWindow.destroy()


def drawDraw(event, canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    x = int(round((event.x - canvas.data.imageTopX) * canvas.data.imageScale))
    y = int(round((event.y - canvas.data.imageTopY) * canvas.data.imageScale))
    draw = ImageDraw.Draw(canvas.data.image)
    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=canvas.data.drawColour, outline=None)
    # canvas.data.undoQueue.append(canvas.data.image.copy())
    check_deque(canvas)
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)


def flip_HZ(canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.image = canvas.data.image.transpose(Image.FLIP_LEFT_RIGHT)
    check_deque(canvas)
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)


def flip_Vert(canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.image = canvas.data.image.transpose(Image.FLIP_TOP_BOTTOM)
    check_deque(canvas)
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)


def changeContrast(canvas, contrastWindow, contrastSlider, previousVal):
    if canvas.data.contrastWindowClose is True:
        contrastWindow.destroy()
        canvas.data.contrastWindowClose = False
    else:
        sliderVal = contrastSlider.get()
        if (previousVal != sliderVal):
            canvas.data.image = canvas.data.recentBeforeChange.point(
                lambda i: int(round(128 + (259 * (sliderVal + 255)) / (255 * (259 - sliderVal)) * (i - 128))))
            canvas.data.imageForTk = drawImageForTk(canvas)
            drawImageOnCanvas(canvas)
        canvas.after(200, lambda: changeContrast(canvas, contrastWindow, contrastSlider, sliderVal))


def closeContrastWindow(canvas, state=1):
    if state == 0:
        canvas.data.image = canvas.data.recentBeforeChange
        canvas.data.imageForTk = drawImageForTk(canvas)
        drawImageOnCanvas(canvas)
    else:
        canvas.data.undoQueue.append(canvas.data.recentBeforeChange.copy())
        check_deque(canvas)
    canvas.data.contrastWindowClose = True


def contrast(canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.recentBeforeChange = canvas.data.image
    contrastWindow = Toplevel(canvas.data.mainWindow)
    contrastWindow.attributes('-toolwindow', True)
    contrastWindow.protocol('WM_DELETE_WINDOW', lambda: closeContrastWindow(canvas, 0))
    contrastWindow.title("Contrast")
    contrastSlider = Scale(contrastWindow, from_=-100, to=100, orient=HORIZONTAL)
    contrastSlider.pack()

    OkContrastFrame = Frame(contrastWindow)
    OkContrastButton = Button(OkContrastFrame, text="OK", command=lambda: closeContrastWindow(canvas))
    OkContrastButton.grid(row=0, column=0)
    OkContrastFrame.pack(side=BOTTOM)
    changeContrast(canvas, contrastWindow, contrastSlider, 0)
    contrastSlider.set(0)


def changeBrightness(canvas, brightnessWindow, brightnessSlider, previousVal):
    if canvas.data.brightnessWindowClose is True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose = False
    else:
        sliderVal = brightnessSlider.get()
        if (previousVal != sliderVal):
            canvas.data.image = canvas.data.recentBeforeChange.point(lambda i: i + int(round(i * sliderVal / 100.0)))
            canvas.data.imageForTk = drawImageForTk(canvas)
            drawImageOnCanvas(canvas)
        canvas.after(200, lambda: changeBrightness(canvas, brightnessWindow, brightnessSlider, sliderVal))


def closeBrightnessWindow(canvas, state=1):
    if state == 0:
        canvas.data.image = canvas.data.recentBeforeChange
        canvas.data.imageForTk = drawImageForTk(canvas)
        drawImageOnCanvas(canvas)
    else:
        canvas.data.undoQueue.append(canvas.data.recentBeforeChange.copy())
        check_deque(canvas)
    canvas.data.brightnessWindowClose = True


def brightness(canvas):

    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.recentBeforeChange = canvas.data.image
    brightnessWindow = Toplevel(canvas.data.mainWindow)
    brightnessWindow.attributes('-toolwindow', True)
    brightnessWindow.protocol('WM_DELETE_WINDOW', lambda: closeBrightnessWindow(canvas, 0))
    brightnessWindow.title("Brightness")
    brightnessSlider = Scale(brightnessWindow, from_=-100, to=100, orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame = Frame(brightnessWindow)
    OkBrightnessButton = Button(OkBrightnessFrame, text="OK", command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0, column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider, 0)
    brightnessSlider.set(0)


#Tkinter and canvas operations go below

def drawImageForTk(canvas):
    im = canvas.data.image

    imageWidth = canvas.data.image.size[0]
    imageHeight = canvas.data.image.size[1]
    if imageWidth > imageHeight:
        resizedImage = im.resize((canvas.data.width, int(round(float(imageHeight) * canvas.data.width / imageWidth))))
        canvas.data.imageScale = float(imageWidth) / canvas.data.width
    else:
        resizedImage = im.resize((int(round(float(imageWidth) * canvas.data.height / imageHeight)), canvas.data.height))
        canvas.data.imageScale = float(imageHeight) / canvas.data.height
    canvas.data.resizedIm = resizedImage
    return ImageTk.PhotoImage(resizedImage)


def drawImageOnCanvas(canvas):
    canvas.data.imageTopX = int(round(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0))
    canvas.data.imageTopY = int(round(canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0))
    canvas.create_image(canvas.data.imageTopX, canvas.data.imageTopY, image=canvas.data.imageForTk, anchor=NW)


def open_image(canvas):
    global save_button
    global crop_button
    global export_button
    global brightness_button
    global contrast_button
    global RGB_button
    global flip_button
    global mirror_button
    global rotate_button
    global draw_button
    global filter_button
    global img
    img_location = fd.askopenfilename(title="Select file",
                                      filetypes=(("Image files", "*.jpg *.png"), ("all files", "*.*")))
    img = Image.open(img_location)
    img = img.convert('RGB')
    canvas.data.imageLocation = img_location
    canvas.data.image = img
    canvas.data.originalImage = img.copy()
    canvas.data.undoQueue.append(img.copy())
    canvas.data.imageSize = img.size
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)

    save_button.config(state=NORMAL)
    export_button.config(state=NORMAL)
    clear_button.config(state=NORMAL)
    crop_button.config(state=NORMAL)
    brightness_button.config(state=NORMAL)
    contrast_button.config(state=NORMAL)
    RGB_button.config(state=NORMAL)
    flip_button.config(state=NORMAL)
    mirror_button.config(state=NORMAL)
    rotate_button.config(state=NORMAL)
    draw_button.config(state=NORMAL)
    filter_button.config(state=NORMAL)


def init_canvas(root):
    canvasWidth = 1280
    canvasHeight = 720
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, background="#282828", highlightthickness=0,
                    relief='ridge')

    class Struct:
        pass

    canvas.data = Struct()
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    canvas.data.undoQueue = deque([], 10)
    canvas.data.redoQueue = deque([], 10)
    canvas.data.mainWindow = root

    canvas.data.brightnessWindowClose = False
    canvas.data.contrastWindowClose = False
    canvas.data.RGBWindowClose = False

    return canvas

#Create buttons and filters below

def create_button(_frame, _btn_name, _btn_command, _side="left", _width=12):
    init_button = Button(_frame, text=_btn_name, fg="black", background="white", width=_width, height=1,
                         command=_btn_command, font=Font_tuple)
    init_button.pack(side=_side)
    return init_button


def filter_with_lib(canvas, filter):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    check_deque(canvas)
    canvas.data.image = canvas.data.image.filter(filter)
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)


def filters(canvas):
    blurWindow = Toplevel(canvas.data.mainWindow)
    blurWindow.attributes('-toolwindow', True)
    blurWindow.title("Filters")
    create_button(blurWindow, "BLUR", lambda: filter_with_lib(canvas, ImageFilter.BLUR),
                  "top", 20)
    create_button(blurWindow, "SMOOTH", lambda: filter_with_lib(canvas, ImageFilter.SMOOTH), "top", 20)
    create_button(blurWindow, "SHARPEN", lambda: filter_with_lib(canvas, ImageFilter.SHARPEN), "top", 20)
    create_button(blurWindow, "NEGATIVE", lambda: negative_filter(canvas), "top", 20)
    create_button(blurWindow, "GRAYSCALE", lambda: grayscale(canvas), "top", 20)


def negative_filter(canvas):
    canvas.data.undoQueue.append(canvas.data.image.copy())
    check_deque(canvas)
    canvas.data.image = canvas.data.image.point(lambda i: 255 - i)
    canvas.data.imageForTk = drawImageForTk(canvas)
    drawImageOnCanvas(canvas)

#initialise the buttons below

def init_buttons(root, canvas):
    global save_button
    global export_button
    global undo_button
    global redo_button
    global clear_button
    global crop_button
    global brightness_button
    global contrast_button
    global RGB_button
    global flip_button
    global mirror_button
    global rotate_button
    global draw_button
    global filter_button

    menuKitFrame = Frame(root)
    create_button(menuKitFrame, "Open📂", lambda: open_image(canvas))
    save_button = create_button(menuKitFrame, "Save💾", lambda: save(canvas))
    export_button = create_button(menuKitFrame, "Export📁", lambda: export(canvas))
    undo_button = create_button(menuKitFrame, "Undo", lambda: undo(canvas))
    redo_button = create_button(menuKitFrame, "Redo", lambda: redo(canvas))
    clear_button = create_button(menuKitFrame, "Clear Changes", lambda: clear(canvas))
    menuKitFrame.pack(side=TOP)

    toolKitFrame = Frame(root)
    crop_button = create_button(toolKitFrame, "Crop", lambda: crop(canvas, crop_button))
    brightness_button = create_button(toolKitFrame, "Brightness", lambda: brightness(canvas))
    contrast_button = create_button(toolKitFrame, "Contrast", lambda: contrast(canvas))
    RGB_button = create_button(toolKitFrame, "RGB", lambda: RGB(canvas))
    filter_button = create_button(toolKitFrame, "Filters", lambda: filters(canvas))
    flip_button = create_button(toolKitFrame, "Flip Horizontally", lambda: flip_HZ(canvas))
    mirror_button = create_button(toolKitFrame, "Flip Vertically", lambda: flip_Vert(canvas))
    rotate_button = create_button(toolKitFrame, "Rotate CW", lambda: rotate90CW(canvas))
    draw_button = create_button(toolKitFrame, "Draw", lambda: colorPallette(canvas))


    toolKitFrame.pack(side=BOTTOM)
    save_button.config(state="disabled")
    export_button.config(state="disabled")
    undo_button.config(state="disabled")
    redo_button.config(state="disabled")
    clear_button.config(state="disabled")
    crop_button.config(state="disabled")
    brightness_button.config(state="disabled")
    contrast_button.config(state="disabled")
    RGB_button.config(state="disabled")
    flip_button.config(state="disabled")
    mirror_button.config(state="disabled")
    rotate_button.config(state="disabled")
    draw_button.config(state="disabled")
    filter_button.config(state="disabled")


#define the main config below

def run():
    root = Tk()
    root.configure(background='#282828')
    root.state("zoomed")
    root.title("Image Editor")
    canvas = init_canvas(root)
    init_buttons(root, canvas)
    canvas.pack()
    root.mainloop()


run()