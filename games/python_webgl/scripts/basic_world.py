from pyodide import create_proxy, to_js
from js import THREE, window, document, Array

import math

container = document.querySelector('#c')

class BasicWorld:
    def __init__(self, container):
       
        self.container = container
        
        self.renderer = self.setup_renderer()

        self.container.append(self.renderer.domElement)

        self.camera = self.setup_camera()

        self.scene = THREE.Scene.new()
        self.scene.add(self.setup_directional_light())
        self.scene.add(THREE.AmbientLight.new(0x101010))
        self.scene.add(self.setup_plane())
        self.scene.add(self.setup_box())

        self.setup_background_single()

        self.controls = self.setup_controls()

        window.addEventListener('resize',create_proxy(self.onWindowResize) , False)
        self.animate()

    def setup_renderer(self):
        renderer = THREE.WebGLRenderer.new(to_js({
            "antialias": True
        }))
        renderer.shadowMap.enabled = True
        renderer.shadowMap.type = THREE.PCFSoftShadowMap
        renderer.setSize(self.container.clientWidth, self.container.clientHeight)
        renderer.setPixelRatio(window.devicePixelRatio)
        return renderer

    def setup_camera(self):
        fov = 60
        aspect = self.container.clientWidth/self.container.clientHeight
        near = 1.0
        far = 10000.0
        camera = THREE.PerspectiveCamera.new(fov, aspect, near, far)
        camera.position.set(75,20,0)
        return camera

    def setup_directional_light(self):
        light = THREE.DirectionalLight.new(0xffffff,1.0)
        light.position.set(20,100,10)
        light.target.position.set(0,0,0)
        light.castShadow = True
        light.shadow.bias = -0.001
        light.shadow.mapSize.width = 2048
        light.shadow.mapSize.height = 2048
        light.shadow.camera.near = 0.1
        light.shadow.camera.far = 500.0
        light.shadow.camera.near = 0.5
        light.shadow.camera.far = 500.0
        light.shadow.camera.left = 100
        light.shadow.camera.right = -100
        light.shadow.camera.top = 100
        light.shadow.camera.bottom = -100
        return light

    def setup_plane(self):
        plane = THREE.Mesh.new(
                    THREE.PlaneGeometry.new(100, 100, 10, 10),
                    THREE.MeshStandardMaterial.new(to_js({
                        "color": 0xFFFFFF
                })))

        plane.castShadow = False
        plane.receiveShadow = True
        plane.rotation.x = -math.pi / 2
        return plane

    def setup_box(self):
        box = THREE.Mesh.new(
            THREE.BoxGeometry.new(8,8,8),
            THREE.MeshStandardMaterial.new(
                to_js(
                    {"color": "blue"}
                )
            )
        )
        box.position.set(0,10,0)
        box.castShadow = True
        box.receiveShadow = True

        return box

    def setup_background(self):
        loader = THREE.CubeTextureLoader.new()
        texture = loader.load(to_js([
            "./sky_image/skybox_front.png",
            "./sky_image/skybox_back.png",
            "./sky_image/skybox_up.png",
            "./sky_image/skybox_down.png",
            "./sky_image/skybox_right.png",
            "./sky_image/skybox_left.png"
        ]))
        self.scene.background = texture

    def setup_background_single(self):
        ft = THREE.TextureLoader.new().load("./sky_image/skybox_front.png")
        bk = THREE.TextureLoader.new().load("./sky_image/skybox_back.png")
        up = THREE.TextureLoader.new().load("./sky_image/skybox_up.png")
        dn = THREE.TextureLoader.new().load("./sky_image/skybox_down.png")
        rt = THREE.TextureLoader.new().load("./sky_image/skybox_right.png")
        lf = THREE.TextureLoader.new().load("./sky_image/skybox_left.png")

        textures = [ft, bk, up, dn, rt, lf]

        materials = Array.new()

        for i in textures:
            mat = THREE.MeshBasicMaterial.new()
            mat.map = i
            mat.side = THREE.BackSide
            materials.push(mat)

        skyboxGeo = THREE.BoxGeometry.new(10000, 10000, 10000)
        skybox = THREE.Mesh.new(skyboxGeo, materials)

        self.scene.add(skybox)
        

    def setup_controls(self):
        controls = THREE.OrbitControls.new(self.camera, self.renderer.domElement )
        controls.target.set(0,20,0)
        controls.update()
        return controls

    def onWindowResize(self,event):
        self.camera.aspect = self.container.clientWidth/self.container.clientHeight
        self.camera.updateProjectionMatrix()
        self.renderer.setSize(self.container.clientWidth, self.container.clientHeight)

    def animate(self,*args):
        window.requestAnimationFrame(create_proxy(self.animate) )
        self.controls.update()
        self.renderer.render( self.scene, self.camera )


app = BasicWorld(container)