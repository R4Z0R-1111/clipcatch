import os
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog
import yt_dlp
from threading import Thread
from PIL import Image, ImageTk  
import webbrowser 


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class ClipCatchApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap("logo.ico")

        
        self.title("ClipCatch - YouTube Downloader by R4Z0R1337")
        self.geometry("700x800")  
        self.center_window(700, 800)  
        self.resizable(False, False)

        
        logo_path = "logo.png"  
        try:
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((150, 150), Image.Resampling.LANCZOS)  
            self.logo_photo = ImageTk.PhotoImage(logo_image)
            self.logo_label = tk.Label(self, image=self.logo_photo, bg='#1c1c1c')
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading logo: {e}")

        
        self.header_label = ctk.CTkLabel(
            self, text="CLIPCATCH\nYour Ultimate YouTube Downloader", font=("Arial", 20, "bold")
        )
        self.header_label.pack(pady=10)

        
        self.url_label = ctk.CTkLabel(self, text="YouTube Video or Playlist URL:")
        self.url_label.pack(pady=10)
        self.url_entry = ctk.CTkEntry(self, width=400)
        self.url_entry.pack(pady=10)

        
        self.quality_label = ctk.CTkLabel(self, text="Select Quality:")
        self.quality_label.pack(pady=10)

        
        self.quality_options = ["1080p", "720p", "480p", "360p", "Audio Only (MP3)"]
        self.quality_combobox = ctk.CTkComboBox(self, values=self.quality_options, state="readonly")
        self.quality_combobox.set("1080p")
        self.quality_combobox.pack(pady=10)

       
        self.path_label = ctk.CTkLabel(self, text="Select Download Path:")
        self.path_label.pack(pady=10)
        self.path_button = ctk.CTkButton(self, text="Choose Folder", command=self.select_path)
        self.path_button.pack(pady=10)
        self.selected_path = ""

       
        self.progress_bar = ctk.CTkProgressBar(self, width=400)  
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)

        
        self.download_button = ctk.CTkButton(self, text="Download", command=self.start_download_thread)
        self.download_button.pack(pady=20)

       
        self.progress_label = ctk.CTkLabel(self, text="")
        self.progress_label.pack(pady=5)

       
        self.footer_label = ctk.CTkLabel(
            self, text="You can enter either a single YouTube video link or a playlist link.\nClipCatch will automatically detect and download accordingly.", font=("Arial", 12)
        )
        self.footer_label.pack(pady=5)

     
        self.github_label = ctk.CTkLabel(
            self, text="Visit our GitHub repository", font=("Arial", 12, "underline"), cursor="hand2"
        )
        self.github_label.pack(pady=5)
        self.github_label.bind("<Button-1>", self.open_github_link)

       
        self.footer_credit = ctk.CTkLabel(
            self, text="Made with ♥ by R4Z0R1337 | OPEN SOURCE", font=("Arial", 12), text_color="lightgray"
        )
        self.footer_credit.pack(side="bottom", pady=10)  


    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    
    def select_path(self):
        self.selected_path = filedialog.askdirectory()
        if not self.selected_path:
            messagebox.showerror("Error", "Please select a directory to save the video.", parent=self)  # Center the error
        else:
            self.path_label.configure(text=f"Selected Path: {self.selected_path}")

   
    def start_download_thread(self):
        self.progress_bar.set(0)  
        self.progress_label.configure(text="")
        thread = Thread(target=self.start_download)
        thread.start()

   
    def start_download(self):
        url = self.url_entry.get()
        quality = self.quality_combobox.get()

        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.", parent=self)  
            return

        if not self.selected_path:
            messagebox.showerror("Error", "Please select a directory to save the video.", parent=self) 
            return

        self.download_video_or_playlist(url, quality, self.selected_path)

    
    def download_video_or_playlist(self, url, quality, save_path):
        ydl_opts = self.get_ydl_options(quality, save_path)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Success", "Download completed successfully!", parent=self)  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download: {str(e)}", parent=self)  

   
    def get_ydl_options(self, quality, save_path):
        ydl_opts = {
            "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
            "progress_hooks": [self.ydl_progress_hook],
        }

      
        if quality == "1080p":
            ydl_opts.update({"format": "bestvideo[height<=1080]+bestaudio/best"})
        elif quality == "720p":
            ydl_opts.update({"format": "bestvideo[height<=720]+bestaudio/best"})
        elif quality == "480p":
            ydl_opts.update({"format": "bestvideo[height<=480]+bestaudio/best"})
        elif quality == "360p":
            ydl_opts.update({"format": "bestvideo[height<=360]+bestaudio/best"})
        elif quality == "Audio Only (MP3)":
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]
            })

        return ydl_opts

 
    def ydl_progress_hook(self, d):
        if d["status"] == "downloading":
            downloaded_bytes = d.get("downloaded_bytes", 0)
            total_bytes = d.get("total_bytes", 1) 
            progress = downloaded_bytes / total_bytes
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"Downloading: {int(progress * 100)}%")

        if d["status"] == "finished":
            self.progress_bar.set(1)
            self.progress_label.configure(text="Download Complete!")

  
    def open_github_link(self, event):
        webbrowser.open("https://github.com/R4Z0R-1111/ClipCatch")  



if __name__ == "__main__":
    app = ClipCatchApp()
    app.mainloop()
