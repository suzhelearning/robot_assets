"""Extract wrist-rooted retargeting hands from the canonical full robot URDF.

Run with project Python. Optimizer configuration and vendored algorithms are
never rewritten; only the model resources and their provenance are generated.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

PACKAGE = Path(__file__).resolve().parent
REPO = PACKAGE.parents[3]
SOURCE = PACKAGE.parents[1] / "simulation/tianji_wuji2/urdf/tianji_wuji2.urdf"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = ET.parse(SOURCE).getroot()
    links = {link.get("name"): link for link in source.findall("link")}
    joints = source.findall("joint")
    previous = json.loads((PACKAGE / "source_manifest.json").read_text())
    files, hands = [], {}
    for side, prefix in (("left", "l_"), ("right", "r_")):
        root = prefix + "wrist"
        names = {root}
        pending = [root]
        while pending:
            parent = pending.pop()
            for joint in joints:
                if joint.find("parent").get("link") == parent:
                    child = joint.find("child").get("link")
                    if child in names:
                        raise ValueError(f"hand tree contains a cycle or duplicate: {child}")
                    names.add(child)
                    pending.append(child)
        selected = [joint for joint in joints
                    if joint.find("parent").get("link") in names]
        active = [joint for joint in selected if joint.get("type") != "fixed"]
        if len(active) != 20 or any(joint.get("type") != "revolute" for joint in active):
            raise ValueError(f"{side} must retain the existing 20-DOF hand contract")
        hand = ET.Element("robot", name=f"wujihand2-{side}")
        mesh_records = {}
        for name, source_link in links.items():
            if name not in names:
                continue
            link = deepcopy(source_link)
            for mesh in link.findall(".//mesh"):
                mesh_source = (SOURCE.parent / mesh.get("filename")).resolve(strict=True)
                if not mesh_source.is_relative_to(SOURCE.parent.parent / "meshes"):
                    raise ValueError(f"mesh escapes source package: {mesh_source}")
                destination = Path("meshes") / side / mesh_source.name
                target = PACKAGE / destination
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(mesh_source, target)
                mesh.set("filename", "../" + destination.as_posix())
                mesh_records[destination.as_posix()] = {
                    "source": str(mesh_source.relative_to(REPO)),
                    "destination": destination.as_posix(), "sha256": sha256(target),
                }
            hand.append(link)
        for joint in selected:
            hand.append(deepcopy(joint))
        ET.indent(hand, space="  ")
        target = PACKAGE / "urdf" / f"{side}.urdf"
        target.write_bytes(ET.tostring(hand, encoding="utf-8", xml_declaration=True) + b"\n")
        files.append({"source": str(SOURCE.relative_to(REPO)),
                      "source_root_link": root, "destination": str(target.relative_to(PACKAGE)),
                      "sha256": sha256(target)})
        files.extend(mesh_records[name] for name in sorted(mesh_records))
        hands[side] = {"root": root, "links": len(names), "joints": len(selected),
                       "active_joints": len(active), "meshes": len(mesh_records)}
    legacy = previous.get("legacy_beta1_provenance", previous)
    manifest = {
        "purpose": "Latest wrist-rooted hand models for the unchanged native retargeter.",
        "implementation": "scripts/wuji_hand_native/third_party/wuji_hand_retargeting",
        "source_urdf": str(SOURCE.relative_to(REPO)),
        "source_urdf_sha256": sha256(SOURCE),
        "model_integrity": "Complete wrist subtrees copied without changing joint origins, axes, limits, inertias or tip/IMU frames; only mesh paths are rewritten. Upstream mounting frames and arms are excluded to preserve the optimizer's wrist-local input convention.",
        "model_license": "User-provided full robot package has no separate license declaration. Existing LICENSE and legacy provenance are retained, not asserted as a new model license.",
        "runtime_configuration": "config/{left,right}.yaml and all optimizer parameters remain unchanged; each new worker loads the selected URDF and derives geometry and limits at startup.",
        "hands": hands,
        "files": files,
        "legacy_beta1_provenance": legacy,
    }
    (PACKAGE / "source_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"source_urdf_sha256": manifest["source_urdf_sha256"], "hands": hands}, indent=2))


if __name__ == "__main__":
    main()
