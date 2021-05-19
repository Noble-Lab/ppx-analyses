#!/usr/bin/env bash
#$ -l h_rt=72:0:0,mfree=8G
#$ -q noble-long.q
#$ -cwd
#$ -N snakemake_master
set -euo pipefail
cd workflow
snakemake --profile sge --use-conda
