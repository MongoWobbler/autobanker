# Author: Christian Corsica

import maya.cmds as mc


# function to get some fat looking curves
def createQuadArrow():
    control = mc.curve(d=1, p=[(1, 0, 1),(3, 0, 1),(3, 0, 2),(5, 0, 0),(3, 0, -2),(3, 0, -1),(1, 0, -1),(1, 0, -3),(2, 0, -3),(0, 0, -5),(-2, 0, -3),(-1, 0, -3),(-1, 0, -1),(-3, 0, -1),(-3, 0, -2),(-5, 0, 0),(-3, 0, 2),(-3, 0, 1),(-1, 0, 1),(-1, 0, 3),(-2, 0, 3),(0, 0, 5),( 2, 0, 3),(1, 0, 3),(1, 0, 1),], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
    mc.xform(cp=True)
    mc.scale(0.2, 0.2, 0.2)
    mc.makeIdentity(apply=True, t=True, r=True, s=True)
    return control
    

def create():
    # select all geometry that you would like to bank
    selected = mc.ls(sl=True)

    # warning for selecting nothing
    if len(selected) < 1:
        mc.warning("You have nothing selected, must select at least one object")  
        return

    # this lets you perform the operation on more than one object! yay for loops!  
    for selection in selected:
    
        # Gets all the verts from selected object and adds the to a list called "verts"
        xOrig = mc.xform(selection + '.vtx[*]', q=True, ws=True, t=True)
        verts = zip(xOrig[0::3], xOrig[1::3], xOrig[2::3])     	
        
        # variable lists for x, y, z coordinates of verts
        vx = []
        vy = []
        vz = []
        
        # gets all the y values from the verts and adds them to the list "vy"
        for vert in verts:
            vy.append(vert[1])
        
        # gets the lowest vert of the object, gets the highest, gets the length of the object, and makes the threshold. The treshold is the height of the sole of the footing
        minVY = min(vy)
        maxVY = max(vy)
        length = maxVY - minVY
        threshold = ((length/35) + minVY)
        
        # if the vert is inside the threshold, add its x to vx, and it z to vz.    
        for vert in verts:
            if vert[1] <= threshold:
                vx.append(vert[0]) 
                vz.append(vert[2])
        
        # variables for the vert at the right of the foot, the left, the front, and the back        
        minVX = min(vx)
        maxVX = max(vx)
        minVZ = min(vz)
        maxVZ = max(vz)
        
        # naming variables to make code more readable
        bankingName = selection +"_banking_grp"
        control_name = selection +"_cntrl"
        geometry_grp_name = selection + "_geo_grp"
        
        # there is that fat curve. Add attributes to it called "bankSideways", and "bankForwards". move the curve to the base of the selected object
        quad_arrow = createQuadArrow()
        mc.rename(quad_arrow, control_name)
        mc.addAttr(ln="bankSideways", at="double", dv=0, w=True, r=True, k=True)
        mc.addAttr(ln="bankForwards", at="double", dv=0, w=True, r=True, k=True)
        mc.setAttr(control_name + ".tx", ((maxVX + minVX)/2))
        mc.setAttr(control_name + ".ty", minVY)
        mc.setAttr(control_name + ".tz", ((maxVZ + minVZ)/2))
        
        # creating banking grp null
        mc.createNode ('transform', n=bankingName)
        
        # create bank left null and place at the left of the footing
        mc.createNode ('transform', n="bankLeft")
        mc.move(maxVX, minVY, ((maxVZ + minVZ)/2), "|bankLeft")
        
        # create bank right null and place at the right of the footing    
        mc.createNode ('transform', n="bankRight")
        mc.move(minVX, minVY, ((maxVZ + minVZ)/2), "|bankRight")
        
        # create bank bankward null and place at the back of the footing
        mc.createNode ('transform', n="bankBackward")
        mc.move(((maxVX + minVX)/2), minVY, minVZ, "|bankBackward")
        
        # create bank forward null and place at the front of the footing
        mc.createNode ('transform', n="bankForward")
        mc.move(((maxVX + minVX)/2), minVY, maxVZ, "|bankForward")
        
        # create a condition node that makes cntrl.bankSideways rotate bank left only if it is greater than 0
        mc.createNode('condition', n=selection + "_bankLeft_condition")
        mc.setAttr(selection + "_bankLeft_condition.operation", 3)
        mc.setAttr(selection + "_bankLeft_condition.colorIfFalseR", 0)
        mc.connectAttr(control_name + ".bankSideways", selection + "_bankLeft_condition.colorIfTrueR")
        mc.connectAttr(control_name + ".bankSideways", selection + "_bankLeft_condition.secondTerm")
        mc.connectAttr(selection + "_bankLeft_condition.outColorR", "|bankLeft.rz")
        
        # create a condition node that makes cntrl.bankForwards rotate bank backward only if it is greater than 0
        mc.createNode('condition', n=selection + "_bankBackward_condition")
        mc.setAttr(selection + "_bankBackward_condition.operation", 3)
        mc.setAttr(selection + "_bankBackward_condition.colorIfFalseR", 0)
        mc.connectAttr(control_name + ".bankForwards", selection + "_bankBackward_condition.colorIfTrueR")
        mc.connectAttr(control_name + ".bankForwards", selection + "_bankBackward_condition.secondTerm")
        mc.connectAttr(selection + "_bankBackward_condition.outColorR", "|bankBackward.rx")
        
        # create a condition node that makes cntrl.bankSideways rotate bank right only if it is less than 0
        mc.createNode('condition', n=selection + "_bankRight_condition")
        mc.setAttr(selection + "_bankRight_condition.operation", 4)
        mc.setAttr(selection + "_bankRight_condition.colorIfFalseR", 0)
        mc.connectAttr(control_name + ".bankSideways", selection + "_bankRight_condition.colorIfTrueR")
        mc.connectAttr(control_name + ".bankSideways", selection + "_bankRight_condition.secondTerm")
        mc.connectAttr(selection + "_bankRight_condition.outColorR", "|bankRight.rz")
        
        # create a condition node that makes cntrl.bankForwards rotate bank forward only if it is less than 0
        mc.createNode('condition', n=selection + "_bankForward_condition")
        mc.setAttr(selection + "_bankForward_condition.operation", 4)
        mc.setAttr(selection + "_bankForward_condition.colorIfFalseR", 0)
        mc.connectAttr(control_name + ".bankForwards", selection + "_bankForward_condition.colorIfTrueR")
        mc.connectAttr(control_name + ".bankForwards", selection + "_bankForward_condition.secondTerm")
        mc.connectAttr(selection + "_bankForward_condition.outColorR", "|bankForward.rx")
        
        # parent the cntrl under bankLeft, freezetransforms, delete history. 
        # parent bankleft under bankright, bankright under bankbackward, bankbackwards under bankforwards, bankforwards under bank_grp. 
        # at last, group the geometry
        mc.parent(control_name, "|bankLeft")
        mc.makeIdentity("|bankLeft|" + control_name, apply=True)
        mc.delete("|bankLeft|" + control_name, ch = 1)
        mc.parent("|bankLeft", "|bankRight")
        mc.parent("|bankRight", "|bankBackward")
        mc.parent("|bankBackward", "|bankForward")
        mc.parent("|bankForward", bankingName)
        mc.group(selection, n=geometry_grp_name)
        
        # make the cntrl drive geo_grp by using a parent constraint
        mc.parentConstraint(bankingName + "|bankForward|bankBackward|bankRight|bankLeft|" + control_name, geometry_grp_name, mo=True)
        mc.select(control_name)
