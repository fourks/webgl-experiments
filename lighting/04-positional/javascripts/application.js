var gl = null;     // WebGL context
var prg = null;    // The program (shaders)
var c_width = 0;   // Variable to store the width of the canvas
var c_height = 0;  // Variable to store the height of the canvas

var camera = null;
var interactor = null;
var transforms = null;

/**
* Entry point. This function is invoked when the page is loaded
*/

function initialise()
{
  var app = new WebGLApp("glcanvas")
  app.configureGLHook = configure;
  app.loadSceneHook   = load;
  app.drawSceneHook   = draw;
  app.run();
}

/**
*  Configures the gl context
*/

function configure()
{    
  gl.clearColor(0.3, 0.3, 0.3, 1.0);
  gl.clearDepth(100.0);
  gl.enable(gl.DEPTH_TEST);
  gl.depthFunc(gl.LEQUAL);

  //Creates and sets up the camera location
  camera = new Camera(CAMERA_ORBIT_TYPE);
  camera.goHome([0, 0, 100]);
  camera.hookRenderer = draw;

  //Creates and sets up the mouse and keyboard interactor
  var canvas = document.getElementById('glcanvas');
  interactor = new CameraInteractor(camera, canvas);
  
  //Scene transforms
  transforms = new SceneTransforms(camera);
  transforms.init();
  
  //Intialise light values
  initLights();
}

/**
* Defines the initial values for the uniforms related to lighting
*/
function initLights()
{
  // Light uniforms
  gl.uniform3fv(prg.uLightPosition,     [15.0, 15.0, 15.0]); 
  gl.uniform4fv(prg.uLightAmbient,      [1.0, 1.0, 1.0, 1.0]);
  gl.uniform4fv(prg.uLightDiffuse,      [1.0, 1.0, 1.0, 1.0]);
  gl.uniform4fv(prg.uLightSpecular,     [1.0, 1.0, 1.0, 1.0]);

  // Object uniforms
  gl.uniform1f(prg.uShininess, 200.0);
  gl.uniform4fv(prg.uMaterialAmbient, 	[0.1, 0.1, 0.1, 1.0]);
  gl.uniform4fv(prg.uMaterialDiffuse, 	[0.8, 0.0, 0.8, 1.0]);
  gl.uniform4fv(prg.uMaterialSpecular, 	[1.0, 1.0, 1.0, 1.0]);
}

/**
* Loads the scene
*/
function load()
{
  Scene.addObject(Cube);
  Scene.addObject(SmallSphere);
}

/**
* invoked on every rendering cycle
*/
function draw()
{    
  gl.viewport(0, 0, c_width, c_height);
  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
  
  transforms.updatePerspective();

  try
  {
    for (var i = 0; i < Scene.objects.length; i++)
    {
      var object = Scene.objects[i];
      
			transforms.calculateModelView();
      transforms.push();
        
      if (object.alias == 'smallsphere')
      {
        var lightPos = gl.getUniform(prg, prg.uLightPosition);
        mat4.translate(transforms.mvMatrix, lightPos);
      }
      
      transforms.setMatrixUniforms();
      transforms.pop();

      if (object.ambient)
      {
        gl.uniform4fv(prg.uMaterialDiffuse, object.ambient);
      }      
      if (object.diffuse)
      {
        gl.uniform4fv(prg.uMaterialDiffuse, object.diffuse);
      }
      if (object.specular)
      {
        gl.uniform4fv(prg.uMaterialSpecular, object.specular); 
      }

      //Setting vertex shader attributes
      gl.bindBuffer(gl.ARRAY_BUFFER, object.vbo);
      gl.vertexAttribPointer(prg.aVertexPosition, 3, gl.FLOAT, false, 0, 0);
      gl.enableVertexAttribArray(prg.aVertexPosition);

      gl.bindBuffer(gl.ARRAY_BUFFER, object.nbo);
      gl.vertexAttribPointer(prg.aVertexNormal, 3, gl.FLOAT, false, 0, 0);
      gl.enableVertexAttribArray(prg.aVertexNormal);

      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, object.ibo);

      gl.drawElements(gl.TRIANGLES, object.indices.length, gl.UNSIGNED_SHORT, 0);

      gl.bindBuffer(gl.ARRAY_BUFFER, null);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null);
    }
  }
  catch(err)
  {
    console.log(err);
    console.error(err.description);
  }
}