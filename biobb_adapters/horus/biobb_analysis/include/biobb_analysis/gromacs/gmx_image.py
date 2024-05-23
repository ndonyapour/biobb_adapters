# Import all the required classes from the HorusAPI
import shutil
from pathlib import Path
from HorusAPI import PluginBlock, PluginVariable, VariableTypes

######################
# Define INPUTS
# These variables will appear under the palced block.
# They expect to be conected to the outputs of other blocks
######################

input_traj_path = PluginVariable(
    id="input_traj_path",  # ID of the variable, will allow us to identify the value
    name="input_traj_path",  # The name that will appear in the frontend
    description='Path to the GROMACS trajectory file',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['xtc', 'trr', 'cpt', 'gro', 'g96', 'pdb', 'tng']
)

input_top_path = PluginVariable(
    id="input_top_path",  # ID of the variable, will allow us to identify the value
    name="input_top_path",  # The name that will appear in the frontend
    description='Path to the GROMACS input topology file',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['tpr', 'gro', 'g96', 'pdb', 'brk', 'ent']
)

input_index_path = PluginVariable(
    id="input_index_path",  # ID of the variable, will allow us to identify the value
    name="input_index_path",  # The name that will appear in the frontend
    description='Path to the GROMACS index file',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['ndx']
)


output_traj_path = PluginVariable(
    id="output_traj_path",  # ID of the variable, will allow us to identify the value
    name="output_traj_path",  # The name that will appear in the frontend
    description='Path to the output file',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['xtc', 'trr', 'cpt', 'gro', 'g96', 'pdb', 'tng']
)

######################
# Define Variables
# These variables appear under the block "config" button
######################

fit_selection = PluginVariable(
    id="fit_selection",
    name="fit_selection",
    description='Group where the fitting will be performed. If **input_index_path** provided, check the file for the accepted values. ',
    type=VariableTypes.STRING
)

center_selection = PluginVariable(
    id="center_selection",
    name="center_selection",
    description='Group where the trjconv will be performed. If **input_index_path** provided, check the file for the accepted values. ',
    type=VariableTypes.STRING
)

cluster_selection = PluginVariable(
    id="cluster_selection",
    name="cluster_selection",
    description='Group assigned to be the cluster, onto which all atoms are wrapped around the box, such that they are closest to the center of mass of the cluster, which is iteratively updated. If **input_index_path** provided, check the file for the accepted values. ',
    type=VariableTypes.STRING
)

output_selection = PluginVariable(
    id="output_selection",
    name="output_selection",
    description='Group that is going to be written in the output trajectory. If **input_index_path** provided, check the file for the accepted values. ',
    type=VariableTypes.STRING
)

pbc = PluginVariable(
    id="pbc",
    name="pbc",
    description='. ',
    type=VariableTypes.STRING
)

center = PluginVariable(
    id="center",
    name="center",
    description='Center atoms in box.',
    type=VariableTypes.BOOLEAN
)

ur = PluginVariable(
    id="ur",
    name="ur",
    description='Unit-cell representation. ',
    type=VariableTypes.STRING
)

fit = PluginVariable(
    id="fit",
    name="fit",
    description='Fit molecule to ref structure in the structure file. ',
    type=VariableTypes.STRING
)

binary_path = PluginVariable(
    id="binary_path",
    name="binary_path",
    description='Path to the GROMACS executable binary.',
    type=VariableTypes.STRING
)

remove_tmp = PluginVariable(
    id="remove_tmp",
    name="remove_tmp",
    description='Remove temporal files.',
    type=VariableTypes.BOOLEAN
)

restart = PluginVariable(
    id="restart",
    name="restart",
    description='Do not execute if output files exist.',
    type=VariableTypes.BOOLEAN
)

container_path = PluginVariable(
    id="container_path",
    name="container_path",
    description='Container path definition.',
    type=VariableTypes.STRING
)

container_image = PluginVariable(
    id="container_image",
    name="container_image",
    description='Container image definition.',
    type=VariableTypes.STRING
)

container_volume_path = PluginVariable(
    id="container_volume_path",
    name="container_volume_path",
    description='Container volume path definition.',
    type=VariableTypes.STRING
)

container_working_dir = PluginVariable(
    id="container_working_dir",
    name="container_working_dir",
    description='Container working directory definition.',
    type=VariableTypes.STRING
)

container_user_id = PluginVariable(
    id="container_user_id",
    name="container_user_id",
    description='Container user_id definition.',
    type=VariableTypes.STRING
)

container_shell_path = PluginVariable(
    id="container_shell_path",
    name="container_shell_path",
    description='Path to default shell inside the container.',
    type=VariableTypes.STRING
)

