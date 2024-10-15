
# Source Code Documentation

This directory contains the source code and Jupyter notebooks used for analyzing energy consumption and resource allocation strategies in minimized *E. coli* cells. The primary focus is on energy calculations and visualizations regarding genome and proteome reduction.

## Structure

```
src/
│
├── Energy_simulations/        # Additional simulations (Replication, Transcription, UPF costs)
│   ├── Replication_cost.ipynb
│   ├── Transcription_cost.ipynb
│   └── UPF_cost.ipynb
│
├── Energy.ipynb               # Main notebook for energy consumption analysis in ME model
├── Genome_vs_proteome.ipynb   # Comparison of genome and proteome reduction
├── Multipanel_Energy_protReleased_Energy.pdf # Energy plot outputs
├── Prot_vs_Genome.pdf         # Genome vs Proteome comparison plot
├── __init__.py                # Package initialization file
├── energy_analisis.py         # Functions for energy analysis in the ME model
├── get_gene_info.py           # Functions to retrieve genome information
├── get_proteome_info.py       # Functions to retrieve proteome data
├── plot_energy.py             # Plotting functions related to energy consumption
└── plot_proteome.py           # Plotting functions related to proteome distributions
```

## Notebooks

### 1. **Energy_simulations/**
This directory contains notebooks that simulate specific energy-consuming processes:

- **Replication_cost.ipynb**
  - **Purpose**: Simulates ATP costs for increasing DNA content in the ME model.
  - **Inputs**: 
    - `../../files/models/iJL1678b.pickle` (original model).
    - Percent DNA data: `[1, 1.125, 1.25, 1.5]`.
  - **Outputs**:
    - Models saved as `../../files/models/DNA_per{value}.pickle` with modified DNA percentages.

- **Transcription_cost.ipynb**
  - **Purpose**: Simulates ATP costs associated with transcription processes in the ME model.
  - **Inputs**: 
    - `../../files/models/iJL1678b.pickle` (original model).
    - `../../files/ecolime_data/codon_usage.csv` (codon usage data).
    - Genes added (Approximately a 5%, 10%, 15%, and 20% of the 4600 genes): `[230, 460, 690, 920]`.
  - **Outputs**:
    - Models saved as `../../files/models/AumGenes_GLC_OX_{number}.pickle` with added transcribed genes.

- **UPF_cost.ipynb**
  - **Purpose**: Simulates ATP costs associated with the Universal Protein Fraction (UPF) in the ME model.
  - **Inputs**: 
    - `../../files/models/iJL1678b.pickle` (original model).
    - UPF new values:  `[0.24, .27, 0.30, .33, 0.36]`.
  - **Outputs**:
    - Models saved as `../../files/models/ATPM_UPF_OX_GLC{UPF_value}.pickle` with different UPF settings.

### 2. **Energy.ipynb**
- **Purpose**: Analyzes ATP consumption at the reaction, gene, and strain levels using the ME model. It incorporates ATP costs for replication, transcription, and protein production derived from the energy simulations.
- **Inputs**:
  - ME model solved data from `../files/models/iJL1678b_solver.pickle`.
  - ATP costs for replication from `Replication_cost.ipynb` outputs.
  - ATP costs for transcription from `Transcription_cost.ipynb` outputs.
  - ATP costs for UPF from `UPF_cost.ipynb` outputs.
- **Outputs**:
  - Data files on ATP consumption per reaction saved as `../files/energy/energy_per_reaction.pickle`.
  - Data files on ATP consumption per gene saved as `../files/energy/energy_per_gene.pickle`.
  - Data files on ATP consumption per strain, including visualizations saved as part of the output figures.

### 3. **Genome_vs_proteome.ipynb**
- **Purpose**: Compares genome and proteome reduction strategies by calculating energy and proteome load savings from eliminating non-essential genes.
- **Inputs**:
  - Gene deletion ranges for various strains:
    - `../files/deleted_ranges/delta_16.csv` (for Δ16 strain).
    - `../files/deleted_ranges/MS56.csv` (for MS56 strain).
    - `../files/deleted_ranges/MDS42_69.csv` (for MDS strains).
    - `../files/deleted_ranges/MDS12_V2.csv` (for MDS12 strain).
    - `../files/deleted_ranges/MGF_line.csv` (for W3110-related strains).
  - Proteomic data from Schmidt et al., 2016:
    - `../files/proteome_Schmidt/Proteomic_data_fg.xlsx` (proteomic data).
    - `../files/proteome_Schmidt/Proteome_size.xlsx` (total proteome sizes).
  - Genome data from GenBank files:
    - `../files/genomes/MG1655.gb` (MG1655 genome).
    - `../files/genomes/W3110.gb` (W3110 genome).
