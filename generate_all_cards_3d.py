"""
Blender 4.2 Procedural 3D Icon & Hero Sculpture Studio Generator
Generates high-resolution transparent RGBA 3D renders (BLENDER_EEVEE_NEXT)
for all 7 Workout Holo Cards (day_1_3d.png .. day_7_3d.png) and 3 Hero Slides.
"""

import bpy
import math
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets3d")
os.makedirs(OUT_DIR, exist_ok=True)


def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def create_mat(name, base_color, metallic=0.8, roughness=0.22, emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = base_color
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Roughness"].default_value = roughness
        if emission_color is not None and "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = emission_color
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def build_palette():
    return {
        "chrome": create_mat("Chrome", (0.86, 0.89, 0.93, 1.0), metallic=0.96, roughness=0.12),
        "obsidian": create_mat("Obsidian", (0.045, 0.048, 0.055, 1.0), metallic=0.45, roughness=0.26),
        "rubber": create_mat("Rubber", (0.025, 0.026, 0.03, 1.0), metallic=0.1, roughness=0.65),
        "crimson_anodized": create_mat(
            "CrimsonAnodized",
            (0.55, 0.025, 0.13, 1.0),
            metallic=0.84,
            roughness=0.18,
            emission_color=(0.75, 0.03, 0.18, 1.0),
            emission_strength=0.15,
        ),
        "crimson_glow": create_mat(
            "CrimsonGlow",
            (0.85, 0.05, 0.22, 1.0),
            metallic=0.3,
            roughness=0.15,
            emission_color=(0.95, 0.08, 0.28, 1.0),
            emission_strength=2.6,
        ),
        "olive_metal": create_mat("OliveMetal", (0.26, 0.31, 0.22, 1.0), metallic=0.78, roughness=0.22),
        "emerald_glow": create_mat(
            "EmeraldGlow",
            (0.32, 0.58, 0.36, 1.0),
            metallic=0.4,
            roughness=0.18,
            emission_color=(0.42, 0.78, 0.45, 1.0),
            emission_strength=1.8,
        ),
        "gold_brass": create_mat("GoldBrass", (0.94, 0.74, 0.28, 1.0), metallic=0.94, roughness=0.15),
        "hydro_cyan": create_mat(
            "HydroCyan",
            (0.25, 0.72, 0.88, 1.0),
            metallic=0.65,
            roughness=0.12,
            emission_color=(0.25, 0.78, 0.95, 1.0),
            emission_strength=1.4,
        ),
    }


def setup_studio_lights_and_cam(res_x=860, res_y=760, cam_loc=(4.2, -4.6, 2.2), cam_rot=(66, 0, 42), lens=42.0):
    scene = bpy.context.scene
    world = bpy.data.worlds.new("CardStudioWorld")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.04, 0.045, 0.05, 1.0)
        bg.inputs[1].default_value = 0.9

    # Warm Key Light
    bpy.ops.object.light_add(type="AREA", location=(3.8, -3.8, 4.2))
    kl = bpy.context.active_object
    kl.data.energy = 620.0
    kl.data.size = 3.2
    kl.data.color = (1.0, 0.97, 0.94)
    kl.rotation_euler = (math.radians(46), 0, math.radians(42))

    # Crimson Rim Light
    bpy.ops.object.light_add(type="AREA", location=(-3.8, 3.4, 2.8))
    rl = bpy.context.active_object
    rl.data.energy = 540.0
    rl.data.size = 2.6
    rl.data.color = (0.98, 0.14, 0.34)
    rl.rotation_euler = (math.radians(58), 0, math.radians(-135))

    # Cool Top/Side Fill Light
    bpy.ops.object.light_add(type="AREA", location=(-3.0, -3.2, 3.0))
    fl = bpy.context.active_object
    fl.data.energy = 340.0
    fl.data.size = 3.0
    fl.data.color = (0.78, 0.88, 1.0)
    fl.rotation_euler = (math.radians(52), 0, math.radians(-42))

    # Camera
    bpy.ops.object.camera_add(
        location=cam_loc,
        rotation=(math.radians(cam_rot[0]), math.radians(cam_rot[1]), math.radians(cam_rot[2])),
    )
    cam = bpy.context.active_object
    cam.data.lens = lens
    scene.camera = cam

    scene.render.engine = "BLENDER_EEVEE_NEXT"
    scene.render.film_transparent = True
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"


