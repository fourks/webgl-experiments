
/**
*   Defines the initial values for the transformation matrices
*/
function initTransforms(){
    //Initialize Model-View matrix
    mvMatrix = camera.getViewTransform();
    
    //Initialize Perspective matrix
    mat4.identity(pMatrix);
    mat4.perspective(30, c_width / c_height, 0.1, 1000.0, pMatrix);
    
    //Initialize Normal matrix
    mat4.identity(nMatrix);
    mat4.set(mvMatrix, nMatrix);
    mat4.inverse(nMatrix);
    mat4.transpose(nMatrix);
    
 }

/**
*   Updates the Model-View matrix if there is any translation or change in 
*   coordinate system (world->camera or camera->world). Updates the Normal matrix according to the translation.
*   Please notice that the normal matrix will ALWAYS operate in world coordinates.
*   Called once per rendering cycle.
*/
function updateTransforms(){
    mat4.perspective(30, c_width / c_height, 0.1, 1000.0, pMatrix);  // We can resize the screen at any point so the perspective matrix should be updated always.
}


/**
* Maps the matrices to shader matrix uniforms
*
* Called once per rendering cycle. 
*/
function setMatrixUniforms(){
    
    gl.uniformMatrix4fv(prg.uMVMatrix, false, camera.getViewTransform());        //Maps the Model-View matrix to the uniform prg.uMVMatrix
    
    gl.uniformMatrix4fv(prg.uPMatrix, false, pMatrix);    //Maps the Perspective matrix to the uniform prg.uPMatrix
    
    mat4.transpose(camera.matrix, nMatrix);               //Calculates the Normal matrix 
    gl.uniformMatrix4fv(prg.uNMatrix, false, nMatrix);    //Maps the Normal matrix to the uniform prg.uNMatrix
}

/**
*  Configures the gl context
*/
var camera = null;
var interactor = null;

function configure(){
    
    gl.clearColor(0.3, 0.3, 0.3, 1.0);
    gl.clearDepth(100.0);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    
    //Creates and sets up the camera location
    camera = new Camera(CAMERA_ORBIT_TYPE);
    camera.goHome([0, 0, 50]);
    camera.hookRenderer = draw;
    
    //Creates and sets up the mouse and keyboard interactor
    var canvas = document.getElementById('glcanvas');
    interactor = new CameraInteractor(camera, canvas);
    
    //init transforms
    initTransforms();
}


/**
* Loads the scene
*/
function load(){
	Scene.addObject(Cube);
}


/**
* invoked on every rendering cycle
*/
function draw() {
    gl.viewport(0, 0, c_width, c_height);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        
    try{        
        updateTransforms();   
        setMatrixUniforms(); 
        
        for (var i = 0; i < Scene.objects.length; i++){

            var object = Scene.objects[i];
            
            //Setting uniforms
						gl.uniform3fv(prg.uLightDirection,    [0.0, -1.0, -1.0]);
						gl.uniform4fv(prg.uLightDiffuse,      [1.0, 1.0, 1.0, 1.0]);
            gl.uniform4fv(prg.uMaterialDiffuse, 	object.diffuse);
            
            //Setting attributes            
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
    catch(err){
        alert(err);
        console.error(err.description);
    }
}

/**
* Entry point. This function is invoked when the page is loaded
*/
var app = null;
function runWebGLApp() {
    app = new WebGLApp("glcanvas")
    app.configureGLHook = configure;
    app.loadSceneHook   = load;
    app.drawSceneHook   = draw;
    app.run();

}