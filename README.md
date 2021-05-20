# An example Snakemake workflow using ppx and ANN-SoLo  

[ppx](https://github.com/wfondrie/ppx) provides programmatic access to files
stored in proteomics data repositories, such as PRIDE and MassIVE. In doing
so, ppx enhances the reproducibility of proteomics analyses. Here, we provide
an example [Snakemake](https://snakemake.readthedocs.io/en/stable/) workflow,
which in part reproduces the open modification search results from 
[ANN-SoLo](https://github.com/bittremieux/ANN-SoLo) presented by Bittremieux,
et al. 

This workflow uses ppx to download the MGF mass spectrometry data files and the
spectral library from the original publication's project on PRIDE Archive,
[PXD009861](https://www.ebi.ac.uk/pride/archive/projects/PXD009861). These MGF
files are then searched using ANN-SoLo. Additionally, the workflow downloads
the [MSFragger](https://msfragger.nesvilab.org/) result files created in the
original publication (`*.tsv`). Finally, the workflow a single figure
displaying the modification mass shifts detected by ANN-SoLo and MSFragger.

## Prerequisites  

You can run this workflow on MacOS and Linux systems, due to the requirements
for ANN-SoLo. You'll also need the following software installed:

- **A conda-based Python distribution** - We recommend
  [miniconda](https://docs.conda.io/en/latest/miniconda.html). This provides
  the conda package manager.
- **git** - [git](https://github.com/git-guides/install-git) is a tool for
  managing versions of code. You'll need git to grab this workflow from here on
  GitHub.

You can confirm that both requirements are met by opening your terminal and
trying the following commands:

**conda**
``` sh
$ conda --version
conda 4.10.1
```

**git**
``` sh
$ git --version
git version 2.31.1
```

## Running the workflow
### Downloading the workflow

We'll use git to download this workflow from GitHub:

``` sh
$ git clone https://github.com/Noble-Lab/ppx-analyses.git
$ cd ppx-analyses
```

Alternatively, you can use click `Code -> Download ZIP` in the [GitHub
repository](https://github.com/Noble-Lab/ppx-analyses), unpack the zip archive,
and navigate to the new `ppx-analyses` directory in your terminal.

### Create a conda environment

We'll create a conda environment, which will automatically install Snakemake,
ppx, and their dependencies:

``` sh
$ conda env create -f environment.yaml
$ conda activate ppx-analyses
```

### Execute the workflow

Now we'll use Snakemake to execute our workflow. Snakemake will manage install
ANN-SoLo and other dependencies, then run all of the steps required for our
analyses.

In this example, we'll use `--configfile config/one.yaml`, which will restrict
our analysis to a single MGF file:

``` sh
$ snakemake -j -d workflow --use-conda --config-file config/one.yaml
```

Here is what each parameter does:

- `-j`: Use the maximum number of cores. You can also specify a number, such
  as `-j4` to use 4 cores.
- `-d workflow`: Tells Snakemake that our working directory should be the 
  `workflow` directory. This is where our `Snakefile` is.
- `--use-conda`: Tells Snakemake that we want it to handle setting up conda
  environment, such as for ANN-SoLo.
- `--config-file config/one.yaml`: Specifies a config file, other than the 
  default one. The `config/one.yaml` file changes the workflow to only download
  and search a single MGF file, instead of all of them.

Alternatively, you could analyze all of the files as we did in the ppx paper.
Note that this could take awhile depending on your system:

``` sh
$ snakemake -j -d workflow --use-conda
```

## Conclusion  

We've described how to run this workflow that uses ppx, ANN-SoLo, and Snakemake
to reproduce a previously published analysis with data shared in PRIDE Archive.
Our intention with this workflow is that it would be an illustration of how ppx
can help create reproducible and sharable proteomics analyses.

To find out more about ppx, see our documentation: https://ppx.readthedocs.io
