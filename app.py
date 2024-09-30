import cv2
import os
import time
import threading
import cv2
from PIL import Image, ImageTk 
from tkinter import Label, Button, Tk, PhotoImage
from tkinter import ttk 


import yaml

def get_yaml_config(pth):
    with open(pth, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


class CameraApp:
    def __init__(self, window):
        path_config = "config.yaml"
        config=get_yaml_config(path_config)
        self.path_save = config["path_save"]
        self.img_save_size = tuple(config["img_save_size"])
        self.img_wind_size = tuple(config["img_wind_size"])
        self.counter=1

        self.window = window
        self.window.title("My Camera")
        # self.window.geometry("1000x800")
        self.window.geometry(config["init_window_size"])
        self.window.configure(bg="#0c0c36")
        self.window.resizable(1, 1)
        self.TakePhoto_b = ttk.Button(self.window, width = 20, text = "Shot", command=self.TakePhoto) # relief = 'flat'
        self.ImageLabel = Label(self.window, width = self.img_wind_size[0], height= self.img_wind_size[1], bg = "#4682B4")
        self.ImageLabel.place(x=0, y=0)
        self.TakePhoto_b.place(x = self.img_wind_size[0]/2, y = self.img_wind_size[1]+20)

        self.take_picture = False
        # self.PictureTaken = False
        self.Main()

    # @staticmethod
    def LoadCamera(self):
        camera = cv2.VideoCapture(0) # cv2.VideoCapture(index=0, apiPreference=0)  cv2.CAP_GSTREAMER, cv2.CAP_DSHOW  ## VideoWriter(filename, apiPreference, fourcc, fps, frameSize[, isColor]) ####, fourcc= cv2.VideoWriter_fourcc('M','J','P','G'),
        camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G')) 

        # Settings 
        print(f"self.img_save_size[0] {self.img_save_size[0]}")
        print(f"self.img_save_size[0] {self.img_save_size[1]}")

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.img_save_size[0])
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.img_save_size[1])

        frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)) 
        frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"frame_width {frame_width}")
        print(f"frame_height {frame_height}")


        # camera.set(cv2.CAP_PROP_FPS, 5.0)
        if camera.isOpened():
            ret, frame = camera.read()
        while ret:
            ret, frame = camera.read()
            if ret:
                yield frame
            else:
                yield False

    def TakePhoto(self):
        self.take_picture = True
        file_name = f"{str(self.counter).zfill(3)}.png"
        print(f"file_name save {file_name}")
        full_path= os.path.join(self.path_save,file_name)
        cv2.imwrite(full_path, self.picture_save)
        self.counter+=1

    def Main(self):
        self.render_thread = threading.Thread(target=self.StartCamera)
        self.render_thread.daemon = True
        self.render_thread.start()

    def StartCamera(self):
        frame = self.LoadCamera()
        # CaptureFrame = None
        while True:
            Frame = next(frame)
            if frame:
                self.picture_save = Frame.copy()
                Frame = cv2.cvtColor(Frame, cv2.COLOR_BGR2RGB)
                picture = Image.fromarray(Frame)
                picture_wind = picture.resize(self.img_wind_size, resample=0)

                # CaptureFrame = picture.copy()
                picture_wind = ImageTk.PhotoImage(picture_wind)
                self.ImageLabel.configure(image = picture_wind)
                self.ImageLabel.photo = picture_wind
                time.sleep(0.001)

            else:
                pass

root = Tk()
App = CameraApp(root)
root.mainloop()
