import os,sys
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import whisper
import threading
import time
os.environ['WHISPER_CACHE_DIR'] = "./"
os.environ['WHISPER_FFMPEG_PATH'] = r"./ffmpeg/bin/ffmpeg.exe"
model_path = './large-v3.pt'



class Main:
    data_to_convert = ''
    data_from_conver = ''

    def __init__(self):
        self.main = Tk(); self.main.title('Перевод из аудио в текст'); self.main.minsize(200,100);self.main.maxsize(800,600);self.main.geometry('400x300')
        self.open_button = ttk.Button(text="Выбрать файл", command=Main.openfile);self.open_button.pack(fill=X,anchor="center")
        self.convert_button = ttk.Button(text="Преобразовать в текст", command=Main.potok1.start());self.convert_button.pack(fill=X,anchor="center")
        self.exit_button = ttk.Button(text="Выход",command=Main.exit_app);self.exit_button.pack(fill=X,anchor="center")
        self.text_from_whisper = Text(); self.text_from_whisper.pack(expand=1,fill=X);img = PhotoImage(file="./logo.png")
        self.text_from_whisper.image_create("1.0",image=img)
        self.main.mainloop()


    def openfile(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path !="":
            Main.data_to_convert += self.file_path
        else:
            pass
        if print(os.path.exists(Main.data_to_convert)) == True:
            label_1_namefile = ttk.Label(textvariable=Main.data_to_convert);label_1_namefile.pack(anchor="nw",padx=10,pady=13)
        else:
            pass

    
    def convert(self):
        model = whisper.load_model(model_path)
        data = model.transcribe(Main.data_to_convert,temperature=0,condition_on_previous_text=True,fp16=False)
        print(data["text"])
        Main.data_from_conver += data["text"]
        with open("./Готовый текст/text.txt","w") as file:
            file.write(data["text"])
    potok1 = threading.Thread(target=convert)
    
    def exit_app(self):
        os._exit(Main)
        sys.exit(Main)
        
Main()