# Import all the required classes from the HorusAPI
import shutil
from pathlib import Path
from HorusAPI import PluginBlock, PluginVariable, VariableTypes

######################
# Define INPUTS
# These variables will appear under the palced block.
# They expect to be conected to the outputs of other blocks
######################

input_top_zip_path = PluginVariable(
    id="input_top_zip_path",  # ID of the variable, will allow us to identify the value
    name="input_top_zip_path",  # The name that will appear in the frontend
    description='Path the input topology TOP and ITP files zipball',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['zip']
)

input_itp_path = PluginVariable(
    id="input_itp_path",  # ID of the variable, will allow us to identify the value
    name="input_itp_path",  # The name that will appear in the frontend
    description='Path to the ligand ITP file to be inserted in the topology',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['itp']
)

input_posres_itp_path = PluginVariable(
    id="input_posres_itp_path",  # ID of the variable, will allow us to identify the value
    name="input_posres_itp_path",  # The name that will appear in the frontend
    description='Path to the position restriction ITP file',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['itp']
)


output_top_zip_path = PluginVariable(
    id="output_top_zip_path",  # ID of the variable, will allow us to identify the value
    name="output_top_zip_path",  # The name that will appear in the frontend
    description='Path/Name the output topology TOP and ITP files zipball',  # The description that will appear in the frontend
    type=VariableTypes.FILE,  # The type. This will render the variable accrodingly
    # The allowedValues parameter depends on the type of variable,
    # in the case of files, they denote the allowed extensions.
    allowedValues=['zip']
)

######################
# Define Variables
# These variables appear under the block "config" button
######################

posres_name = PluginVariable(
    id="posres_name",
    name="posres_name",
    description='String to be included in the ifdef clause.',
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

# Define the action that the block will perform
def append_ligand_action(biobb_block: PluginBlock):

    # It is better to have imports inside the function
    # because the environment gets cleaned up between each
    # of the blocks that run in the flow. Having the imports
    # inside will ensure integrity on the action of the block
    import subprocess
    import json

    # Obtain the variable values
    # biobb_block.inputs is just a dictionary with the ID of the variables as keys
    # and the value as the value the user enetered
    
    input_top_zip_path_value = biobb_block.inputs["input_top_zip_path"]
    
    input_itp_path_value = biobb_block.inputs["input_itp_path"]
    
    input_posres_itp_path_value = biobb_block.inputs["input_posres_itp_path"]
    
    
    output_top_zip_path_value = biobb_block.inputs["output_top_zip_path"]
    
    # Define the properties for the biobb tool
    properties_values = {}
    
    properties_values["posres_name"] = biobb_block.variables["posres_name"]
    
    properties_values["remove_tmp"] = biobb_block.variables["remove_tmp"]
    
    properties_values["restart"] = biobb_block.variables["restart"]
    
    for key in list(properties_values.keys()):
        if properties_values[key] is None:
            del properties_values[key]
    properties = {"properties": properties_values}


    with open("append_ligand.json", "w", encoding="utf-8") as f:
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
            "quay.io/biocontainers/biobb_gromacs:4.1.1--pyhdfd78af_0",
            "append_ligand",
            "--config",
            "/tmp/append_ligand.json",
            
            "--input_top_zip_path",
            f"/tmp/{Path(input_top_zip_path_value).name}",
            
            "--input_itp_path",
            f"/tmp/{Path(input_itp_path_value).name}",
            
            "--input_posres_itp_path",
            f"/tmp/{Path(input_posres_itp_path_value).name}",
            
            
            "--output_top_zip_path",
            f"/tmp/{Path(output_top_zip_path_value).name}",
            
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
        abs_path_out = Path(output_top_zip_path_value).absolute()
        abs_path_name = Path(Path(output_top_zip_path_value).name).absolute()
        if not abs_path_name.samefile(abs_path_out):
            shutil.copy(f"{Path(output_top_zip_path_value).name}", output_top_zip_path_value)
        biobb_block.setOutput("output_top_zip_path", output_top_zip_path_value)
        
        # If the block has any output, one can set its value using the ID of the output variable
        # and the corresponding value


# Define the block
inputs_list = []
outputs_list = []
variables_list = []

inputs_list.append(input_top_zip_path)

inputs_list.append(input_itp_path)

inputs_list.append(input_posres_itp_path)


outputs_list.append(output_top_zip_path)


variables_list.append(posres_name)

variables_list.append(remove_tmp)

variables_list.append(restart)


append_ligand_block = PluginBlock(
    # The name which will appear on the frontend
    name="append_ligand",
    # Its description
    description='This class takes a ligand ITP file and inserts it in a topology.',
    # The action
    action=append_ligand_action,
    # A list of inputs, variables and outputs
    inputs=inputs_list + outputs_list,
    variables=variables_list,
    outputs=outputs_list,
)