#!/usr/bin/env cwl-runner
cwlVersion: v1.0

class: CommandLineTool

label: Calculate correlation between helical parameters for a single inter-base pair.

doc: |-
  None

baseCommand: interhpcorr

hints:
  DockerRequirement:
    dockerPull: quay.io/biocontainers/biobb_dna:3.8.2--pyhdfd78af_1

inputs:
  input_filename_shift:
    label: Path to .csv file with data for helical parameter 'shift'
    doc: |-
      Path to .csv file with data for helical parameter 'shift'
      Type: string
      File type: input
      Accepted formats: csv
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_shift_AA.csv
    type: File
    format:
    - edam:format_3752
    inputBinding:
      position: 1
      prefix: --input_filename_shift

  input_filename_slide:
    label: Path to .csv file with data for helical parameter 'slide'
    doc: |-
      Path to .csv file with data for helical parameter 'slide'
      Type: string
      File type: input
      Accepted formats: csv
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_slide_AA.csv
    type: File
    format:
    - edam:format_3752
    inputBinding:
      position: 2
      prefix: --input_filename_slide

  input_filename_rise:
    label: Path to .csv file with data for helical parameter 'rise'
    doc: |-
      Path to .csv file with data for helical parameter 'rise'
      Type: string
      File type: input
      Accepted formats: csv
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_rise_AA.csv
    type: File
    format:
    - edam:format_3752
    inputBinding:
      position: 3
      prefix: --input_filename_rise

  input_filename_tilt:
    label: Path to .csv file with data for helical parameter 'tilt'
    doc: |-
      Path to .csv file with data for helical parameter 'tilt'
      Type: string
      File type: input
      Accepted formats: csv
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_tilt_AA.csv
    type: File
    format:
    - edam:format_3752
    inputBinding:
      position: 4
      prefix: --input_filename_tilt

  input_filename_roll:
    label: Path to .csv file with data for helical parameter 'roll'
    doc: |-
      Path to .csv file with data for helical parameter 'roll'
      Type: string
      File type: input
      Accepted formats: csv
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_roll_AA.csv
    type: File
    format:
    - edam:format_3752
    inputBinding:
      position: 5
      prefix: --input_filename_roll

  input_filename_twist:
    label: Path to .csv file with data for helical parameter 'twist'
    doc: |-
      Path to .csv file with data for helical parameter 'twist'
      Type: string
      File type: input
      Accepted formats: csv
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/data/stiffness/series_twist_AA.csv
    type: File
    format:
    - edam:format_3752
    inputBinding:
      position: 6
      prefix: --input_filename_twist

  output_csv_path:
    label: Path to directory where output is saved
    doc: |-
      Path to directory where output is saved
      Type: string
      File type: output
      Accepted formats: csv
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/inter_hpcorr_ref.csv
    type: string
    format:
    - edam:format_3752
    inputBinding:
      position: 7
      prefix: --output_csv_path
    default: system.csv

  output_jpg_path:
    label: Path to .jpg file where output is saved
    doc: |-
      Path to .jpg file where output is saved
      Type: string
      File type: output
      Accepted formats: jpg
      Example file: https://raw.githubusercontent.com/bioexcel/biobb_dna/master/biobb_dna/test/reference/correlation/inter_hpcorr_ref.jpg
    type: string
    format:
    - edam:format_3579
    inputBinding:
      position: 8
      prefix: --output_jpg_path
    default: system.jpg

  config:
    label: Advanced configuration options for biobb_dna InterHelParCorrelation
    doc: |-
      Advanced configuration options for biobb_dna InterHelParCorrelation. This should be passed as a string containing a dict. The possible options to include here are listed under 'properties' in the biobb_dna InterHelParCorrelation documentation: https://biobb-dna.readthedocs.io/en/latest/interbp_correlations.html#interbp-correlations-interhpcorr-module
    type: string?
    inputBinding:
      prefix: --config

outputs:
  output_csv_path:
    label: Path to directory where output is saved
    doc: |-
      Path to directory where output is saved
    type: File
    outputBinding:
      glob: $(inputs.output_csv_path)
    format: edam:format_3752

  output_jpg_path:
    label: Path to .jpg file where output is saved
    doc: |-
      Path to .jpg file where output is saved
    type: File
    outputBinding:
      glob: $(inputs.output_jpg_path)
    format: edam:format_3579

$namespaces:
  edam: https://edamontology.org/

$schemas:
- https://raw.githubusercontent.com/edamontology/edamontology/master/EDAM_dev.owl