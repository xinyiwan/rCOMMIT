import nibabel as nib
import numpy as np
import os
import glob
import json
import io


def generate_subsets(raw_file_path, subset_sizes):
    
    global sub_file_path

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
        
        ## Generate random index for subset
        num_streamlines = subset_sizes[i]
        idx_list = np.random.choice(
            np.arange(raw.header["nb_streamlines"]),
            size=num_streamlines,
            replace=False,
        ).tolist()

        ## save it to the subsets path
        subsets_info = {"size": [subset_sizes[i]], "idx": idx_list}
        with io.open(os.path.join(sub_file_path, 'idx.json'), 'w') as f:
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

    print("All the paths of subsets are in %s" %paths)
    with open(os.path.join(raw_file_path,"paths.txt"), "w") as output:
        for i in paths:
            output.write(str(i) + '\n')
    return 

