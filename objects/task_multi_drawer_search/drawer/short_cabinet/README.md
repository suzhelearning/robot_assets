# Short Cabinet Asset

Source: `short_cabinet` from the LIBERO benchmark assets.

- Repository: https://github.com/Lifelong-Robot-Learning/LIBERO
- License: MIT; see `LICENSE` in this directory.
- Upstream path: `libero/libero/assets/articulated_objects/short_cabinet`

The multi-drawer search scene uses the upstream visual meshes and wood texture.
Its MJCF applies a 1.2x horizontal and 2x vertical scale for larger objects,
uses the upstream fitted box collision assembly at the same scale, enlarges the
handle collisions, and retunes drawer mass and damping for the YAM robot.

The task-specific `drawer_*_handleless.obj` meshes contain only the upstream
`Whitw` drawer-body geometry. The original `Steel` handle geometry is omitted
so the scene displays only its larger custom handles.
