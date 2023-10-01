import tkinter as tk
import urllib.request as web

def config_UI(root):
  root.title("Emotions Detector")
  root.resizable(False, False)
  x = int(root.winfo_screenwidth()/2 - 600)
  y = int(root.winfo_screenheight()/2 - 450)
  root.geometry(f"1200x800+{x}+{y}")
  root.iconbitmap("assets/app.ico")
  return root

def add_menu(root):
  menu = tk.Menu(root)
  root.config(menu=menu)
  file_menu = tk.Menu(menu, tearoff=False)
  menu.add_cascade(label="File", menu=file_menu)
  file_menu.add_command(label="Reset App", command=lambda: reset_app(root))
  file_menu.add_command(label="Open", command=lambda: print("Open File"))
  file_menu.add_separator()
  file_menu.add_command(label="Exit", command=root.destroy)
  help_menu = tk.Menu(menu, tearoff=False)
  menu.add_cascade(label="Help", menu=help_menu)
  help_menu.add_command(label="Github Repo", command=lambda: web.urlopen("https://github.com"))
  help_menu.add_command(label="About", command=lambda: print("About"))
  return root

def reset_app(root):
  root.destroy()
  main()

def main():
  root = tk.Tk()
  config_UI(root)
  add_menu(root)
  root.mainloop()
    
if __name__ == "__main__": 
    main()