# Define the action that the block will perform
def gmx_image_action(biobb_block: PluginBlock):

    # It is better to have imports inside the function
    # because the environment gets cleaned up between each
    # of the blocks that run in the flow. Having the imports
    # inside will ensure integrity on the action of the block
    import subprocess
    import json

    # Obtain the variable values
    # biobb_block.inputs is just a dictionary with the ID of the variables as keys
    # and the value as the value the user enetered
    
    input_traj_path_value = biobb_block.inputs["input_traj_path"]
    
    input_top_path_value = biobb_block.inputs["input_top_path"]
    
    input_index_path_value = biobb_block.inputs["input_index_path"]
    
    
    output_traj_path_value = biobb_block.inputs["output_traj_path"]
    
    # Define the properties for the biobb tool
    properties_values = {}
    
    properties_values["fit_selection"] = biobb_block.variables["fit_selection"]
    
    properties_values["center_selection"] = biobb_block.variables["center_selection"]
    
    properties_values["cluster_selection"] = biobb_block.variables["cluster_selection"]
    
    properties_values["output_selection"] = biobb_block.variables["output_selection"]
    
    properties_values["pbc"] = biobb_block.variables["pbc"]
    
    properties_values["center"] = biobb_block.variables["center"]
    
    properties_values["ur"] = biobb_block.variables["ur"]
    
    properties_values["fit"] = biobb_block.variables["fit"]
    
    properties_values["binary_path"] = biobb_block.variables["binary_path"]
    
    properties_values["remove_tmp"] = biobb_block.variables["remove_tmp"]
    
    properties_values["restart"] = biobb_block.variables["restart"]
    
    properties_values["container_path"] = biobb_block.variables["container_path"]
    
    properties_values["container_image"] = biobb_block.variables["container_image"]
    
    properties_values["container_volume_path"] = biobb_block.variables["container_volume_path"]
    
    properties_values["container_working_dir"] = biobb_block.variables["container_working_dir"]
    
    properties_values["container_user_id"] = biobb_block.variables["container_user_id"]
    
    properties_values["container_shell_path"] = biobb_block.variables["container_shell_path"]
    
    for key in list(properties_values.keys()):
        if properties_values[key] is None:
            del properties_values[key]
    properties = {"properties": properties_values}


    with open("gmx_image.json", "w", encoding="utf-8") as f:
        json.dump(properties, f)

    # Get the executable and engine form the config
    executable = biobb_block.config["executable_path"]

    # Copy inputs to the tmp folder
    for key, value in biobb_block.inputs.items():
        if value is not None:
            if Path(value).exists():
                abs_path_out = Path(value).absolute()
                abs_path_name = Path(Path(value).name).absolute()
                if not abs_path_name.samefile(abs_path_out):
                    shutil.copy(value, f"{Path(value).name}")

    # Call the docker biobb tool
    with subprocess.Popen(
        [
            executable,
            "run",
            "-v",
            ".:/tmp",
            "quay.io/biocontainers/biobb_analysis:4.1.0--pyhdfd78af_0",
            "gmx_image",
            "--config",
            "/tmp/gmx_image.json",
            
            "--input_traj_path",
            f"/tmp/{Path(input_traj_path_value).name}",
            
            "--input_top_path",
            f"/tmp/{Path(input_top_path_value).name}",
            
            "--input_index_path",
            f"/tmp/{Path(input_index_path_value).name}",
            
            
            "--output_traj_path",
            f"/tmp/{Path(output_traj_path_value).name}",
            
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    ) as process:
        if process.stdout is not None:
            for line in process.stdout:
                # printing anything inside the block action will
                # redirect the output to the Horus integrated terminal
                print(line)

        if process.stderr is not None:
            for line in process.stderr:
                print(line)

        process.wait()

        if process.returncode != 0:
            # Raising an exception inside the block action will display the block as with an error,
            # and will display the error inside the block
            raise Exception(
                process.stderr
                if process.stderr
                else "An error ocurred while running the flow"
            )


        
        # Copy the outputs to the output folder
        abs_path_out = Path(output_traj_path_value).absolute()
        abs_path_name = Path(Path(output_traj_path_value).name).absolute()
        if not abs_path_name.samefile(abs_path_out):
            shutil.copy(f"{Path(output_traj_path_value).name}", output_traj_path_value)
        biobb_block.setOutput("output_traj_path", output_traj_path_value)
        
        # If the block has any output, one can set its value using the ID of the output variable
        # and the corresponding value


# Define the block
inputs_list = []
outputs_list = []
variables_list = []

inputs_list.append(input_traj_path)

inputs_list.append(input_top_path)

inputs_list.append(input_index_path)


outputs_list.append(output_traj_path)


variables_list.append(fit_selection)

variables_list.append(center_selection)

variables_list.append(cluster_selection)

variables_list.append(output_selection)

variables_list.append(pbc)

variables_list.append(center)

variables_list.append(ur)

variables_list.append(fit)

variables_list.append(binary_path)

variables_list.append(remove_tmp)

variables_list.append(restart)

variables_list.append(container_path)

variables_list.append(container_image)

variables_list.append(container_volume_path)

variables_list.append(container_working_dir)

variables_list.append(container_user_id)

variables_list.append(container_shell_path)


gmx_image_block = PluginBlock(
    # The name which will appear on the frontend
    name="gmx_image",
    # Its description
    description='Wrapper of the GROMACS trjconv module for correcting periodicity (image) from a given GROMACS compatible trajectory file.',
    # The action
    action=gmx_image_action,
    # A list of inputs, variables and outputs
    inputs=inputs_list + outputs_list,
    variables=variables_list,
    outputs=outputs_list,
)