# Import all the required classes from the HorusAPI
import shutil
from pathlib import Path
from HorusAPI import PluginBlock, PluginVariable, VariableTypes

######################
# Define INPUTS
# These variables will appear under the palced block.
# They expect to be conected to the outputs of other blocks
######################

input_path = PluginVariable(
    id="input_path",  # ID of the variable, will allow us to identify the value
    name="input_path",  # The name that will appear in the frontend
    description='Path to the input file',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['dat', 'ent', 'fa', 'fasta', 'gro', 'inp', 'log', 'mcif', 'mdl', 'mmcif', 'mol', 'mol2', 'pdb', 'pdbqt', 'png', 'sdf', 'smi', 'smiles', 'txt', 'xml', 'xtc']
)


output_path = PluginVariable(
    id="output_path",  # ID of the variable, will allow us to identify the value
    name="output_path",  # The name that will appear in the frontend
    description='Path to the output file',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['ent', 'fa', 'fasta', 'gro', 'inp', 'mcif', 'mdl', 'mmcif', 'mol', 'mol2', 'pdb', 'pdbqt', 'png', 'sdf', 'smi', 'smiles', 'txt']
)

######################
# Define Variables
# These variables appear under the block "config" button
######################

input_format = PluginVariable(
    id="input_format",
    name="input_format",
    description='Format of input file. If not provided, input_path extension will be taken. ',
    type=VariableTypes.STRING
)

output_format = PluginVariable(
    id="output_format",
    name="output_format",
    description='Format of output file. If not provided, output_path extension will be taken. ',
    type=VariableTypes.STRING
)

coordinates = PluginVariable(
    id="coordinates",
    name="coordinates",
    description='Type of coordinates: 2D or 3D. ',
    type=VariableTypes.INTEGER
)

ph = PluginVariable(
    id="ph",
    name="ph",
    description='Add hydrogens appropriate for pH.',
    type=VariableTypes.NUMBER
)

flex = PluginVariable(
    id="flex",
    name="flex",
    description='Remove all but the largest contiguous fragment (strip salts).',
    type=VariableTypes.BOOLEAN
)

binary_path = PluginVariable(
    id="binary_path",
    name="binary_path",
    description='Path to the obabel executable binary.',
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
def babel_convert_action(biobb_block: PluginBlock):

    # It is better to have imports inside the function
    # because the environment gets cleaned up between each
    # of the blocks that run in the flow. Having the imports
    # inside will ensure integrity on the action of the block
    import subprocess
    import json

    # Obtain the variable values
    # biobb_block.inputs is just a dictionary with the ID of the variables as keys
    # and the value as the value the user enetered
    
    input_path_value = biobb_block.inputs["input_path"]
    
    
    output_path_value = biobb_block.inputs["output_path"]
    
    # Define the properties for the biobb tool
    properties_values = {}
    
    properties_values["input_format"] = biobb_block.variables["input_format"]
    
    properties_values["output_format"] = biobb_block.variables["output_format"]
    
    properties_values["coordinates"] = biobb_block.variables["coordinates"]
    
    properties_values["ph"] = biobb_block.variables["ph"]
    
    properties_values["flex"] = biobb_block.variables["flex"]
    
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


    with open("babel_convert.json", "w", encoding="utf-8") as f:
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
            "quay.io/biocontainers/biobb_chemistry:4.1.0--pyhdfd78af_0",
            "babel_convert",
            "--config",
            "/tmp/babel_convert.json",
            
            "--input_path",
            f"/tmp/{Path(input_path_value).name}",
            
            
            "--output_path",
            f"/tmp/{Path(output_path_value).name}",
            
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
        abs_path_out = Path(output_path_value).absolute()
        abs_path_name = Path(Path(output_path_value).name).absolute()
        if not abs_path_name.samefile(abs_path_out):
            shutil.copy(f"{Path(output_path_value).name}", output_path_value)
        biobb_block.setOutput("output_path", output_path_value)
        
        # If the block has any output, one can set its value using the ID of the output variable
        # and the corresponding value


# Define the block
inputs_list = []
outputs_list = []
variables_list = []

inputs_list.append(input_path)


outputs_list.append(output_path)


variables_list.append(input_format)

variables_list.append(output_format)

variables_list.append(coordinates)

variables_list.append(ph)

variables_list.append(flex)

variables_list.append(binary_path)

variables_list.append(remove_tmp)

variables_list.append(restart)

variables_list.append(container_path)

variables_list.append(container_image)

variables_list.append(container_volume_path)

variables_list.append(container_working_dir)

variables_list.append(container_user_id)

variables_list.append(container_shell_path)


babel_convert_block = PluginBlock(
    # The name which will appear on the frontend
    name="babel_convert",
    # Its description
    description='This class is a wrapper of the Open Babel tool.',
    # The action
    action=babel_convert_action,
    # A list of inputs, variables and outputs
    inputs=inputs_list + outputs_list,
    variables=variables_list,
    outputs=outputs_list,
)