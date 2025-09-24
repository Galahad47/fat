import os, sys,threading,time,whisper,tqdm
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tqdm.tk import tqdm
from tkinter.ttk import *
from time import sleep




os.environ['WHISPER_CACHE_DIR'] = "./"
os.environ['WHISPER_FFMPEG_PATH'] = r"./ffmpeg/bin/ffmpeg.exe"
model_path = './large-v3.pt'

class MainApp:
    def __init__(self):        
        self.data_to_convert = '';self.converted_text = '';self.name_file = ""
        self.main = Tk();self.main.title('Перевод из аудио в текст');self.main.attributes("-alpha",0.95);                                   self.main.geometry('400x700')#эта хрень отвечает за резолюшнс и всякое расположение относительно окошка, fill padx/y ты поймешь сам
        self.open_button = ttk.Button(text="Выбрать файл", command=self.openfile);                                                          self.open_button.pack(fill=X, padx=20, pady=10)
        self.convert_button = ttk.Button(text="Преобразовать в текст",command=self.start_conversion);                                       self.convert_button.pack(fill=X, padx=20, pady=10)
        self.exit_button = ttk.Button(text="Выход", command=self.exit_app);                                                                 self.exit_button.pack(fill=X, padx=20, pady=10)
        self.file_label = ttk.Label(text="Файл не выбран");                                                                                 self.file_label.pack(anchor="nw", padx=20, pady=5)
        self.text_widget = Text(self.main, wrap=WORD);                                                                                      self.text_widget.pack(expand=True, fill=BOTH, padx=20, pady=10)
        self.status_label = ttk.Label(text="Готово");                                                                                       self.status_label.pack(side=BOTTOM, fill=X, padx=20, pady=5)
        self.img = PhotoImage(file="./logo.png")
        self.text_widget.image_create("1.0", image=self.img)
 


        #Вот тут надо доделать а то фигня получается, а я вот хотел чтоб не получалась 
        # self.bar = ttk.Progressbar(self.main).pack(fill=X,pady=5)
        # self.progress = Progressbar(self.main,length=100,orient="horizontal").pack(fill=X,padx=25,pady=5)
            #print(tqdm(data)) #окак тут я пытаюсь понять int для визуализации прогрессбара
        # Да и не забыть прикрутить костыль пож tqdm чтобы отображать прогресс 


        self.main.mainloop()
    

        

    def openfile(self):
        file_path = filedialog.askopenfilename()
        
        
        if file_path:
            self.data_to_convert = file_path
            self.file_label.config(text=f"Выбранный файл: {os.path.basename(file_path)}") #прикалываюсь
            self.name_file = os.path.basename(file_path) #имя выбранного файла сохряняю тут, чтобы назвать потом файл с расширением txt

            if  os.path.exists(file_path) != 1:
                self.status_label.config(text="ОШИБКА: Файл не существует!", foreground="red")
            else:
                self.status_label.config(text="Файл выбран", foreground="green")

    
    
    def start_conversion(self):
        if not self.data_to_convert:
            self.status_label.config(text="Сначала выберите файл!", foreground="red")
            return
            
        if not os.path.exists(self.data_to_convert):
            self.status_label.config(text="ОШИБКА: Файл не существует!", foreground="red")
            return
        self.status_label.config(text="Обработка...", foreground="blue")
        self.convert_button.config(state=DISABLED)     
        threading.Thread(target=self.convert, daemon=True).start()#опа паралелим
          

    def convert(self):
        
        try:

            model = whisper.load_model(model_path,device="cpu")
            
            self.data = model.transcribe(self.data_to_convert,temperature=0.2,condition_on_previous_text=True,fp16=False,verbose=False,word_timestamps=True)
            # for segment in self.data['segments']:
            #     print(f"Прогресс: {segment['percentDone']}%")
            
            self.converted_text = self.data["text"]
            os.makedirs("./Готовый текст", exist_ok=True)
            name = self.name_file
            #print(self.name_file)
            with open(f"./Готовый текст/{name}.txt", "w", encoding="utf-8") as file:
                file.write(self.converted_text)
            self.main.after(0, self.update_ui)
            
             
            
        finally:
            self.main.after(0, lambda: self.convert_button.config(state=NORMAL))

    def update_ui(self):
        self.text_widget.delete(1.0, END)
        self.text_widget.insert(END, self.converted_text)
        self.status_label.config(text="Готово!", foreground="green")


    def show_error(self, message):
        self.status_label.config(text=f"ОШИБКА: {message}", foreground="red")

        self.text_widget.delete(1.0, END)
        self.text_widget.insert(END, f"Ошибка преобразования:\n{message}")

    
    def exit_app(self):
        self.main.destroy()
        sys.exit(0)




if __name__ == "__main__":
    MainApp()