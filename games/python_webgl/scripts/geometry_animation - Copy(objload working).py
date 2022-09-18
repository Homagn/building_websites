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
#from js import loadobject
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

import js, pyodide
def onMouseMove(event):
  event.preventDefault();
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
js.document.addEventListener('mousemove', pyodide.create_proxy(onMouseMove))

camera = THREE.PerspectiveCamera.new( 35, window.innerWidth / window.innerHeight, 1, 500 )
scene = THREE.Scene.new()
cameraRange = 3

camera.aspect = window.innerWidth / window.innerHeight
camera.updateProjectionMatrix()
renderer.setSize( window.innerWidth, window.innerHeight )

setcolor = "#000000"

scene.background = THREE.Color.new(setcolor)
scene.fog = THREE.Fog.new(setcolor, 2.5, 3.5);

sceneGruop = THREE.Object3D.new();
particularGruop = THREE.Object3D.new();

def mathRandom(num = 1):
  setNumber = - Math.random() * num + Math.random() * num
  return setNumber

particularGruop =  THREE.Object3D.new();
modularGruop =  THREE.Object3D.new();


######################################
'''
#Adding some of my own stuff
'''

# example using externally defined javascript functions
result_square = await js.square(4) #must use await
print("using external js function ",result_square)

#load chair obj file from local storage
response = await fetch('assets/chair.obj');  
text = await response.text();
#load chair mtl file from local storage
response_mat = await fetch('assets/chair.mtl');  
text_mat = await response_mat.text();



chair_object = THREE.Object3D.new();



objloader = THREE.OBJLoader2.new();


mtlloader = THREE.MTLLoader.new();
chair_mat = mtlloader.parse(text_mat);
objloader.setMaterials(chair_mat)


def onload(obj):
  chair_object.add(obj)


chair = objloader.parse(text);



print("chair mesh ",chair)
print("load object parts ",chair_mat)



chair.scale.set(0.1,0.1,0.1);
chair_object.add(chair);


  
######################################



perms = {"flatShading":True, "color":"#111111", "transparent":False, "opacity":1, "wireframe":False}
perms = Object.fromEntries(to_js(perms))

particle_perms = {"color":"#FFFFFF", "side":THREE.DoubleSide}
particle_perms = Object.fromEntries(to_js(particle_perms))

def create_cubes(mathRandom, modularGruop):
  i = 0
  while i < 30:
    geometry = THREE.IcosahedronGeometry.new();
    material = THREE.MeshStandardMaterial.new(perms);
    cube = THREE.Mesh.new(geometry, material);
    cube.speedRotation = Math.random() * 0.1;
    cube.positionX = mathRandom();
    cube.positionY = mathRandom();
    cube.positionZ = mathRandom();
    cube.castShadow = True;
    cube.receiveShadow = True;
    newScaleValue = mathRandom(0.3);
    cube.scale.set(newScaleValue,newScaleValue,newScaleValue);
    cube.rotation.x = mathRandom(180 * Math.PI / 180);
    cube.rotation.y = mathRandom(180 * Math.PI / 180);
    cube.rotation.z = mathRandom(180 * Math.PI / 180);
    cube.position.set(cube.positionX, cube.positionY, cube.positionZ);
    modularGruop.add(cube);
    i += 1

create_cubes(mathRandom, modularGruop)


def generateParticle(mathRandom, particularGruop, num, amp = 2):
  gmaterial = THREE.MeshPhysicalMaterial.new(particle_perms);
  gparticular = THREE.CircleGeometry.new(0.2,5);
  i = 0
  while i < num:
    pscale = 0.001+Math.abs(mathRandom(0.03));
    particular = THREE.Mesh.new(gparticular, gmaterial);
    particular.position.set(mathRandom(amp),mathRandom(amp),mathRandom(amp));
    particular.rotation.set(mathRandom(),mathRandom(),mathRandom());
    particular.scale.set(pscale,pscale,pscale);
    particular.speedValue = mathRandom(1);
    particularGruop.add(particular);
    i += 1

generateParticle(mathRandom, particularGruop, 200, 2)

sceneGruop.add(particularGruop);
scene.add(modularGruop);
scene.add(sceneGruop);

scene.add(chair_object);





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

scene.add(sceneGruop);
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

time = 0.0003;
camera.lookAt(scene.position)

while True:
  time = performance.now() * 0.0003;
  i = 0
  while i < particularGruop.children.length:
    newObject = particularGruop.children[i];
    newObject.rotation.x += newObject.speedValue/10;
    newObject.rotation.y += newObject.speedValue/10;
    newObject.rotation.z += newObject.speedValue/10;
    i += 1

  i = 0
  while i < modularGruop.children.length:
    newCubes = modularGruop.children[i];
    newCubes.rotation.x += 0.008;
    newCubes.rotation.y += 0.005;
    newCubes.rotation.z += 0.003;

    newCubes.position.x = Math.sin(time * newCubes.positionZ) * newCubes.positionY;
    newCubes.position.y = Math.cos(time * newCubes.positionX) * newCubes.positionZ;
    newCubes.position.z = Math.sin(time * newCubes.positionY) * newCubes.positionX;
    i += 1

  particularGruop.rotation.y += 0.005;

  modularGruop.rotation.y -= ((mouse.x * 4) + modularGruop.rotation.y) * uSpeed;
  modularGruop.rotation.x -= ((-mouse.y * 4) + modularGruop.rotation.x) * uSpeed;

  renderer.render( scene, camera )
  await asyncio.sleep(0.02)