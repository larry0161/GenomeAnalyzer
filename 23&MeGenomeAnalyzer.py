import sys
import json
import ray
import os
import shutil
#This program will input your raw genetic data from 23&Me and 
# cross-reference your genotype with NCBI database for associated 
# traits. The first file "AnalyzedGenome.txt" will include all 
#results from cross referencing including those without any 
#associated trait or data. The second file, "CleanedAnalysis.txt"
#will only include RSID/genotype pairs that match documented
#phenotype associations.

#The motivation behind this script was to provide a means for
#users to gain insight into their genetic makeup without having
#to divulge their private genetic profile. It is also a way to analyze
#the genome at zero cost besides computation time. 

# Replace "YOUR_23&ME_RAW_DATA.txt" with the name of your file.
# Make sure your raw data is in the same directory as this program
file = 'YOUR_23&ME_RAW_DATA.txt'
data = open(file,'r').readlines()
n = len(data)
cpu=os.cpu_count()


@ray.remote
def f(data_split,file_num):
    temp_file = open('file'+str(file_num),'w')
    
    server = "http://grch37.rest.ensembl.org/variation/human/"
    ext = "?phenotypes=1"
    for i in data_split:
        rsid,chrome,position,alleles =i.split()

        r = requests.get(server+rsid+ext, headers={ "Content-Type" : "application/json"})
        gene = 'N/A'
        most_severe = 'N/A'
        detected = 'N/A'
        trait = 'N/A'
        if not r.ok:
            temp_file.write(rsid+'\t'+gene+'\t'+trait+'\n')
        else:
            decoded = r.json()
            if 'most_severe_consequence' in decoded:
                most_severe = decoded['most_severe_consequence']
            hold =set()
            if 'phenotypes' in decoded:
                for j in decoded['phenotypes']:
                    if gene == 'N/A' and 'genes' in j and j['genes']:
                        gene = j['genes']
                    if 'risk_allele' in j and j['risk_allele'] in alleles:
                        if 'trait' in j and j['trait']:
                            hold.add(j['trait'])
            if hold:
                trait = ', '.join(i for i in hold)
            temp_file.write(rsid+'\t'+gene+'\t'+trait+'\n')



step = n//cpu
steps = [i for i in range(0,n-step+1,step)]
steps.append(n)

def go():

    ray.get([f.remote(data[steps[i]:steps[i+1]],i) for i in range(cpu)])
go()
#AnalyzedGenome.txt includes results from all 600k+ RSID genotypes, including those with no associated traits or RSID's not found in the database
with open('AnalyzedGenome.txt','wb') as wfd:
    wfd.write(("RSID"+'\t'+"GENE"+'\t'+"POSSIBLE TRAITS"+'\n').encode(encoding='UTF-8'))
    files = ['file'+str(i) for i in range(cpu)]
    for f in files:
        with open(f,'rb') as fd:
            shutil.copyfileobj(fd, wfd)


#CleanedAnalysis.txt only includes results where RSID and user genotype were documented with an associated phenotype
AnalyzedGenome = open('AnalyzedGenome.txt','r').readlines()
n=len(AnalyzedGenome)
CleanedAnalysis = open("CleanedAnalysis.txt",'w')
CleanedAnalysis.write(("RSID"+'\t'+"GENE"+'\t'+"POSSIBLE_TRAITS"+'\n'))
for i in range(1,n):
    row = AnalyzedGenome[i].split()
    if row[-1]!='N/A':
        CleanedAnalysis.write(yo[i])
CleanedAnalysis.close()