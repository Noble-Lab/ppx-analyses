#!/usr/bin/env bash
#$ -l h_rt=72:0:0,mfree=8G
#$ -N snakemake_job
#$ -cwd
set -euo pipefail

cd workflow
snakemake --profile ../profiles/sge --use-conda --config gpu=True
