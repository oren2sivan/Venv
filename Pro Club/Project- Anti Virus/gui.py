import tkinter as tk
from tkinter import filedialog
import Scanning as scan

app = tk.Tk()
app.title("Anti_Virus")
app.geometry("1200x600+200+100")
app.configure(bg='white')

main_title = tk.Label(app, text='Anti Virus by Oren Sivan', bg="green", height="2", width="20", font=("Helvetica", "16"))
main_title.pack(pady=20)

selected_path = ""
files_list = []
id_list=[]
text = tk.Text(app)



def choose_file():
    global selected_path, files_list
    file_path = filedialog.askopenfilename()
    if file_path:
        selected_path = file_path
        print("Selected file:", file_path)
        files_list = scan.get_files(selected_path)
        print("Files list:", files_list)
    else:
        print("No file selected.")

def choose_folder():
    global selected_path, files_list
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_path = folder_path
        print("Selected folder:", folder_path)
        files_list = scan.get_files(selected_path)
        print("Files list:", files_list)
    else:
        print("No folder selected.")

import os

def confirm_files():
    global id_list
    if files_list:
        for file in files_list:
            response = scan.upload_file(file)
            id_list.append(response)
            text.insert(tk.END, f"File {os.path.basename(file)} was uploaded \n")
        text.pack()
    else:
        print("No files to upload.")


def start_scan():
    global id_list, files_list
    text.pack_forget()
    scan_results = scan.get_analysis_results(id_list, files_list)
    display_scan_results(scan_results)

def display_scan_results(scan_results):
    result_text = tk.Text(app)
    result_text.insert(tk.END, "Scan Results:\n\n")
    for file, result in scan_results.items():
        result_text.insert(tk.END, f"{file}: \n {result}\n\n")
    result_text.pack(expand=True, fill='both')




file_button = tk.Button(app, text="Choose File", command=choose_file)
file_button.pack()

folder_button = tk.Button(app, text="Choose Folder", command=choose_folder)
folder_button.pack()

confirm_button = tk.Button(app, text="Confirm files", command=confirm_files)
confirm_button.pack()


start_scan_button = tk.Button(app, text="START SCAN", command=start_scan)
start_scan_button.pack()





app.mainloop()