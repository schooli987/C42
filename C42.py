from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
import requests


class MarsPhotoApp(MDApp):
    def build(self):
        self.title = "Mars Rover Photo Gallery"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Red"

        root = MDBoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Title and Subtitle
        title_label = MDLabel(
            text="[b]MARS ROVER PHOTO GALLERY[/b]",
            halign="center",
            markup=True,
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            font_style="H5",
            size_hint_y=None,
            height=dp(40)
        )

       
        # Top input layout
        top_box = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=dp(60))

        self.sol_input = MDTextField(
            hint_text="Enter a Mars sol (e.g., 1000)",
            mode="rectangle",
        
            text="1000",
            size_hint_x=0.7
        )
        search_btn = MDRaisedButton(
            text=" Search",
            size_hint_x=0.3,
            on_release=self.fetch_mars_photos
        )
        top_box.add_widget(self.sol_input)
        top_box.add_widget(search_btn)

        # Scrollable grid for gallery
        self.scroll = MDScrollView()
        self.gallery = GridLayout(
            cols=2,
            spacing=dp(15),
            padding=[dp(10), dp(10)],
            size_hint_y=None
        )
        self.gallery.bind(minimum_height=self.gallery.setter('height'))
        self.scroll.add_widget(self.gallery)

        # Add widgets to root
        root.add_widget(title_label)
       
        root.add_widget(top_box)
        root.add_widget(self.scroll)

        footer = FloatLayout(size_hint_y=None, height=dp(60))

        footer_content = MDBoxLayout(
            orientation='horizontal',
            spacing=dp(4),  # very close spacing
            size_hint=(None, None),
            size=(dp(300), dp(40)),  # tighter size
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        nasa_logo = AsyncImage(
            source="nasa.png",
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            allow_stretch=True
        )

        citation_label = MDLabel(
            text="Images courtesy of NASA's Mars Rover API",
            halign="left",
            theme_text_color="Hint",
            font_style="Caption",
            size_hint=(None, None),
            size=(dp(250), dp(30)),
            valign="middle"
        )

        footer_content.add_widget(nasa_logo)
        footer_content.add_widget(citation_label)
        footer.add_widget(footer_content)
        root.add_widget(footer)


        return root

    def fetch_mars_photos(self, instance):
        sol = self.sol_input.text.strip()
        self.gallery.clear_widgets()

        url = f"https://mars-photo-api-dyzg.onrender.com/api/v1/rovers/Curiosity/photos?sol={sol}"
        try:
            response = requests.get(url)
            data = response.json()
            photos = data["photos"][:6]  # Show only first 6

            if not photos:
                self.gallery.add_widget(MDLabel(
                    text="No photos found for this sol.",
                    halign="center",
                    theme_text_color="Hint",
                    size_hint_x=2
                ))
                return

            for photo in photos:
                img_url = photo["img_src"]
                camera = photo["camera"]["full_name"]
                earth_date = photo["earth_date"]

                card = MDCard(
                    orientation='vertical',
                    size_hint=(1, None),
                    height=dp(350),
                    padding=dp(10),
                    elevation=8,
                
                    radius=[20, 20, 20, 20],
                    ripple_behavior=True,
                    style="elevated"
                )

                image = AsyncImage(source=img_url, size_hint=(1, 0.8), allow_stretch=True, keep_ratio=True)
                caption = MDLabel(
                    text=f"{camera}\n{earth_date}",
                    halign="center",
                    theme_text_color="Primary",
                    size_hint=(1, 0.2),
                    font_style="Caption"
                )

                card.add_widget(image)
                card.add_widget(caption)
                self.gallery.add_widget(card)

        except Exception as e:
            self.gallery.add_widget(MDLabel(
                text=f"Error: {str(e)}",
                halign="center",
                theme_text_color="Error",
                size_hint_x=2
            ))
        


MarsPhotoApp().run()
