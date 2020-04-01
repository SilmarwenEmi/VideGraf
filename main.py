import kivy
import pymongo
import os
import cv2
import pygame

from PIL import Image
from random import random

from kivy.clock import Clock

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

class ChibiMan(Widget):
    pass

class HeaderSubjectTitle(Widget):
    pass

class InterventionsSelection(Widget):
    def fire_popup(self):
        pops = DescriptionPopup()
        pops.open()
    
    def fire_popupGraffiti(self):
        pops = GraffitiPopup()
        pops.open()
    

class InterventionsSelectionEmpty(Widget):

    def fire_popup(self):
        pops = DescriptionPopup()
        pops.open()

    def fire_popupGraffiti(self):
        pops = GraffitiPopup()
        pops.open()

    def fire_popupAddGraffiti(self):
        pops = AddGraffitiPopup()
        pops.open()

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
    pass


class MyWidget(Widget):

    def export_scaled_png(self, filename, image_scale=1):
        re_size = (self.width * image_scale, self.height * image_scale)
        print("##################################")
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

        # graffiti number (without video)
        global graffitiNb 
        graffitiNb = 0
        print("filename")
        print(filename)
        try: 
            files = os.listdir(filename)
            print(files)
            files.remove("subject")

            if ".DS_Store" in files:
                files.remove(".DS_Store")
            
            graffitiNb = len(files)
            
        except:
            print("erreur file")
        
        # save graffiti as png
        fbo.add(self.canvas)
        fbo.draw()
        print("longueur liste : " + str(len(files)))
        print("graff" + str(graffitiNb+1) + ".png")
        print("FILE NAME HERE : " + filename+"graff" + str(graffitiNb+1) + ".png" + "####################")

        fbo.texture.save(filename+"graff" + str(graffitiNb+1) + ".png", flipped=False)
        
        print("save ok")
        fbo.remove(self.canvas)
        print("remove ok")

        if self.parent is not None and canvas_parent_index > -1:
            self.parent.canvas.insert(canvas_parent_index, self.canvas)


class AddVideoContent(Widget):
    pass


class GraffitiDraw(Widget):

    def on_touch_down(self, touch):
        color = (random(), random(), random())
        #print(color)
        color = (.349, .5686, .392)
        with self.canvas:
            Color(*color, mode='hsv') # (numéro couleur rgb) / 255
            d = 5.
            print("X: " + str(touch.spos[0]) + " - Y: " + str(touch.spos[1]))
            if 0.2125 < touch.spos[0] < 0.7833 and 0.2914 < touch.spos[1] < 0.7276:
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                #try:
                touch.ud['line'] = Line(points=(touch.x, touch.y),width=4)
                #except:
                    #print("erreur lors du dessin de caca - début")
                

    def on_touch_move(self, touch):
        if 0.2125 < touch.spos[0] < 0.7833 and 0.2914 < touch.spos[1] < 0.7276:
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


class DescriptionPopup(Popup):
    pass

class GraffitiPopup(Popup):
    pass

class AddGraffitiPopup(Popup):
    pass

