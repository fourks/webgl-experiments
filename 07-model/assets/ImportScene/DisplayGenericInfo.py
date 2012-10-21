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
from fbx import KFbxProperty
from fbx import KFbxObject
from fbx import eBOOL1
from fbx import eDOUBLE1
from fbx import eDOUBLE4
from fbx import eINTEGER1
from fbx import eDOUBLE3
from fbx import eFLOAT1
from fbx import eSTRING

def DisplayGenericInfo(pScene):
    lRootNode = pScene.GetRootNode()

    for i in range(lRootNode.GetChildCount()):
        DisplayNodeGenericInfo(lRootNode.GetChild(i), 0)

    #Other objects directly connected onto the scene
    for i in range(pScene.GetSrcObjectCount(KFbxObject.ClassId)):
        DisplayProperties(pScene.GetSrcObject(KFbxObject.ClassId, i))


def DisplayNodeGenericInfo(pNode, pDepth):
    lString = ""
    for i in range(pDepth):
        lString += "     "

    lString += pNode.GetName()
    lString += "\n"

    DisplayString(lString)

    #Display generic info about that Node
    DisplayProperties(pNode)
    DisplayString("")
    for i in range(pNode.GetChildCount()):
        DisplayNodeGenericInfo(pNode.GetChild(i), pDepth + 1)

def DisplayProperties(pObject):
    DisplayString("Type: %s     Name: %s" % (pObject.ClassId.GetFbxFileTypeName(), pObject.GetName()))

    # Display all the properties
    lCount = 0
    lProperty = pObject.GetFirstProperty()
    while lProperty.IsValid():
        lCount += 1
        lProperty = pObject.GetNextProperty(lProperty)

    lTitleStr = "    Property Count: "

    if lCount == 0:
        return # there are no properties to display

    DisplayInt(lTitleStr, lCount)

    i=0
    lProperty = pObject.GetFirstProperty()
    while lProperty.IsValid():
        # exclude user properties
        DisplayInt("        Property ", i)
        lString = lProperty.GetLabel()
        DisplayString("            Display Name: ", lString.Buffer())
        lString = lProperty.GetName()
        DisplayString("            Internal Name: ", lString.Buffer())
        lString = lProperty.GetPropertyDataType().GetName()
        DisplayString("            Type: ", lString)
        if lProperty.HasMinLimit():
            DisplayDouble("            Min Limit: ", lProperty.GetMinLimit())
        if lProperty.HasMaxLimit():
            DisplayDouble("            Max Limit: ", lProperty.GetMaxLimit())
        DisplayBool  ("            Is Animatable: ", lProperty.GetFlag(KFbxProperty.eANIMATABLE))
        DisplayBool  ("            Is Temporary: ", lProperty.GetFlag(KFbxProperty.eTEMPORARY))


        if lProperty.GetPropertyDataType().GetType() == eBOOL1:
            DisplayBool("            Default Value: ", lProperty.Get())
        elif lProperty.GetPropertyDataType().GetType() == eDOUBLE1:
            DisplayDouble("            Default Value: ",lProperty.Get())
        elif lProperty.GetPropertyDataType().GetType() == eDOUBLE4:
            lDefault = lProperty.Get()
            lBuf = "R=%f, G=%f, B=%f, A=%f" % (lDefault[0], lDefault[1], lDefault[2], lDefault[3])
            DisplayString("            Default Value: ", lBuf)
        elif lProperty.GetPropertyDataType().GetType() == eINTEGER1:
            DisplayInt("            Default Value: ", lProperty.Get())
        elif lProperty.GetPropertyDataType().GetType() == eDOUBLE3:
            lDefault = lProperty.Get()
            lBuf  = "X=%f, Y=%f, Z=%f" % (lDefault[0], lDefault[1], lDefault[2])
            DisplayString("            Default Value: ", lBuf)
        #case  DTEnum:
        #    DisplayInt("            Default Value: ", lProperty.Get())
        #    break

        elif lProperty.GetPropertyDataType().GetType() == eFLOAT1:
            DisplayDouble("            Default Value: ", lProperty.Get())
        elif lProperty.GetPropertyDataType().GetType() == eSTRING:
            lString = lProperty.Get()
            DisplayString("            Default Value: ", lString.Buffer())
        else:
            DisplayString("            Default Value: UNIDENTIFIED")
        
        i += 1
        lProperty = pObject.GetNextProperty(lProperty)
