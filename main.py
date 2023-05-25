import sys

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.showbase.ShowBase import ShowBase
from map import Map
from player import Player
from panda3d.core import loadPrcFileData

configVars = '''
win-size 2300 1000
show-frame-rate-meter 1
'''
loadPrcFileData('', configVars)


class MyGame(ShowBase):
    def __init__(self):
        super().__init__(self)
        self.set_background_color((0.1, 0.191, 0.3, 0.5))
        # self.model1 = loader.loadModel('models/environment')
        # self.model1.reparentTo(render)
        base.camLens.setFov(100)

        self.menu_panel = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-0.5, 0.5, -0.5, 0.5))
        self.menu_button1 = DirectButton(text='Exit', scale=0.1, command=sys.exit, parent=self.menu_panel)
        self.menu_button1.setPos(0, 0, -0.4)
        self.menu_button2 = DirectButton(text='Start game', scale=0.1, command=self.start_game, parent=self.menu_panel)
        self.menu_button2.setPos(0, 0, -0.2)
        self.menu_button3 = DirectButton(text='Settings', scale=0.1, command=self.settings, parent=self.menu_panel)
        self.menu_button3.setPos(0, 0, 0)

    def start_game(self):
        self.menu_panel.hide()
        self.land = Map()
        self.player = Player((5, 15, -3), self.land.blocks)

    def settings(self):
        self.menu_panel.hide()
        self.settings_panel = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-0.5, 0.5, -0.5, 0.5))
        self.settings_button2 = DirectButton(text='Main menu', scale=0.1, command=self.exit_settings,
                                             parent=self.settings_panel)
        self.settings_button2.setPos(0, 0, -0.4)

    def exit_settings(self):
        self.settings_panel.hide()
        self.menu_panel.show()


game = MyGame()

game.run()

