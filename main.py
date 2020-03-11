import kivy

from random import random

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.image import Image 

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Rectangle, Color, RoundedRectangle, Ellipse, Line

from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.properties import StringProperty, ListProperty


from kivy.core.window import Window
Window.clearcolor = (.94, .94, .94, 1)


class Subject(Widget):
    pass

class Intervention(Widget):
    pass

class Topics(Widget):
    pass

class Header(Widget):
    pass

class HeaderTopicName(Widget):
    pass

class HeaderSubjectTitle(Widget):
    pass

class InterventionsSelection(Widget):
    pass

class InterventionDisplayedContent(Widget):
    pass

class InterventionContent(Widget):

    video_state = StringProperty("pause")

    def play(self):
        if self.video_state == 'play':
            self.video_state = 'pause'

        elif self.video_state == 'pause':
            self.video_state = 'play'

        print("Hello")

class AddGraffitiContent(Widget):
    def save_grafffiti_png(self):
        #self.ids.painter_widget.export_to_png("test.png")
        print("hello")

class GraffitiDraw(Widget):

    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color, mode='hsv') # (numéro couleur rgb) / 255
            d = 5.
            print("X: " + str(touch.spos[0]) + " - Y: " + str(touch.spos[1]))
            if 0.19 < touch.spos[0] < 0.96 and 0.05 < touch.spos[1] < 0.86:
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                #try:
                touch.ud['line'] = Line(points=(touch.x, touch.y))
                #except:
                    #print("erreur lors du dessin de caca - début")
                

    def on_touch_move(self, touch):
        if 0.19 < touch.spos[0] < 0.96 and 0.05 < touch.spos[1] < 0.86:
            try:
                touch.ud['line'].points += [touch.x, touch.y]
            except:
                print("erreur lors du dessin de caca - tracé")

class InterventionDisplayedScreen(Screen):
    pass


class TopicsSelectionScreen(Screen):
    pass

class TopicDisplayScreen(Screen):
    pass

class AddGraffitiScreen(Screen):
    pass

class MyApp(App): # <- Main Class
    subjectsTitles = ListProperty()

    def build(self):

        self.interventionContentRef = InterventionContent()
        self.addGraffitiContentRef = AddGraffitiContent()

        subjectName = StringProperty('test')
        subjectCamNb = StringProperty('test1')
        subjectGrafNb = StringProperty('test2')

        interventionLabel = StringProperty("test3")
        interventionView = StringProperty("test4")

        #screens declaration
        topicsSelectionScreen = TopicsSelectionScreen(name ="screen_TopicsSelection")
        topicDisplayScreen = TopicDisplayScreen(name="screen_TopicDisplay")
        interventionDisplayedScreen = InterventionDisplayedScreen(name="screen_InterventionDisplayed")
        addGraffitiScreen = AddGraffitiScreen(name="screen_AddGraffiti")

        #topics selection screen
        header = Header()
        topicsSelectionScreen.ids.top_box.add_widget(header)

        topics = Topics()
        header.ids.content_box.add_widget(topics)

        subjectsTitles = [["Les 50 ans de la faculté d'informatique", "10", "2"], 
                          ["La réforme du cursus en informatique","1", "3"], 
                          ["Master en sciences informatiques à Charleroi","1", "3"], 
                          ["Les universités de Mons, de Bruxelles et de Namur vont organiser ensemble un nouveau master en sciences informatiques à Charleroi","1", "3"], 
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
        
        #topic display screen
            #TODO: if len() == 0 then chibi mec else ce qui est déjà fait
        headerTopicName = HeaderTopicName()
        topicDisplayScreen.ids.top_box.add_widget(headerTopicName)

        interventionsSelection = InterventionsSelection()
        headerTopicName.ids.content_box.add_widget(interventionsSelection)

        interventionsContents = [["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff_2.png"],
                                 ["Bonjour", "intervention_graff_2.png"], 
                                 ["Bonjour", "intervention_graff.png"],

                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff.png"],

                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff_2.png"], 
                                 ["Bonjour", "intervention_graff.png"], 
                                 ["Bonjour", "intervention_graff_2.png"]
                                ] 

        listInterventions = []
        for i in interventionsContents:
            self.interventionLabel = i[0]
            self.interventionView = i[1]
            listInterventions.append(Intervention())

        for intervention in listInterventions:
            interventionsSelection.ids.intervention_content.add_widget(intervention)

        #intervention display screen
        interventionHeader = HeaderSubjectTitle()
        interventionDisplayedScreen.ids.top_box.add_widget(interventionHeader)

        interventionContent = InterventionContent()
        interventionHeader.ids.content_box.add_widget(interventionContent)

        #add graffiti
        graffTitleHeader = HeaderSubjectTitle()
        addGraffitiScreen.ids.top_box.add_widget(graffTitleHeader)

        addGraffitiContent = AddGraffitiContent()
        graffTitleHeader.ids.content_box.add_widget(addGraffitiContent)

            #paint widget
        paintGraffiti = addGraffitiContent.ids.painter_widget
        self.painter = GraffitiDraw()
        paintGraffiti.add_widget(self.painter)

        #add screens to screenmanager
        screenManager = ScreenManager()

        screenManager.add_widget(topicsSelectionScreen)
        screenManager.add_widget(topicDisplayScreen)
        screenManager.add_widget(interventionDisplayedScreen)
        screenManager.add_widget(addGraffitiScreen)

        return screenManager

    def clear_canvas(self, obj):
            self.painter.canvas.clear()
            

if __name__ == "__main__":
    MyApp().run()