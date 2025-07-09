#!pip install tkinter --quiet
#!pip install ffmpeg --quiet
#!pip install git+https://github.com/openai/whisper.git --quiet


import os,sys
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import whisper

os.environ['WHISPER_CACHE_DIR'] = "./"
os.environ['WHISPER_FFMPEG_PATH'] = r"./ffmpeg/bin/ffmpeg.exe"
# language = 'ru'
model_path = './large-v3.pt'



class Main:
    data_to_convert = ''
    data_from_conver = dict()
    
    def openfile():
        file_path = filedialog.askopenfilename()
        if file_path !="":
            Main.data_to_convert += file_path
        if print(os.path.exists(Main.data_to_convert)) == True:
            label_1_namefile = ttk.Label(textvariable=Main.data_to_convert);label_1_namefile.pack(anchor="nw",padx=10,pady=13)

    def convert():
        model = whisper.load_model(model_path)
        data = model.transcribe(Main.data_to_convert,temperature=0,condition_on_previous_text=False)
        print(data["text"])

    def exit_app():
        sys.exit()
        

main = Tk(); main.title('Перевод из аудио в текст'); main.geometry('400x300')
editor = Text()
open_button = ttk.Button(text="Выбрать файл", command=Main.openfile);open_button.pack(anchor="nw",padx=10,pady=10)
convert_button = ttk.Button(text="Преобразовать в текст", command=Main.convert);convert_button.pack(anchor="nw",padx=10,pady=15)
exit_button = ttk.Button(text="Выход",command=Main.exit_app);exit_button.pack(anchor="nw",padx=10,pady=20)
progress_convert = ttk.Progressbar(main,orient="horizontal", mode="indeterminate");progress_convert.pack(anchor="nw",padx=10,pady=25)
main.mainloop()