# Hejret 2023 dataset: primary-source notes

Verified 2026-11-10. Research only; no assignment or solution implemented. Counts below were computed directly from the downloaded files, not copied from the paper. Repository sources are pinned to the inspected commits.

## Exact dataset and downloads

The current [miRBench loader][loader] names the dataset `AGO2_CLASH_Hejret2023` and downloads **miRBench-processed version 7**, [Zenodo record 20540907][zenodo] (released 2026-06-04):

- Train: https://zenodo.org/records/20540907/files/AGO2_CLASH_Hejret2023_train.tsv.gz?download=1
- Test: https://zenodo.org/records/20540907/files/AGO2_CLASH_Hejret2023_test.tsv.gz?download=1

Both are gzip-compressed, header-bearing TSV files. The loader decompresses them to `dataset.tsv` and reads with a tab separator. **Hejret has only `train` and `test`; no official Hejret `leftout` file.** The loader's `leftout` belongs to `AGO2_eCLIP_Manakov2022`.

Observed counts:

| Split | Rows | `label=1` | `label=0` | Target chromosome |
| --- | ---: | ---: | ---: | --- |
| Train | 8,140 | 4,084 | 4,056 | All represented chromosomes except 1 |
| Test | 1,018 | 495 | 523 | 1 only |
| Combined | 9,158 | 4,579 | 4,579 | Both splits |

The classes balance across the combined data, including per family, **not within each split**. Download checksums matched Zenodo: train MD5 `55f1fbc97234cb3747ca7480b2ef70c6`; test MD5 `224fe08e101b6997ebae54090664c9f7`. Pin this record and these checksums: the [release notes][zenodo] describe v7 fixes for duplicate pairs, annotation inconsistencies, and negative generation. Older paper results and example files need not describe this exact release.

## Prediction unit, labels, and score direction

One example is a **mature miRNA sequence paired with a 50-nucleotide target-site sequence**, not a whole gene, patient, replicate, or measured gene-expression response. `gene` is the target sequence, despite its name. Both sequences are documented as 5′→3′; the observed alphabet is `A/C/G/T`, using T rather than U. All targets are length 50; observed miRNA lengths are 17–26 in both splits (the older Zenodo description gives a broader generic 16–28 range). [Data][zenodo], [miRBench paper §2.2][benchpaper].

- **`label=1`:** a miRNA–target pair retained from high-confidence AGO2-CLASH chimeric interaction calls, after filtering/deduplication.
- **`label=0`:** an **in-silico constructed negative**, pairing a miRNA with a target from another eligible target-sequence cluster. The generation code excludes clusters observed with that miRNA family, preserves the miRNA sequences, and samples at most one target per eligible cluster per family. For `unknown` families it operates per miRNA sequence. These are presumed negatives, not experimentally demonstrated non-binding pairs. [Filtering code][filter], [negative-generation code][negatives], [paper §2.2][benchpaper].

**These labels do not encode repression efficacy, fold change, or luciferase activity.** Hejret's paper separately tests functional repression for selected pairs; those measurements are not the binary labels in these files. Binding evidence does not establish repression for every positive. [Hejret paper, functional validation and CNN sections][hejretpaper].

For evaluation, specify a score where **larger means stronger support for `label=1`**. A positive-class probability is one option; an arbitrary ranking score need not be a calibrated probability. miRBench's CNN wrapper returns interaction predictions, whereas its RNACofold wrapper **negates minimum free energy**, because lower raw energy otherwise has the opposite direction. A repression-related score from another predictor needs its own documented conversion; do not infer direction from its name. [Predictor code][predictors]. Average precision (the paper's main metric) and trapezoidal PR area are different calculations; the evaluator should name the metric precisely. [Paper §2.1][benchpaper].

## Concrete observed processed schema

Both downloaded headers contain exactly these **18 columns, in this order**:

```text
gene	noncodingRNA	noncodingRNA_name	noncodingRNA_fam	feature	label	chr	start	end	strand	Nunique	dominant_region	regions_present	read_start_in_sel_tx_1based	read_end_in_sel_tx_1based	gene_cluster_ID	gene_phyloP	gene_phastCons
```

