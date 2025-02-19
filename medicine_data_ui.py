
import tkinter as tk
from tkinter import Toplevel, messagebox, simpledialog
import tkinter.ttk as ttk
from tkinter import *
import pandas as pd


db = pd.read_excel('medicine_data.xlsx')
print(db.head()) 
print(db.loc[0, 'box_number'])


def check_filled(item_value):
    if db.loc[item_value, 'fill_status'] == False:
        response = messagebox.askyesnocancel("Return", f"{db.loc[item_value, 'box_number']} is currently empty. Would you like to add a new medicine?")
        if response == True:
            messagebox.showinfo("return", "Opening new Medicine")
            add_new_medicine(item_value)
        elif response == False:
            print("Action Cancelled")
        elif response == None:
            print("Action Cancelled")
    else:
        response = messagebox.askquestion('Return', f'Currently, this box is storing the medicine {db.loc[item_value, 'current_stored_medicine']}. Would you like to view?')
        if response == 'yes':
            view_medicine(item_value)
            return 
  

def add_new_medicine(item_value, is_edit=False):
    add_window = tk.Toplevel()
    add_window.title('Edit Medicine' if is_edit else "Adding Medicine")
    add_window.geometry('300x400')
    
    header = ttk.Label(add_window, text ="Edit Medicine" if is_edit else 'Add New Medicine',foreground = "black",
                       font = ('', 12, 'underline')).pack() 
    medicine_name_label = ttk.Label(add_window, text= 'Medicine Name', foreground ="black",font = ('', 10)).pack(anchor='w', padx=20)
    medicine_name_entry = ttk.Entry(add_window)
    medicine_name_entry.pack(anchor='w',padx=20)

    expiration_label = ttk.Label(add_window, text= 'Expiration Date (In MMDDYYYY)', foreground ="black",font = ('', 10)).pack(anchor='w',padx=20) #figure out a way to check and make sur eits entered correctly (debugging)
    expiration_date_entry = ttk.Entry(add_window)
    expiration_date_entry.pack(anchor='w',padx=20)

    type_label = ttk.Label(add_window, text= 'Type (Liquid, Cream, Pill, Other)', foreground ="black",font = ('', 10)).pack(anchor='w',padx=20)
    type_entry = ttk.Entry(add_window)
    type_entry.pack(anchor='w',padx=20)

    description_label = ttk.Label(add_window, text= 'Description', foreground ="black",font = ('', 10)).pack(anchor='w',padx=20)
    description_entry = tk.Text(add_window, height=10, width=30)
    description_entry.pack(anchor='w',padx=20)

    if is_edit:
        medicine_name_entry.insert(0, db.loc[item_value, 'current_stored_medicine'])
        expiration_date_entry.insert(0, db.loc[item_value, 'expiration_date'])
        type_entry.insert(0, db.loc[item_value, 'type'])
        description_entry.insert("1.0", db.loc[item_value, 'description'])


    def save_new_medicine(item_value, medicine_name_entry, expiration_date_entry, type_entry, description_entry):
        try:
            medicine_name = medicine_name_entry.get().strip()
            if not medicine_name:
                raise ValueError("Medicine name cannot be empty.")
                add_window.lift()
            db.loc[item_value, 'current_stored_medicine'] = medicine_name
         
            expiration_date = expiration_date_entry.get().strip()
            if not expiration_date.isdigit() or len(expiration_date) != 8:
                raise ValueError("Expiration Date cannot be empty.")
                add_window.lift() 
            db.loc[item_value, 'expiration_date'] = expiration_date
                  
            medicine_type = type_entry.get().strip()
            if medicine_type not in {'Liquid', 'Pill', 'Cream', 'Other'}:
                raise ValueError("Please enter one of the valid types for this medicine.")
                add_window.lift()                   
            db.loc[item_value, 'type'] = medicine_type

            description = description_entry.get("1.0", "end-1c").strip()
            if not description:
                raise ValueError("Description cannot be empty.")
                add_window.lift()
            db.loc[item_value, 'description'] = description

            db.loc[item_value, 'fill_status'] = True
            db.to_excel('medicine_data.xlsx', index=False)
       

            messagebox.showinfo("Successfully saved!", "Medicine information has been saved.")
            add_window.destroy()
        except ValueError as e:
            messagebox.showwarning("Invalid Input", str(e))
            add_window.lift()
        except ValueError:
            messagebox.showwarning("Invalid Input. Please try again.")
            add_window.lift()
        return 
    
    save_button = ttk.Button(add_window, text = 'Update Medicine' if is_edit else 'Save', style='SaveStyle.TButton', command=lambda:save_new_medicine(item_value, medicine_name_entry, expiration_date_entry, type_entry, description_entry)).pack(pady=20)