def add_base_platform(pal, accent_mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=2.35, depth=0.14, location=(0, 0, -1.25))
    base = bpy.context.active_object
    base.data.materials.append(pal["obsidian"])
    bpy.ops.object.shade_smooth()

    bpy.ops.mesh.primitive_torus_add(
        major_radius=2.18, minor_radius=0.025, major_segments=96, minor_segments=24, location=(0, 0, -1.17)
    )
    ring = bpy.context.active_object
    ring.data.materials.append(accent_mat)
    bpy.ops.object.shade_smooth()


def render_to(filename):
    out_path = os.path.join(OUT_DIR, filename)
    bpy.context.scene.render.filepath = out_path
    bpy.ops.render.render(write_still=True)
    print("Rendered:", out_path)


# ============================================================================
# DAY 1: MONDAY — BARBELL HIP THRUST & HORIZONTAL VECTOR GYRO (90° TIBIA)
# ============================================================================
def build_day_1():
    clear_scene()
    pal = build_palette()
    setup_studio_lights_and_cam(cam_loc=(4.1, -4.4, 2.05), cam_rot=(67, 0, 42), lens=43)
    add_base_platform(pal, pal["crimson_glow"])

    # Horizontal Vector Torque Ring
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.68,
        minor_radius=0.042,
        major_segments=96,
        minor_segments=32,
        location=(0, 0, 0.1),
        rotation=(math.radians(90), 0, math.radians(16)),
    )
    bpy.context.active_object.data.materials.append(pal["crimson_glow"])
    bpy.ops.object.shade_smooth()

    # Secondary Knee-Safe 90-Deg Calibration Ring
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.35,
        minor_radius=0.032,
        major_segments=96,
        minor_segments=24,
        location=(0, 0, 0.1),
        rotation=(math.radians(32), math.radians(40), 0),
    )
    bpy.context.active_object.data.materials.append(pal["olive_metal"])
    bpy.ops.object.shade_smooth()

    # Olympic Barbell + Hip Pad + Calibrated Plates
    az = math.radians(16)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=48, radius=0.042, depth=3.6, location=(0, 0, 0.1), rotation=(0, math.radians(90), az)
    )
    bpy.context.active_object.data.materials.append(pal["chrome"])
    bpy.ops.object.shade_smooth()

    # Protective Hip Thrust Foam Pad in Center
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=48, radius=0.13, depth=0.95, location=(0, 0, 0.1), rotation=(0, math.radians(90), az)
    )
    bpy.context.active_object.data.materials.append(pal["crimson_anodized"])
    bpy.ops.object.shade_smooth()

    # Bumper Plates
    for side in (-1, 1):
        for idx, (dist, rad, mat_key) in enumerate(
            [(1.02, 0.68, "crimson_anodized"), (1.16, 0.58, "rubber"), (1.28, 0.48, "crimson_anodized")]
        ):
            px = side * dist * math.cos(az)
            py = side * dist * math.sin(az)
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=64, radius=rad, depth=0.10, location=(px, py, 0.1), rotation=(0, math.radians(90), az)
            )
            bpy.context.active_object.data.materials.append(pal[mat_key])
            bpy.ops.object.shade_smooth()

    # Golden Knee-Safe Pivot Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.14, location=(0.0, -0.45, 0.55))
    bpy.context.active_object.data.materials.append(pal["gold_brass"])
    bpy.ops.object.shade_smooth()

    render_to("day_1_3d.png")


