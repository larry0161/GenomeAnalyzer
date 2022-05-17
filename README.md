# GenomeAnalyzer
23&amp;Me Genome Analysis

Motivation behind this script was the lack of services providing free genome analysis without having to divulge your private genetic profile. This script allows users to analyze their own genome without having to give up such sensitive information. 

Steps to use this script:

1.) Download your raw data from 23&Me.

2.) Download the file 23&MeGenomeAnalyzer.py

3.) Insert the name of your file in the script under file variable. Ex: file='YOUR_GENOME.txt'

4.) Run the script!

Two files will be produced:

GenomeAnalysis.txt will provide every result from all RSID's given, including those missing from the database or without any associated traits.

CleanedAnalysis.txt will only provide you with results where your RSID and genotype were associated with a documented trait.

The output files will be spaced in the following format:      RSID   GENE_NAME    POSSIBLE_TRAITS

I hope you find the script useful. Have fun!
