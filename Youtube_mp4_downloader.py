# This program will allow you to download mp4 files from Youtube #

from pytube import YouTube

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

import threading

class YtDownloader():
    
    def __init__(self, root):

        self.radios = []
        self.labels = []
        self.title_label = ttk.Label()
        self.duration_label = ttk.Label()

        self.download_button = ttk.Button()
        self.browse_button = ttk.Button()
        self.destination_text = ttk.Entry()
        self.pb = ttk.Progressbar()

        self.percentage_of_completion = 0

        root.title("Youtube downloader")
        root.geometry("800x400")

        self.mainframe = ttk.Frame(root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky=N)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Youtube mp4 Downloader", font="Times 40 bold").grid(column=1,row=1)

        self.url = StringVar()
        url_entry = ttk.Entry(self.mainframe, width=70, textvariable=self.url, font='20')
        url_entry.grid(column=1, row=2)
        url_entry.insert(END, 'Copy your link here...')

        Button(
        self.mainframe,
        text="Show",
        command= self.asyncWaitForQuality,
        height=2,
        width=30,
        ).grid(column=1, row=3)

        self.video_info_frame = ttk.Frame(self.mainframe)
        self.video_info_frame.grid(column=1, row=5)

        self.destination_frame = ttk.Frame(self.mainframe)
        self.destination_frame.grid(column=1, row=6)

        self.download_button_frame = ttk.Frame(self.mainframe)
        self.download_button_frame.grid(column=1, row=7)

        self.progress_bar_frame = ttk.Frame(self.mainframe)
        self.progress_bar_frame.grid(column=1, row=8)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5)

        # url_entry.focus()

        url_entry.bind("<1>", lambda x: url_entry.delete(0,END))

    def showInfoAboutVideo(self, *args):
        yt = YouTube(self.url.get(), on_progress_callback = self.progressFunc, on_complete_callback=self.completeFunc)

        # show info about video
        dots = '...'

        self.title_label = ttk.Label(self.video_info_frame,
        text=f'title: {yt.title if len(yt.title) < 40 else yt.title[0:40] + dots}', font='Times 20')
        self.title_label.grid(column=1, row=1, columnspan=2, sticky=W)

        minutes = int(yt.length / 60)
        seconds = str(int(yt.length % 60)) if (yt.length % 60) > 10 else '0' + str(int(yt.length % 60))

        self.duration_label = ttk.Label(self.video_info_frame,
        text=f'duration: {minutes}:{seconds} min', font='Times 20')
        self.duration_label.grid(column=1, row=2, columnspan=2, sticky=W)
        

        items = yt.streams.filter(file_extension='mp4', progressive=True)
        row_counter = 4
        
        check_radio = StringVar()
        radio_var = []

        for item in items:
            quality = ttk.Label(self.video_info_frame, text=item.resolution)
            quality.grid(column=1, row=row_counter, sticky=E)
            self.labels.append(quality)

            variable = item.resolution
            radio_var.append(variable)

            choose_quality = ttk.Radiobutton(self.video_info_frame, variable=check_radio, value=row_counter,
            command=lambda : self.chooseStream(items[int(check_radio.get())-4]))
            choose_quality.grid(column=2, row=row_counter, sticky=W)
            self.radios.append(choose_quality)

            row_counter += 1

    def chooseStream(self, item, *args):
        self.video = item
        self.browse_button = ttk.Button(self.destination_frame, text="Browse", command=self.browse)
        self.browse_button.grid(column=1, row=1)

        self.download_path = StringVar()
        self.destination_text = ttk.Entry(self.destination_frame, textvariable=self.download_path)
        self.destination_text.grid(column=2, row=1)

        self.download_button = ttk.Button(
        self.download_button_frame,
        text="Download",
        command = lambda : self.asyncDownload(item))
        self.download_button.grid(column=1, row=1)

        self.destination_text.focus()

    def browse(self, *args):
        download_dir = filedialog.askdirectory(initialdir="/")
        self.download_path.set(download_dir)

    def downloadClick(self, *args):
        folder = self.download_path.get()
        item = self.video

        self.pb = ttk.Progressbar(
            self.progress_bar_frame,
            orient='horizontal',
            mode='determinate',
            length=600)

        self.pb.grid(column=1, row=1)

        item.download(folder)

    def asyncWaitForQuality(self, *args):
        # delete widgets every time Show button is clicked
        self.wait_label = ttk.Label(self.video_info_frame, text="wait...")
        self.wait_label.grid(column=1, columnspan=2, row=4, sticky=N)

        for widget in self.radios:
            widget.destroy()
        for widget in self.labels:
            widget.destroy()
        
        self.title_label.destroy()
        self.duration_label.destroy()
        self.browse_button.destroy()
        self.destination_text.destroy()
        self.download_button.destroy()
        self.pb.destroy()

        # with that app don't stuck then waiting for quality of video
        threading.Thread(target=self.showInfoAboutVideo).start()

    # *args is necessary 
    def asyncDownload(self, *args):
        # app don't stuck when video is downloading
        threading.Thread(target=self.downloadClick).start()

    def progressFunc(self, stream, chunk, bytes_remaining, *args):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        self.percentage_of_completion = bytes_downloaded / total_size * 100
        self.percentage_left = 100 - self.percentage_of_completion
        self.pb['value'] = self.percentage_of_completion

    def completeFunc(self, *args):
        messagebox.showinfo("Success!", "Download complete!")

if __name__ == '__main__':
    root = Tk()
    YtDownloader(root)
    root.mainloop()