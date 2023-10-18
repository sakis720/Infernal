import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkthemes import ThemedTk
import subprocess


class SMPHeaderStripper:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title('SMP Header Stripper')
        self.root.resizable(False, False)

        self.icon_path = "ghostbusters.ico"
        if os.path.exists(self.icon_path):
            self.root.iconbitmap(self.icon_path)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='File', menu=self.file_menu)

        self.file_menu.add_command(label='Select Directory', command=self.browse_directory)
        self.file_menu.add_command(label='Select File', command=self.browse_file)
        #self.file_menu.add_command(label='Exit', command=self.root.quit)

        self.about_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label='?', menu=self.about_menu)
        self.about_menu.add_command(label='About', command=self.show_about_dialog)

        self.console_frame = ttk.Frame(self.root)
        self.console_frame.pack(pady=10)

        self.console = tk.Text(self.console_frame, width=40, height=10)
        self.console.pack(pady=5)

        self.progress_label = tk.Label(self.root, text="Progress: 0/0")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.root, mode='determinate')
        self.progress_bar.pack(pady=5)

    def strip_smp_header(self, input_file):
        try:
            output_dir = os.path.join(os.path.dirname(input_file), 'Stripped')
            os.makedirs(output_dir, exist_ok=True)

            with open(input_file, 'rb') as f_in:
                f_in.seek(160)
                content = f_in.read()

            filename = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(output_dir, filename + '.ogg')
            with open(output_file, 'wb') as f_out:
                f_out.write(content)

            self.console.config(state=tk.NORMAL)
            self.console.tag_configure("green", foreground="green")
            self.console.insert(tk.END, f"Processed: {filename}\n", "green")
            self.console.see(tk.END)
            self.console.update()
            self.console.config(state=tk.DISABLED)

            self.progress_label.config(text="Progress: 1/1")
            self.progress_bar['value'] = 1

            messagebox.showinfo('Conversion Complete', f'SMP header stripped for file: {filename}')
            self.open_output_directory(output_dir)

        except FileNotFoundError:
            messagebox.showerror('File Not Found', 'The selected file does not exist or cannot be found.')

    def strip_smp_files(self, input_path):
        try:
            files = [os.path.basename(file) for file in os.listdir(input_path) if file.endswith('.smp')]

            if not files:
                messagebox.showinfo('No Files Found', 'No .smp files were found in the selected directory.')
                return

            output_dir = os.path.join(input_path, 'stripped')
            os.makedirs(output_dir, exist_ok=True)

            total_files = len(files)

            self.console.config(state=tk.NORMAL)
            self.console.tag_configure("green", foreground="green")

            for progress, file in enumerate(files, start=1):
                input_file = os.path.join(input_path, file)

                try:
                    with open(input_file, 'rb') as f_in:
                        f_in.seek(160)
                        content = f_in.read()

                    filename = os.path.splitext(file)[0]
                    output_file = os.path.join(output_dir, filename + '.ogg')
                    with open(output_file, 'wb') as f_out:
                        f_out.write(content)

                    self.console.insert(tk.END, f"Processed: {filename}\n", "green")

                except IOError:
                    self.console.insert(tk.END, f"Error processing file: {file}\n")

                self.progress_label.config(text=f"Progress: {progress}/{total_files}")
                self.progress_bar['value'] = progress
                self.console.see(tk.END)
                self.console.update()

            self.console.config(state=tk.DISABLED)

            messagebox.showinfo('Stripping Complete', 'SMP header stripping completed!.')
            self.open_output_directory(output_dir)

        except OSError:
            messagebox.showerror('Error', 'Failed to create output directory.')

    def browse_directory(self):
        input_path = filedialog.askdirectory()
        if input_path:
            self.strip_smp_files(input_path)

    def browse_file(self):
        input_file = filedialog.askopenfilename(filetypes=[('SMP Files', '*.smp')])
        if input_file:
            self.strip_smp_header(input_file)

    def show_about_dialog(self):
        messagebox.showinfo('About', 'Version: 1.0\nCreator: Nomadwithoutahome')

    def open_output_directory(self, directory):
        if os.path.exists(directory):
            try:
                if sys.platform.startswith('darwin'):
                    subprocess.Popen(['open', directory])
                elif os.name == 'nt':
                    subprocess.Popen(['explorer', os.path.normpath(directory)])
                elif os.name == 'posix':
                    subprocess.Popen(['xdg-open', directory])
            except Exception as e:
                messagebox.showerror('Error', f'Failed to open output directory: {str(e)}')
        else:
            messagebox.showerror('Error', 'Output directory does not exist.')

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    smp_stripper = SMPHeaderStripper()
    smp_stripper.run()
