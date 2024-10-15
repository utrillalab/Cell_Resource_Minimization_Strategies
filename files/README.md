# Files Documentation

### 1. **deleted_genes/**

This directory contains files mapping deleted genes from various *E. coli* strains to their corresponding genomic information. The files are essential for analyzing the impact of gene deletions on the proteome and overall energy consumption.

#### Contents:
- **mapped_del_genes_Δ16.csv**: Genes deleted from the Δ16 strain.
- **mapped_del_genes_MS56.csv**: Genes deleted from the MS56 strain.
- **mapped_del_genes_MDS12.csv**: Genes deleted from the MDS12 strain.
- **mapped_del_genes_MDS42.csv**: Genes deleted from the MDS42 strain.
- **mapped_del_genes_MDS69.csv**: Genes deleted from the MDS69 strain.
- **mapped_del_genes_DGF298.csv**: Genes deleted from the DGF298 strain.
- **mapped_del_genes_DGF327.csv**: Genes deleted from the DGF327 strain.
- **mapped_del_genes_MGF02.csv**: Genes deleted from the MGF02 strain.

---

### 2. **deleted_ranges/**

This directory contains files that specify genomic ranges corresponding to gene deletions for various *E. coli* strains. These files are used to identify the specific genes that are affected when certain regions of the genome are deleted.

#### Contents:
- **delta_16.csv**: Genomic ranges for the Δ16 strain.
- **MS56.csv**: Genomic ranges for the MS56 strain.
- **MDS42_69.csv**: Genomic ranges for the MDS42 and MDS69 strains.
- **MDS12_V2.csv**: Genomic ranges for the MDS12 strain.
- **MGF_line.csv**: Genomic ranges for W3110-related strains.

---

### 3. **ecolime_data/**

This directory contains auxiliary data files related to the ECOLIme project. It includes essential data for analyzing codon usage, which is important for understanding the implications of gene deletions on protein expression.

#### Contents:
- **codon_usage.csv**: A CSV file detailing the usage frequency of different codons in the *E. coli* genome.

---

### 4. **energy/**

This directory stores files related to energy consumption analysis derived from the ME model simulations. The files contain results that help quantify ATP consumption across various reactions and genes.

#### Contents:
- **energy_per_reaction.pickle**: A pickled DataFrame containing ATP consumption and production data for each reaction in the ME model.
- **energy_per_gene.pickle**: A pickled DataFrame containing ATP consumption data for each gene present in the ME model.
- **Costs_L&M_ME.csv**: A CSV file comparing ATP costs from the ME model with literature data.

---

### 5. **genomes/**

This directory contains GenBank files for various *E. coli* strains. These files are utilized to extract genomic information necessary for analyzing gene deletions and their impacts on proteome and energy dynamics.

#### Contents:
- **MG1655.gb**: GenBank file for the MG1655 strain.
- **W3110.gb**: GenBank file for the W3110 strain.

---

### 6. **models/**

This directory includes the models used for energy analysis simulations in the ME framework. These models are crucial for understanding how different genetic configurations affect energy consumption.

#### Contents:
- **iJL1678b.pickle**: The original model used in the simulations.
- **DNA_per{value}.pickle**: Models saved from the Replication cost simulation with different DNA content percentages.
- **AumGenes_GLC_OX_{number}.pickle**: Models saved from the Transcription cost simulation with added transcribed genes.
- **ATPM_UPF_OX_GLC{UPF_value}.pickle**: Models saved from the UPF cost simulation with different UPF settings.

---

### 7. **proteome_Schmidt/**

This directory contains proteomic data from the study by Schmidt et al. (2016). The data is used for analyzing the impact of gene deletions on the proteomic landscape of *E. coli*.

#### Contents:
- **Proteomic_data_fg.xlsx**: Excel file containing proteomic data for various conditions.
- **Proteome_size.xlsx**: Excel file providing the total proteome size for each condition.

---

### 8. **proteome_genome/**

This directory includes files comparing the proteomic and genomic data for the strains analyzed. These files are essential for visualizing and understanding the relationship between genome reduction and proteome efficiency.

#### Contents:
- **protVSgen.csv**: A CSV file comparing the proteomic load and minimized genome for each strain, including visualizations and analysis results.