# ============================================================================
# DAY 2: TUESDAY — UPPER V-TAPER, DUMBBELLS & VASCULAR HELIX
# ============================================================================
def build_day_2():
    clear_scene()
    pal = build_palette()
    setup_studio_lights_and_cam(cam_loc=(4.0, -4.3, 2.15), cam_rot=(66, 0, 43), lens=44)
    add_base_platform(pal, pal["crimson_glow"])

    # V-Taper Lat Wings Frame (Two angled metallic arches)
    for side in (-1, 1):
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=36,
            radius=0.055,
            depth=2.3,
            location=(side * 0.72, 0.15, 0.15),
            rotation=(0, math.radians(side * 28), 0),
        )
        bpy.context.active_object.data.materials.append(pal["crimson_glow"])
        bpy.ops.object.shade_smooth()

    # Crossed Pro Dumbbells (Brachioradialis Hammer/Reverse Curl + Lateral Raise)
    for angle_deg, z_pos in [(-24, 0.32), (24, -0.18)]:
        rz = math.radians(angle_deg)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=32, radius=0.045, depth=1.65, location=(0, 0, z_pos), rotation=(0, math.radians(90), rz)
        )
        bpy.context.active_object.data.materials.append(pal["chrome"])
        bpy.ops.object.shade_smooth()

        for side in (-1, 1):
            for d_off, rad, mkey in [(0.55, 0.36, "obsidian"), (0.68, 0.30, "crimson_anodized")]:
                px = side * d_off * math.cos(rz)
                py = side * d_off * math.sin(rz)
                bpy.ops.mesh.primitive_cylinder_add(
                    vertices=8,
                    radius=rad,
                    depth=0.11,
                    location=(px, py, z_pos),
                    rotation=(0, math.radians(90), rz),
                )
                bpy.context.active_object.data.materials.append(pal[mkey])

    # Vascular Pump Outer Gyro Ring
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.65,
        minor_radius=0.038,
        major_segments=96,
        minor_segments=24,
        location=(0, 0, 0.12),
        rotation=(math.radians(72), math.radians(-18), math.radians(20)),
    )
    bpy.context.active_object.data.materials.append(pal["chrome"])
    bpy.ops.object.shade_smooth()

    render_to("day_2_3d.png")


# ============================================================================
# DAY 3: WEDNESDAY — RDL HIP-HINGE & SEATED HAMSTRING STRETCH CAM (MAEO 2021)
# ============================================================================
def build_day_3():
    clear_scene()
    pal = build_palette()
    setup_studio_lights_and_cam(cam_loc=(4.1, -4.4, 2.1), cam_rot=(66, 0, 42), lens=43)
    add_base_platform(pal, pal["emerald_glow"])

    # Eccentric Cam-Pulley Wheel (Seated Flexor Resistance Profile)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,
        radius=1.15,
        depth=0.16,
        location=(-0.25, 0.2, 0.22),
        rotation=(math.radians(90), 0, math.radians(25)),
    )
    bpy.context.active_object.data.materials.append(pal["olive_metal"])
    bpy.ops.object.shade_smooth()

    # Glowing Lengthened-Tension Rim around Cam
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.22,
        minor_radius=0.045,
        major_segments=96,
        minor_segments=32,
        location=(-0.25, 0.2, 0.22),
        rotation=(math.radians(90), 0, math.radians(25)),
    )
    bpy.context.active_object.data.materials.append(pal["crimson_glow"])
    bpy.ops.object.shade_smooth()

    # Hip-Hinge Lever Arms (Femur + Torso Hinge Vector at 85 deg)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=0.075,
        depth=1.8,
        location=(0.35, -0.25, 0.45),
        rotation=(math.radians(45), math.radians(-35), math.radians(15)),
    )
    bpy.context.active_object.data.materials.append(pal["chrome"])
    bpy.ops.object.shade_smooth()

    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32,
        radius=0.075,
        depth=1.6,
        location=(0.1, -0.25, -0.35),
        rotation=(math.radians(-18), math.radians(12), 0),
    )
    bpy.context.active_object.data.materials.append(pal["chrome"])
    bpy.ops.object.shade_smooth()

    # Golden Hip-Hinge Fulcrum Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.22, location=(-0.1, -0.25, 0.1))
    bpy.context.active_object.data.materials.append(pal["gold_brass"])
    bpy.ops.object.shade_smooth()

    # Outer Lengthened Partial Orbit
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.68,
        minor_radius=0.032,
        major_segments=96,
        minor_segments=24,
        location=(0, 0, 0.15),
        rotation=(math.radians(42), math.radians(28), 0),
    )
    bpy.context.active_object.data.materials.append(pal["emerald_glow"])
    bpy.ops.object.shade_smooth()

    render_to("day_3_3d.png")


