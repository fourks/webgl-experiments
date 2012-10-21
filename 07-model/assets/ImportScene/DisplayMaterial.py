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

from fbx import *
from DisplayCommon import *

def DisplayMaterial(pGeometry):
    lMaterialCount = 0
    lNode = None
    if pGeometry:
        lNode = pGeometry.GetNode()
        if lNode:
            lMaterialCount = lNode.GetMaterialCount()

    for l in range(pGeometry.GetLayerCount()):
        leMat = pGeometry.GetLayer(l).GetMaterials()
        if leMat:
            if leMat.GetReferenceMode() == KFbxLayerElement.eINDEX:
                #Materials are in an undefined external table
                continue

            if lMaterialCount > 0:
                theColor = KFbxColor()
                
                header = "    Materials on layer %d: " % l 
                DisplayString(header)

                for lCount in range(lMaterialCount):
                    DisplayInt("        Material ", lCount)

                    lMaterial = lNode.GetMaterial(lCount)

                    DisplayString("            Name: \"", lMaterial.GetName(), "\"") 

                    #Get the implementation to see if it's a hardware shader.
                    lImplementation = GetImplementation(lMaterial, "ImplementationHLSL")
                    lImplemenationType = "HLSL"
                    if not lImplementation:
                        lImplementation = GetImplementation(lMaterial, "ImplementationCGFX")
                        lImplemenationType = "CGFX"
                    if lImplementation:
                        #Now we have a hardware shader, let's read it
                        print("            Hardware Shader Type: %s\n" % lImplemenationType.Buffer())
                        lRootTable = lImplementation.GetRootTable()
                        lFileName = lRootTable.DescAbsoluteURL.Get()
                        lTechniqueName = lRootTable.DescTAG.Get() 


                        lTable = lImplementation.GetRootTable()
                        lEntryNum = lTable.GetEntryCount()

                        for i in range(lEntryNum):
                            lEntry = lTable.GetEntry(i)
                            lEntry.GetEntryType(True) 

                            lTest = lEntry.GetSource()
                            print("            Entry: %s\n" % lTest.Buffer())

                            if cmp( KFbxPropertyEntryView.sEntryType, lEntrySrcType ) == 0:
                                lFbxProp = lMaterial.FindPropertyHierarchical(lEntry.GetSource()) 
                                if not lFbxProp.IsValid():
                                    lFbxProp = lMaterial.RootProperty.FindHierarchical(lEntry.GetSource())
                            elif cmp( KFbxConstantEntryView.sEntryType, lEntrySrcType ) == 0:
                                lFbxProp = lImplementation.GetConstants().FindHierarchical(lEntry.GetSource())
                            
                            if lFbxProp.IsValid():
                                if lFbxProp.GetSrcObjectCount( KFbxTexture.ClassId ) > 0:
                                    #do what you want with the texture
                                    for j in range(lFbxProp.GetSrcObjectCount(KFbxTexture.ClassId)):
                                        lTex = lFbxProp.GetSrcObject(KFbxTexture.ClassId,j)
                                        print("                Texture: %s\n" % lTex.GetFileName())
                                else:
                                    lFbxType = lFbxProp.GetPropertyDataType()
                                    blah = lFbxType.GetName()
                                    if (DTBool == lFbxType):
                                        DisplayBool("                Bool: ", lFbxProp.Get(EFbxType.eBOOL1))
                                    elif ( DTInteger == lFbxType or  DTEnum  == lFbxType ):
                                        DisplayInt("                Int: ", lFbxProp.Get(EFbxType.eINTEGER1))
                                    elif ( DTFloat == lFbxType):
                                        DisplayDouble("                Float: ", lFbxProp.Get(EFbxType.eFLOAT1))
                                    elif ( DTDouble == lFbxType):
                                        DisplayDouble("                Double: ", lFbxProp.Get(EFbxType.eDOUBLE1))
                                    elif ( DTString == lFbxType or DTUrl  == lFbxType or DTXRefUrl  == lFbxType ):
                                        DisplayString("                String: ", lFbxProp.Get(EFbxType.eSTRING))
                                    elif ( DTDouble2 == lFbxType):
                                        res, lDouble2= lFbxProp.Get(EFbxType.eDOUBLE2)
                                        lVect = []
                                        lVect[0] = lDouble2[0]
                                        lVect[1] = lDouble2[1]
                                        Display2DVector("                2D vector: ", lVect)
                                    elif ( DTVector3D == lFbxType or DTDouble3 == lFbxType or DTColor3 == lFbxType):
                                        res, lDouble3 = lFbxProp.Get(EFbxType.eDOUBLE3)
                                        lVect = []
                                        lVect[0] = lDouble3[0]
                                        lVect[1] = lDouble3[1]
                                        lVect[2] = lDouble3[2]
                                        Display3DVector("                3D vector: ", lVect)
                                    elif ( DTVector4D == lFbxType or DTDouble4 == lFbxType or DTColor4 == lFbxType):
                                        res, lDouble4 = lFbxProp.Get(EFbxType.eDOUBLE4)
                                        lVect = []
                                        lVect[0] = lDouble4[0]
                                        lVect[1] = lDouble4[1]
                                        lVect[2] = lDouble4[2]
                                        lVect[3] = lDouble4[3]
                                        Display4DVector("                4D vector: ", lVect)
                                    elif ( DTDouble44 == lFbxType):
                                        res, lDouble44 = lFbxProp.Get(EFbxType.eDOUBLE44)
                                        for j in range(4):
                                            lVect = []
                                            lVect[0] = lDouble44[j][0]
                                            lVect[1] = lDouble44[j][1]
                                            lVect[2] = lDouble44[j][2]
                                            lVect[3] = lDouble44[j][3]
                                            Display4DVector("                4x4D vector: ", lVect)

                    elif (lMaterial.GetClassId().Is(KFbxSurfacePhong.ClassId)):
                        # We found a Phong material.  Display its properties.

                        # Display the Ambient Color
                        lKFbxDouble3 = lMaterial.Ambient
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Ambient: ", theColor)

                        # Display the Diffuse Color
                        lKFbxDouble3 = lMaterial.Diffuse
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Diffuse: ", theColor)

                        # Display the Specular Color (unique to Phong materials)
                        lKFbxDouble3 = lMaterial.Specular
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Specular: ", theColor)

                        # Display the Emissive Color
                        lKFbxDouble3 = lMaterial.Emissive
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Emissive: ", theColor)

                        # Opacity is Transparency factor now
                        lKFbxDouble1 = lMaterial.TransparencyFactor
                        DisplayDouble("            Opacity: ", 1.0-lKFbxDouble1.Get())

                        # Display the Shininess
                        lKFbxDouble1 = lMaterial.Shininess
                        DisplayDouble("            Shininess: ", lKFbxDouble1.Get())

                        # Display the Reflectivity
                        lKFbxDouble3 = lMaterial.Reflection
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Reflectivity: ", theColor)
                    elif lMaterial.GetClassId().Is(KFbxSurfaceLambert.ClassId):
                        # We found a Lambert material. Display its properties.
                        # Display the Ambient Color
                        lKFbxDouble3 = lMaterial.Ambient
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Ambient: ", theColor)

                        # Display the Diffuse Color
                        lKFbxDouble3 = lMaterial.Diffuse
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Diffuse: ", theColor)

                        # Display the Emissive
                        lKFbxDouble3 = lMaterial.Emissive
                        theColor.Set(lKFbxDouble3.Get()[0], lKFbxDouble3.Get()[1], lKFbxDouble3.Get()[2])
                        DisplayColor("            Emissive: ", theColor)

                        # Display the Opacity
                        lKFbxDouble1 = lMaterial.TransparencyFactor
                        DisplayDouble("            Opacity: ", 1.0-lKFbxDouble1.Get())
                    else:
                        DisplayString("Unknown type of Material")

                    lString = lMaterial.ShadingModel
                    DisplayString("            Shading Model: ", lString.Get().Buffer())
                    DisplayString("")
