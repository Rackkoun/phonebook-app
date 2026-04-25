# file frontend/app/main.py
import httpx
from nicegui import ui
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_PATH = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT_PATH / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

API_URL = os.getenv("API_URL") or os.getenv("BACKEND_API_URL", "http://localhost:8000")
print(f"[DEBUG] API_URL: {API_URL}")

class ContactManager:
    def __init__(self):
        self.contacts = []
        self.selected_contact = None

    async def load_contacts(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/contacts/")
                response.raise_for_status()
                self.contacts = response.json()
                self.update_table()
        except Exception as e:
            ui.notify(f"Error loading contacts: {e}", type="negative")
            print(f"Load error: {e}")
    
    def update_table(self):
        self.table.rows = self.contacts
    
    async def create_contact(self):
        data = {
            "first_name": self.first_name.value,
            "last_name": self.last_name.value,
            "phone": self.phone.value,
            "email": self.email.value
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{API_URL}/contacts/", json=data)
                response.raise_for_status()
            ui.notify("Contact created!", type="positive")
            await self.load_contacts()  # refresh list
            self.clear_form()
        except Exception as e:
            ui.notify(f"Error creating contact!", type="negative")
            print(f"Create Error: {e}")
    
    async def update_contact(self):
        if not self.selected_contact:
            ui.notify("Select a contact first", type="warning")
            return
        data = {
            "first_name": self.first_name.value,
            "last_name": self.last_name.value,
            "phone": self.phone.value,
            "email": self.email.value
        }
        try:
            async with httpx.AsyncClient() as client:
                await client.put(f"{API_URL}/contacts/{self.selected_contact['id']}", json=data)
            ui.notify("Contact updated!", type="positive")
            await self.load_contacts()
            self.clear_form()
        except Exception as e:
            ui.notify(f"Error Updating Contact: {e}", type="negative")
    
    async def delete_contact(self):
        if not self.selected_contact:
            ui.notify("Select a contact first", type="warning")
            return
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"{API_URL}/contacts/{self.selected_contact['id']}")
                response.raise_for_status()
            ui.notify("Contact deleted!", type="positive")
            await self.load_contacts()
            self.clear_form()
        except Exception as e:
            ui.notify(f"Error Deleting Contact: {e}", type="negative")
    
    def clear_form(self):
        self.first_name.value = ""
        self.last_name.value = ""
        self.phone.value = ""
        self.email.value = ""
        self.selected_contact = None
    
    def select_contact(self, e):
        self.selected_contact = e.args[1]
        self.first_name.value = self.selected_contact["first_name"]
        self.last_name.value = self.selected_contact["last_name"]
        self.phone.value = self.selected_contact["phone"]
        self.email.value = self.selected_contact["email"]

# Ui setup
manager = ContactManager()

with ui.column().classes("w-full max-w-3xl mx-auto p-4"):
    ui.label("Phonebook Manager").classes("text-3xl font-bold mb-4")

    # form
    with ui.card().classes("w-full mb-4"):
        with ui.row().classes("w-full gap-4"):
            manager.first_name = ui.input("First Name").classes("flex-1")
            manager.last_name = ui.input("Last Name").classes("flex-1")
        with ui.row().classes("w-full gap-4"):
            manager.phone = ui.input("Phone").classes("flex-1")
            manager.email = ui.input("Email").classes("flex-1")
        
        with ui.row():
            ui.button("Create", on_click=manager.create_contact).classes("bg-green-500")
            ui.button("Update", on_click=manager.update_contact).classes("bg-blue-500")
            ui.button("Delete", on_click=manager.delete_contact).classes("bg-red-500")
            ui.button("Clear", on_click=manager.clear_form).classes("bg-grey-500")

    # tables
    columns = [
        {"name": "first_name", "label": "First Name", "field": "first_name", "sortable": True},
        {"name": "last_name", "label": "Last Name", "field": "last_name", "sortable": True},
        {"name": "phone", "label": "Phone", "field": "phone"},
        {"name": "email", "label": "Email", "field": "email"},
    ]

    manager.table = ui.table(
        columns=columns, rows=[], row_key="id",
        on_select=manager.select_contact
    ).classes("w-full")

    # load contacts when page starts
    ui.timer(0.5, manager.load_contacts, once=True)

if __name__ == "__main__":
    ui.run(host="0.0.0.0", port=8080, reload=False)