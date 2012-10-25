var Scene = {
    objects : [],
    getObject : function(alias){
        for(var i=0; i<Scene.objects.length; i++){
            if (alias == Scene.objects[i].alias) return Scene.objects[i];
        }
        return null;
    },

    loadObject : function(filename,alias){
        var request = new XMLHttpRequest();
        console.info('Requesting ' + filename);
        request.open("GET",filename);
    
        request.onreadystatechange = function() {
            if (request.readyState == 4) {
                if(request.status == 404) {
                    console.info(filename + ' does not exist');
                }
                else {
                    var o = JSON.parse(request.responseText);
                    o.alias = (alias==null)?'none':alias;
                    o.remote = true;
                    Scene.addObject(o);
                }
            }
        }
        request.send();
    },
    
    loadObjectByParts: function(path, alias, parts){
        for(var i = 1; i <= parts; i++){
            var partFilename =  path+''+i+'.json';
            var partAlias = alias+''+i;
            Scene.loadObject(partFilename,partAlias);
        }
    },
    
    addObject : function(object) {    
        var vertexBufferObject = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vertexBufferObject);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(object.vertices), gl.STATIC_DRAW);
       
        var vertexTextureCoordBufferObject;
        var vertexTextureCoordBufferObject = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vertexTextureCoordBufferObject); 
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(object.uvs), gl.STATIC_DRAW);
        
        var normalBufferObject = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, normalBufferObject);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(object.normals), gl.STATIC_DRAW);
    
        var indexBufferObject = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBufferObject);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(object.faces), gl.STATIC_DRAW);
        
        object.vbo = vertexBufferObject;
        object.ibo = indexBufferObject;
        object.nbo = normalBufferObject;
        object.tex = vertexTextureCoordBufferObject;

        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null);
        gl.bindBuffer(gl.ARRAY_BUFFER,null);
    
        Scene.objects.push(object);
        
        if (object.remote){
          console.info(object.alias + ' has been added to the scene [Remote]');
        }
        else {
          console.info(object.alias + ' has been added to the scene [Local]');
        }
    } 
}