| Columns | Meaning / observed representation |
| --- | --- |
| `gene`, `noncodingRNA` | Target-site and miRNA sequences; the two sequence inputs. |
| `noncodingRNA_name` | miRNA annotation, sometimes multiple candidates separated by `|`, e.g. `hsa-miR-320a-3p|hsa-miR-320b`; not a unique example ID. |
| `noncodingRNA_fam` | Family string, e.g. `let-7`, `mir-17`, or `unknown`; 368 combined rows have `unknown`. |
| `feature` | Original genomic annotation, e.g. `three_prime_utr`, `exon,intron`; 807 combined rows are blank. |
| `label` | Integer text `0` or `1`. |
| `chr`, `start`, `end`, `strand` | GRCh38 target location; chromosome strings such as `1`, `X`, `MT`; 1-based inclusive coordinates; `+`/`-`. Every observed interval spans 50 bases. |
| `Nunique` | Supporting unique-read count retained for positives; **set to zero for constructed negatives**. |
| `dominant_region`, `regions_present` | Selected-transcript overlap annotation, e.g. `INTRON`, `CDS|INTRON`; `NO_TRANSCRIPT` also occurs. |
| `read_start_in_sel_tx_1based`, `read_end_in_sel_tx_1based` | Transcript-relative coordinates, nullable integers; both blank in 908 combined rows. **No selected transcript identifier is included.** |
| `gene_cluster_ID` | Target-sequence similarity cluster identifier used for negative generation; not a biological gene ID or study identifier. |
| `gene_phyloP`, `gene_phastCons` | Serialized lists of per-position conservation values; 18 combined rows have blank values in each column. |

Concrete first train row, restricted to the two inputs and label:

```text
gene:         CAGCCTCCAGCCAAGCCCAGCTCACCGTCATTGCTTGCTCTCCTCCAGGT
noncodingRNA: TGAGGGCTCCAGGTGACGGTGG
label:        1
```

The same row is annotated `hsa-miR-4721`, family `unknown`, chromosome `16`, coordinates `28843854–28843903`, strand `-`, `Nunique=1541`, cluster `4187`. The [Zenodo description][zenodo] explains the historical and added columns; the actual downloaded header above supersedes its older 11-column summary. [Annotation filtering code][annotation] confirms that transcript IDs are not retained.

## Original study data versus miRBench processing

The [post-processing instructions][pipeline] explicitly link this precursor:

- Browse: https://github.com/ML-Bioinfo-CEITEC/HybriDetector/blob/main/ML/Datasets/AGO2_CLASH_Hejret2023_full_dataset.tsv
- Direct TSV: https://raw.githubusercontent.com/ML-Bioinfo-CEITEC/HybriDetector/main/ML/Datasets/AGO2_CLASH_Hejret2023_full_dataset.tsv

At inspected HybriDetector commit `3c104d9358e0f06dcc2511f63355c4a5d801e921`, this uncompressed **HybriDetector output** has **14,205 rows and 39 columns**, including 4,583 miRNA rows plus tRNA, YRNA, rRNA, snoRNA, and vaultRNA interactions. It is already processed experimental interaction data, **not raw sequencing reads** and not the ready-to-train miRBench positive/negative table. It has no `label` column. Relevant observed columns include `seq.g`, `noncodingRNA_seq`, `noncodingRNA_real_seq`, `noncodingRNA` (names here, not sequences), `noncodingRNA_type`, `miRNA_fam`, `gene_name`, `gene_biotype`, `chr.g`, `start.g`, `end.g`, `strand.g`, `Nunique`, and `rep`. [Pinned precursor][precursor].

Observed `rep` values contain `LBUB1`, `LBUB2`, `LBUB3`, singly or comma-separated when an interaction occurs in multiple replicates. These are precursor annotations, **not supplied study/project grouping IDs in miRBench**; they cannot simply be assumed to partition its constructed negatives. The processed schema drops `rep`, `gene_name`, and `gene_biotype`. The pipeline maps `seq.g` → `gene`, `noncodingRNA_seq` → `noncodingRNA`, and original `noncodingRNA` names → `noncodingRNA_name`; `miRNA_fam` must first be renamed `noncodingRNA_fam`. [Pipeline][pipeline], [filtering code][filter].

For actual original AGO2-CLASH sequencing data, the authors' [HybriDetector README][hybreadme] points to **GEO [GSE221573](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE221573)**. The separate older `ML/Datasets/miRNA_train_set.tsv` and `miRNA_test_set_1.tsv` are the original model datasets, not these corrected miRBench files; the miRBench paper identifies their miRNA-frequency bias and different original training class ratio. [Paper §2.1–2.2][benchpaper].

## Held-out evaluation: grouping and leakage caveats

