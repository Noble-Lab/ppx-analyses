"""Utility functions used in our notebooks

These functions were adapted from:
https://github.com/bittremieux/ANN-SoLo/blob/master/notebooks/hek293_stats.ipynb
"""
import tqdm
import pandas as pd
from ann_solo import reader


def read_matches(mztab_files):
    """Read the SSMs from the ANN-SoLo result files.

    Parameters
    ----------
    mztab_files : list of str
        The mzTab files to read.

    Returns
    -------
    pandas.DataFrame
        A table of the detected SSMs.
    """
    psms_list = []

    # Parse the ANN-SoLo results:
    for res_file in tqdm.tqdm(mztab_files, unit="files"):
        psms_df = reader.read_mztab_ssms(res_file)
        psms_list.append(psms_df)

    psms = pd.concat(psms_list).reset_index(drop=True)
    psms["mass_diff"] = psms["exp_mass_to_charge"] - psms["calc_mass_to_charge"]
    psms["mass_diff"] *= psms["charge"]

    keep = [
        "sequence",
        "charge",
        "exp_mass_to_charge",
        "calc_mass_to_charge",
        "search_engine_score[1]",
        "mass_diff",
    ]
    return psms.loc[:, keep]


def get_mass_groups(psms, tol_mass, tol_mode):
    """Calculate mass groups from an open modification search.

    Note that the score, `search_engine_score[1]` should indicate more
    confident SSMs with higher scores.

    Parameters
    ----------
    psms : pandas.DataFrame
        A table of the deteced SSMs, from the `read_matches()` function.
    tol_mass : float
        The mass tolerance that determines if two masse differences should be
        aggregated as the same modification.
    tol_mode : {"ppm", "Da"}
        Is the `tol_mass` in ppm or Da?

    Returns
    -------
    pandas.DataFrame
        A table containing the mass differences that were found, the number of
        SSMs in each.
    """
    # start with the highest ranked PSM
    mass_groups = []
    psms_remaining = psms.sort_values("search_engine_score[1]", ascending=False)
    while len(psms_remaining) > 0:
        # find all remaining PSMs within the precursor mass window
        mass_diff = psms_remaining["mass_diff"].iloc[0]
        if tol_mass is None or tol_mode not in ("Da", "ppm"):
            psms_selected = psms_remaining
        elif tol_mode == "Da":
            psms_selected = psms_remaining[
                (psms_remaining["mass_diff"] - mass_diff).abs() <= tol_mass
            ]
        elif tol_mode == "ppm":
            psms_selected = psms_remaining[
                (psms_remaining["mass_diff"] - mass_diff).abs()
                / psms_remaining["exp_mass_to_charge"]
                * 10 ** 6
                <= tol_mass
            ]
        mass_groups.append(psms_selected)
        # exclude the selected PSMs from further selections
        psms_remaining.drop(psms_selected.index, inplace=True)

    mass_group_stats = []
    for mass_group in mass_groups:
        mass_group_stats.append(
            (
                mass_group["mass_diff"].median(),
                mass_group["mass_diff"].mean(),
                len(mass_group),
            )
        )
    mass_group_stats = pd.DataFrame.from_records(
        mass_group_stats,
        columns=["mass_diff_median", "mass_diff_mean", "num_psms"],
    )
    return mass_group_stats
