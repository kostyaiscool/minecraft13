class Map:
    def __init__(self):
        self.default_image = 'source/derevo.jpg'
        self.default_model = 'source/block.egg'
        self.create_branch()
        for x in range(10):
            for y in range(10, 20):
                for z in range(-5, -3):
                    self.create_block((x, y, z))

    def create_block(self, position):
        self.model = loader.loadModel(self.default_model)
        self.texture = loader.loadTexture(self.default_image)
        self.model.setTexture(self.texture)
        self.model.setPos(position)
        self.model.reparentTo(self.branch)

    def create_branch(self):
        self.branch = render.attachNewNode('map_branch')
