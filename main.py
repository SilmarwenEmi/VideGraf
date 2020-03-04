import kivy
from kivy.app import App
from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.image import Image 

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Rectangle, Color, RoundedRectangle

from kivy.properties import StringProperty, ListProperty


from kivy.core.window import Window
Window.clearcolor = (.94, .94, .94, 1)


class Subject(Widget):
    pass

class Topics(Widget):
    pass

class Header(Widget):
    pass

class MainBox(BoxLayout):
    pass

class MyApp(App): # <- Main Class
    subjectsTitles = ListProperty()
    def build(self):

        abcd = StringProperty('test')

        mainBox = MainBox()

        header = Header()
        mainBox.ids.top_box.add_widget(header)

        topics = Topics()
        header.ids.content_box.add_widget(topics)

        subjectsTitles = ["Emi", "Laurent", "Hawa", "Kirby", "Jack", "Nala"]
        listSubject = []
        for i in subjectsTitles:
            self.abcd = i
            listSubject.append(Subject())

        for subject in listSubject:
            topics.ids.contents.add_widget(subject)

        return mainBox


if __name__ == "__main__":
    MyApp().run()