import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("My Contact Book")
        self.root.geometry("950x650")
        self.root.configure(bg='#ecf0f1')

        self.contacts_file = "contacts.json"
        self.all_contacts = []
        self.current_edit_id = None

        # load saved contacts first
        self.load_all_contacts()
        self.setup_ui()
        self.refresh_contact_display()

    def setup_ui(self):
        # tried different layouts, this one works best
        container = tk.Frame(self.root, bg='#ecf0f1')
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # left panel for adding/editing
        left_panel = tk.Frame(container, bg='white', relief=tk.GROOVE, bd=3)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        left_panel.config(width=320)

        self.title_label = tk.Label(left_panel, text="Add New Contact",
                                    font=('Helvetica', 15, 'bold'),
                                    bg='white', fg='#34495e')
        self.title_label.pack(pady=15, padx=15)

        # input form section
        input_area = tk.Frame(left_panel, bg='white')
        input_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # name field
        name_label = tk.Label(input_area, text="Full Name *",
                              font=('Helvetica', 10, 'bold'),
                              bg='white', fg='#2c3e50', anchor='w')
        name_label.pack(fill=tk.X, pady=(8, 2))
        self.name_input = tk.Entry(input_area, font=('Helvetica', 11),
                                   relief=tk.GROOVE, bd=2)
        self.name_input.pack(fill=tk.X, pady=(0, 8), ipady=6)

        # phone field
        phone_label = tk.Label(input_area, text="Phone Number *",
                               font=('Helvetica', 10, 'bold'),
                               bg='white', fg='#2c3e50', anchor='w')
        phone_label.pack(fill=tk.X, pady=(8, 2))
        self.phone_input = tk.Entry(input_area, font=('Helvetica', 11),
                                    relief=tk.GROOVE, bd=2)
        self.phone_input.pack(fill=tk.X, pady=(0, 8), ipady=6)

        # email - optional
        email_label = tk.Label(input_area, text="Email Address",
                               font=('Helvetica', 10, 'bold'),
                               bg='white', fg='#2c3e50', anchor='w')
        email_label.pack(fill=tk.X, pady=(8, 2))
        self.email_input = tk.Entry(input_area, font=('Helvetica', 11),
                                    relief=tk.GROOVE, bd=2)
        self.email_input.pack(fill=tk.X, pady=(0, 8), ipady=6)

        # address - also optional
        addr_label = tk.Label(input_area, text="Address",
                              font=('Helvetica', 10, 'bold'),
                              bg='white', fg='#2c3e50', anchor='w')
        addr_label.pack(fill=tk.X, pady=(8, 2))
        self.addr_input = tk.Text(input_area, font=('Helvetica', 11),
                                  relief=tk.GROOVE, bd=2, height=3, wrap=tk.WORD)
        self.addr_input.pack(fill=tk.X, pady=(0, 8))

        # buttons at bottom
        btn_container = tk.Frame(input_area, bg='white')
        btn_container.pack(fill=tk.X, pady=15)

        self.submit_button = tk.Button(btn_container, text="Add Contact",
                                       command=self.handle_save,
                                       bg='#3498db', fg='white',
                                       font=('Helvetica', 11, 'bold'),
                                       relief=tk.FLAT, cursor='hand2', bd=0,
                                       activebackground='#2980b9')
        self.submit_button.pack(fill=tk.X, ipady=10)

        self.cancel_button = tk.Button(btn_container, text="Cancel Edit",
                                       command=self.handle_cancel,
                                       bg='#95a5a6', fg='white',
                                       font=('Helvetica', 11, 'bold'),
                                       relief=tk.FLAT, cursor='hand2', bd=0,
                                       activebackground='#7f8c8d')
        # hide cancel initially since we're not editing

        # right side for contact list
        right_panel = tk.Frame(container, bg='white', relief=tk.GROOVE, bd=3)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        # search bar at top
        search_container = tk.Frame(right_panel, bg='white')
        search_container.pack(fill=tk.X, padx=15, pady=15)

        search_icon = tk.Label(search_container, text="🔍",
                               font=('Helvetica', 13), bg='white')
        search_icon.pack(side=tk.LEFT, padx=(0, 8))

        self.search_text = tk.StringVar()
        self.search_text.trace('w', self.handle_search)

        self.search_box = tk.Entry(search_container, textvariable=self.search_text,
                                   font=('Helvetica', 11), relief=tk.GROOVE, bd=2)
        self.search_box.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)

        # placeholder text for search
        self.search_box.insert(0, "Type to search contacts...")
        self.search_box.config(fg='grey')
        self.search_box.bind('<FocusIn>', self.clear_search_placeholder)
        self.search_box.bind('<FocusOut>', self.restore_search_placeholder)

        # scrollable area for contacts
        scroll_container = tk.Frame(right_panel, bg='white')
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        canvas = tk.Canvas(scroll_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical",
                                  command=canvas.yview)

        self.contact_display = tk.Frame(canvas, bg='white')

        # configure scroll region when size changes
        self.contact_display.bind("<Configure>",
                                  lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.contact_display, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # mouse wheel support
        def scroll_handler(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", scroll_handler)

    def clear_search_placeholder(self, event):
        if self.search_box.get() == "Type to search contacts...":
            self.search_box.delete(0, tk.END)
            self.search_box.config(fg='black')

    def restore_search_placeholder(self, event):
        if not self.search_box.get():
            self.search_box.insert(0, "Type to search contacts...")
            self.search_box.config(fg='grey')

    def load_all_contacts(self):
        # check if file exists first
        if not os.path.exists(self.contacts_file):
            self.all_contacts = []
            return

        try:
            with open(self.contacts_file, 'r') as file:
                self.all_contacts = json.load(file)
        except Exception as e:
            print(f"Error loading contacts: {e}")
            self.all_contacts = []

    def save_contacts_to_file(self):
        # write to file
        try:
            with open(self.contacts_file, 'w') as file:
                json.dump(self.all_contacts, file, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def handle_save(self):
        # get values from form
        contact_name = self.name_input.get().strip()
        contact_phone = self.phone_input.get().strip()
        contact_email = self.email_input.get().strip()
        contact_address = self.addr_input.get("1.0", tk.END).strip()

        # basic validation
        if not contact_name:
            messagebox.showwarning("Missing Info", "Please enter a name!")
            self.name_input.focus()
            return

        if not contact_phone:
            messagebox.showwarning("Missing Info", "Please enter a phone number!")
            self.phone_input.focus()
            return

        # create contact dict
        new_contact = {
            'id': self.current_edit_id if self.current_edit_id else self.create_id(),
            'name': contact_name,
            'phone': contact_phone,
            'email': contact_email,
            'address': contact_address,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if self.current_edit_id:
            # update existing
            for idx, contact in enumerate(self.all_contacts):
                if contact['id'] == self.current_edit_id:
                    self.all_contacts[idx] = new_contact
                    break
            messagebox.showinfo("Done", "Contact updated!")
        else:
            # add new
            self.all_contacts.append(new_contact)
            messagebox.showinfo("Done", "Contact added!")

        self.save_contacts_to_file()
        self.clear_inputs()
        self.refresh_contact_display()

    def handle_edit(self, contact_id):
        # find the contact
        contact = None
        for c in self.all_contacts:
            if c['id'] == contact_id:
                contact = c
                break

        if not contact:
            return

        self.current_edit_id = contact_id

        # populate form fields
        self.name_input.delete(0, tk.END)
        self.name_input.insert(0, contact['name'])

        self.phone_input.delete(0, tk.END)
        self.phone_input.insert(0, contact['phone'])

        self.email_input.delete(0, tk.END)
        if contact.get('email'):
            self.email_input.insert(0, contact['email'])

        self.addr_input.delete("1.0", tk.END)
        if contact.get('address'):
            self.addr_input.insert("1.0", contact['address'])

        # change UI for editing mode
        self.title_label.config(text="Update Contact")
        self.submit_button.config(text="Save Changes")
        self.cancel_button.pack(fill=tk.X, ipady=10, pady=(8, 0))

    def handle_delete(self, contact_id):
        # confirm first
        confirm = messagebox.askyesno("Delete Contact",
                                      "Are you sure you want to delete this contact?")

        if confirm:
            self.all_contacts = [c for c in self.all_contacts if c['id'] != contact_id]
            self.save_contacts_to_file()
            self.refresh_contact_display()
            messagebox.showinfo("Deleted", "Contact has been removed")

    def handle_cancel(self):
        self.clear_inputs()

    def clear_inputs(self):
        # reset everything
        self.name_input.delete(0, tk.END)
        self.phone_input.delete(0, tk.END)
        self.email_input.delete(0, tk.END)
        self.addr_input.delete("1.0", tk.END)

        self.current_edit_id = None
        self.title_label.config(text="Add New Contact")
        self.submit_button.config(text="Add Contact")
        self.cancel_button.pack_forget()

    def handle_search(self, *args):
        query = self.search_text.get()
        if query == "Type to search contacts...":
            query = ""

        query = query.lower().strip()

        if query:
            results = []
            for contact in self.all_contacts:
                if query in contact['name'].lower() or query in contact['phone']:
                    results.append(contact)
            self.refresh_contact_display(results)
        else:
            self.refresh_contact_display()

    def refresh_contact_display(self, contacts_list=None):
        # clear old widgets
        for widget in self.contact_display.winfo_children():
            widget.destroy()

        if contacts_list is None:
            contacts_list = self.all_contacts

        # show message if empty
        if len(contacts_list) == 0:
            empty_frame = tk.Frame(self.contact_display, bg='white')
            empty_frame.pack(fill=tk.BOTH, expand=True, pady=40)

            icon = tk.Label(empty_frame, text="📱", font=('Helvetica', 50),
                            bg='white', fg='#bdc3c7')
            icon.pack(pady=15)

            msg = tk.Label(empty_frame, text="No contacts yet",
                           font=('Helvetica', 15, 'bold'),
                           bg='white', fg='#7f8c8d')
            msg.pack(pady=5)

            if len(self.all_contacts) > 0:
                hint = "No results found - try different keywords"
            else:
                hint = "Add your first contact using the form"

            hint_label = tk.Label(empty_frame, text=hint,
                                  font=('Helvetica', 10),
                                  bg='white', fg='#95a5a6')
            hint_label.pack(pady=5)
            return

        # sort alphabetically
        sorted_list = sorted(contacts_list, key=lambda x: x['name'].lower())

        # create cards for each contact
        for contact in sorted_list:
            self.build_contact_card(contact)

    def build_contact_card(self, contact):
        # main card frame
        card = tk.Frame(self.contact_display, bg='#f8f9fa',
                        relief=tk.RIDGE, bd=2)
        card.pack(fill=tk.X, pady=6, padx=6)

        # top section with name and buttons
        top_section = tk.Frame(card, bg='#f8f9fa')
        top_section.pack(fill=tk.X, padx=12, pady=(12, 8))

        name_label = tk.Label(top_section, text=contact['name'],
                              font=('Helvetica', 13, 'bold'),
                              bg='#f8f9fa', fg='#2c3e50', anchor='w')
        name_label.pack(side=tk.LEFT)

        # action buttons
        action_frame = tk.Frame(top_section, bg='#f8f9fa')
        action_frame.pack(side=tk.RIGHT)

        edit_btn = tk.Button(action_frame, text="Edit",
                             command=lambda: self.handle_edit(contact['id']),
                             bg='#27ae60', fg='white',
                             font=('Helvetica', 9, 'bold'),
                             relief=tk.FLAT, cursor='hand2',
                             padx=10, pady=5, bd=0)
        edit_btn.pack(side=tk.LEFT, padx=3)

        del_btn = tk.Button(action_frame, text="Delete",
                            command=lambda: self.handle_delete(contact['id']),
                            bg='#e74c3c', fg='white',
                            font=('Helvetica', 9, 'bold'),
                            relief=tk.FLAT, cursor='hand2',
                            padx=10, pady=5, bd=0)
        del_btn.pack(side=tk.LEFT, padx=3)

        # contact info section
        info_section = tk.Frame(card, bg='#f8f9fa')
        info_section.pack(fill=tk.X, padx=12, pady=(0, 12))

        # phone row
        phone_row = tk.Frame(info_section, bg='#f8f9fa')
        phone_row.pack(fill=tk.X, pady=4)
        icon1 = tk.Label(phone_row, text="📞", font=('Helvetica', 10), bg='#f8f9fa')
        icon1.pack(side=tk.LEFT, padx=(0, 10))
        text1 = tk.Label(phone_row, text=contact['phone'],
                         font=('Helvetica', 10), bg='#f8f9fa', fg='#34495e')
        text1.pack(side=tk.LEFT)

        # email row if exists
        if contact.get('email') and contact['email']:
            email_row = tk.Frame(info_section, bg='#f8f9fa')
            email_row.pack(fill=tk.X, pady=4)
            icon2 = tk.Label(email_row, text="📧", font=('Helvetica', 10), bg='#f8f9fa')
            icon2.pack(side=tk.LEFT, padx=(0, 10))
            text2 = tk.Label(email_row, text=contact['email'],
                             font=('Helvetica', 10), bg='#f8f9fa', fg='#34495e')
            text2.pack(side=tk.LEFT)

        # address row if exists
        if contact.get('address') and contact['address']:
            addr_row = tk.Frame(info_section, bg='#f8f9fa')
            addr_row.pack(fill=tk.X, pady=4)
            icon3 = tk.Label(addr_row, text="📍", font=('Helvetica', 10),
                             bg='#f8f9fa')
            icon3.pack(side=tk.LEFT, padx=(0, 10), anchor='n')
            text3 = tk.Label(addr_row, text=contact['address'],
                             font=('Helvetica', 10), bg='#f8f9fa',
                             fg='#34495e', wraplength=380, justify=tk.LEFT)
            text3.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def create_id(self):
        # generate unique id using timestamp
        from time import time
        return int(time() * 1000)


# run the app
if __name__ == "__main__":
    window = tk.Tk()
    app = ContactBook(window)
    window.mainloop()