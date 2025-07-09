import tkinter as tk
from tkinter import ttk, messagebox
from main import Contact, load_contacts, save_contacts

class ContactManagerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Contact Management System")
        master.geometry("800x550")
        master.configure(bg="#f0f0f0")


        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
            background="#ffffff",
            foreground="#333333",
            rowheight=25,
            fieldbackground="#ffffff"
        )
        style.map("Treeview", background=[("selected", "#4da6ff")])
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

        label_font = ("Helvetica", 11, "bold")


        ttk.Label(master, text="Name:", font=label_font).grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(master, width=40)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Label(master, text="Phone:", font=label_font).grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.phone_entry = ttk.Entry(master, width=40)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Label(master, text="Email:", font=label_font).grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.email_entry = ttk.Entry(master, width=40)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        ttk.Label(master, text="Address:", font=label_font).grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.address_entry = ttk.Entry(master, width=40)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)


        ttk.Button(master, text="Add Contact", width=20, command=self.add_contact).grid(row=4, column=0, pady=10, padx=5)
        ttk.Button(master, text="Show All Contacts", width=20, command=self.load_contacts_into_treeview).grid(row=4, column=1, pady=10, padx=5, sticky=tk.W)
        ttk.Button(master, text="Search", width=20, command=self.search_contact).grid(row=5, column=0, pady=5, padx=5)
        ttk.Button(master, text="Delete Contact", width=20, command=self.delete_contact).grid(row=5, column=1, pady=5, padx=5, sticky=tk.W)


        columns = ("Name", "Phone", "Email", "Address")
        self.tree = ttk.Treeview(master, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


        scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=6, column=2, sticky='ns')


        self.tree.tag_configure("oddrow", background="#f2f2f2")
        self.tree.tag_configure("evenrow", background="#ffffff")

        self.load_contacts_into_treeview()

    def add_contact(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_entry.get().strip()

        if name == "":
            messagebox.showwarning("Warning", "Name cannot be empty.")
            return

        new_contact = Contact(name, phone, email, address)
        contacts = load_contacts()
        contacts.append(new_contact)
        save_contacts(contacts)
        messagebox.showinfo("Success", "Contact added successfully!")
        self.clear_entries()
        self.load_contacts_into_treeview()

    def delete_contact(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Select a contact to delete.")
            return

        contact_data = self.tree.item(selected_item, 'values')
        name = contact_data[0]

        contacts = load_contacts()
        updated_contacts = [c for c in contacts if c.name != name]
        save_contacts(updated_contacts)
        messagebox.showinfo("Deleted", f"Contact '{name}' deleted.")
        self.load_contacts_into_treeview()

    def search_contact(self):
        search_term = self.name_entry.get().strip().lower()
        contacts = load_contacts()
        self.tree.delete(*self.tree.get_children())

        for i, c in enumerate(contacts):
            if search_term in c.name.lower():
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", tk.END, values=(c.name, c.phone, c.email, c.address), tags=(tag,))
        if not self.tree.get_children():
            messagebox.showinfo("Search", "No matching contact found.")

    def load_contacts_into_treeview(self):
        contacts = load_contacts()
        self.tree.delete(*self.tree.get_children())
        for i, c in enumerate(contacts):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(c.name, c.phone, c.email, c.address), tags=(tag,))

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ContactManagerGUI(root)
    root.mainloop()