1. **Exclude `Nunique` from predictors.** Across all 9,158 downloaded rows, it is zero for every negative and at least one for every positive. Thus `Nunique > 0` directly reconstructs the target. This is confirmed both by data inspection and the line assigning `negatives_df['Nunique'] = 0` in [negative generation][negatives]. For a sequence-prediction project, explicitly whitelist `gene` and `noncodingRNA` as inputs; treat the remaining fields as labels/audit metadata unless separately justified.
2. **The official holdout is by target chromosome.** [Filtering][filter] flags chromosome 1, [splitting code][split] uses that flag, and the downloads confirm it. It tests targets on a withheld chromosome; it is not a new study, replicate, miRNA, or family holdout.
3. **Observed overlap is narrower than biological independence.** There are no duplicate `(gene, noncodingRNA)` pairs within either file or across the two files, and no exact target sequence shared across splits. Nevertheless, **201 miRNA sequences**, **98 family-field values (including `unknown`)**, and **6 `gene_cluster_ID` values** occur in both train and test. All 98 test family-field values are represented in training. Clustering uses DECIPHER with default cutoff `0.1`; cluster IDs describe similar target sequences, not independent genes. [Clustering code][clustering]. Chromosome separation therefore does not guarantee disjoint sequence clusters or unseen miRNA families.
4. **Choose grouping to match the claim.** Available keys are target sequence, miRNA sequence, family, target cluster, and genomic locus/chromosome. `unknown` is not a real shared family; names may contain alternative annotations. There is no processed patient, study, project, replicate, biological gene ID, or transcript ID. Randomly splitting the combined rows would also disperse repeatedly used targets and related sequences. Cluster-held-out and family-held-out evaluation address different generalization questions; neither should be mislabeled an official Hejret split.
5. **Construction limits interpretation.** Clusters and negative sampling are computed before the chromosome split, using the pooled precursor targets and positive-family associations. The holdout is therefore part of a jointly curated benchmark, not a wholly independent experimental acquisition. Corrected miRNA frequencies balance globally but can differ by split, as discussed in paper §3.2. Synthetic negatives and the experiment's ascertainment limit claims about natural prevalence, calibrated biological binding probabilities, or repression efficacy. [Generation][negatives], [pipeline][pipeline], [paper][benchpaper].

## Implications for the instructor's requested project

For the requested team of three with a shared GitHub repository, commits/notes, an independently built predictor, and a model-independent evaluator: the data support a sequence-pair binary prediction task. A concrete evaluator contract should declare row identity/order, `label=1` as the positive class, score direction, and the named metrics. No stable row ID is provided; a project-created identifier must be documented as such. The evaluator should consume saved predictions without depending on a particular predictor's internals.

The official Hejret test file can be reserved as the untouched final holdout; development, threshold selection, and model selection should use only the training file and a documented internal validation split. These are project-design implications, not additional dataset fields or an implemented assignment. Git history/notes can record the pinned version, split decision, excluded leakage fields, and final evaluation procedure.

**Instructor clarification:** “left out project” means a standard held-out test set, not a study/project holdout. Exercise 10 therefore uses the official Hejret test file and reserves validation examples from its training file. Do not invent a `project` grouping column or substitute Manakov's specifically defined family-disjoint `leftout` for Hejret's chromosome-1 test. [Loader][loader], [paper §3.4.1][benchpaper].

[loader]: https://github.com/katarinagresova/miRBench/blob/6a9c9cca8891fc0dea8deab22030fcb6256c2412/src/miRBench/dataset.py
[zenodo]: https://zenodo.org/records/20540907
[benchpaper]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12261448/
[hejretpaper]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10739727/
[predictors]: https://github.com/katarinagresova/miRBench/blob/6a9c9cca8891fc0dea8deab22030fcb6256c2412/src/miRBench/predictor.py
[pipeline]: https://github.com/BioGeMT/miRBench_paper/blob/6a52d8705ce8ba5e831acadee61a6d8fb283d37e/code/post_process/README.md
[filter]: https://github.com/BioGeMT/miRBench_paper/blob/6a52d8705ce8ba5e831acadee61a6d8fb283d37e/code/filtering/filtering.py
[negatives]: https://github.com/BioGeMT/miRBench_paper/blob/6a52d8705ce8ba5e831acadee61a6d8fb283d37e/code/make_neg_sets/make_neg_sets.py
[annotation]: https://github.com/BioGeMT/miRBench_paper/blob/6a52d8705ce8ba5e831acadee61a6d8fb283d37e/code/genomic_region_annotator_filtering/genomic_region_annotator_filtering.py
[split]: https://github.com/BioGeMT/miRBench_paper/blob/6a52d8705ce8ba5e831acadee61a6d8fb283d37e/code/post_process/postprocess_4_train_test_splits.sh
[clustering]: https://github.com/BioGeMT/miRBench_paper/blob/6a52d8705ce8ba5e831acadee61a6d8fb283d37e/code/clustering/clustering.R
[precursor]: https://github.com/ML-Bioinfo-CEITEC/HybriDetector/blob/3c104d9358e0f06dcc2511f63355c4a5d801e921/ML/Datasets/AGO2_CLASH_Hejret2023_full_dataset.tsv
[hybreadme]: https://github.com/ML-Bioinfo-CEITEC/HybriDetector/blob/3c104d9358e0f06dcc2511f63355c4a5d801e921/README.md#data-availability
