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

# Supporting Module for generating STEPS morph sectioning file using NEURON

import sys
from neuron import h
h.load_file('stdlib.hoc')
h.load_file('import3d.hoc')

def hoc2morph(hoc_file):
    """
    Generate morph sectioning data from NEURON hoc file.
    """
    sections = {}
    h.load_file(hoc_file)

    for sec in h.allsec():
        sections[sec.name()] = {}
        sections[sec.name()]["name"] = sec.name()
        sr = h.SectionRef(sec=sec)
        if sr.has_parent():
            parent = sr.parent.name()
        else:
            parent = None
        sections[sec.name()]["parent"] = parent

        children = []
        for child in sr.child:
            children.append(child.name())

        sections[sec.name()]["children"] = children
        x = []
        y = []
        z = []
        d = []
        n3d = int(h.n3d())
        sections[sec.name()]["points"] = []
        for i in range(n3d):
            sections[sec.name()]["points"].append([h.x3d(i), h.y3d(i), h.z3d(i), h.diam3d(i)])
    return sections

def swc2morph(swc_file):
    """
    Generate morph sectioning data from swc file.
    """
    cell = h.Import3d_SWC_read()
    cell.input(swc_file)

    i3d = h.Import3d_GUI(cell, 0)
    i3d.instantiate(None)

    sections = {}

    for sec in h.allsec():
        sections[sec.name()] = {}
        sections[sec.name()]["name"] = sec.name()
        sr = h.SectionRef(sec=sec)
        if sr.has_parent():
            parent = sr.parent.name()
        else:
            parent = None
        sections[sec.name()]["parent"] = parent

        children = []
        for child in sr.child:
            children.append(child.name())

        sections[sec.name()]["children"] = children
        x = []
        y = []
        z = []
        d = []
        n3d = int(h.n3d())
        sections[sec.name()]["points"] = []
        for i in range(n3d):
            sections[sec.name()]["points"].append([h.x3d(i), h.y3d(i), h.z3d(i), h.diam3d(i)])
    return sections
