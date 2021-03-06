#!/usr/bin/env python
import os

from aether.diagnostics import set_diagnostics_on
from aether.indices import ventilation_indices, get_ne_radius
from aether.geometry import define_node_geometry, define_1d_elements, define_rad_from_file, append_units
from aether.ventilation import evaluate_vent
from aether.exports import export_1d_elem_geometry, export_node_geometry, export_elem_field, export_1d_elem_field, export_terminal_solution

from pulmonary.utils.io_files import get_default_output_path, get_default_geometry_path


def main():
    set_diagnostics_on(False)

    # Read settings
    ventilation_indices()

    define_node_geometry(get_default_geometry_path('SmallTree.ipnode'))
    define_1d_elements(get_default_geometry_path('SmallTree.ipelem'))
    define_rad_from_file(get_default_geometry_path('SmallTree.ipfiel'))
    append_units()

    # Set the working directory to the this files directory and then reset after running simulation.
    file_location = os.path.dirname(os.path.abspath(__file__))
    cur_dir = os.getcwd()
    os.chdir(file_location)

    # Run simulation.
    evaluate_vent()

    # Set the working directory back to it's original location.
    os.chdir(cur_dir)

    # Output results
    # Export airway nodes and elements
    group_name = 'vent_model'
    export_1d_elem_geometry(get_default_output_path('small_tree.exelem'), group_name)
    export_node_geometry(get_default_output_path('small_tree.exnode'), group_name)

    # Export flow element
    field_name = 'flow'
    export_elem_field(get_default_output_path('ventilation_fields.exelem'), group_name, field_name)

    # Export element field for radius
    ne_radius = get_ne_radius()
    field_name = 'radius'
    export_1d_elem_field(ne_radius, get_default_output_path('ventilation_radius_field.exelem'), group_name, field_name)

    # Export terminal solution
    export_terminal_solution(get_default_output_path('terminal.exnode'), group_name)


if __name__ == '__main__':
    main()
