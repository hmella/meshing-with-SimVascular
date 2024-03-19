#!/usr/bin/env python
"""File format conversion

category: vtk, file conversion, tomb"""
import os, sys
import vtk

def vtk2vtp(invtkfile, outvtpfile, binary=False):
    """What it says on the label"""
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(invtkfile)

    model = vtk.vtkGeometryFilter()
    model.SetInputConnection(reader.GetOutputPort())
    model.Update()

    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(outvtpfile)
    if binary:
        writer.SetFileTypeToBinary()
    writer.SetInputConnection(model.GetOutputPort())
    writer.Update()

if __name__ == '__main__':
    args = sys.argv
    binary = False
    vtkfile = 'caroCritic_5kv.vtk'
    vtk2vtp(vtkfile, vtkfile[:-4]+'.vtp', binary=binary)