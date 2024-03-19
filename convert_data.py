import meshio
import vtk
import numpy as np
import os

# Mesh path
path = "Meshes/0095_0001-mesh-complete/"

# Import vtp file
reader = vtk.vtkXMLPolyDataReader()
reader.SetFileName(path+"mesh-complete.exterior.vtp")
reader.Update()
vtp = reader.GetOutput()

# Convert polydata to unstructured grid
append_filter = vtk.vtkAppendFilter()
append_filter.AddInputData(vtp)
append_filter.Update()
vtu = append_filter.GetOutput()

# Export vtu for meshio
writer = vtk.vtkXMLUnstructuredGridWriter()
writer.SetFileName(path+"tmp.vtu")
writer.SetInputData(vtu)
writer.Update()
writer.Write()

# Import mesh
mesh = meshio.read(path+"mesh-complete.mesh.vtu")

# Import markers
markers = meshio.read(path+"tmp.vtu")
vtp_global_node_ID = markers.point_data["GlobalNodeID"] - 1

# The triangles obtained from tmp.vtp are defined using a local ordering of the
# nodes. Therefore, the triangle's connectivity needs to be re-mapped using
# the global node indexing defined in the tetrahedral mesh. This can be done 
# using the 'GlobalElementID' field defined in the surface mesh as follows
facets = markers.cells[0].data
N = facets.shape[0]
facets = facets.flatten()
global_id = markers.cell_data['GlobalElementID'][0]
facets = vtp_global_node_ID[facets].reshape((N, 3))

# Get facet and cell markers
cell_markers = np.ones_like(mesh.cell_data['GlobalElementID'][0]).astype(int)
facet_markers = markers.cell_data['ModelFaceID'][0].astype(int)

# Export mesh in msh format
points = mesh.points.astype(np.double)
cells = [
  ("tetra", mesh.cells[0].data),
  ("triangle", facets)]

# Export the mesh in given formats
formats = ['mesh','vtk']
for f in formats:

  # Generate meshio mesh
  mesh = meshio.Mesh(
      points,
      cells,
      cell_data={'markers': [
        cell_markers, 
        facet_markers]}
  )

  # Export
  mesh.write(
      path+"mesh."+f,  # str, os.PathLike, or buffer/open file
      # file_format="vtk",  # optional if first argument is a path; inferred from extension
  )
