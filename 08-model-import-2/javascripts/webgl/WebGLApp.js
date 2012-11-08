var WEBGLAPP_RENDER = undefined;

function WebGLApp(canvas)
{
  this.loadSceneHook = undefined;
  this.configureGLHook = undefined;
  gl = Utils.getGLContext(canvas);
  Program.load();  
}

WebGLApp.prototype.run = function()
{
  if (this.configureGLHook == undefined)
  {
    console.log('The WebGL application cannot start because the configureGLHook has not been specified'); return;
  }
  if (this.loadSceneHook == undefined)
  {
    console.log('The WebGL application cannot start because the loadSceneHook has not been specified'); return;
  }
  if (this.drawSceneHook == undefined)
  {
    console.log('The WebGL application cannot start because the drawSceneHook has not been specified'); return;
  }

  this.configureGLHook();
  this.loadSceneHook();
  WEBGLAPP_RENDER = this.drawSceneHook;
  renderLoop();
}

renderLoop = function()
{
  WEBGLAPP_RENDER();
  requestAnimFrame(renderLoop);
}