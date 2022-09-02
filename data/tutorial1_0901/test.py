from fileinput import filename
import commit
import amico
from commit import trk2dictionary


## Generate a dictionary
trk2dictionary.run(
    filename_tractogram = 'demo01_fibers.tck',
    filename_peaks = 'peaks.nii.gz',
    filename_mask = 'WM.nii.gz',
    fiber_shift = 0.5,
    peaks_use_affine = True
)

## Generate dwi scheme for use
amico.util.fsl2scheme('bvals.txt','bvecs.txt','DWI.scheme')

mit = commit.Evaluation('.','.')
mit.load_data('DWI.nii.gz','DWI.scheme')
mit.set_model('StickZeppelinBall')
d_par = 1.7E-3
d_perps_zrp = [0.51E-3]
d_isos = [1.7E-3, 3.0E-3]
mit.model.set(d_par,d_perps_zrp,d_isos)
mit.generate_kernels(regenerate=True )
mit.load_kernels()
mit.load_dictionary('COMMIT')
mit.set_threads()
mit.build_operator()
mit.fit(tol_fun = 1e-3, max_iter=1000)
mit.save_results()
x_ic, x_ec, x_iso = mit.get_coeffs()
print(x_ic.size,x_ic.max,x_ic.min)
