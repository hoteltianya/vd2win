import tkinter as tk
import vd4win

win = tk.Tk()
win.title('vdbench test')
win.geometry('800x600')

var1 = tk.StringVar()
var2 = tk.StringVar()

good_l = tk.Label(win, textvariable=var1, bg='green', width=25, height=2).pack('left')
bad_l = tk.Label(win, textvariable=var2, bg='green', width=25, height=2).pack('right')

run_log = tk.Text(win, height=25).pack('down')

def run_vdbench():
    a = vd4win.Vdbench()
    a.run()
    var1.set(a.good_list)
    var2.set(a.bad_list)
    run_log.insert('insert', a.vdlog)

b = tk.Button(win, text='Run Vdbench Test', width=15, height=2, command=run_vdbench).pack()

win.mainloop()
