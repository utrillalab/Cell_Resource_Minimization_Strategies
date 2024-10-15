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

### 1. **Energy.ipynb**
- **Purpose**: This notebook analyzes ATP consumption at the reaction, gene, and strain levels using the ME model. It includes ATP costs for replication, transcription, and protein production derived from the energy simulations.
- **Outputs**:
  - Data on ATP consumption per reaction and per strain.
  - Visualizations of energy consumption for different strains.

### 2. **Genome_vs_proteome.ipynb**
- **Purpose**: Compares genome and proteome reduction strategies by calculating energy and proteome load savings from eliminating non-essential genes.
- **Outputs**:
  - Data files and visualizations comparing genome and proteome reductions.

### 3. **Energy_simulations/**
- **Purpose**: This directory contains notebooks that simulate specific energy-consuming processes:
  - **Replication_cost.ipynb**: Simulates ATP costs for increasing DNA content.
  - **Transcription_cost.ipynb**: Simulates ATP costs for transcription processes.
  - **UPF_cost.ipynb**: Simulates ATP costs for protein production (UPF).

## Python Scripts

### 1. **energy_analisis.py**
- **Purpose**: Contains functions for calculating energy consumption across reactions, genes, and strains in the ME model.
- **Key Functions**:
  - `get_energy_consumption_production(me)`: 
    - Calculates ATP consumption and production for each reaction in the ME model.
    - Returns two dataframes: one for energy consumption and one for energy production.
  - `energy_per_model(modelos, group=False)`: 
    - Aggregates energy consumption for models.
    - Returns total energy consumption and grouped consumption by reaction type if `group=True`.
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
  - `plot_distribution(distribucion_prot, tipo, eng=False, save=False, identifier='', colors_distribution=colors_distribution)`: 
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
