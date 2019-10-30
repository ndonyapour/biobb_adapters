#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: extract_heteroatoms
hints:
  DockerRequirement:
    dockerPull: mmbirb/biobb_structure_utils:latest
inputs:
  input_structure_path:
    type: File
    inputBinding:
      position: 1
      prefix: --input_structure_path

  output_heteroatom_path:
    type: string
    inputBinding:
      position: 2
      prefix: --output_heteroatom_path
    default: "output.pdb"

  config:
    type: string?
    inputBinding:
      position: 3
      prefix: --config

outputs:

  output_heteroatom_file:
    type: File
    outputBinding:
      glob: $(inputs.output_heteroatom_path)

$namespaces:
  edam: http://edamontology.org/
$schemas:
  - http://edamontology.org/EDAM_1.22.owl
