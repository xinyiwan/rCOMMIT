import nibabel as nib
import numpy as np
import os
import glob
import json
import io
from func.rc_run_commit_once import run_commit_on_subsets
from func.rc_clean_commit_results import clean_commit_results
from func.rc_get_key_results_from_commit import get_key_results_from_commit


def generate_run_subsets(raw_file_path, subset_sizes, raw_size):
    
    global sub_file_path
    vote = 5
    if os.path.exists(raw_file_path):
        rawfile = glob.glob(os.path.join(raw_file_path, "*.tck"), recursive=True)
    if rawfile[0]:
        rawfile = rawfile[0]

    raw = nib.streamlines.load(rawfile)
    paths = []
    for i in range(len(subset_sizes)):
        ## Make files for each subset
        sub_file_path = os.path.join(raw_file_path,"sub_%s" %subset_sizes[i])
        if not os.path.exists(sub_file_path):
            os.makedirs(sub_file_path)
        paths.append(sub_file_path)
        num_streamlines = subset_sizes[i]

        ## Define repeation times
        rep = int(raw_size*vote/subset_sizes[i])
        for j in range(rep):
            ## Generate random index for subset
            idx_list = np.random.choice(
                np.arange(raw.header["nb_streamlines"]),
                size=num_streamlines,
                replace=False,
            ).tolist()

            ## save it to the subsets path
            subsets_info = {"size": [subset_sizes[i]],"runtime":[j], "idx": idx_list}
            with io.open(os.path.join(sub_file_path, 'idx_%s.json'%j), 'w') as f:
                json.dump(subsets_info, f)

            ## Generate subsets
            t_new = nib.streamlines.Tractogram(
                streamlines=raw.streamlines[idx_list],
                affine_to_rasmm=raw.header['voxel_to_rasmm']
            )
            nib.streamlines.save(
                t_new,
                os.path.join(sub_file_path,"new_%s.tck" %num_streamlines),
                header=raw.header
            )
            run_commit_on_subsets(raw_file_path,sub_file_path,j)
            get_key_results_from_commit(sub_file_path,raw_file_path,subset_sizes[i], j)
            clean_commit_results(sub_file_path)

    # print("All the paths of subsets are in %s" %paths)
    # with open(os.path.join(raw_file_path,"paths.txt"), "w") as output:
    #     for i in paths:
    #         output.write(str(i) + '\n')
    return 

