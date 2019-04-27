import pygame
import sys
import os
import random
from flask import Flask, request

app = Flask(__name__)
pygame.init()

all_emotion = ["HAPPY", "SAD", "ANGRY", "SCARED"]

class Player(object):
    def __init__(self):
        self.isPlaying = False
        self.startPlay = False
        self.prefix = "CENG3410MusicFile/"
        self.current_emotion = "SAD"
        self.current_song = self.random_song()

    def random_song(self):
        if(self.current_emotion not in all_emotion):
            print("songs cannot be found")
            return None

        songs = os.listdir(os.path.join(self.prefix, self.current_emotion))
        return os.path.join(self.prefix, self.current_emotion, songs[random.randint(0, len(songs)-1)])

    def force_next_track(self, path):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.prefix+u"HAPPY/Maroon 5 - Sugar.wav")
        pygame.mixer.music.play()

    def toggle_pause(self):
        if(not self.startPlay):
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            self.startPlay = True
            self.isPlaying = True
            return "Start music"
        else:
            if not self.isPlaying:
                pygame.mixer.music.unpause()
                self.isPlaying = not self.isPlaying
                return "unpause music"
            else:
                pygame.mixer.music.pause()
                self.isPlaying = not self.isPlaying
                return "pause music"


    def next_track(self):
        song_name = self.random_song()
        pygame.mixer.music.load(song_name)
        pygame.mixer.music.play()
        self.startPlay = True
        self.isPlaying = True
        self.current_song = song_name
        return song_name

    def stop(self):
        self.startPlay = False
        self.isPlaying = False
        pygame.mixer.music.stop()

    def get_flags(self):
        s=u''
        s+=u'self.isPlaying {0} <br> '.format(self.isPlaying)
        s+=u'self.startPlay {0} <br> '.format(self.startPlay)
        s+=u'self.current_emotion {0} <br> '.format(self.current_emotion)
        s+=u'self.current_song {0} <br> '.format(self.current_song.decode(sys.stdout.encoding))
        return s

    def update_emotion(self, emotion):
        if(emotion.upper() not in all_emotion):
            return False
        else:
            self.current_emotion = emotion.upper()
            return True

    def list_dir(self):
        result = ''
        for emotion in all_emotion:
            result += '=============================={0}==============================<br>'.format(emotion.lower())
            result += '<br>'.join(os.listdir(os.path.join(self.prefix, emotion)))
            result += '<hr>'
        return result

player = Player()

@app.route("/toggle_play")
def toggle_pause():
    operation = player.toggle_pause()
    result = player.get_flags()
    result += '<hr>'
    result += operation
    return result

@app.route("/stop")
def stop():
    player.stop()
    result = player.get_flags()
    result += '<hr>'
    result += 'Stopped!'
    return result

@app.route("/next_track")
def next_track():
    song = player.next_track()
    result = player.get_flags()
    result += '<hr>'
    result += 'Next track!'
    return result

@app.route("/update_emotion")
def update_emotion():
    emotion = request.args.get('emotion')
    success = player.update_emotion(emotion)
    if(success):
        return "emotion update success: {0}".format(emotion)
    else:
        return "not success: {0} not found".format(emotion)

@app.route("/list_dir")
def list_dir():
    return player.list_dir()

@app.route("/get_flags")
def get_flags():
    return player.get_flags()

app.run("0.0.0.0", 8080)