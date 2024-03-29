####################################################################################
#
#    STEPS - STochastic Engine for Pathway Simulation
#    Copyright (C) 2007-2017 Okinawa Institute of Science and Technology, Japan.
#    Copyright (C) 2003-2006 University of Antwerp, Belgium.
#    
#    See the file AUTHORS for details.
#    This file is part of STEPS.
#    
#    STEPS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2,
#    as published by the Free Software Foundation.
#    
#    STEPS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################   
###

""" Example of triangle directional dcst."""

import random
import steps.model as smodel
import steps.geom as sgeom
import steps.rng as srng
import steps.solver as solv
from steps.utilities import meshio
import time

DCST = 0.2e-9

# define model
model = smodel.Model()
A = smodel.Spec('A', model)
surfsys = smodel.Surfsys('ssys',model)
D_a = smodel.Diff('D_a', surfsys, A)
DCST = 0.2e-9
D_a.setDcst(DCST)
    
mesh = meshio.importAbaqus2("mesh_tet.inp", "mesh_tri.inp", 1e-6, "mesh_conf")[0]
    
boundary_tris = mesh.getROIData("boundary")
v1_tets = mesh.getROIData("v1_tets")
    
comp1 = sgeom.TmComp("comp1", mesh, v1_tets)
    
patch1 = sgeom.TmPatch("patch", mesh, boundary_tris, comp1)
patch1.addSurfsys("ssys")
    
neigh_tris = mesh.getROIData("neigh_tri")
focus_tri = mesh.getROIData("focus_tri")[0]

rng = srng.create('mt19937', 512)
rng.initialize(int(time.time()%4294967295))

solver = solv.Tetexact(model, mesh, rng)

print "Set dcst from focus_tri to all neighbor tris to 0..."
for tri in neigh_tris:
    solver.setTriDiffD(focus_tri, "D_a", 0, tri)
    print solver.getTriDiffD(focus_tri, "D_a", tri)
solver.setTriCount(focus_tri, "A", 10)
print "Patch Count: ", solver.getPatchCount("patch", "A")
print "tri Count: ", solver.getTriCount(focus_tri, "A")
solver.run(1)
print "Patch Count: ", solver.getPatchCount("patch", "A")
print "tri Count: ", solver.getTriCount(focus_tri, "A")

print "Set dcst from focus_tri to all neighbor tris to 1/10 of DCST..."
solver.reset()
for tri in neigh_tris:
    solver.setTriDiffD(focus_tri, "D_a", DCST / 10, tri)
    print solver.getTriDiffD(focus_tri, "D_a", tri)
solver.setTriCount(focus_tri, "A", 10)
print "Patch Count: ", solver.getPatchCount("patch", "A")
print "tri Count: ", solver.getTriCount(focus_tri, "A")
solver.run(1)
print "Patch Count: ", solver.getPatchCount("patch", "A")
print "tri Count: ", solver.getTriCount(focus_tri, "A")

print "Set nondirectional dcst..."
solver.reset()
for tri in neigh_tris:
    solver.setTriDiffD(focus_tri, "D_a", DCST)
    print solver.getTriDiffD(focus_tri, "D_a", tri)
solver.setTriCount(focus_tri, "A", 10)
print "Patch Count: ", solver.getPatchCount("patch", "A")
print "tri Count: ", solver.getTriCount(focus_tri, "A")
solver.run(1)
print "Patch Count: ", solver.getPatchCount("patch", "A")
print "tri Count: ", solver.getTriCount(focus_tri, "A")