# ============================================================================
# DAY 4: THURSDAY — UPPER VASCULAR B & HEAVY KETTLEBELL / FARMER WALK
# ============================================================================
def build_day_4():
    clear_scene()
    pal = build_palette()
    setup_studio_lights_and_cam(cam_loc=(4.0, -4.3, 2.05), cam_rot=(67, 0, 42), lens=44)
    add_base_platform(pal, pal["crimson_glow"])

    # Pair of 3D Competition Kettlebells (Farmer's Walk Forearm Vascularity)
    for side, x_pos, y_pos, rot_z in [(-1, -0.62, 0.12, 18), (1, 0.62, -0.18, -22)]:
        # Kettlebell Body Sphere
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=48, ring_count=32, radius=0.56, location=(x_pos, y_pos, -0.35)
        )
        kb = bpy.context.active_object
        kb.data.materials.append(pal["crimson_anodized"] if side == 1 else pal["obsidian"])
        bpy.ops.object.shade_smooth()

        # Kettlebell Chrome Handle Torus
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.36,
            minor_radius=0.068,
            major_segments=48,
            minor_segments=24,
            location=(x_pos, y_pos, 0.22),
            rotation=(math.radians(90), 0, math.radians(rot_z)),
        )
        handle = bpy.context.active_object
        handle.data.materials.append(pal["chrome"])
        bpy.ops.object.shade_smooth()

    # Reactive Hyperemia / eNOS Vascular Pulse Rings above
    for z_h, rad, mkey in [(0.65, 1.35, "crimson_glow"), (0.95, 0.95, "gold_brass")]:
        bpy.ops.mesh.primitive_torus_add(
            major_radius=rad,
            minor_radius=0.035,
            major_segments=96,
            minor_segments=24,
            location=(0, 0, z_h),
            rotation=(math.radians(18), math.radians(-14), 0),
        )
        bpy.context.active_object.data.materials.append(pal[mkey])
        bpy.ops.object.shade_smooth()

    render_to("day_4_3d.png")


# ============================================================================
# DAY 5: FRIDAY — 3D GLUTE SYNTHESIS (3-VECTOR GEODESIC GYROSCOPE)
# ============================================================================
def build_day_5():
    clear_scene()
    pal = build_palette()
    setup_studio_lights_and_cam(cam_loc=(4.0, -4.3, 2.15), cam_rot=(66, 0, 42), lens=44)
    add_base_platform(pal, pal["crimson_glow"])

    # 3 Orthogonal Biomechanical Vector Rings (Horizontal, Axial, 30° Frontal Abduction)
    rings = [
        (1.68, 0.052, (90, 0, 15), "crimson_glow"),
        (1.42, 0.048, (35, 55, 0), "olive_metal"),
        (1.16, 0.044, (60, -45, 30), "chrome"),
    ]
    for mr, mnr, rot, mkey in rings:
        bpy.ops.mesh.primitive_torus_add(
            major_radius=mr,
            minor_radius=mnr,
            major_segments=96,
            minor_segments=32,
            location=(0, 0, 0.18),
            rotation=(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2])),
        )
        bpy.context.active_object.data.materials.append(pal[mkey])
        bpy.ops.object.shade_smooth()

    # Central 3D Glute Synthesis Core (Anodized Crimson Faceted Icosahedron + Gold Orbit)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.58, location=(0, 0, 0.18))
    core = bpy.context.active_object
    core.data.materials.append(pal["crimson_anodized"])

    bpy.ops.mesh.primitive_torus_add(
        major_radius=0.76,
        minor_radius=0.032,
        major_segments=64,
        minor_segments=24,
        location=(0, 0, 0.18),
        rotation=(math.radians(20), math.radians(20), 0),
    )
    bpy.context.active_object.data.materials.append(pal["gold_brass"])
    bpy.ops.object.shade_smooth()

    render_to("day_5_3d.png")