- **Outputs**:
  - Data files of mapped deleted genes saved as:
    - `../files/deleted_genes/mapped_del_genes_Δ16.csv`
    - `../files/deleted_genes/mapped_del_genes_MS56.csv`
    - `../files/deleted_genes/mapped_del_genes_MDS12.csv`
    - `../files/deleted_genes/mapped_del_genes_MDS42.csv`
    - `../files/deleted_genes/mapped_del_genes_MDS69.csv`
    - `../files/deleted_genes/mapped_del_genes_DGF298.csv`
    - `../files/deleted_genes/mapped_del_genes_DGF327.csv`
    - `../files/deleted_genes/mapped_del_genes_MGF02.csv`
  - Data files of proteomic load and percentages saved as `../files/proteome_genome/protVSgen.csv`.
  - Visualizations comparing genome and proteome reductions.

## Python Scripts

### 1. **energy_analisis.py**
- **Purpose**: Contains functions for calculating energy consumption across reactions, genes, and strains in the ME model.
- **Key Functions**:
  - `get_energy_consumption_production(me)`: 
    - Calculates ATP consumption and production for each reaction in the ME model.
    - **Outputs**: Returns two dataframes: one for energy consumption and one for energy production.
  - `energy_per_model(modelos, group=False)`: 
    - Aggregates energy consumption for models.
    - **Outputs**: Returns total energy consumption and grouped consumption by reaction type if `group=True`.
  - `get_energy_per_gene(energy_consumption, me)`: 
    - Distributes energy consumption across genes based on reaction types (metabolic, transcription, translation).
  - `get_energy_ME_proteome(strains, genes_finales, proteomic_data, replication_cost, transcription_tcost, upf_cost)`: 
    - Combines ME model data with proteomic data to estimate energy costs for genome-reduced strains.
  - `get_energy_PFC(strains, reduced, replication_cost, transcription_tcost, upf_cost)`:
    - Calculates energy costs associated with a proteome-reduced strain (PFC) based on the provided lengths of deleted genes.

### 2. **plot_energy.py**
- **Purpose**: Contains functions for visualizing energy consumption at various levels (reactions, genes, strains).
- **Key Functions**:
  - `plot_type_energy(energy_consumption, energy_production)`: 
    - Visualizes ATP consumption by reaction type (e.g., metabolic, transcription).
  - `plot_ME_energy(names, consumo, consumo_per)`: 
    - Plots ATP consumption per strain, showing how much energy is released.
  - `plot_glc_ox_atp(consumption_me, modelos, tipo)`: 
    - Generates plots comparing glucose and oxygen consumption with ATP consumption for specific processes.
  - `plot_energy_ME_proteome(names, aportaciones, leyendas, medio, colores=colors, normalizado=False, eng=True, save=False, identifier='')`: 
    - Plots released energy for different strains with optional normalization.

### 3. **get_gene_info.py**
- **Purpose**: Extracts and manages genome information from GenBank files, mapping genes to strains for genome reduction analysis.
- **Key Functions**:
  - `get_genome_info(genome_path)`: 
    - Extracts relevant information (gene name, Bnumber, start/end positions, and length) from the GenBank file.
  - `get_genes_from_ranges(rangos, genome)`: 
    - Maps genes that should be deleted based on specified genomic ranges.

### 4. **get_proteome_info.py**
- **Purpose**: Handles proteomics data and calculates proteome load for various strains based on gene deletions.
- **Key Functions**:
  - `match_proteomic_data(names, cepas, proteomic_data)`: 
    - Maps deleted genes to proteomic data to assess energy savings.
  - `calculate_proteomic_load(names, matched_genes_cepas, proteome_size)`: 
    - Calculates proteomic load for each condition and its percentage.

### 5. **plot_proteome.py**
- **Purpose**: Contains functions for visualizing proteome distributions across various conditions and strains.
- **Key Functions**:
  - `display_side_by_side(*args, titles=cycle(['']))`: 
    - Displays multiple pandas DataFrames side by side in a single output cell for comparison.
  - `plot_perc_load(prot_load, prot_perc, conditions=None, strains=None, save=False, identifier='', colors_per_strain=colors_per_strain)`: 
    - Plots released proteomic load and its percentage for specified strains and conditions.
  - `plot_distribution(distribucion_prot, tipo, eng=False, save =False, identifier='', colors_distribution=colors_distribution)`: 
    - Plots histograms for average proteome distribution or specific conditions.
  - `plot_strain_distribution(info_cepas, distribucion_prot, names, title, tipo, save=False, identifier='', colors_per_strain=colors_per_strain)`: 
    - Visualizes the distribution of proteome load for specific strains.
  - `plot_gen_vs_prot(prot_vs_genome_df, forma=forma, colors=None, save=False)`: 
    - Creates scatter plots comparing genome reductions versus proteome reductions for various strains.

## How to Use

1. **Run the notebooks in order**:
   - Start with **Energy Simulations** notebooks to simulate ATP costs for specific processes.
   - Next, run **Energy.ipynb** for core energy consumption analysis.
   - Finally, use **Genome_vs_proteome.ipynb** to compare genome and proteome reduction strategies.

2. **Script Functionality**:
   - **energy_analisis.py** provides the primary functions for energy analysis.
   - **get_gene_info.py** and **get_proteome_info.py** manage genome and proteome data extraction.
   - **plot_energy.py** and **plot_proteome.py** are used for generating visualizations.
