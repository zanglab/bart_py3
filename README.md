
# README for BART(v1.0.1)

## Introduction

[BART](http://faculty.virginia.edu/zanglab/bart) (**B**inding **A**nalysis for **R**egulation of **T**ranscription) is a bioinformatics tool for predicting functional transcription factors (TFs) that bind at genomic cis-regulatory regions to regulate gene expression in the human or mouse genomes, given a query gene set or a ChIP-seq dataset as input. BART leverages 3,485 human TF binding profiles and 3,055 mouse TF binding profiles from the public domain (collected in Cistrome Data Browser) to make the prediction.

BART is implemented in Python and distributed as an open-source package along with necessary data libraries.

BART is developed and maintained by the [Chongzhi Zang Lab](http://faculty.virginia.edu/zanglab/) at the University of Virginia.

**We only provide the source code package on github. In order to run BART, you have to download the [Data Libraries](http://faculty.virginia.edu/zanglab/bart/index.htm#download).**

BART web interface (Beta version) can be accessed [here](http://bartweb.uvasomrc.io/).


## Installation

### Prerequisites

BART uses Python's distutils tools for source installation. Before installing BART, please make sure either Python2 (Python2.7 or higher is recommended) or Python3 (Python 3.3 or higher is recommended) is installed in the system, and the following python packages are installed:

- [setuptools](https://pypi.python.org/pypi/setuptools)
- [numpy](https://pypi.python.org/pypi/numpy)
- [pandas](https://pypi.python.org/pypi/pandas)
- [scipy](https://pypi.python.org/pypi/scipy)
- [matplotlib](https://matplotlib.org/users/installing.html)


### Install from source package without data libraries 

You can download the [Human or Mouse Data Library](http://faculty.virginia.edu/zanglab/bart/index.htm#download) separately under your own directory. In this case, you have to edit the config file (e.g. `BART1.1/BART/bart.conf`) after you unpack the source package to provide the directory for the data. For example, if you download the `hg38_library.tar.gz` (or `mm10_library.tar.gz`) and unpack it under `/path/to/data`, then you can modify the bart.conf file as:

```shell
hg38_library_dir = /path/to/data/
```

To install a source distribution of BART, unpack the distribution tarball and open up a command terminal. Go to the directory where you unpacked BART, and simply run the install script an install BART globally or locally. 

e.g., if you want to install the package `BART-v1.1-py3.tar.gz`:

```shell
$ tar zxf BART-v1.1-py3.tar.gz
$ cd BART-v1.1-py3
```

Install with root/administrator permission (by default, the script will install python library and executable codes globally):

```shell
$ python setup.py install
```

If you want to install everything under your own directory, for example, a directory as `/path/to/bart/`, use these commands:

```shell
$ mkdir -p /path/to/bart/lib/pythonX.Y/site-packages 
$ export PYTHONPATH=/path/to/bart/lib/pythonX.Y/site-packages/:$PYTHONPATH 
$ python setup.py install --prefix /path/to/bart 
$ export PATH=/path/to/bart/bin/:$PATH
```

In this value, X.Y stands for the major–minor version of Python you are using (such as 2.7 or 3.5 ; you can find this with` sys.version[:3]` from a Python command line).


### Configure environment variables

You’ll need to add those two lines in your bash file (varies on each platform, usually is `~/.bashrc` or `~/.bash_profile`) so that you can use the BART command line directly:

```shell
  $ export PYTHONPATH=/path/to/bart/lib/pythonX.Y/site-packages/:$PYTHONPATH 
  $ export PATH=/path/to/bart/bin/:$PATH
```


 

## Tutorial

### Positional arguments

{geneset,profile}


### bart geneset

Given a query gene set (at least 100 genes recommended), predict functional transcription factors that regulate these genes.

#### *Usage*:	
`bart geneset [-h] -i <file> -s <species> [-t <target>] [-p <processes>] [--nonorm] [--outdir <outdir>] [-o <ofilename>]`

#### *Example*:	
`bart geneset -i name_enhancer_prediction.txt -s hg38 -t target.txt -p 4 --outdir bart_output`


#### *Input arguments*:

**-i <file>, --infile <file>**

Input file, the name_enhancer_prediction.txt profile generated from MARGE.

**-s <species>, --species <species>**

Species, please choose from "hg38" or "mm10".

**-t <target>, --target <target>**

Target transcription factors of interests, please put each TF in one line. BART will generate extra plots showing prediction results for each TF.

**-p <processes>, --processes <processes>**

Number of CPUs BART can use.

**--nonorm**

Whether or not do the standardization for each TF by all of its Wilcoxon statistic scores in our compendium. If set, BART will not do the normalization. Default: FALSE.

#### *Output arguments*:

**--outdir <outdir>**

If specified, all output files will be written to that directory. Default: the current working directory

**-o <ofilename>, --ofilename <ofilename>**

Name string of output files. Default: the base name of the input file.

#### *Notes*:

The input file for `BART geneset`, i.e., the `enhancer_prediction.txt` file generated by MARGE might have these two formats (depends on py2 or py3 version):

- Python2 version:
```
1	98.19
2	99.76
3	99.76
4	9.49
5	44.37
6	18.14
```

- Python3 version:
```
chrom	start	end	UDHSID	Score
chr3	175483637	175483761	643494	3086.50
chr3	175485120	175485170	643497	2999.18
chr3	175484862	175485092	643496	2998.28
chr3	175484804	175484854	643495	2976.27
chr3	175491775	175491825	643507	2879.01
chr3	175478670	175478836	643491	2836.90
```

### bart profile

Given a ChIP-seq data file (`bed` or `bam` format mapped reads), predict transcription factors whose binding pattern associates with the input ChIP-seq profile.


#### *Usage*: 	

`bart profile [-h] -i <file> -f <format> [-n <int>] -s <species>
                    			[-t <target>] [-p <processes>] [--nonorm]
                    			[--outdir <outdir>] [-o <ofilename>]`

#### *Example*:	

`bart profile -i ChIP.bed -f bed -s hg38 -t target.txt -p 4 --outdir bart_output`



#### *Input files arguments*:

**-i <file>, --infile <file>**

Input ChIP-seq bed or bam file.

**-f <format>, --format <format>**

Specify "bed" or "bam" format.

**-n <int>, --fragmentsize <int>**

Fragment size of ChIP-seq reads, in bps. Default: 150.

**-s <species>, --species <species>**

Species, please choose from "hg38" or "mm10".

**-t <target>, --target <target>**

Target transcription factors of interests, please put each TF in one line. BART will generate extra plots showing prediction results for each TF.

**-p <processes>, --processes <processes>**

Number of CPUs BART can use.

**--nonorm**

Whether or not do the standardization for each TF by all of its Wilcoxon statistic scores in our compendium. If set, BART    will not do the normalization. Default: FALSE.

#### *Output arguments*:

**--outdir <outdir>**

If specified, all output files will be written to that directory. Default: the current working directory

**-o <ofilename>, --ofilename <ofilename>**

Name string of output files. Default: the base name of input file.


#### *Notes*:

The input file for `BART profile` should be [BED](https://genome.ucsc.edu/FAQ/FAQformat#format1) or [BAM](http://samtools.github.io/hts-specs/SAMv1.pdf) format in either `hg38` or `mm10`. 

Bed is a tab-delimited text file that defines the data lines, and the BED file format is described on [UCSC genome browser website](https://genome.ucsc.edu/FAQ/FAQformat). For BED format input, the first three columns should be `chrom`, `chromStart`, `chromEnd`, and the 6th column of `strand` information is required by BART. 

BAM is a binary version of [Sequence Alignment/Map(SAM)](http://samtools.sourceforge.net) format, and for more information about BAM custom tracks, please [click here](https://genome.ucsc.edu/goldenPath/help/bam.html). 



### Output files

1. **name_auc.txt** contains the ROC-AUC scores for all TF datasets in human/mouse, we use this score to measure the similarity of TF dataset to cis-regulatory profile, and all TFs are ranked decreasingly by scores. The file should be like this:
```
AR_56254	    AUC = 0.954
AR_44331	    AUC = 0.950
AR_44338	    AUC = 0.949
AR_50273	    AUC = 0.947
AR_44314	    AUC = 0.945
AR_44330	    AUC = 0.943
AR_50100	    AUC = 0.942
AR_44315	    AUC = 0.942
AR_50044	    AUC = 0.926
AR_50041	    AUC = 0.925
FOXA1_50274	    AUC = 0.924
AR_50042	    AUC = 0.921
```

2. **name_bart_results.txt** is a ranking list of all TFs, which includes the Wilcoxon statistic score, Wilcoxon p value, standard Wilcoxon statistic score (zscore), maximum ROC-AUC score, rank score (relative rank of z score, p value and max auc) and Irwin Hall p value (p value for the relative rank) for each TF. The most functional TFs of input data are ranked first. The file should be like this:
```
TF	statistic	pvalue	zscore	max_auc	re_rank	irwin_hall_pvalue
AR	18.654	5.861e-78	3.024	0.954	0.004	3.733e-07
FOXA1	13.272	1.673e-40	2.847	0.924	0.008	2.300e-06
PIAS1	3.987	3.339e-05	2.802	0.872	0.017	2.389e-05
SUMO2	5.213	9.269e-08	3.494	0.749	0.018	2.700e-05
HOXB13	3.800	7.230e-05	2.632	0.909	0.019	3.037e-05
GATA3	5.800	3.316e-09	2.549	0.769	0.025	7.410e-05
TOP1	2.254	1.210e-02	3.057	0.779	0.026	8.063e-05
HDAC3	2.310	1.044e-02	2.478	0.845	0.033	1.682e-04
NR3C1	4.500	3.394e-06	2.042	0.871	0.036	2.160e-04
GATA6	4.240	1.118e-05	2.602	0.632	0.043	3.549e-04
```

3. **name_plot** is a folder which contains all the extra plots for the TFs listed in target files (target.txt file in test data). For each TF, we have rank dot plot, which shows the rank position of the TF amont all TFs on x-axis and Irwin Hall p value on y-axis (derived from the rank score in name_bart_results.txt), and the cumulative distribution plot, which compares the distribution of ROC-AUC scores from datasets of the TF and the scores of all background datasets (derived from the AUC scores in name_auc.txt).