def psmcboot(sample):
    for i in range(1,101):
	    with open(f'{i}_{sample}.sh','w') as f:
		    f.write(f'''
#!/bin/bash
#PBS    -N {i}_{sample}
#PBS    -l nodes=1:ppn=1
#PBS    -l mem=1G
#PBS    -q batch
#PBS    -V
export ROAD=../
export road=psmc
$road/psmc -N25 -t15 -r5 -b -p "4+25*2+4+6" -o {sample}-{i}.psmc $ROAD/split.{sample}.psmcfa
		''')
from sys import argv
psmcboot(argv[1])
