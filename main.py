import gspread
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Setup
def get_google_sheet():
    # Authenticate and open the Google Spreadsheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("~/documents/personal/menu_files/bar-menu-448602-586e39802c4c.json", scope)
    client = gspread.authorize(creds)
    return client.open("Bar Menu")  # Replace with your spreadsheet name

# Fetch data from the spreadsheet
def fetch_data():
    sheet = get_google_sheet()
    main_sheet = sheet.worksheet("alcohol_categories")  # Replace with your sheet name
    linked_sheet = sheet.worksheet("alcohols")  # Replace with your linked sheet name
    data = main_sheet.get_all_records()  # Fetch all records as a list of dicts
    return data

# Kivy App
class AlcoholMenuApp(App):
    def build(self):
        # Fetch data
        data = fetch_data()

        # Main Layout
        layout = BoxLayout(orientation='vertical')
        scroll_view = ScrollView(size_hint=(1, None), size=(self.window_size()))

        # Populate Menu
        for item in data:
            name = item['name']  # Replace with your column name
            category = item['category']  # Replace with your column name

            # Add Labels for each item
            item_label = Label(text=f"{name} ({category})", size_hint_y=None, height=40)
            scroll_view.add_widget(item_label)

        # Add ScrollView to Layout
        layout.add_widget(scroll_view)

        # Add Buttons
        layout.add_widget(Button(text="Add Item", size_hint=(1, 0.1), on_press=self.add_item))
        layout.add_widget(Button(text="Remove Item", size_hint=(1, 0.1), on_press=self.remove_item))

        return layout

    def add_item(self, instance):
        print("Add Item button clicked")

    def remove_item(self, instance):
        print("Remove Item button clicked")

# Run the App
if __name__ == "__main__":
    AlcoholMenuApp().run()
