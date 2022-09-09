from fileinput import filename
import commit
import amico
from commit import trk2dictionary
import glob
import os


def run_commit(subset_path):
    ## Generate a dictionary
    subset = glob.glob(os.path.join(subset_path, "*.tck"), recursive=True)
    trk2dictionary.run(
        filename_tractogram = subset[0],
        filename_peaks = '/Users/xinyi/Documents/GitHub/rCOMMIT/599671/peaks.nii.gz',
        # filename_mask = 'WM.nii.gz',
        fiber_shift = 0.5,
        peaks_use_affine = True  
    ) 

    ## Generate dwi scheme for use
    # amico.util.fsl2scheme('/Users/xini/Documents/GitHub/rCOMMIT/599671/bvals.txt','/Users/xinyi/Documents/GitHub/rCOMMIT/599671/bvecs.txt','DWI.scheme')

    mit = commit.Evaluation('.','.')

    scheme = glob.glob(os.path.join(subset_path, "*.scheme"), recursive=True)
    scheme = scheme[0]
    mit.load_data('/Users/xinyi/Documents/GitHub/rCOMMIT/599671/data.nii.gz',scheme)

    mit.set_model('StickZeppelinBall')
    d_par = 1.7E-3
    d_perps_zrp = [0.51E-3]
    d_isos = [1.7E-3, 3.0E-3]
    mit.model.set(d_par,d_perps_zrp,d_isos)
    mit.generate_kernels(regenerate=True )
    mit.load_kernels()


    mit.load_dictionary(os.path.join(subset_path,'COMMIT'))
    mit.set_threads()
    mit.build_operator()
    mit.fit(tol_fun = 1e-3, max_iter=1000)
    mit.save_results()
    x_ic, x_ec, x_iso = mit.get_coeffs()
    print(x_ic.size,x_ic.max,x_ic.min)

