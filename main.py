from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
from perlin_noise import PerlinNoise
from numpy import floor
from ursina.shaders import lit_with_shadows_shader

window.vsync = False

app = Ursina()
window.borderless = False
window.title = "3craft"
window.icon = "assets/icns/app.icns"

noise = PerlinNoise(octaves=4, seed=random.randint(1000, 9999))
amp = 24
freq = 128
terrainWidth = 50
terrainDepth = 1

FPC = FirstPersonController()

window.fps_counter.enabled = True
window.exit_button.visible = True
window.vsync = False

punch = Audio('assets/music/punch', autoplay=False)
venus = Audio('assets/music/venus', autoplay=True)
moog = Audio('assets/music/moog', autoplay=False)

blocks = [
    load_texture('assets/textures/grass.png'), # 0
    load_texture('assets/textures/grass.png'), # 1
    load_texture('assets/textures/stone.png'), # 2
    load_texture('assets/textures/gold.png'),  # 3
    load_texture('assets/textures/lava.png'),  # 4
    load_texture('assets/textures/iron.png'),  # 5
    load_texture('assets/textures/log.png'), # 6
    load_texture('assets/textures/leaves.png'), # 7
    load_texture('assets/textures/planks.png'), # 8
    load_texture('assets/textures/planks.png') # 9
]

block_id = 1

def input(key):
    global block_id, hand
    if key.isdigit():
        block_id = int(key)
        if block_id >= len(blocks):
            block_id = len(blocks) - 1
        hand.texture = blocks[block_id]
    elif key == 'escape':
        mouse.locked = not mouse.locked
    
        
#hotbar = Entity(
  #  parent=camera.ui,
   # model='',
   # texture='assets/hotbar.png',
   # scale= -0.1,
  #  rotation=Vec3(0, 0, 0),
   # position=Vec2(0, -0.4175)
#)

sky = Entity(
    parent=scene,
    model='sphere',
    texture=load_texture('assets/textures/sky.jpg'),
    scale=10000,
    double_sided=True
)

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/objects/block',
            #texture=load_texture('assets/arm_texture.png'),
            scale=0.2,
            rotation=Vec3(-10, -10, 10),
            position=Vec2(0.7, -0.6),
            shader=lit_with_shadows_shader
            )

def update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.position = Vec2(0.2, -0.3)
        hand.position = Vec2(0.4, -0.5)
    else:
        hand.position = Vec2(0.6, -0.6)

    if held_keys['m']:
        moog.play()
        venus.pause()

    if player.position.y < -8:
        player.position = Vec3(0,20,0)
        
        

class Voxel(Button): #Grass
    def __init__(self, position=(0, 0, 0), texture='assets/textures/grass.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/objects/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5,
            highlight_color=color.gray,
            shader=lit_with_shadows_shader
        )
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':

                destroy(self)
                punch.play()
            elif key == 'right mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])


for z in range(25):
    for x in range(25):
        y = 0 #+ noise([x/20, z/20])
        voxel = Voxel(position=(x, 0, z))
        

class Voxel(Button): #Bedrock
    def __init__(self, position=(0, 0, 0), texture='assets/textures/bedrock.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/objects/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5,
            highlight_color=color.gray,
            shader=lit_with_shadows_shader
            )

for z in range(25):
    for x in range(25):
        y = 0.25 # + noise([x/20, z/20])
        voxel = Voxel(position=(x, -2, z))
        

class Voxel(Button): #Stone
    def __init__(self, position=(0, 0, 0), texture='assets/textures/stone.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/objects/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1.0)),
            scale=0.5,
            highlight_color=color.gray,
            shader=lit_with_shadows_shader
        )
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
                punch.play()
            elif key == 'right mouse down':
                Voxel(position=self.position + mouse.normal, texture=blocks[block_id])


for z in range(25):
    for x in range(25):
        y = 0.25 # + noise([x/20, z/20])
        voxel = Voxel(position=(x, -1, z))


player = FirstPersonController()
hand = Hand()
app.run()
