import os
import random
import time
from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivymd.uix.button import MDIconButton
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.config import Config
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
import filechooser
# import filechooser_tk

play_icon = '/Users/mcwilan/Library/Mobile Documents/com~apple~CloudDocs/pro4/McEdit/Textures/play_icon.png'
stop_icon = '/Users/mcwilan/Library/Mobile Documents/com~apple~CloudDocs/pro4/McEdit/Textures/pause_icon.png'
volume_icon = '/Users/mcwilan/Library/Mobile Documents/com~apple~CloudDocs/pro4/McEdit/Textures/volume_icon.png'
mute_icon = '/Users/mcwilan/Library/Mobile Documents/com~apple~CloudDocs/pro4/McEdit/Textures/mute_icon.png'



Config.set('graphics', 'resizable', True)

window_size_x = 800
window_size_y = 600

#   ############################ Main App ############################
class McEdit(MDApp):
    def build(self):
        # [r, g, b, a], a ~ alpha channel value(AKA color intensity)
        layout = MDRelativeLayout(md_bg_color=[230 / 255, 0 / 255, 0 / 255, 0.5])  # Tlo aplikacji

        # self.music_dir = 'Music'
        # self.music_files = os.listdir(self.music_dir)

        self.sample_dir = '/Users/mcwilan/Library/Mobile Documents/com~apple~CloudDocs/pro4/McEdit/Samples'
        self.sample_files = os.listdir(self.sample_dir)

        # self.music_list = [x for x in self.music_files if x.endswith('mp3')]
        # self.music_count = len(self.music_list)

        self.sample_list = [x for x in self.sample_files if x.endswith('mp3')]
        self.sample_count = len(self.sample_list)

        self.openButton = Button(text='Open File', pos_hint={'center_x': 0.45, 'center_y': 0.95}, size_hint=(0.1, 0.05),
                                 on_press=self.open_file)
        self.saveButton = Button(text='Save File', pos_hint={'center_x': 0.55, 'center_y': 0.95}, size_hint=(0.1, 0.05),
                                 on_press=self.save_file)
        self.audioLabel = Label(pos_hint={'center_x': 0.12, 'center_y': 0.05},
                                size_hint=(1, 1),
                                font_size=30)
        self.playButton = MDIconButton(pos_hint={'center_x': 0.45, 'center_y': 0.1},
                                       icon=play_icon,
                                       on_press=self.play_audio)
        self.pauseButton = MDIconButton(pos_hint={'center_x': 0.55, 'center_y': 0.1},
                                        icon=stop_icon,
                                        on_press=self.stop_audio,
                                        disabled=True)
        self.muteButton = MDIconButton(pos_hint={'center_x': 0.79, 'center_y': 0.05},
                                       icon=volume_icon, user_font_size=1,
                                       on_press=self.mute_audio)
        # self.unmuteButton = MDIconButton(pos_hint={'center_x': 0.8, 'center_y': 0.05},
        #                                icon=mute_icon, user_font_size=1,
        #                                on_press=self.unmute_audio)
        self.progressbar = ProgressBar(value=0, max=100, pos_hint={'center_x': 0.5, 'center_y': 0.05},
                                       size_hint={0.4, 0.5})
        self.currentTime = Label(text='00:00', pos_hint={'center_x': 0.26, 'center_y': 0.05},
                                 size_hint=(1, 1),
                                 font_size=24,
                                 color=(0 / 255, 0 / 255, 255 / 255, 0.5))
        self.totalTime = Label(text='00:00', pos_hint={'center_x': 0.74, 'center_y': 0.05},
                               size_hint=(1, 1),
                               font_size=24,
                               color=(0 / 255, 0 / 255, 255 / 255, 1))
        self.volumeSlider = Slider(min=0, max=1, value=0.5, orientation='horizontal',
                                   pos_hint={'center_x': 0.90, 'center_y': 0.05},
                                   size_hint=(0.2, 0.2), cursor_size=(35, 35),
                                   value_track=True,
                                   value_track_color=[1, 1, 1, 0.75])


        Clock.schedule_once(self.play_audio)


        # Przyciski, icony, suwaki itd:
        layout.add_widget(self.openButton)
        layout.add_widget(self.saveButton)
        layout.add_widget(self.audioLabel)
        layout.add_widget(self.playButton)
        layout.add_widget(self.pauseButton)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.currentTime)
        layout.add_widget(self.totalTime)
        layout.add_widget(self.volumeSlider)
        layout.add_widget(self.muteButton)
        # layout.add_widget(self.unmuteButton)

        # Zwiazanie suwaka z glosnoscia sampla:
        def volume(instance, value):
            self.sample.volume = value
        self.volumeSlider.bind(value = volume)


        return layout

    def play_audio(self, obj):  # Odtwarzacz muzyki i sampli
        # self.music_title = self.music_list[random.randrage(0, self.music_count)]
        # self.music = SoundLoader.load('{}/{}'.format(self.music_dir, self.music_title))
        # self.music.play()

        self.sample_title = self.sample_list[random.randrange(0, self.sample_count)]
        self.sample = SoundLoader.load('{}/{}'.format(self.sample_dir, self.sample_title))
        self.audioLabel.text = self.sample_title[0:-4] # Wypisz nazwe bez .mp3
        self.playButton.disabled = True
        self.pauseButton.disabled = False
        self.progressbar_event = Clock.schedule_interval(self.udpate_progressbar, self.sample.length / 60)
        self.set_time_event = Clock.schedule_interval(self.set_time, 1)

        self.sample.play()

    def stop_audio(self, obj):
        # self.music.stop()
        self.playButton.disabled = False
        self.pauseButton.disabled = True
        self.progressbar_event.cancel()
        self.set_time_event.cancel()
        self.progressbar.value = 0
        self.currentTime.text = '00:00'
        self.totalTime.text = '00:00'

        self.sample.stop()

    def mute_audio(self, value):
        self.sample.volume = 0
        self.muteButton.icon = mute_icon
        self.volumeSlider.value = 0
        self.muteButton.on_press == False
        if self.muteButton.on_press == True:
            self.muteButton.icon = volume_icon


    # def unmute_audio(self, value):
    #     self.sample.volume = 1
    #     self.unmuteButton.icon = volume_icon

    def udpate_progressbar(self, value):
        if self.progressbar.value < 100:
            self.progressbar.value += 1

    def set_time(self, t):
        current_time = time.strftime('%M:%S', time.gmtime(self.progressbar.value))
        total_time = time.strftime('%M:%S', time.gmtime(self.sample.length))
        print(current_time)
        self.currentTime.text = current_time
        self.totalTime.text = total_time

    def open_file(self, obj):
        self.saveButton.disabled = True
        self.openButton.disabled = False

        # return filechooser_tk.window()

    def save_file(self, obj):
        self.saveButton.disabled = False
        self.openButton.disabled = True

if __name__ == '__main__':
    McEdit().run()
