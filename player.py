from direct.actor.Actor import Actor
import sys

class Player:
    def __init__(self, position):
        self.player = Actor('source/ralph',
            {
                'walk': 'source/ralph_walk',
                'run': 'source/ralph_run'
            }
        )
        self.player.setTexture(loader.loadTexture('source/ralph.jpg'))
        self.player.reparentTo(render)
        self.player.setPos(position)
        self.player.setScale(0.3)
        self.player.setH(45)
        self.eventHandler()
        self.firstFace()

        taskMgr.add(self.gravity, 'gravity')

        taskMgr.add(self.checkZ, 'checkZ')
    def firstFace(self):
        # base.disableMouse()
        base.camera.reparentTo(self.player)
        base.camera.setZ(1.5)
        base.camera.setH(135)

    def eventHandler(self):
        base.accept('arrow_left', self.left)

    def left(self):
        self.player.setX(self.player.getX() - 1)

    def gravity(self, task):
        self.player.setZ(self.player.getZ() - 1)

        return task.cont

    def checkZ(self, task):
        if self.player.getZ() < -100:
           sys.exit()

        return task.cont