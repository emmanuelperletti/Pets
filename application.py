from kivy.app import App
from kivy.uix.label import Label

class PetApp(App):
    def build(self):
        return Label(text='My pets')

if __name__ == "__main__":
    PetApp().run()
