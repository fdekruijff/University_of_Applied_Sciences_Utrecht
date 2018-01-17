import tkinter as tk
import tkinter.font

root = tk.Tk()

my_font = tkinter.font.Font(family="Monaco", size=12)  #Must come after the previous line.

root.geometry("1000x200")

lb = tk.Listbox(root, width=150, font=my_font)
lb.insert("1", "{:4}{:4}".format("a", "b") )
lb.insert(tk.END, "1234567890" * 4)
lb.insert(tk.END, "{:>10}{:>10}".format(100, 200) )
lb.pack()

root.mainloop()