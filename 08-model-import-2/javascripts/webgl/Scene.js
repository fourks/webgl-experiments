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
                    var scene = JSON.parse(request.responseText);
                    for(var i in scene)
                    {
                      var o = scene[i]
                      o.alias = (alias==null)?'none':alias;
                      o.remote = true;
                      Scene.addObject(o, i);
                    }
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

    addObject : function(object, i) {
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
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(object.indices), gl.STATIC_DRAW);

        object.vbo = vertexBufferObject;
        object.ibo = indexBufferObject;
        object.nbo = normalBufferObject;
        object.tex = vertexTextureCoordBufferObject;

        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null);
        gl.bindBuffer(gl.ARRAY_BUFFER,null);

        Scene.loadTexture(object, i);

        Scene.objects.push(object);

        if (object.remote){
          console.info(object.alias + ' has been added to the scene [Remote]');
        }
        else {
          console.info(object.alias + ' has been added to the scene [Local]');
        }
    },

    loadTexture: function(object, i)
    {
      var texture = gl.createTexture();
      var image = new Image();
      image.onload = function() { Scene.onTextureLoaded(object, image, texture, i); }
      image.src = object.texture;
    },

    onTextureLoaded: function(object, image, texture, i)
    {
      gl.bindTexture(gl.TEXTURE_2D, texture);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
      gl.bindTexture(gl.TEXTURE_2D, null);
      
      object.gl_tex = texture;
    }
}