class MyApp(App): # <- Main Class
    subjectsTitles = ListProperty()
    subjectTitle = StringProperty("")
    currentDescription = StringProperty("test descr")
    currentIntervention = StringProperty("")


    def build(self):

        #connection to DB
        self.client = pymongo.MongoClient("mongodb+srv://Silmarwen:Kirby2011@stage-sodbw.gcp.mongodb.net/test?retryWrites=true&w=majority")
        if self.client != None:
            db = self.client["VideGraff"]
            self.collection = db["data"]
        
        #upadate DB if graffiti deleted
        directories = os.listdir("data/")

        if ".DS_Store" in directories:
                directories.remove(".DS_Store")

        for directory in directories:

            files = os.listdir("data/%s" % (directory))
            files.remove("subject")

            if ".DS_Store" in files:
                files.remove(".DS_Store")

            nbGraff = 0
            for fileName in files:
                
                if "graff" in fileName:
                    nbGraff += 1

            myquery = { "title": directory }
            newvalues = { "$set": { "graffitis": nbGraff } }

            self.client["VideGraff"]["data"].update_one(myquery, newvalues)


        #app code
        
        self.interventionContentRef = InterventionContent()
        addGraffitiContent = AddGraffitiContent()
        self.addGraffitiContentRef = addGraffitiContent
        self.mywgtRef = MyWidget()
        self.interventionsSelection = InterventionsSelection()
        self.addGraffitiPopup = AddGraffitiPopup()
        self.myWidget = MyWidget()
        

        interventionView = StringProperty("")
        subjectName = StringProperty('test')
        subjectCamNb = StringProperty('test1')
        subjectGrafNb = StringProperty('test2')
        self.subjectDescription = {}
        interventionLabel = StringProperty("test3")

        #screens declaration
        self.topicsSelectionScreen = TopicsSelectionScreen(name ="screen_TopicsSelection")
        self.topicDisplayScreen = TopicDisplayScreen(name="screen_TopicDisplay")
        self.interventionDisplayedScreen = InterventionDisplayedScreen(name="screen_InterventionDisplayed")
        addGraffitiScreen = AddGraffitiScreen(name="screen_AddGraffiti")
        addVideoScreen = AddVideoScreen(name="screen_AddVideo")

        #topics selection screen
        self.header = Header()
        self.topicsSelectionScreen.ids.top_box.add_widget(self.header)

        self.topics = Topics()
        self.header.ids.content_box.add_widget(self.topics)

        #takes info from mongodb
        subjectsTitles = self.collection.find({})
        
        print("################################")
        print(subjectsTitles)
        self.subjectsDescription = {}

        listSubject = []
        for subject in subjectsTitles:
            self.subjectDescription[subject["title"]] = subject["description"]
            self.subjectName = subject["title"]
            self.subjectCamNb = subject["video"]
            self.subjectGrafNb = subject["graffitis"]
            listSubject.append(Subject())

        for subject in listSubject:
            self.topics.ids.contents.add_widget(subject)
        
        #topic display screen
        self.headerTopicName = HeaderTopicName()
        self.topicDisplayScreen.ids.top_box.add_widget(self.headerTopicName)

    
        #intervention display screen
        interventionHeader = HeaderSubjectTitle()
        self.interventionDisplayedScreen.ids.top_box.add_widget(interventionHeader)

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

        """self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)
        addVideoContent.ids.camera_display.add_widget(self.my_camera)"""

        videoTitleHeader.ids.content_box.add_widget(addVideoContent)


        #add screens to screenmanager
        screenManager = ScreenManager()

        screenManager.add_widget(self.topicsSelectionScreen)
        screenManager.add_widget(self.topicDisplayScreen)
        screenManager.add_widget(self.interventionDisplayedScreen)
        screenManager.add_widget(addGraffitiScreen)
        screenManager.add_widget(addVideoScreen)

        return screenManager

    def clear_graff(self):
        self.painter.canvas.clear()
    
    
    def displayInterventions(self):

        self.topicDisplayScreen.ids.top_box.remove_widget(self.headerTopicName)
        self.headerTopicName = HeaderTopicName()
        self.topicDisplayScreen.ids.top_box.add_widget(self.headerTopicName)

        try: 
            files = os.listdir("data/%s" % (self.subjectTitle))
            files.remove("subject")

            if ".DS_Store" in files:
                files.remove(".DS_Store")
            
            if len(files) > 0 :
                self.interventionsSelection = InterventionsSelection()
                
                for fileName in files:
                    self.interventionView = "data/%s/%s" % (self.subjectTitle, fileName)
                    self.interventionsSelection.ids.intervention_content.add_widget(Intervention())

                self.headerTopicName.ids.content_box.add_widget(self.interventionsSelection)
            
            else:
                self.interventionsSelectionEmpty = InterventionsSelectionEmpty()
                self.headerTopicName.ids.content_box.add_widget(self.interventionsSelectionEmpty)
        
    

        except:
            pass
            
     
    def updateGraffitiNumberDB(self):
        myquery = { "title": self.subjectTitle }
        newvalues = { "$set": { "graffitis": graffitiNb + 1 } }

        print(myquery)
        print(newvalues)

        self.client["VideGraff"]["data"].update_one(myquery, newvalues)

        #takes info from mongodb
        subjectsTitles = self.client["VideGraff"]["data"].find({})

        self.header.ids.content_box.remove_widget(self.topics)
        self.topics = Topics()

        listSubject = []
        for subject in subjectsTitles:
            self.subjectName = subject["title"]
            self.subjectCamNb = subject["video"]
            self.subjectGrafNb = subject["graffitis"]
            listSubject.append(Subject())

        for subject in listSubject:
            self.topics.ids.contents.add_widget(subject)
        
        self.header.ids.content_box.add_widget(self.topics)
    
    def fire_popupAddGraffiti(self):
        self.addGraffitiPopup = AddGraffitiPopup()

        self.myWidget = MyWidget()

        paintGraffiti = self.addGraffitiPopup.ids.painter_widget
        self.painter = GraffitiDraw()
        paintGraffiti.add_widget(self.painter)
        paintGraffiti.add_widget(self.myWidget)

        print("paintgraffiti")
        print(self.myWidget)

        self.addGraffitiPopup.open()

        

            

if __name__ == "__main__":
    MyApp().run()