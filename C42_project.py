import requests
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDTopAppBar

planet_images = {
    "mercury": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Mercury_in_true_color.jpg",
    "venus": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Venus-real_color.jpg",
    "earth": "https://upload.wikimedia.org/wikipedia/commons/9/97/The_Earth_seen_from_Apollo_17.jpg",
    "mars": "https://upload.wikimedia.org/wikipedia/commons/0/02/OSIRIS_Mars_true_color.jpg",
    "jupiter": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Jupiter.jpg",
    "saturn": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Saturn_during_Equinox.jpg",
    "uranus": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Uranus2.jpg",
    "neptune": "https://upload.wikimedia.org/wikipedia/commons/5/56/Neptune_Full.jpg",
    "pluto": "https://en.wikipedia.org/wiki/File:Pluto_in_True_Color_-_High-Res.jpg",
}

class PlanetInfoApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.theme_style = "Dark"

        root = MDBoxLayout(orientation='vertical')

        # Top bar
        top_bar = MDTopAppBar(title="Planet Explorer", elevation=5)
        root.add_widget(top_bar)

        # Main layout with scroll
        scroll = ScrollView()
        self.main_layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))

        # Input field
        self.input = MDTextField(
            hint_text="Enter planet name (e.g., mars)",
            size_hint_x=1,
            mode="rectangle"
        )

        # Button
        fetch_btn = MDRaisedButton(
            text="Get Info",
            on_release=self.fetch_planet_info,
            pos_hint={"center_x": 0.5}
        )

        # Planet Image
        self.planet_image = AsyncImage(source="", size_hint=(1, None), height=280, allow_stretch=True)

        # Result Card
        self.result_card = MDCard(orientation='vertical', size_hint_y=None)
        self.result_card.height = self.result_card.minimum_height

        self.result_label = MDLabel(text="Planet info will appear here.", halign="center", markup=True)
        self.result_card.add_widget(self.result_label)

        self.main_layout.add_widget(self.input)
        self.main_layout.add_widget(fetch_btn)
        self.main_layout.add_widget(self.planet_image)
        self.main_layout.add_widget(self.result_card)

        scroll.add_widget(self.main_layout)
        root.add_widget(scroll)

        return root

    def fetch_planet_info(self, *args):
        planet = self.input.text.strip().lower()
        if not planet:
            self.result_label.text = "Please enter a planet name."
            self.planet_image.source = ""
            return

        url = f"https://api.le-systeme-solaire.net/rest.php/bodies/{planet}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                gravity = data.get('gravity', 'N/A')
                mass = data.get('mass', {}).get('massValue', 'N/A')
                moons = data.get('moons')
                moon_count = len(moons) if moons else 0

                self.result_label.text = (
                    f"[b]{planet.capitalize()}[/b]\n"
                    f"Gravity: {gravity} m/s²\n"
                    f"Mass: {mass} x10²⁴ kg\n"
                    f"Moons: {moon_count}"
                )

                # Set image if found
                image_url = planet_images.get(planet, "")
                self.planet_image.source = image_url
            else:
                self.result_label.text = "Planet not found."
                self.planet_image.source = ""
        except Exception as e:
            self.result_label.text = f"Error: {str(e)}"
            self.planet_image.source = ""

if __name__ == "__main__":
    PlanetInfoApp().run()
