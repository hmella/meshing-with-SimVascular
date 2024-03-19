#!/usr/bin/env python
"""File format conversion

category: vtk, file conversion, tomb"""
import os, sys
import vtk

def vtk2vtp(invtkfile, outvtpfile, binary=False):
    # Set vtk reader
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(invtkfile)

    # Set model
    model = vtk.vtkGeometryFilter()
    model.SetInputConnection(reader.GetOutputPort())
    model.Update()

    # # Get surface triangles
    # triangle = vtk.vtkTriangleFilter()
    # triangle.SetInputConnection(model.GetOutputPort())
    # triangle.Update()

    # Export data
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(outvtpfile)
    if binary:
        writer.SetFileTypeToBinary()
    # writer.SetInputConnection(triangle.GetOutputPort())
    writer.SetInputConnection(model.GetOutputPort())
    writer.Update()

if __name__ == '__main__':
    args = sys.argv
    binary = False
    vtkfile = 'caroCritic_5kv.vtk'
    vtk2vtp(vtkfile, vtkfile[:-4]+'.vtp', binary=binary)