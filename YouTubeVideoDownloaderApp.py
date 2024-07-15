import yt_dlp
import os
import customtkinter
from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkFont, CTkFrame
from tkinter import Tk
import sys
from threading import Thread

class HomeScreen(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry('800x500')
        
        # Define fonts
        self.my_font = CTkFont(family="Times New Roman", size=30, weight="bold")
        self.label_font = CTkFont(family="Times New Roman", size=20, weight="bold")
        self.label_font2 = CTkFont(family="Times New Roman", size=20, weight="bold")

        # Main label
        self.label = CTkLabel(master=self, text="Youtube \nVideo Downloader", font=self.my_font)
        self.label.pack(pady=40)
        
        self.frame = CTkFrame(master=self, fg_color='#001a33', border_color='#03396c', width=500, height=220, border_width=4, corner_radius=20)
        self.frame.pack(expand=True)
        self.frame.place(relx=0.5, rely=0.55, anchor='center')

        self.entry = CTkEntry(master=self.frame, placeholder_text="URL...", width=320)
        self.entry.configure(text_color='black')
        self.entry.place(relx=0.5, rely=0.5, anchor='center')
        
        self.label2 = CTkLabel(master=self.frame, text="Enter URL/Link", font=self.label_font)
        self.label2.configure(text_color='white')
        self.label2.place(relx=0.5, rely=0.3, anchor='center')

        self.button = CTkButton(master=self.frame, text='Paste', fg_color="#5940f1",
                                 hover_color='#555555', 
                                 border_color="#252525", border_width=2, width=35, height=30,
                                 command=self.paste)
        self.button.place(relx=0.89, rely=0.5, anchor='center')

        self.downloadButton = CTkButton(master=self.frame, text='Download', 
                                        fg_color='#5940f1', hover_color='#555555',
                                        border_color="#252525", border_width=2,
                                        command=self.start_download_thread)
        self.downloadButton.place(relx=0.5, rely=0.7, anchor='center')

        self.restartButton = CTkButton(master=self.frame, text='Restart', 
                                        fg_color='#5940f1', hover_color='#A6BF0E',
                                        border_color="#252525", border_width=3, width=29, height=29,
                                         command=self.restart_program
                                        )
        self.restartButton.place(relx=0.9, rely=0.15, anchor='center')

        self.informativeLabel = CTkLabel(master=self, text='', font=self.label_font2)
        self.informativeLabel.place(relx=0.5, rely=0.83, anchor='center')

    def paste(self):
        try:
            clipboard_contents = self.clipboard_get()
            self.entry.delete(0, 'end')
            self.entry.insert(0, clipboard_contents)
        except Exception as e:
            print(f"Error: {e}")

    def dl_progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes', 1)
            percentage = downloaded / total * 100
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)

            self.informativeLabel.configure(text=f'Downloading: {percentage:.2f}% at {speed:.2f} bytes/s, ETA: {eta}s')
            self.update_idletasks()

    def download(self):
        try:
            video_url = self.entry.get()
            output_directory = os.path.join(os.path.expanduser('~'), 'Desktop')

            ydl_opts = {
                'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
                'progress_hooks': [self.dl_progress_hook],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_title = info_dict.get('title', None)

            self.informativeLabel.configure(text=f'The video has been downloaded.\n {video_title} was saved on the desktop.')

        except Exception as e:
            self.informativeLabel.configure(text=f"Error downloading video: {e}")

    def start_download_thread(self):
        Thread(target=self.download).start()
        
    def restart_program(self):
        # Restart the Python script
        python = sys.executable
        os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    main_app = HomeScreen()
    main_app.mainloop()