# ============================================================================
# DAY 6: SATURDAY (HOME) — METABOLIC OCCLUSION BAND & ISOMETRIC CORE
# ============================================================================
def build_day_6():
    clear_scene()
    pal = build_palette()
    setup_studio_lights_and_cam(cam_loc=(4.0, -4.3, 2.1), cam_rot=(66, 0, 42), lens=44)
    add_base_platform(pal, pal["gold_brass"])

    # Thick 3D Elastic Resistance Band Ribbon (Sculpted Wide Torus)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.35,
        minor_radius=0.22,
        major_segments=96,
        minor_segments=32,
        location=(0, 0, 0.12),
        rotation=(math.radians(28), math.radians(-22), math.radians(15)),
    )
    band = bpy.context.active_object
    band.scale = (1.0, 1.0, 0.55)
    band.data.materials.append(pal["crimson_anodized"])
    bpy.ops.object.shade_smooth()

    # Concentric Metabolic Pump & Capillary Glow Rings
    for r_maj, rot_x, mkey in [(1.65, 75, "gold_brass"), (0.92, -40, "crimson_glow")]:
        bpy.ops.mesh.primitive_torus_add(
            major_radius=r_maj,
            minor_radius=0.038,
            major_segments=96,
            minor_segments=24,
            location=(0, 0, 0.12),
            rotation=(math.radians(rot_x), math.radians(25), 0),
        )
        bpy.context.active_object.data.materials.append(pal[mkey])
        bpy.ops.object.shade_smooth()

    # Zero-Impact Floating Joint-Safe Core Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.46, location=(0, 0, 0.12))
    bpy.context.active_object.data.materials.append(pal["chrome"])
    bpy.ops.object.shade_smooth()

    render_to("day_6_3d.png")


# ============================================================================
# DAY 7: SUNDAY — SYSTEMIC SUPERCOMPENSATION, MYOFIBRILLAR HELIX & 3L HYDRO
# ============================================================================
def build_day_7():
    clear_scene()
    pal = build_palette()
    setup_studio_lights_and_cam(cam_loc=(4.0, -4.3, 2.1), cam_rot=(66, 0, 42), lens=44)
    add_base_platform(pal, pal["hydro_cyan"])

    # Central Plasma Hydration & Glycogen Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.58, location=(0, 0, 0.15))
    bpy.context.active_object.data.materials.append(pal["hydro_cyan"])
    bpy.ops.object.shade_smooth()

    # Double-Helix Myofibrillar Protein Synthesis Nodes around the Core
    num_nodes = 14
    for i in range(num_nodes):
        t = (i / num_nodes) * math.pi * 2.0
        z = -0.65 + (i / num_nodes) * 1.65
        for strand, mkey in [(0, "emerald_glow"), (math.pi, "chrome")]:
            x = 1.25 * math.cos(t + strand)
            y = 1.25 * math.sin(t + strand)
            bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.11, location=(x, y, z))
            bpy.context.active_object.data.materials.append(pal[mkey])
            bpy.ops.object.shade_smooth()

    # Calm Recovery Orbit Ring
    bpy.ops.mesh.primitive_torus_add(
        major_radius=1.62,
        minor_radius=0.035,
        major_segments=96,
        minor_segments=24,
        location=(0, 0, 0.15),
        rotation=(math.radians(65), math.radians(20), 0),
    )
    bpy.context.active_object.data.materials.append(pal["emerald_glow"])
    bpy.ops.object.shade_smooth()

    render_to("day_7_3d.png")


if __name__ == "__main__":
    build_day_1()
    build_day_2()
    build_day_3()
    build_day_4()
    build_day_5()
    build_day_6()
    build_day_7()
    print("ALL_7_3D_CARDS_COMPLETE")
