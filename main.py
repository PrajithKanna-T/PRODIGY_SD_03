import csv
import os

CONTACTS_FILE = "contacts.csv"
FIELDNAMES = ["Name", "Phone", "Email", "Address"]

class Contact:
    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "Name": self.name,
            "Phone": self.phone,
            "Email": self.email,
            "Address": self.address
        }

def load_contacts():
    contacts = []
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, fieldnames=FIELDNAMES)
            for row in reader:
                if not any(row.values()):
                    continue
                contacts.append(Contact(
                    name=row.get("Name", ""),
                    phone=row.get("Phone", ""),
                    email=row.get("Email", ""),
                    address=row.get("Address", "")
                ))
    return contacts

def save_contacts(contacts):
    with open(CONTACTS_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        for contact in contacts:
            writer.writerow(contact.to_dict())
