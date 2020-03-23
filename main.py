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
    pass

class InterventionsSelectionEmpty(Widget):
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


class MyWidget(Widget):

    def export_scaled_png(self, filename, image_scale=1):
        re_size = (self.width * image_scale, self.height * image_scale)

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
        print(color)
        color = (.349, .5686, .392)
        with self.canvas:
            Color(*color, mode='hsv') # (numéro couleur rgb) / 255
            d = 5.
            print("X: " + str(touch.spos[0]) + " - Y: " + str(touch.spos[1]))
            if 0.19 < touch.spos[0] < 0.96 and 0.05 < touch.spos[1] < 0.83:
                Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
                #try:
                touch.ud['line'] = Line(points=(touch.x, touch.y),width=4)
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

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class MyApp(App): # <- Main Class
    subjectsTitles = ListProperty()
    subjectTitle = StringProperty("")
    
    currentIntervention = StringProperty("")


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
        self.mywgtRef = MyWidget()
        self.interventionsSelection = InterventionsSelection()

        interventionView = StringProperty("")
        subjectName = StringProperty('test')
        subjectCamNb = StringProperty('test1')
        subjectGrafNb = StringProperty('test2')
        interventionLabel = StringProperty("test3")

        #screens declaration
        self.topicsSelectionScreen = TopicsSelectionScreen(name ="screen_TopicsSelection")
        self.topicDisplayScreen = TopicDisplayScreen(name="screen_TopicDisplay")
        self.interventionDisplayedScreen = InterventionDisplayedScreen(name="screen_InterventionDisplayed")
        addGraffitiScreen = AddGraffitiScreen(name="screen_AddGraffiti")
        addVideoScreen = AddVideoScreen(name="screen_AddVideo")

        #topics selection screen
        header = Header()
        self.topicsSelectionScreen.ids.top_box.add_widget(header)

        topics = Topics()
        header.ids.content_box.add_widget(topics)

        #takes info from mongodb
        subjectsTitles = collection.find({})

        listSubject = []
        for subject in subjectsTitles:
            self.subjectName = subject["title"]
            self.subjectCamNb = subject["video"]
            self.subjectGrafNb = subject["graffitis"]
            listSubject.append(Subject())

        for subject in listSubject:
            topics.ids.contents.add_widget(subject)
        
        #topic display screen
            #TODO: if len() == 0 then chibi mec else ce qui est déjà fait
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
    
    
    def save_grafffiti_png(self):
        print("save graffiti png")
        try:
            Window.screenshot(name="Screenshot.png")
 
            #if platform == 'android':
                #Window.screenshot(name='/storage/emulated/0/Pictures/Screenshots/Screenshot.png')
            
        except:
            pass
    
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
                self.headerTopicName.ids.content_box.add_widget(InterventionsSelectionEmpty())
        
    

        except:
            print("exception")
            
     
    
    def printInterventionView(self):
        print(self.interventionView)

            

if __name__ == "__main__":
    MyApp().run()