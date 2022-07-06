from pytube import YouTube

from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox

class YtDownloader():
    
    def __init__(self, root):

        root.title("Youtube downloader")

        self.mainframe = ttk.Frame(root, padding="10 10 10 10")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        ttk.Label(self.mainframe, text="Youtube Downloader").grid(column=1,row=1)

        self.url = StringVar()
        url_entry = ttk.Entry(self.mainframe, width=50, textvariable=self.url)
        url_entry.grid(column=1, row=2, sticky=(W,E))

        ttk.Button(self.mainframe, text="Check resolutions!", command=self.showInfoAboutVideo).grid(column=1, row=3)

        self.chose_quality_frame = ttk.Frame(self.mainframe)
        self.chose_quality_frame.grid(column=1, row=5)

        self.destination_frame = ttk.Label(self.mainframe)
        self.destination_frame.grid(column=1, row=6)

        self.download_button = ttk.Frame(self.mainframe)
        self.download_button.grid(column=1, row=7)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5)

        url_entry.focus()

    def showInfoAboutVideo(self, *args):
        yt = YouTube(self.url.get(), on_complete_callback=self.completeFunc)
        items = yt.streams.filter(file_extension='mp4', progressive=True)
        row_counter = 1
        
        check_radio = StringVar()
        radio_var = []

        for item in items:
            ttk.Label(self.chose_quality_frame, text=item.resolution).grid(column=1, row=row_counter)

            variable = item.resolution
            radio_var.append(variable)

            ttk.Radiobutton(self.chose_quality_frame, variable=check_radio, value=row_counter,
            command=lambda: self.chooseStream(items[int(check_radio.get())-1])).grid(column=2, row=row_counter)

            row_counter += 1

    def chooseStream(self, item, *args):
        browse_button = ttk.Button(self.destination_frame, text="Browse", command=self.browse)
        browse_button.grid(column=1, row=1)

        self.download_path = StringVar()
        destination_text = ttk.Entry(self.destination_frame, textvariable=self.download_path)
        destination_text.grid(column=2, row=1)

        download_button = ttk.Button(self.download_button, text="Download",
        command = lambda: self.downloadClick(item))
        download_button.grid(column=1, row=1)

        destination_text.focus()

    def browse(self, *args):
        download_dir = filedialog.askdirectory(initialdir="Your directiory path")
        self.download_path.set(download_dir)

    def downloadClick(self, item, *args):
        folder = self.download_path.get()
        item.download(folder)

    def completeFunc(self, *args):
        messagebox.showinfo("Success!", "Download complete!")

root = Tk()
YtDownloader(root)
root.mainloop()