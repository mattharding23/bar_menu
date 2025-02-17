import kivy
import creds
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from creds import get_google_sheet
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

# Fetch data from the spreadsheet
def fetch_data():
    sheet = get_google_sheet()
    main_sheet = sheet.worksheet("alcohols")  # Replace with your sheet name
    data = main_sheet.get_all_records()  # Fetch all records as a list of dicts
    return data

# Background Widget
class BackgroundWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.bg = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self.update_bg, pos=self.update_bg)

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

# Kivy App
class AlcoholMenuApp(App):
    def build(self):
        # Root Layout (Vertical)
        root_layout = BoxLayout(orientation="vertical")

        # Title Label
        title = Label(
            text="Home Bar Menu",
            font_size="30sp",
            bold=True,
            size_hint=(1, None),
            height=60
        )
        root_layout.add_widget(title)

        # Scrollable View
        scroll_view = ScrollView(size_hint=(1, 1))

        # Outer Layout (Holds Sections)
        outer_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        outer_layout.bind(minimum_height=outer_layout.setter("height"))

        # Fetch Data
        data = fetch_data()

        # Group Data by Category
        category_dict = {}
        for item in data:
            category = item.get("category", "Unknown Category")
            if category not in category_dict:
                category_dict[category] = []
            category_dict[category].append(item)

        # Add Sections
        for category, drinks in category_dict.items():
            # Section Header
            section_header = Label(
                text=f"[b]{category}[/b]",
                markup=True,
                font_size="24sp",
                size_hint_y=None,
                height=50,
                bold=True
            )
            outer_layout.add_widget(section_header)

            # Grid Layout for Drinks
            grid_layout = GridLayout(cols=1, size_hint_y=None)
            grid_layout.bind(minimum_height=grid_layout.setter("height"))

            for item in drinks:
                name = item.get("name", "Unknown Item")
                label = Label(
                    text=f"{name}",
                    size_hint_y=None,
                    height=40
                )
                grid_layout.add_widget(label)

            outer_layout.add_widget(grid_layout)

        # Add Outer Layout to ScrollView
        scroll_view.add_widget(outer_layout)

        # Add ScrollView to Root Layout
        root_layout.add_widget(scroll_view)

        return root_layout

# Run the App
if __name__ == "__main__":
    AlcoholMenuApp().run()