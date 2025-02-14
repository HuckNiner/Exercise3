from pubsub import pub
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, Texture, CardMaker
from view_object import ViewObject

class PlayerView:
    def __init__(self, game_logic):
        self.game_logic = game_logic
        self.view_objects = {}
        self.lights_on = True

        # Ambient Light
        self.ambient_light = AmbientLight("ambient")
        self.ambient_light.setColor((0.5, 0.5, 0.5, 1))
        self.ambient_np = base.render.attachNewNode(self.ambient_light)
        base.render.setLight(self.ambient_np)

        # Directional Light
        self.directional_light = DirectionalLight("directional")
        self.directional_light.setColor((0.8, 0.8, 0.8, 1))
        self.directional_np = base.render.attachNewNode(self.directional_light)
        self.directional_np.setHpr(0, -60, 0)
        base.render.setLight(self.directional_np)

        # Create background
        self.create_background()

        pub.subscribe(self.toggle_light, 'input')
        pub.subscribe(self.new_game_object, 'create')

    def create_background(self):
        # Create a large background card (large enough to be visible behind the scene)
        card_maker = CardMaker("background_card")
        card_maker.setFrame(50, 50, 50, 50)  # Size of the background
        background_card = base.render.attachNewNode(card_maker.generate())

        # Load texture for the background
        background_texture = base.loader.loadTexture("textures/sky.png")  # Replace with actual texture path
        background_card.setTexture(background_texture)

        # Position the background behind the scene
        background_card.setPos(0, -20, 0)  # Place it far enough back in the scene

        # Ensure it's rendered last, behind all objects
        background_card.setBin("background", 0)
        background_card.setDepthWrite(False)  # Disable depth writing to avoid clipping issues

    def new_game_object(self, game_object):
        if game_object.kind == "player":
            return

        view_object = ViewObject(game_object)
        self.view_objects[game_object.id] = view_object

    def toggle_light(self, events=None):
        if 'toggleLight' in events:
            self.lights_on = not self.lights_on
            if self.lights_on:
                base.render.setLight(self.ambient_np)
                base.render.setLight(self.directional_np)
            else:
                base.render.clearLight(self.ambient_np)
                base.render.clearLight(self.directional_np)

    def tick(self):
        for key in self.view_objects:
            self.view_objects[key].tick()