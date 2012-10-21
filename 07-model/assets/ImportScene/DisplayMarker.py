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
from fbx import KFbxMarker
from fbx import KFbxColor


def DisplayMarker(pNode):
    lMarker = pNode.GetNodeAttribute()

    DisplayString("Marker Name: ", pNode.GetName())

    # Type
    lString = "    Marker Type: "
    if lMarker.GetType() == KFbxMarker.eSTANDARD:
        lString += "Standard"
    elif lMarker.GetType() == KFbxMarker.eOPTICAL:
         lString += "Optical"
    elif lMarker.GetType() == KFbxMarker.eIK_EFFECTOR:
         lString += "IK Effector"
    elif lMarker.GetType() == KFbxMarker.eFK_EFFECTOR:
         lString += "FK Effector"
    DisplayString(lString)

    # Look
    lString = "    Marker Look: "
    if lMarker.Look.Get() == KFbxMarker.eCUBE:
        lString += "Cube"
    elif lMarker.Look.Get() == KFbxMarker.eHARD_CROSS:
        lString += "Hard Cross"
    elif lMarker.Look.Get() == KFbxMarker.eLIGHT_CROSS:
        lString += "Light Cross"
    elif lMarker.Look.Get() == KFbxMarker.eSPHERE:
        lString += "Sphere"
    DisplayString(lString)

    # Size
    #lString = "    Size: "
    #lString += str(lMarker.Size.Get())
    DisplayDouble("    Size: ", lMarker.Size.Get())

    # Color
    c = lMarker.Color.Get()
    color = KFbxColor(c[0], c[1], c[2])
    DisplayColor("    Color: ", color)

    # IKPivot
    Display3DVector("    IKPivot: ", lMarker.IKPivot.Get())
