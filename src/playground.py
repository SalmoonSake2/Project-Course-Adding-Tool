import ttkbootstrap as ttk

from ttkbootstrap.scrolled import ScrolledFrame


def event(obj):
    obj.container.destroy()

root = ttk.Window()

frame = ScrolledFrame(master=root)
frame.pack(pady=100)
btn1 = ttk.Button(master=frame,text="hello world!",command=lambda x = frame:event(x))
btn1.pack()
btn2 = ttk.Button(master=frame,text="hello world!")
btn2.pack(pady=100)

root.mainloop()