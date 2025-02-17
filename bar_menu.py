import kivy
import creds
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from creds import get_google_sheet


# Fetch data from the spreadsheet
def fetch_data():
    sheet = get_google_sheet()
    main_sheet = sheet.worksheet("alcohols")  # Replace with your sheet name
    data = main_sheet.get_all_records()  # Fetch all records as a list of dicts
    return data


class AlcoholMenuApp(App):
    def build(self):
        # Main Layout
        layout = BoxLayout(orientation="vertical")

        # Scrollable View
        scroll_view = ScrollView(size_hint=(1, 1))

        # GridLayout for content (1 column to ensure each category spans fully)
        main_grid = GridLayout(cols=1, size_hint_y=None)
        main_grid.bind(minimum_height=main_grid.setter("height"))

        # Fetch and organize data by category
        data = fetch_data()
        category_dict = {}
        for item in data:
            category = item.get("category", "Unknown Category")
            if category not in category_dict:
                category_dict[category] = []
            category_dict[category].append(item)

        # Add categories and drinks to the layout
        for category, items in category_dict.items():
            # Category header (spans both columns)
            category_label = Label(
                text=f"[b]{category}[/b]",  # Bold text
                markup=True,  # Enable bold styling
                size_hint_y=None,
                height=50,
                font_size=24,
                halign="center",
                valign="middle"
            )
            category_label.bind(size=category_label.setter('text_size'))
            main_grid.add_widget(category_label)

            # GridLayout for items in this category (2 columns: name + ABV)
            category_grid = GridLayout(cols=2, size_hint_y=None)
            category_grid.bind(minimum_height=category_grid.setter("height"))

            for item in items:
                name = item.get("name", "Unknown Item")
                abv = item.get("abv", "N/A")  # Assuming ABV is stored as a column

                # Format ABV to 1 decimal place
                formatted_abv = "{:.1f}".format(float(abv)) if abv != "N/A" else "N/A"

                # Left-aligned drink name with padding
                drink_label = Label(
                    text=f"    {name}",  # Adds padding using spaces
                    halign="left",
                    size_hint_y=None,
                    height=40
                )
                drink_label.bind(size=drink_label.setter('text_size'))

                # Right-aligned ABV value
                abv_label = Label(
                    text=f"{formatted_abv}%",
                    halign="right",
                    size_hint_y=None,
                    height=40
                )
                abv_label.bind(size=abv_label.setter('text_size'))

                # Add both labels to the category grid
                category_grid.add_widget(drink_label)
                category_grid.add_widget(abv_label)

            # Add category grid to main layout
            main_grid.add_widget(category_grid)

        # Add everything to the scrollable view
        scroll_view.add_widget(main_grid)
        layout.add_widget(scroll_view)

        return layout


# Run the App
if __name__ == "__main__":
    AlcoholMenuApp().run()
