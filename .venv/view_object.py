from pubsub import pub

class ViewObject:
    def __init__(self, game_object):
        self.game_object = game_object
        self.cube = base.loader.loadModel("models/cube")
        self.cube.reparentTo(base.render)

        self.cube.setTag('selectable', '')
        self.cube.setPythonTag("owner", self)

        self.cube.setPos(*game_object.position)
        self.cube.setScale(1, 1, 1)

        # Load multiple textures
        self.textures = [
            base.loader.loadTexture("textures/crate.png"),
            base.loader.loadTexture("textures/metal.png"),
            base.loader.loadTexture("textures/chrome.png"),
        ]
        self.current_texture_index = 0
        self.cube.setTexture(self.textures[self.current_texture_index])

        self.toggle_texture_pressed = False
        self.is_selected = False

        pub.subscribe(self.toggle_texture, 'input')

    def deleted(self):
        self.cube.setPythonTag("owner", None)

    def selected(self):
        self.is_selected = True

    def toggle_texture(self, events=None):
        if 'toggleTexture' in events:
            self.toggle_texture_pressed = True

    def tick(self):
        h = self.game_object.z_rotation
        p = self.game_object.x_rotation
        r = self.game_object.y_rotation
        self.cube.setHpr(h, p, r)

        if self.toggle_texture_pressed and self.is_selected:
            # Cycle to the next texture
            self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)
            self.cube.setTexture(self.textures[self.current_texture_index])

            self.toggle_texture_pressed = False
