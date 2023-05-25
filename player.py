import sys

from direct.actor.Actor import Actor
from direct.gui.DirectButton import DirectButton
from direct.gui.DirectFrame import DirectFrame
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionTraverser, CollisionNode, BitMask32, CollisionHandlerQueue, CollisionBox, Vec3, \
    WindowProperties


class Player:
    keyMap = {
        "forward": False,
        "backward": False,
        "left": False,
        "right": False,
    }
    SPEED = 2
    GRAVITY = -0.04
    JUMP_FORCE = 0.5
    FRICTION = -0.12

    def __init__(self, position, blocks):
        self.player = Actor('source/ralph',
            {
                'walk': 'source/ralph_walk',
                'run': 'source/ralph_run'
            }
        )
        self.player.setTexture(loader.loadTexture('source/ralph.jpg'))
        self.player.reparentTo(render)
        self.player.setPos(position)
        self.player.setScale(0.2)

        self.blocks = blocks
        self.position = Vec3(position)
        self.acceleration = Vec3(0.0, 0.0, 0.0)
        self.velocity = Vec3(0.0, 0.0, 0.0)

        self.lastMouseX, self.lastMouseY = None, None
        self.rotateX, self.rotateY = 0, 0
        self.manualRecenterMouse = True
        self.is_jumping = False
        self.jump_count = 0
        self.mouseMagnitude = 10
        self.paused = False

        self.firstFace()
        self.collisionsCreate()
        self.events()
        self.hideCursor(True)
        self.pause_menu()

        taskMgr.add(self.move, "move")
        taskMgr.add(self.mouseTask, "mouseTask")

    def firstFace(self):
        base.disableMouse()
        base.camera.reparentTo(self.player)
        base.camera.setH(180)
        base.camera.setPos(0, 0, 3.5)

    def collisionsCreate(self):
        self.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerQueue()
        
        self.player_col = self.player.attachNewNode(CollisionNode("player_col"))
        self.player_col.node().addSolid(CollisionBox((-1, -1, 0.4), (1, 1, 5.5)))
        self.player_col.setCollideMask(BitMask32.bit(0))
        self.player_col.setTag("type", "player")
        # self.player_col.show()

        self.cTrav.addCollider(self.player_col, self.cHandler)

        for block in self.blocks:
            cNode = CollisionNode("block_col")
            cNode.addSolid(CollisionBox((-0.5, -0.5, -0.5), (0.5, 0.5, 0.5)))
            cNode.setFromCollideMask(BitMask32.bit(1))
            cNodePath = block.attachNewNode(cNode)
            cNode.setTag("type", "block")
            # cNodePath.show()
            self.cTrav.addCollider(cNodePath, self.cHandler)

    def updateKeyMap(self, controllName, state):
        self.keyMap[controllName] = state

    def events(self) -> None:
        base.accept("w", self.updateKeyMap, ['forward', True])
        base.accept("a", self.updateKeyMap, ['left', True])
        base.accept("s", self.updateKeyMap, ['backward', True])
        base.accept("d", self.updateKeyMap, ['right', True])
        base.accept("w-up", self.updateKeyMap, ['forward', False])
        base.accept("a-up", self.updateKeyMap, ['left', False])
        base.accept("s-up", self.updateKeyMap, ['backward', False])
        base.accept("d-up", self.updateKeyMap, ['right', False])
        base.accept('space', self.jump)
        base.accept('escape', self.pause)

    def jump(self):
        self.is_jumping = True
        self.velocity.z = self.JUMP_FORCE
        self.jump_count += 1
        if self.jump_count > 1:
            # self.jump_count = 0
            self.is_jumping = False

    def differenceAngle(self, angle):
        if 0 <= angle < 20 or 335 <= angle < 360:
            return 0, -1
        elif 20 <= angle < 65:
            return 1, -1
        elif 65 <= angle < 110:
            return 1, 0
        elif 110 <= angle < 155:
            return 1, 1
        elif 155 <= angle < 200:
            return 0, 1
        elif 200 <= angle < 245:
            return -1, 1
        elif 245 <= angle < 290:
            return -1, 0
        elif 290 <= angle < 335:
            return -1, -1

    def move(self, task):
        dt = globalClock.getDt()

        self.acceleration = Vec3(0, 0, self.GRAVITY)
        # self.acceleration = Vec3(0, 0, 0)

        if self.keyMap['forward']:
            dif_x, dif_y = self.differenceAngle(self.player.getH() % 360)
            self.acceleration.x = self.SPEED * dt * dif_x
            self.acceleration.y = self.SPEED * dt * dif_y
        if self.keyMap['backward']:
            dif_x, dif_y = self.differenceAngle((self.player.getH() + 180) % 360)
            self.acceleration.x = self.SPEED * dt * dif_x
            self.acceleration.y = self.SPEED * dt * dif_y
        if self.keyMap['left']:
            dif_x, dif_y = self.differenceAngle((self.player.getH() + 90) % 360)
            self.acceleration.x = self.SPEED * dt * dif_x
            self.acceleration.y = self.SPEED * dt * dif_y
        if self.keyMap['right']:
            dif_x, dif_y = self.differenceAngle((self.player.getH() + 270) % 360)
            self.acceleration.x = self.SPEED * dt * dif_x
            self.acceleration.y = self.SPEED * dt * dif_y

        self.acceleration.x += self.velocity.x * self.FRICTION
        self.acceleration.y += self.velocity.y * self.FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + (self.acceleration * 0.5)

        self.cTrav.traverse(render)

        for entry in self.cHandler.getEntries():
            if entry.getFromNodePath().getNetTag("type") == "player":
                inp = entry.getFromNodePath().getPos(render)
                if not self.is_jumping:
                    self.position.z = inp.z
                else:
                    self.is_jumping = False

        self.player.setPos(self.position)

        return task.cont

    def mouseTask(self, task):
        mw = base.mouseWatcherNode

        hasMouse = mw.hasMouse()
        if hasMouse:
            # get the window manager's idea of the mouse position
            x, y = mw.getMouseX(), mw.getMouseY()

            if self.lastMouseX is not None:
                # get the delta
                if self.manualRecenterMouse:
                    # when recentering, the position IS the delta
                    # since the center is reported as 0, 0
                    dx, dy = x, y
                else:
                    dx, dy = x - self.lastMouseX, y - self.lastMouseY
            else:
                # no data to compare with yet
                dx, dy = 0, 0

            self.lastMouseX, self.lastMouseY = x, y

        else:
            x, y, dx, dy = 0, 0, 0, 0

        if self.manualRecenterMouse:
            # move mouse back to center
            self.recenterMouse()
            self.lastMouseX, self.lastMouseY = 0, 0

        self.rotateX += dx * 10 * self.mouseMagnitude
        self.rotateY += dy * 10 * self.mouseMagnitude

        self.player.setH(-self.rotateX)
        self.player.setP(-self.rotateY)

        return task.cont

    def hideCursor(self, mouseFlag):
        """Hide the mouse"""
        wp = WindowProperties()
        wp.setCursorHidden(mouseFlag)
        base.win.requestProperties(wp)

    def recenterMouse(self):
        base.win.movePointer(
            0,
            int(base.win.getProperties().getXSize() / 2),
            int(base.win.getProperties().getYSize() / 2)
        )

    def pause_menu(self):
        self.menu_panel = DirectFrame(frameColor=(0, 0, 0, 0.5), frameSize=(-0.5, 0.5, -0.5, 0.5))
        self.menu_button1 = DirectButton(text='Exit', scale=0.1, command=sys.exit, parent=self.menu_panel)
        self.menu_button1.setPos(0, 0, -0.4)
        self.menu_button2 = DirectButton(text='Continue', scale=0.1, command=self.continue_game, parent=self.menu_panel)
        self.menu_button2.setPos(0, 0, -0.2)
        # self.menu_button3 = DirectButton(text = 'Start new game', scale = 0.1, command = self.new_game, parent = self.menu_panel)
        # self.menu_button3.setPos(0, 0, 0)
        self.menu_panel.hide()

    def pause(self):
        self.manualRecenterMouse = False
        self.menu_panel.show()
        self.hideCursor(False)
        taskMgr.remove('move')
        taskMgr.remove('mouseTask')
        # taskMgr.remove('mouse_dir_get')

    def continue_game(self):
        # taskMgr.add(self.mouseTask, 'mouse_dir_get')
        self.manualRecenterMouse = True
        self.paused = False
        self.menu_panel.hide()
        self.hideCursor(True)
        taskMgr.add(self.move, "move")
        taskMgr.add(self.mouseTask, "mouseTask")
