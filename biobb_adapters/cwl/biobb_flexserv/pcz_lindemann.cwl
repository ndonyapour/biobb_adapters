#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Extract Lindemann coefficient (an estimate of the solid-liquid behaviour of
  a protein) from a compressed PCZ file.

doc: |-
  Wrapper of the pczdump tool from the PCAsuite FlexServ module.

baseCommand: pcz_lindemann

hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/biobb_flexserv:4.2.0--pypl5321hdfd78af_0

inputs:
  input_pcz_path:
    label: Input compressed trajectory file
    doc: |-
      Input compressed trajectory file
      Type: string
      File type: input
      Accepted formats: pcz
      Example file: https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/data/pcasuite/pcazip.pcz
    type: File
    format:
    - edam:format_3874
    inputBinding:
      position: 1
      prefix: --input_pcz_path

  output_json_path:
    label: Output json file with PCA Eigen Vectors
    doc: |-
      Output json file with PCA Eigen Vectors
      Type: string
      File type: output
      Accepted formats: json
      Example file: https://github.com/bioexcel/biobb_flexserv/raw/master/biobb_flexserv/test/reference/pcasuite/pcz_lindemann.json
    type: string
    format:
    - edam:format_3464
    inputBinding:
      position: 2
      prefix: --output_json_path
    default: system.json

  config:
    label: Advanced configuration options for biobb_flexserv PCZlindemann
    doc: |-
      Advanced configuration options for biobb_flexserv PCZlindemann. This should be passed as a string containing a dict. The possible options to include here are listed under 'properties' in the biobb_flexserv PCZlindemann documentation: https://biobb-flexserv.readthedocs.io/en/latest/pcasuite.html#module-pcasuite.pcz_lindemann
    type: string?
    inputBinding:
      prefix: --config

outputs:
  output_json_path:
    label: Output json file with PCA Eigen Vectors
    doc: |-
      Output json file with PCA Eigen Vectors
    type: File
    outputBinding:
      glob: $(inputs.output_json_path)
    format: edam:format_3464

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl
