# Energy Simulations in Minimal E. coli Models

## Overview

The `src/Energy_simulations` directory contains Jupyter notebooks and scripts designed to simulate energy costs associated with various cellular processes in a minimal *Escherichia coli* model. The primary focus is on quantifying the energy expenditures related to replication, transcription, and the Universal Protein Fraction (UPF). These simulations leverage the *CobraME* framework to analyze how variations in cellular components influence ATP consumption.

## Table of Contents

- [Directory Structure](#directory-structure)
- [Input Files](#input-files)
- [Output Files](#output-files)
- [Simulations Overview](#simulations-overview)
  - [1. Replication Cost](#1-replication-cost)
  - [2. Transcription Cost](#2-transcription-cost)
  - [3. UPF Cost](#3-upf-cost)

## Directory Structure

```
src/Energy_simulations/
├── Replication_cost.ipynb
├── Transcription_cost.ipynb
├── UPF_cost.ipynb
├── ...
```

## Input Files

The following files are used as input for the simulations:

- **`../../files/models/iJL1678b.pickle`**: The original minimal E. coli model used for all simulations.
- **`../../files/ecolime_data/codon_usage.csv`**: Contains codon usage data for constructing synthetic genes in the transcription simulation.

## Output Files

The notebooks generate various output files, which include:

- **`../../files/models/DNA_per{value}.pickle`**: Models generated from the replication simulations, with varied DNA percentages.
- **`../../files/models/AumGenes_GLC_OX_{number}.pickle`**: Models from the transcription simulations, containing additional transcribed genes.
- **`../../files/models/ATPM_UPF_OX_GLC{UPF_value}.pickle`**: Models generated from the UPF simulations, reflecting different values of UPF.

## Simulations Overview

### 1. Replication Cost
**Notebook**: `Replication_cost.ipynb`

This notebook simulates the energy costs associated with DNA replication in a minimal *E. coli* model. The focus is on understanding how variations in the percentage of DNA influence ATP consumption during replication.

**Key Steps**:
- Load the original model (`iJL1678b.pickle`).
- Modify the DNA percentage for simulations.
- Solve the model at the specified growth rate (\(\mu = 0.69\)).
- Save modified models for further analysis.

### 2. Transcription Cost
**Notebook**: `Transcription_cost.ipynb`

This notebook explores the energy costs associated with transcription in a minimal *E. coli* model. It evaluates how adding transcribed but untranslated genes impacts ATP consumption during transcription.

**Key Steps**:
- Load the original model.
- Generate synthetic genes that are transcribed but not translated.
- Solve the model at the specified growth rate (\(\mu = 0.69\)).
- Save modified models with the newly added genes.

### 3. UPF Cost
**Notebook**: `UPF_cost.ipynb`

This notebook examines the impact of varying the Universal Protein Fraction (UPF) on energy costs in a minimal *E. coli* model.

**Key Steps**:
- Load the original model.
- Set fixed values for UPF and solve the model at the specified growth rate (\(\mu = 0.69\)).
- Save the models reflecting different UPF values for further analysis.

