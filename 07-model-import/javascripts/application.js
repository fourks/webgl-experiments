var gl = null;     // WebGL context
var prg = null;    // The program (shaders)
var c_width = 0;   // Variable to store the width of the canvas
var c_height = 0;  // Variable to store the height of the canvas

var camera = null;
var interactor = null;
var transforms = null;
var modelTexture = null;

var stats = null;


/**
* Entry point. This function is invoked when the page is loaded
*/

function initialise()
{
  createStats();
  	
  var app = new WebGLApp("glcanvas")
  app.configureGLHook = configure;
  app.loadSceneHook   = load;
  app.drawSceneHook   = draw;
  app.run();
}

function createStats()
{
  stats = new Stats();
  stats.setMode(1); // 0: fps, 1: ms

  // Align top-left
  stats.domElement.style.position = 'absolute';
  stats.domElement.style.left = '0px';
  stats.domElement.style.top = '0px';

  document.body.appendChild( stats.domElement );
}

/**
*  Configures the gl context
*/

function configure()
{    
  gl.clearColor(0.0, 0.0, 0.0, 1.0);
  gl.clearDepth(100.0);
  gl.enable(gl.DEPTH_TEST);
  gl.depthFunc(gl.LEQUAL);

  //Creates and sets up the camera location
  camera = new Camera(CAMERA_ORBIT_TYPE);
  camera.goHome([0, 1, 15]);

  //Creates and sets up the mouse and keyboard interactor
  var canvas = document.getElementById('glcanvas');
  interactor = new CameraInteractor(camera, canvas);
  
  //Scene transforms
  transforms = new SceneTransforms(camera);
  transforms.init();
  
  //Load textures
  initTextures();
}

function initTextures()
{
  modelTexture = gl.createTexture();
  modelImage = new Image();
  modelImage.onload = function() { onTextureLoaded(modelImage, modelTexture); }
  modelImage.src = "assets/drillBug_texture.png";
}

function onTextureLoaded(image, texture)
{
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
  gl.bindTexture(gl.TEXTURE_2D, null);
}

/**
* Loads the scene
*/
function load()
{
  Scene.objects = [];
  Scene.loadObject('assets/drillbug.js', 'drillbug');
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
      transforms.setMatrixUniforms();

      //Setting vertex shader attributes
      gl.bindBuffer(gl.ARRAY_BUFFER, object.vbo);
      gl.vertexAttribPointer(prg.aVertexPosition, 3, gl.FLOAT, false, 0, 0);
      gl.enableVertexAttribArray(prg.aVertexPosition);

      gl.bindBuffer(gl.ARRAY_BUFFER, object.tex);
      gl.vertexAttribPointer(prg.aVertexTexCoord, 2, gl.FLOAT, false, 0, 0);
      gl.enableVertexAttribArray(prg.aVertexTexCoord);
      
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, modelTexture);
      gl.uniform1i(gl.getUniformLocation(prg, "uSampler"), 0);

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
  
  stats.update();
}