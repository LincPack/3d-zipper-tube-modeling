import os
import tempfile
import numpy as np

from zipper_tube import Tube


def test_default_tube_properties():
    t = Tube(1.0, 2.0)  # width=1, height=2, default angles
    assert t.width == 1.0
    assert t.height == 2.0
    assert isinstance(t.alpha, float)
    assert t.num_sections == 1
    # before adding any joints, length_list should be empty
    assert t.length_list == []


def test_add_joint_and_box_coordinates(tmp_path):
    t = Tube(3.0, 4.0)
    t.add_joint(5.0, 90, 90)
    assert t.num_sections == 2
    # two boxes should have been created
    assert len(t.boxes) == 2
    # first box is at the origin, second box should have non-zero y coordinate
    second_box = t.boxes[1]
    assert np.any(second_box[:, 1] != 0)

    # verify export_panels_dxf writes files without error
    prefix = tmp_path / "pan"
    t.export_panels_dxf(filename_prefix=str(prefix), scale=1.0)
    # After calling with default single_file=False, files with index suffix should exist
    assert (tmp_path / "pan_0.dxf").exists()
    assert (tmp_path / "pan_1.dxf").exists()


def test_export_single_file(tmp_path):
    t = Tube(2.0, 2.0)
    t.add_joint(1.0, 90, 90)
    prefix = tmp_path / "single"
    t.export_panels_dxf(filename_prefix=str(prefix), scale=1.0, single_file=True)
    assert (tmp_path / "single.dxf").exists()
