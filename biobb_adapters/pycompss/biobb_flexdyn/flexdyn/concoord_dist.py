# Python
import os
import sys
import traceback
# Pycompss
from pycompss.api.task import task
from pycompss.api.parameter import FILE_IN, FILE_OUT
# Adapters commons pycompss
from biobb_adapters.pycompss.biobb_commons import task_config
# Wrapped Biobb
from biobb_flexdyn.flexdyn.concoord_dist import ConcoordDist  # Importing class instead of module to avoid name collision

task_time_out = int(os.environ.get('TASK_TIME_OUT', 0))


@task(input_structure_path=FILE_IN, output_pdb_path=FILE_OUT, output_gro_path=FILE_OUT, output_dat_path=FILE_OUT, 
      on_failure="IGNORE", time_out=task_time_out)
def _concoorddist(input_structure_path, output_pdb_path, output_gro_path, output_dat_path,  properties, **kwargs):
    
    task_config.pop_pmi(os.environ)
    
    try:
        ConcoordDist(input_structure_path=input_structure_path, output_pdb_path=output_pdb_path, output_gro_path=output_gro_path, output_dat_path=output_dat_path, properties=properties, **kwargs).launch()
    except Exception as e:
        traceback.print_exc()
        raise e
    finally:
        sys.stdout.flush()
        sys.stderr.flush()


def concoord_dist(input_structure_path, output_pdb_path, output_gro_path, output_dat_path, properties=None, **kwargs):

    if (output_pdb_path is None or (os.path.exists(output_pdb_path) and os.stat(output_pdb_path).st_size > 0)) and \
       (output_gro_path is None or (os.path.exists(output_gro_path) and os.stat(output_gro_path).st_size > 0)) and \
       (output_dat_path is None or (os.path.exists(output_dat_path) and os.stat(output_dat_path).st_size > 0)) and \
       True:
        print("WARN: Task ConcoordDist already executed.")
    else:
        _concoorddist( input_structure_path,  output_pdb_path,  output_gro_path,  output_dat_path,  properties, **kwargs)