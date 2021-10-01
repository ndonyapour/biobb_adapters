# Python
import os
import sys
import traceback
# Pycompss
from pycompss.api.task import task
from pycompss.api.parameter import FILE_IN, FILE_OUT
from pycompss.api.multinode import multinode
from pycompss.api.constraint import constraint
# Adapters commons pycompss
from biobb_adapters.pycompss.biobb_commons import task_config
# Wrapped Biobb
from biobb_amber.pmemd.pmemd_mdrun import PmemdMDRun  # Importing class instead of module to avoid name collision

task_time_out = int(os.environ.get('TASK_TIME_OUT', 0))
computing_nodes = str(os.environ.get('TASK_COMPUTING_NODES', "1"))
computing_units = str(os.environ.get('TASK_COMPUTING_UNITS', "1"))

@constraint(computing_units=computing_units)
@multinode(computing_nodes=computing_nodes)
@task(input_top_path=FILE_IN, input_crd_path=FILE_IN, output_log_path=FILE_OUT, output_traj_path=FILE_OUT, output_rst_path=FILE_OUT, input_mdin_path=FILE_IN, input_cpin_path=FILE_IN, input_ref_path=FILE_IN, output_cpout_path=FILE_OUT, output_cprst_path=FILE_OUT, output_mdinfo_path=FILE_OUT, 
      on_failure="IGNORE", time_out=task_time_out)
def _pmemdmdrun(input_top_path, input_crd_path, output_log_path, output_traj_path, output_rst_path, input_mdin_path, input_cpin_path, input_ref_path, output_cpout_path, output_cprst_path, output_mdinfo_path,  properties, **kwargs):
    
    task_config.config_multinode(properties)
    
    try:
        PmemdMDRun(input_top_path=input_top_path, input_crd_path=input_crd_path, output_log_path=output_log_path, output_traj_path=output_traj_path, output_rst_path=output_rst_path, input_mdin_path=input_mdin_path, input_cpin_path=input_cpin_path, input_ref_path=input_ref_path, output_cpout_path=output_cpout_path, output_cprst_path=output_cprst_path, output_mdinfo_path=output_mdinfo_path, properties=properties, **kwargs).launch()
    except Exception as e:
        traceback.print_exc()
        raise e
    finally:
        sys.stdout.flush()
        sys.stderr.flush()


def pmemd_mdrun(input_top_path, input_crd_path, output_log_path, output_traj_path, output_rst_path, input_mdin_path=None, input_cpin_path=None, input_ref_path=None, output_cpout_path=None, output_cprst_path=None, output_mdinfo_path=None, properties=None, **kwargs):

    if (output_log_path is None or os.path.exists(output_log_path)) and \
       (output_traj_path is None or os.path.exists(output_traj_path)) and \
       (output_rst_path is None or os.path.exists(output_rst_path)) and \
       (output_cpout_path is None or os.path.exists(output_cpout_path)) and \
       (output_cprst_path is None or os.path.exists(output_cprst_path)) and \
       (output_mdinfo_path is None or os.path.exists(output_mdinfo_path)) and \
       True:
        print("WARN: Task PmemdMDRun already executed.")
    else:
        _pmemdmdrun( input_top_path,  input_crd_path,  output_log_path,  output_traj_path,  output_rst_path,  input_mdin_path,  input_cpin_path,  input_ref_path,  output_cpout_path,  output_cprst_path,  output_mdinfo_path,  properties, **kwargs)