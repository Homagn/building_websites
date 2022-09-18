from pyodide import create_proxy, to_js
import js
import asyncio
from js import window
from js import Math
from js import THREE
from js import performance
from pyodide import to_js
from js import Object
from js import fetch
from js import requestAnimationFrame
import js, pyodide
from js import window


'''
THREE tutorials
https://r105.threejsfundamentals.org/threejs/lessons/threejs-load-obj.html
'''

mouse = THREE.Vector2.new();

renderer = THREE.WebGLRenderer.new({"antialias":True})
renderer.setSize(1000, 1000)
renderer.shadowMap.enabled = False
renderer.shadowMap.type = THREE.PCFSoftShadowMap
renderer.shadowMap.needsUpdate = True

document.body.appendChild( renderer.domElement )
loaderAnim = document.getElementById('js-loader')

def onMouseMove(event):
  event.preventDefault();
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

#add the event listener
js.document.addEventListener('mousemove', pyodide.create_proxy(onMouseMove))




scene = THREE.Scene.new()



camera = THREE.PerspectiveCamera.new( 35, window.innerWidth / window.innerHeight, 1, 500 )
cameraRange = 3
camera.aspect = window.innerWidth / window.innerHeight
camera.updateProjectionMatrix()
renderer.setSize( window.innerWidth, window.innerHeight )



#setcolor = "#000000" #black
setcolor = "white" #white

scene.background = THREE.Color.new(setcolor)
scene.fog = THREE.Fog.new(setcolor, 2.5, 3.5); #foggy effect based on distance from camera










######################################
# gltf loading using python
model_location = 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1376484/stacy_lightweight.glb'
texture_location = 'https://s3-us-west-2.amazonaws.com/s.cdpn.io/1376484/stacy.jpg'

stacy_txt = THREE.TextureLoader.new().load(texture_location);
stacy_txt.flipY = False # we flip the texture so that its the right way up

perms = {"map":stacy_txt, "color":"white", "skinning":True}
perms = Object.fromEntries(to_js(perms))
stacy_mtl = THREE.MeshPhongMaterial.new(perms)



clock = THREE.Clock.new()
loaded_model =  THREE.Object3D.new()

_animations = None
_done = False

def child_func(c):
  #print("Mesh !")
  c.castShadow = True
  c.receiveShadow = True
  c.material = stacy_mtl


def gltf_func(gltf): #goes inside this function only once
  #print("In gltf function ")
  global _animations
  global _done
  fileAnimations = gltf.animations
  

  #scale the whole model
  gltf.scene.scale.set(0.5, 0.5, 0.5)
  #translate the whole model downwards
  gltf.scene.position.y = -0.5
  gltf.scene.traverse(create_proxy(child_func))

  #scene.add(gltf.scene)
  loaded_model.add(gltf.scene)
  _animations = gltf.animations
  _done = True





loader = THREE.GLTFLoader.new();
loader.load(model_location, create_proxy(gltf_func))

scene.add(loaded_model)





mixer = THREE.AnimationMixer.new(loaded_model);
#VERY IMPORTANT ! - Note that since loader.load is asynchronous, you will have to wait until it finishes and call gltf_func
#see the issue here - https://github.com/pyodide/pyodide/discussions/3120#discussioncomment-3672502
import asyncio
while not _done:
  await asyncio.sleep(0.001)
clip = THREE.AnimationClip.findByName(_animations, 'idle')


idle = mixer.clipAction(clip);
idle.play();
#scene.add(person)
######################################










camera.position.set(0, 0, cameraRange);
cameraValue = False;

ambientLight = THREE.AmbientLight.new(0xFFFFFF, 0.1);

light = THREE.SpotLight.new(0xFFFFFF, 3);
light.position.set(5, 5, 2);
light.castShadow = True;
light.shadow.mapSize.width = 10000;
light.shadow.mapSize.height = light.shadow.mapSize.width;
light.penumbra = 0.5;

lightBack = THREE.PointLight.new(0x0FFFFF, 1);
lightBack.position.set(0, -3, -1);

#scene.add(sceneGruop);
scene.add(light);
scene.add(lightBack);

rectSize = 2
intensity = 100
rectLight = THREE.RectAreaLight.new( 0x0FFFFF, intensity,  rectSize, rectSize )
rectLight.position.set( 0, 0, 1 )
rectLight.lookAt( 0, 0, 0 )
scene.add( rectLight )

rectLightHelper = THREE.RectAreaLightHelper.new( rectLight );
raycaster = THREE.Raycaster.new();
uSpeed = 0.1


camera.lookAt(scene.position)













def update()->None:
  loaded_model.rotation.y += 0.005;
  mixer.update(clock.getDelta())

  

while True:

  requestAnimationFrame(create_proxy(lambda _event: update()))

  renderer.render( scene, camera )
  
  
  await asyncio.sleep(0.02)