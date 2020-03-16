import kivy
import pymongo
from PIL import Image

from random import random

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.image import Image 

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivy.graphics import Rectangle, Color, RoundedRectangle, Ellipse, Line, Canvas, Translate, Fbo, ClearColor, ClearBuffers, Scale


from kivy.uix.screenmanager import Screen, ScreenManager

from kivy.properties import StringProperty, ListProperty

import pygame
from kivy.graphics.fbo import Fbo
from kivy.graphics.opengl import glReadPixels, GL_RGBA, GL_UNSIGNED_BYTE
from kivy.graphics.texture import Texture


from kivy.core.window import Window
Window.clearcolor = (.94, .94, .94, 1)

from kivy.uix.popup import Popup
from kivy import platform


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
    def export_scaled_png(self, filename, image_scale=1):
        print("export_scaled_png")
        re_size = (self.width * image_scale, 
                self.height * image_scale)
        
        print(self.parent)

        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=re_size, with_stencilbuffer=True)

        with fbo:
            ClearColor(1, 1, 1, 1)
            ClearBuffers()
            Scale(image_scale, -image_scale, image_scale)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()
        fbo.texture.save(filename, flipped=True)
        fbo.remove(self.canvas)

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)

    """def save_grafffiti_png(self):
        #self.ids.graffiti_draw.export_to_png("test.png") #TODO
        self.ids.painter_widget.export_as_image().save("test.png", flipped=False)
        print("save graffiti to do")"""

class MyWidget(Widget):

    def export_scaled_png(self, filename, image_scale=1):
        print("export scaled png")
        re_size = (self.width * image_scale, self.height * image_scale)

        print(self)

        if self.parent is not None:
            canvas_parent_index = self.parent.canvas.indexof(self.canvas)
            if canvas_parent_index > -1:
                self.parent.canvas.remove(self.canvas)

        fbo = Fbo(size=re_size, with_stencilbuffer=True)

        with fbo:
            ClearColor(1, 1, 1, 1)
            ClearBuffers()
            Scale(image_scale, -image_scale, image_scale)
            Translate(-self.x, -self.y - self.height, 0)

        fbo.add(self.canvas)
        fbo.draw()
        fbo.texture.save(filename, flipped=False)
        fbo.remove(self.canvas)

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)


class AddVideoContent(Widget):
    pass


class GraffitiDraw(Widget):

    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color, mode='hsv') # (numéro couleur rgb) / 255
            d = 5.
            print("X: " + str(touch.spos[0]) + " - Y: " + str(touch.spos[1]))
            if 0.19 < touch.spos[0] < 0.96 and 0.05 < touch.spos[1] < 0.83:
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                #try:
                touch.ud['line'] = Line(points=(touch.x, touch.y))
                #except:
                    #print("erreur lors du dessin de caca - début")
                

    def on_touch_move(self, touch):
        if 0.19 < touch.spos[0] < 0.96 and 0.05 < touch.spos[1] < 0.83:
            try:
                touch.ud['line'].points += [touch.x, touch.y]
            except:
                pass

class InterventionDisplayedScreen(Screen):
    pass


class TopicsSelectionScreen(Screen):
    pass

class TopicDisplayScreen(Screen):
    pass

class AddGraffitiScreen(Screen):
    pass

class AddVideoScreen(Screen):
    pass

class MyApp(App): # <- Main Class
    subjectsTitles = ListProperty()

    def build(self):

        #connection to DB
        client = pymongo.MongoClient("mongodb+srv://Silmarwen:Kirby2011@stage-sodbw.gcp.mongodb.net/test?retryWrites=true&w=majority")
        if client != None:
            db = client["VideGraff"]
            collection = db["data"]


        #app code
        
        self.interventionContentRef = InterventionContent()
        addGraffitiContent = AddGraffitiContent()
        self.addGraffitiContentRef = addGraffitiContent
        mywgt = MyWidget()
        self.mywgtRef = mywgt

        subjectName = StringProperty('test')
        subjectCamNb = StringProperty('test1')
        subjectGrafNb = StringProperty('test2')

        interventionLabel = StringProperty("test3")
        interventionView = StringProperty("test4")
        subjectTitle = StringProperty("test5")

        #screens declaration
        topicsSelectionScreen = TopicsSelectionScreen(name ="screen_TopicsSelection")
        topicDisplayScreen = TopicDisplayScreen(name="screen_TopicDisplay")
        interventionDisplayedScreen = InterventionDisplayedScreen(name="screen_InterventionDisplayed")
        addGraffitiScreen = AddGraffitiScreen(name="screen_AddGraffiti")
        addVideoScreen = AddVideoScreen(name="screen_AddVideo")

        #topics selection screen
        header = Header()
        topicsSelectionScreen.ids.top_box.add_widget(header)

        topics = Topics()
        header.ids.content_box.add_widget(topics)

        """subjectsTitles = [["Les 50 ans de la faculté d'informatique", "10", "2"], 
                          ["La réforme du cursus en informatique","1", "3"], 
                          ["Le monde des chercheur","1", "3"], 
                          ["Les universités de Mons, de Bruxelles et de Namur vont organiser ensemble un nouveau master en sciences informatiques à Charleroi","1", "3"], 
                          ["Jack","1", "3"], 
                          ["Nala","1", "3"]
                        ]"""
        subjectsTitles = collection.find({})

        listSubject = []
        for i in subjectsTitles:
            self.subjectName = i["title"]
            self.subjectCamNb = i["video"]
            self.subjectGrafNb = i["graffitis"]
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
        
        self.subjectTitle = "Ajouter le titre correspondant"

        #intervention display screen
        interventionHeader = HeaderSubjectTitle()
        interventionDisplayedScreen.ids.top_box.add_widget(interventionHeader)

        interventionContent = InterventionContent()
        interventionHeader.ids.content_box.add_widget(interventionContent)

        #add graffiti
        graffTitleHeader = HeaderSubjectTitle()
        addGraffitiScreen.ids.top_box.add_widget(graffTitleHeader)

        graffTitleHeader.ids.content_box.add_widget(self.addGraffitiContentRef)

            #paint widget
        paintGraffiti = addGraffitiContent.ids.painter_widget
        self.painter = GraffitiDraw()
        paintGraffiti.add_widget(self.painter)
        paintGraffiti.add_widget(self.mywgtRef)

        #add video
        videoTitleHeader = HeaderSubjectTitle()
        addVideoScreen.ids.top_box.add_widget(videoTitleHeader)

        addVideoContent = AddVideoContent()
        videoTitleHeader.ids.content_box.add_widget(addVideoContent)


        #add screens to screenmanager
        screenManager = ScreenManager()

        screenManager.add_widget(topicsSelectionScreen)
        screenManager.add_widget(topicDisplayScreen)
        screenManager.add_widget(interventionDisplayedScreen)
        screenManager.add_widget(addGraffitiScreen)
        screenManager.add_widget(addVideoScreen)

        return screenManager

    def clear_canvas(self, obj):
            self.painter.canvas.clear()
    
    def save_grafffiti_png(self):
        print("save graffiti png")
        try:
            Window.screenshot(name="Screenshot.png")
 
            #if platform == 'android':
                #Window.screenshot(name='/storage/emulated/0/Pictures/Screenshots/Screenshot.png')
            
        except:
            pass
            
            

if __name__ == "__main__":
    MyApp().run()