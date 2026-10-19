"""
Procedural Blender 4.2 3D Biomechanical Telemetry & Olympic Barbell Generator
Generates:
1. assets3d/hip_thrust_3d_telemetry.blend
2. assets3d/hip_thrust_3d_telemetry.glb
3. assets3d/hip_thrust_3d_render.png
"""

import bpy
import math
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets3d")
os.makedirs(OUT_DIR, exist_ok=True)

BLEND_PATH = os.path.join(OUT_DIR, "hip_thrust_3d_telemetry.blend")
GLB_PATH = os.path.join(OUT_DIR, "hip_thrust_3d_telemetry.glb")
PNG_PATH = os.path.join(OUT_DIR, "hip_thrust_3d_render.png")


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_pbr_material(name, base_color, metallic=0.0, roughness=0.35, emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if emission_color is not None and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def build_biomechanical_scene():
    reset_scene()
    scene = bpy.context.scene

    # Materials (Prozhe v1.1.0 + Vascular Crimson + Lab Green + Brushed Steel)
    mat_obsidian = make_pbr_material("Mat_Obsidian_Lab", (0.035, 0.038, 0.042, 1.0), metallic=0.35, roughness=0.28)
    mat_chrome = make_pbr_material("Mat_Olympic_Chrome", (0.82, 0.85, 0.88, 1.0), metallic=0.95, roughness=0.14)
    mat_crimson = make_pbr_material(
        "Mat_Vascular_Laser",
        (0.75, 0.04, 0.18, 1.0),
        metallic=0.4,
        roughness=0.2,
        emission_color=(0.85, 0.05, 0.22, 1.0),
        emission_strength=1.8,
    )
    mat_crimson_plate = make_pbr_material(
        "Mat_Anodized_Crimson_Plate",
        (0.48, 0.025, 0.11, 1.0),
        metallic=0.78,
        roughness=0.22,
    )
    mat_lab_green = make_pbr_material(
        "Mat_Lab_Green",
        (0.18, 0.24, 0.15, 1.0),
        metallic=0.65,
        roughness=0.24,
    )
    mat_gold_joint = make_pbr_material(
        "Mat_Pivot_Joint",
        (0.92, 0.72, 0.25, 1.0),
        metallic=0.92,
        roughness=0.15,
    )

    # 1. Studio Pedestal / Calibration Platform
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=3.4, depth=0.16, location=(0, 0, -1.55))
    pedestal = bpy.context.active_object
    pedestal.name = "Telemetry_Platform"
    pedestal.data.materials.append(mat_obsidian)
    bpy.ops.object.shade_smooth()

    # Outer Calibration Ring on Platform
    bpy.ops.mesh.primitive_torus_add(
        major_radius=3.15, minor_radius=0.025, major_segments=96, minor_segments=24, location=(0, 0, -1.45)
    )
    plat_ring = bpy.context.active_object
    plat_ring.name = "Platform_Caliper_Ring"
    plat_ring.data.materials.append(mat_crimson)
    bpy.ops.object.shade_smooth()

    # 2. Vector 01: Horizontal (Anteroposterior) Torque Gyro Ring (Contreras 2015)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=2.15,
        minor_radius=0.045,
        major_segments=96,
        minor_segments=32,
        location=(0, 0, 0.15),
        rotation=(math.radians(90), 0, math.radians(18)),
    )
    ring_v1 = bpy.context.active_object
    ring_v1.name = "Vector01_Horizontal_HipThrust_Ring"
    ring_v1.data.materials.append(mat_crimson)
    bpy.ops.object.shade_smooth()

    # 3. Vector 02: Axial / Lengthened Tension Gyro Ring (Maeo 2021)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.82,
        minor_radius=0.04,
        major_segments=96,
        minor_segments=32,
        location=(0, 0, 0.15),
        rotation=(math.radians(35), math.radians(45), 0),
    )
    ring_v2 = bpy.context.active_object
    ring_v2.name = "Vector02_Axial_Lengthened_Ring"
    ring_v2.data.materials.append(mat_lab_green)
    bpy.ops.object.shade_smooth()

    # 4. Vector 03: 30-Degree Frontal Plane Abduction Ring (Moore 2020)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.48,
        minor_radius=0.035,
        major_segments=96,
        minor_segments=32,
        location=(0, 0, 0.15),
        rotation=(math.radians(60), math.radians(-30), math.radians(25)),
    )
    ring_v3 = bpy.context.active_object
    ring_v3.name = "Vector03_ScapularPlane_30Deg_Ring"
    ring_v3.data.materials.append(mat_chrome)
    bpy.ops.object.shade_smooth()

    # 5. Central Olympic Hip-Thrust Barbell Assembly (Bar + Sleeves + Calibrated Plates)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=48, radius=0.045, depth=4.6, location=(0, 0, 0.15), rotation=(0, math.radians(90), math.radians(18))
    )
    barbell = bpy.context.active_object
    barbell.name = "Olympic_Barbell_20kg"
    barbell.data.materials.append(mat_chrome)
    bpy.ops.object.shade_smooth()

    # Calibrated Bumper Plates on Both Sides
    plate_offsets = [-1.55, -1.38, -1.23, 1.23, 1.38, 1.55]
    plate_radii = [0.62, 0.72, 0.82, 0.82, 0.72, 0.62]
    plate_mats = [mat_crimson_plate, mat_obsidian, mat_crimson_plate, mat_crimson_plate, mat_obsidian, mat_crimson_plate]

    angle_z = math.radians(18)
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)

    for idx, (offset, rad, pmat) in enumerate(zip(plate_offsets, plate_radii, plate_mats)):
        px = offset * cos_z
        py = offset * sin_z
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=64,
            radius=rad,
            depth=0.11,
            location=(px, py, 0.15),
            rotation=(0, math.radians(90), angle_z),
        )
        plate = bpy.context.active_object
        plate.name = f"Calibrated_Plate_{idx+1}"
        plate.data.materials.append(pmat)
        bpy.ops.object.shade_smooth()

    # 6. Biomechanical Hip-Knee-Ankle Lever Nodes (Vertical Tibia 90 deg)
    joint_coords = [
        ("Hip_Axis_Pivot", (-0.55, -0.15, 0.15), 0.16, mat_crimson),
        ("Knee_Axis_90Deg_Safe", (0.45, 0.12, 0.55), 0.13, mat_gold_joint),
        ("Ankle_Vertical_Tibia_Base", (0.45, 0.12, -0.85), 0.11, mat_chrome),
        ("Shoulder_Bench_Anchor", (-1.35, -0.35, 0.10), 0.12, mat_lab_green),
    ]
    for jname, loc, jrad, jmat in joint_coords:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=jrad, location=loc)
        sph = bpy.context.active_object
        sph.name = jname
        sph.data.materials.append(jmat)
        bpy.ops.object.shade_smooth()

    # 7. World Background & Studio 3-Point Area Lighting
    world = bpy.data.worlds.new("StudioWorld")
    scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (0.015, 0.017, 0.02, 1.0)
        bg_node.inputs[1].default_value = 0.7

    # Key Light
    bpy.ops.object.light_add(type="AREA", location=(4.2, -4.5, 4.8))
    key_light = bpy.context.active_object
    key_light.name = "Studio_Key_Light"
    key_light.data.energy = 680.0
    key_light.data.size = 3.5
    key_light.data.color = (1.0, 0.96, 0.94)
    key_light.rotation_euler = (math.radians(48), 0, math.radians(42))

    # Crimson Rim Light
    bpy.ops.object.light_add(type="AREA", location=(-4.5, 3.8, 3.2))
    rim_light = bpy.context.active_object
    rim_light.name = "Vascular_Rim_Light"
    rim_light.data.energy = 540.0
    rim_light.data.size = 2.8
    rim_light.data.color = (0.95, 0.12, 0.32)
    rim_light.rotation_euler = (math.radians(58), 0, math.radians(-132))

    # Cool Lab Fill Light
    bpy.ops.object.light_add(type="AREA", location=(-3.2, -3.8, 2.2))
    fill_light = bpy.context.active_object
    fill_light.name = "Lab_Fill_Light"
    fill_light.data.energy = 280.0
    fill_light.data.size = 3.0
    fill_light.data.color = (0.75, 0.85, 0.95)
    fill_light.rotation_euler = (math.radians(65), 0, math.radians(-40))

    # 8. Camera Setup (Wide 36mm lens framing entire gyroscope + pedestal)
    bpy.ops.object.camera_add(location=(5.7, -6.2, 2.55), rotation=(math.radians(69), 0, math.radians(42.5)))
    cam = bpy.context.active_object
    cam.name = "Telemetry_Studio_Camera"
    cam.data.lens = 36.0
    scene.camera = cam

    # 9. Render Settings (Blender 4.2 EEVEE Next)
    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.filepath = PNG_PATH

    # Save .blend, Export .glb, and Render .png
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    bpy.ops.export_scene.gltf(
        filepath=GLB_PATH,
        export_format="GLB",
        use_selection=False,
        export_apply=True,
        export_yup=True,
        export_materials="EXPORT",
    )
    bpy.ops.render.render(write_still=True)
    print("3D_GENERATION_COMPLETE:", BLEND_PATH, GLB_PATH, PNG_PATH)


if __name__ == "__main__":
    build_biomechanical_scene()
