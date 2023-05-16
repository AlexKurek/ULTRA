import os
import hcipy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

from pastis.config import CONFIG_PASTIS
import pastis.util as util
from pastis.simulators.scda_telescopes import HexRingAPLC


if __name__ == '__main__':

    # Set number of rings
    NUM_RINGS = 1

    # Define the type of WFE.
    WHICH_DM = 'harris_seg_mirror'

    # Define target contrast
    C_TARGET = 1e-11

    if WHICH_DM == 'harris_seg_mirror':
        fpath = CONFIG_PASTIS.get('LUVOIR', 'harris_data_path')  # path to Harris spreadsheet
        pad_orientations = np.pi / 2 * np.ones(CONFIG_PASTIS.getint('LUVOIR', 'nb_subapertures'))
        DM_SPEC = (fpath, pad_orientations, True, False, False)
        NUM_MODES = 5 # TODO: works only for thermal modes currently

    optics_dir = os.path.join(util.find_repo_location(), 'data', 'SCDA')
    sampling = 4
    data_dir = '/Users/asahoo/Desktop/data_repos/paper2/static_mK_harris'

    # Thermal tolerance coefficients
    mus = np.genfromtxt('/Users/asahoo/Desktop/data_repos/paper2/mus_Hex_1_1e-11.csv', delimiter=',')
    # mus = np.genfromtxt('/Users/asahoo/Desktop/data_repos/paper2/mus_Hex_2_1e-11.csv', delimiter=',')
    # mus = np.genfromtxt('/Users/asahoo/Desktop/data_repos/paper2/mus_Hex_3_1e-11.csv', delimiter=',')
    # mus = np.genfromtxt('/Users/asahoo/Desktop/data_repos/paper2/mus_Hex_4_1e-11.csv', delimiter=',')
    # mus = np.genfromtxt('/Users/asahoo/Desktop/data_repos/paper2/mus_Hex_5_1e-11.csv', delimiter=',')

    tel = HexRingAPLC(optics_dir, NUM_RINGS, sampling)

    harris_coeffs_table = np.zeros([NUM_MODES, tel.nseg])
    for qq in range(NUM_MODES):
        for kk in range(tel.nseg):
            harris_coeffs_table[qq, kk] = mus[qq + kk * NUM_MODES]

    # Faceplate silvered
    tel2 = HexRingAPLC(optics_dir, NUM_RINGS, sampling)
    tel2.create_segmented_mirror(1)
    tel2.sm.flatten()
    tel2.sm.actuators = harris_coeffs_table[0]

    # Bulk
    tel3 = HexRingAPLC(optics_dir, NUM_RINGS, sampling)
    tel3.create_segmented_mirror(1)
    tel3.sm.flatten()
    tel3.sm.actuators = harris_coeffs_table[1]

    # Gradient Radial
    tel4 = HexRingAPLC(optics_dir, NUM_RINGS, sampling)
    tel4.create_segmented_mirror(1)
    tel4.sm.actuators = harris_coeffs_table[2]

    # Gradient X Lateral
    tel5 = HexRingAPLC(optics_dir, NUM_RINGS, sampling)
    tel5.create_segmented_mirror(1)
    tel5.sm.actuators = harris_coeffs_table[3]

    # Gradient z axial
    tel6 = HexRingAPLC(optics_dir, NUM_RINGS, sampling)
    tel6.create_segmented_mirror(1)
    tel6.sm.actuators = harris_coeffs_table[4]

    plt.figure(figsize=(32, 5))
    plt.subplot(1, 5, 1)
    # plt.title("Faceplates Silvered", fontsize=18)
    plot_norm = TwoSlopeNorm(vcenter=0.25, vmin=0, vmax=0.5)
    hcipy.imshow_field((tel2.sm.surface) * 1e3, norm=plot_norm, cmap='YlOrRd')
    plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True, labelsize=15)
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=15)
    cbar.set_label("mK", fontsize=15)
    plt.tight_layout()

    plt.subplot(1, 5, 2)
    # plt.title("Bulk", fontsize=18)
    plot_norm = TwoSlopeNorm(vcenter=3.5, vmin=0, vmax=7)
    hcipy.imshow_field((tel3.sm.surface) * 1e3, norm=plot_norm, cmap='YlOrRd')
    plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True, labelsize=15)
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=15)
    cbar.set_label("mK", fontsize=15)
    plt.tight_layout()

    plt.subplot(1, 5, 3)
    # plt.title("Gradiant Radial", fontsize=18)
    plot_norm = TwoSlopeNorm(vcenter=3, vmin=0, vmax=6)
    hcipy.imshow_field((tel4.sm.surface) * 1e3, norm=plot_norm, cmap='YlOrRd')
    plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True, labelsize=15)
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=15)
    cbar.set_label("mK", fontsize=15)
    plt.tight_layout()

    plt.subplot(1, 5, 4)
    # plt.title("Gradient X lateral", fontsize=18)
    plot_norm = TwoSlopeNorm(vcenter=1.0, vmin=0, vmax=2)
    hcipy.imshow_field((tel5.sm.surface)* 1e3, norm=plot_norm, cmap='YlOrRd')
    plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True, labelsize=15)
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=15)
    cbar.set_label("mK", fontsize=15)
    plt.tight_layout()

    plt.subplot(1, 5, 5)
    # plt.title("Gradient Z axial", fontsize=18)
    plot_norm = TwoSlopeNorm(vcenter=1, vmin=0, vmax=2)
    hcipy.imshow_field((tel6.sm.surface)*1e3, norm=plot_norm, cmap='YlOrRd')
    plt.tick_params(top=False, bottom=True, left=True, right=False, labelleft=True, labelbottom=True, labelsize=15)
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=15)
    cbar.set_label("mK", fontsize=15)
    plt.tight_layout()

    plt.tight_layout()
    plt.savefig(os.path.join(data_dir, 'harris_mK_%d_hex.pdf' % NUM_RINGS))


