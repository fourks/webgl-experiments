"""

 Copyright (C) 2001 - 2010 Autodesk, Inc. and/or its licensors.
 All Rights Reserved.

 The coded instructions, statements, computer programs, and/or related material 
 (collectively the "Data") in these files contain unpublished information 
 proprietary to Autodesk, Inc. and/or its licensors, which is protected by 
 Canada and United States of America federal copyright law and by international 
 treaties. 
 
 The Data may not be disclosed or distributed to third parties, in whole or in
 part, without the prior written consent of Autodesk, Inc. ("Autodesk").

 THE DATA IS PROVIDED "AS IS" AND WITHOUT WARRANTY.
 ALL WARRANTIES ARE EXPRESSLY EXCLUDED AND DISCLAIMED. AUTODESK MAKES NO
 WARRANTY OF ANY KIND WITH RESPECT TO THE DATA, EXPRESS, IMPLIED OR ARISING
 BY CUSTOM OR TRADE USAGE, AND DISCLAIMS ANY IMPLIED WARRANTIES OF TITLE, 
 NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE OR USE. 
 WITHOUT LIMITING THE FOREGOING, AUTODESK DOES NOT WARRANT THAT THE OPERATION
 OF THE DATA WILL BE UNINTERRUPTED OR ERROR FREE. 
 
 IN NO EVENT SHALL AUTODESK, ITS AFFILIATES, PARENT COMPANIES, LICENSORS
 OR SUPPLIERS ("AUTODESK GROUP") BE LIABLE FOR ANY LOSSES, DAMAGES OR EXPENSES
 OF ANY KIND (INCLUDING WITHOUT LIMITATION PUNITIVE OR MULTIPLE DAMAGES OR OTHER
 SPECIAL, DIRECT, INDIRECT, EXEMPLARY, INCIDENTAL, LOSS OF PROFITS, REVENUE
 OR DATA, COST OF COVER OR CONSEQUENTIAL LOSSES OR DAMAGES OF ANY KIND),
 HOWEVER CAUSED, AND REGARDLESS OF THE THEORY OF LIABILITY, WHETHER DERIVED
 FROM CONTRACT, TORT (INCLUDING, BUT NOT LIMITED TO, NEGLIGENCE), OR OTHERWISE,
 ARISING OUT OF OR RELATING TO THE DATA OR ITS USE OR ANY OTHER PERFORMANCE,
 WHETHER OR NOT AUTODESK HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH LOSS
 OR DAMAGE. 
 
"""

from DisplayCommon import *
from fbx import KFbxSurfaceMaterial
from fbx import KFbxLayerElement
from fbx import KFbxLayeredTexture
from fbx import KFbxTexture

def DisplayTextureInfo(pTexture, pBlendMode):
    DisplayString("            Name: \"", pTexture.GetName(), "\"")
    DisplayString("            File Name: \"", pTexture.GetFileName(), "\"")
    DisplayDouble("            Scale U: ", pTexture.GetScaleU())
    DisplayDouble("            Scale V: ", pTexture.GetScaleV())
    DisplayDouble("            Translation U: ", pTexture.GetTranslationU())
    DisplayDouble("            Translation V: ", pTexture.GetTranslationV())
    DisplayBool("            Swap UV: ", pTexture.GetSwapUV())
    DisplayDouble("            Rotation U: ", pTexture.GetRotationU())
    DisplayDouble("            Rotation V: ", pTexture.GetRotationV())
    DisplayDouble("            Rotation W: ", pTexture.GetRotationW())

    lAlphaSources = [ "None", "RGB Intensity", "Black" ]

    DisplayString("            Alpha Source: ", lAlphaSources[pTexture.GetAlphaSource()])
    DisplayDouble("            Cropping Left: ", pTexture.GetCroppingLeft())
    DisplayDouble("            Cropping Top: ", pTexture.GetCroppingTop())
    DisplayDouble("            Cropping Right: ", pTexture.GetCroppingRight())
    DisplayDouble("            Cropping Bottom: ", pTexture.GetCroppingBottom())

    lMappingTypes = [ "Null", "Planar", "Spherical", "Cylindrical", "Box", "Face", "UV", "Environment"]

    DisplayString("            Mapping Type: ", lMappingTypes[pTexture.GetMappingType()])

    if pTexture.GetMappingType() == KFbxTexture.ePLANAR:
        lPlanarMappingNormals = ["X", "Y", "Z" ]
        DisplayString("            Planar Mapping Normal: ", lPlanarMappingNormals[pTexture.GetPlanarMappingNormal()])

    lBlendModes   = ["Translucent", "Add", "Modulate", "Modulate2"]   
    if pBlendMode >= 0:
        DisplayString("            Blend Mode: ", lBlendModes[pBlendMode])
    DisplayDouble("            Alpha: ", pTexture.GetDefaultAlpha())

    lMaterialUses = ["Model Material", "Default Material"]

    DisplayString("            Material Use: ", lMaterialUses[pTexture.GetMaterialUse()])

    pTextureUses = ["Standard", "Shadow Map", "Light Map", "Spherical Reflexion Map", "Sphere Reflexion Map"]

    DisplayString("            Texture Use: ", pTextureUses[pTexture.GetTextureUse()])
    DisplayString("")

