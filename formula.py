import tkinter as tk
import tkinter.messagebox

def submit():
    s = entry_name.get()
    s = s.split(',')
    dic = {
        "b1": "b1=a7+a9",
        "b3": "b3=a1+a3+a5+b1+a12+a14+a16+a18+a20+a22+a24+a26"
    }

    for i in s:
        text1 = f"{dic[i]}\n"
        text_result.insert(tk.END, text1)



win = tk.Tk()
win.title("公式查询")
win.geometry("500x500")
label = tk.Label(win, text="公式查询", font=('Times', 24)).place(x=180, y=20)
entry_name = tk.Entry(win)
entry_name.place(x=70, y=80)
label_name = tk.Label(win, text="变量名")
label_name.place(x=10, y=80)


button = tk.Button(win, text="计算公式", command=submit).place(x=70, y=230)

text_result = tk.Text(win)
text_result.configure(height=12, width=65)
text_result.place(x=20, y=295)

win.mainloop()
