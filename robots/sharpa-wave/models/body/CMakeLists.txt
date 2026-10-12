cmake_minimum_required(VERSION 3.10)
project(sharpa_wave_description)

find_package(ament_cmake REQUIRED)

# Keep each USD layer directory intact; URDFs resolve the shared meshes via
# package://sharpa_wave_description/meshes/{left,right}/<file>.
install(
    DIRECTORY urdf mjcf usd meshes config launch
    DESTINATION share/${PROJECT_NAME}
)

install(
    FILES LICENSE.txt NOTICE.txt APACHE-2.0.txt
    DESTINATION share/${PROJECT_NAME}
)

ament_package()
