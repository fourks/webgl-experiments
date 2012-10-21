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
from fbx import eBOOL1
from fbx import eDOUBLE1
from fbx import eDOUBLE4
from fbx import eINTEGER1
from fbx import eDOUBLE3
from fbx import eFLOAT1
from fbx import eSTRING
from fbx import eENUM
#from fbx import DTColor3
#from fbx import DTColor4

def DisplayUserProperties(pObject):
    lCount = 0
    lTitleStr = "    Property Count: "

    lProperty = pObject.GetFirstProperty()
    while lProperty.IsValid():
        if lProperty.GetFlag(KFbxProperty.eUSER):
            lCount += 1

        lProperty = pObject.GetNextProperty(lProperty)

    if lCount == 0:
        return # there are no user properties to display

    DisplayInt(lTitleStr, lCount)

    lProperty = pObject.GetFirstProperty()
    i = 0
    while lProperty.IsValid():
        if lProperty.GetFlag(KFbxProperty.eUSER):
            DisplayInt("        Property ", i)
            lString = lProperty.GetLabel()
            DisplayString("            Display Name: ", lString.Buffer())
            lString = lProperty.GetName()
            DisplayString("            Internal Name: ", lString.Buffer())
            DisplayString("            Type: ", lProperty.GetPropertyDataType().GetName())
            if lProperty.HasMinLimit():
                DisplayDouble("            Min Limit: ", lProperty.GetMinLimit())
            if lProperty.HasMaxLimit():
                DisplayDouble("            Max Limit: ", lProperty.GetMaxLimit())
            DisplayBool  ("            Is Animatable: ", lProperty.GetFlag(KFbxProperty.eANIMATABLE))
            DisplayBool  ("            Is Temporary: ", lProperty.GetFlag(KFbxProperty.eTEMPORARY))
            
            lPropertyDataType=lProperty.GetPropertyDataType()
            
            # BOOL
            if lPropertyDataType.GetType() == eBOOL1:
                val = lProperty.Get()
                DisplayBool("            Default Value: ", val)
            # REAL
            elif lPropertyDataType.GetType() == eDOUBLE1 or lPropertyDataType.GetType() == eFLOAT1:
                val = lProperty.Get()
                DisplayDouble("            Default Value: ",val)
            # COLOR
            #elif lPropertyDataType.Is(DTColor3) or lPropertyDataType.Is(DTColor4):
                val = lProperty.Get()
                #lDefault=KFbxGet <KFbxColor> (lProperty)
                #sprintf(lBuf, "R=%f, G=%f, B=%f, A=%f", lDefault.mRed, lDefault.mGreen, lDefault.mBlue, lDefault.mAlpha)
                #DisplayString("            Default Value: ", lBuf)
            #    pass
            # INTEGER
            elif lPropertyDataType.GetType() == eINTEGER1:
                val = lProperty.Get()
                DisplayInt("            Default Value: ", val)
            # VECTOR
            elif lPropertyDataType.GetType() == eDOUBLE3 or lPropertyDataType.GetType() == eDOUBLE4:
                val = lProperty.Get()
                lBuf = "X=%f, Y=%f, Z=%f", (val[0], val[1], val[2])
                DisplayString("            Default Value: ", lBuf)
#            # LIST
#            elif lPropertyDataType.GetType() == eENUM:
#                val = lProperty.Get()
#                DisplayInt("            Default Value: ", val)
            # UNIDENTIFIED
            else:
                DisplayString("            Default Value: UNIDENTIFIED")
            i += 1

        lProperty = pObject.GetNextProperty(lProperty)
