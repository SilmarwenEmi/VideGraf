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

from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder


from kivy.core.window import Window
Window.clearcolor = (.94, .94, .94, 1)

"""class WindowManager(ScreenManager):
    pass

class MainScreen(Screen):
    pass

class SecondWindow(Screen):
    pass"""



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

        subjectName = StringProperty('test')
        subjectCamNb = StringProperty('test1')
        subjectGrafNb = StringProperty('test2')

        mainBox = MainBox()

        header = Header()
        mainBox.ids.top_box.add_widget(header)

        topics = Topics()
        header.ids.content_box.add_widget(topics)

        subjectsTitles = [["Les 50 ans de la faculté d'informatique", "10", "2"], 
                          ["La réforme du cursus en informatique","1", "3"], 
                          ["Master en sciences informatiques à Charleroi","1", "3"], 
                          ["Kirby","1", "3"], 
                          ["Jack","1", "3"], 
                          ["Nala","1", "3"]
                        ]
        listSubject = []
        for i in subjectsTitles:
            self.subjectName = i[0]
            self.subjectCamNb = i[1]
            self.subjectGrafNb = i[2]
            listSubject.append(Subject())

        for subject in listSubject:
            topics.ids.contents.add_widget(subject)

        return mainBox


if __name__ == "__main__":
    MyApp().run()