def view_medicine(item_value):
 
    view_window = tk.Toplevel()
    view_window.title("Information")
    view_window.pack_propagate(True)
    view_window.lift()
    header = ttk.Label(view_window, text="View or Edit Medicine",foreground = "black",
                       font = ('', 12, 'underline')).pack() 
    frame = ttk.Frame(view_window)
    frame.pack(fill="both", padx=20, pady=20)

    tree = ttk.Treeview(frame, columns=("Attribute", "Value"), show="headings", height=10)
    tree.heading("Attribute", text="Attribute")
    tree.heading("Value", text="Value")
    tree.column("Attribute", width=150)
    tree.column("Value", width=300) #might change width its kinda big

    for c in db.columns:
        tree.insert("", "end", values=(c, db.loc[item_value, c]))
        # ONLY ISSUE IS THAT DESCRIPTION TEXT ISNT WRAPPED :(


    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)
   
    edit_button = ttk.Button(view_window, text = 'Edit', style='SaveStyle.TButton', command=lambda:(call_edit(item_value))).pack(pady=10)
    delete_button = ttk.Button(view_window, text='Delete Medicine',style='SaveStyle.TButton', command=lambda:(delete_medicine(item_value))).pack(pady=10, ipadx=5)

    def delete_medicine(item_value):
        response = messagebox.askyesno("Return", f"Would you like to delete {db.loc[item_value, 'current_stored_medicine']}?")
        if response == True:
            db.loc[item_value, 'expiration_date'] = None
            db.loc[item_value, 'current_stored_medicine'] = None
            db.loc[item_value, 'description'] = None
            db.loc[item_value, 'type'] = None
            db.loc[item_value, 'fill_status'] = False
            db.to_excel('medicine_data.xlsx', index=False)
            view_window.destroy()
            messagebox.showinfo("Action", "Medicine successfully deleted.")
        if response == False:
            view_window.lift()

    def call_edit(item_value):
        messagebox.askyesno("Return", f"Would you like to edit {db.loc[item_value, 'current_stored_medicine']}?")
        if 'yes':
            view_window.destroy()
            add_new_medicine(item_value, is_edit=True)

           
def main():

    root = tk.Tk()
    root.title("Home Page")


    header = ttk.Label(root, text="Pharmacy Databank", foreground = "black",
                       font = ('', 12, 'underline')).grid(padx=20,pady=20)
    subheader = ttk.Label(root, text='Click on a box to add or change medicines.', foreground='black', font = ('', 10)).grid(row=1,padx=20)
    

    item_style = ttk.Style()
    item_style.configure('ItemStyle.TButton', foreground= 'black', background= 'black', borderwidth=2,
                    font = ('arial', 12), relief='raised', cursor='hand2')
    
    save_button_style = ttk.Style()
    save_button_style.configure('SaveStyle.TButton')
    box_1 = ttk.Button(root, text = 'Box One', style= 'ItemStyle.TButton', command=lambda: check_filled(0)).grid(row=2,column=0, padx=30,pady=30, ipadx=30,ipady=30)
    box_2 =  ttk.Button(root, text = 'Box Two', style= 'ItemStyle.TButton', command=lambda: check_filled(1)).grid(row=2,column=1, padx=30,pady=30, ipadx=30,ipady=30)
    box_3 =  ttk.Button(root, text = 'Box Three', style= 'ItemStyle.TButton', command=lambda: check_filled(2)).grid(row=3,column=0, padx=30,pady=30, ipadx=30,ipady=30)
    box_4 =  ttk.Button(root, text = 'Box Four', style= 'ItemStyle.TButton', command=lambda: check_filled(3)).grid(row=3,column=1, padx=30,pady=30, ipadx=30,ipady=30)



    root.mainloop()

if __name__ == "__main__":
    
    main()

   

