import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title('Main')
    root.geometry('700x300')
    orig_desc = '[Desc]'
  
    header = ttk.Label(root, text='Scan Barcode to Generate Medicine Data', foreground='black',
                       font=('', 12, 'underline'))
    header.pack(pady=(10, 10))

    # Table (Treeview)
    columns = ("Code", "Name", "Expiry Date") 
    tree = ttk.Treeview(root, columns=columns, show="headings", height=4)
   
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))


    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=200, anchor="center")

    orig_data = ["[Code]", "[Name]", "[Exp_Date]", "[Desc]"]
    tree.insert("", "end", values=orig_data)
    tree.pack(pady=10)

    code_header = ttk.Label(root, text='Description', foreground='black', font=('arial', 10, 'bold', "underline")).pack()
    descrip_label = ttk.Label(root, text=orig_desc, foreground='black', font=('arial', 10), wraplength=400, justify="left")
    descrip_label.pack(pady= 10)

    reset_button = ttk.Button(root, text = 'Reset', command=lambda: reset_button(tree))
    reset_button.pack(pady= 10)


    def on_click(event=None):
        new_data = ["N/A", "N/A", "N/A", "N/A"] #GENERATED MEDICINE VALUES IN THIS
        tree.delete(*tree.get_children()) 
        tree.insert("", "end", values=new_data)  
        description_val = 'N/A' #GENERATE DESCRIPTON VALUE HERE
        descrip_label.config(text = description_val) 
        descrip_label.pack(padx = 15, pady=10)

    def reset_button(treeview):
        treeview.delete(*treeview.get_children())  
        treeview.insert("", "end", values=orig_data)  
        descrip_label.config(text = orig_desc)


    root.bind("<Return>", on_click)

    root.mainloop()

if __name__ == "__main__":
    main()