def FindAndDisplayTextureInfoByProperty(pProperty, pDisplayHeader, pMaterialIndex):
    if pProperty.IsValid():
        #Here we have to check if it's layeredtextures, or just textures:
        lLayeredTextureCount = pProperty.GetSrcObjectCount(KFbxLayeredTexture.ClassId)
        if lLayeredTextureCount > 0:
            for j in range(lLayeredTextureCount):
                DisplayInt("    Layered Texture: ", j)
                lLayeredTexture = pProperty.GetSrcObject(KFbxLayeredTexture.ClassId, j)
                lNbTextures = lLayeredTexture.GetSrcObjectCount(KFbxTexture.ClassId)
                for k in range(lNbTextures):
                    lTexture = lLayeredTexture.GetSrcObject(KFbxTexture.ClassId,k)
                    if lTexture:
                        if pDisplayHeader:
                            DisplayInt("    Textures connected to Material ", pMaterialIndex)
                            pDisplayHeader = False

                        # NOTE the blend mode is ALWAYS on the LayeredTexture and NOT the one on the texture.
                        # Why is that?  because one texture can be shared on different layered textures and might
                        # have different blend modes.

                        lBlendMode = lLayeredTexture.GetTextureBlendMode(k)
                        DisplayString("    Textures for ", pProperty.GetName())
                        DisplayInt("        Texture ", k)  
                        DisplayTextureInfo(lTexture, lBlendMode)
        else:
            # no layered texture simply get on the property
            lNbTextures = pProperty.GetSrcObjectCount(KFbxTexture.ClassId)
            for j in range(lNbTextures):
                lTexture = pProperty.GetSrcObject(KFbxTexture.ClassId,j)
                if lTexture:
                    # display connectMareial header only at the first time
                    if pDisplayHeader:
                        DisplayInt("    Textures connected to Material ", pMaterialIndex)
                        pDisplayHeader = False
                    
                    DisplayString("    Textures for ", pProperty.GetName().Buffer())
                    DisplayInt("        Texture ", j)  
                    DisplayTextureInfo(lTexture, -1)

        lNbTex = pProperty.GetSrcObjectCount(KFbxTexture.ClassId)
        for lTextureIndex in range(lNbTex):
            lTexture = pProperty.GetSrcObject(KFbxTexture.ClassId, lTextureIndex) 


def DisplayTexture(pGeometry):
    lNbMat = pGeometry.GetNode().GetSrcObjectCount(KFbxSurfaceMaterial.ClassId)
    for lMaterialIndex in range(lNbMat):
        lMaterial = pGeometry.GetNode().GetSrcObject(KFbxSurfaceMaterial.ClassId, lMaterialIndex)
        lDisplayHeader = True

        #go through all the possible textures
        if lMaterial:
            for lTextureIndex in range(KFbxLayerElement.LAYERELEMENT_TYPE_TEXTURE_COUNT):
                lProperty = lMaterial.FindProperty(KFbxLayerElement.TEXTURE_CHANNEL_NAMES[lTextureIndex])
                FindAndDisplayTextureInfoByProperty(lProperty, lDisplayHeader, lMaterialIndex) 
