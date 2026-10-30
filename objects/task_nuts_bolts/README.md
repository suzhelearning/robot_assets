Nuts and bolts sorting assets
=============================

These OBJ files are repo-local generated meshes for the nuts-and-bolts sorting
task:

- `m20_nut_watertight.obj`
- `m20_bolt_watertight.obj`

They are M20-style source visual meshes with closed surfaces and clean winding
for MuJoCo rendering. The task scene scales them to 0.72x, slightly under
M16-sized, so they stay grippable without dominating the workspace. The bolt
includes a hex head and helical thread ridges; the nut includes a hex body and
threaded through-hole. The simulation still uses separate primitive collision
geoms in the scene XML for stable contact.
