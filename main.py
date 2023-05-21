from direct.showbase.ShowBase import ShowBase
from map import Map
from panda3d.core import loadPrcFileData
# game = ShowBase()

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
        self.land = Map()


game = MyGame()

game.run()

