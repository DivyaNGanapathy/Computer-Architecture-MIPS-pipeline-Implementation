ReadMe:

The .pyz is the executable archive created to package the 3 .py files. This .pyz can be opened in notepad++ to see the source code (all the 3 .py files merged)
Alternatively the source code can be found under the directory Simulator
Denpendencies : 1) Python 3.7
		2) Library Tabulate (already installed on the package)
		

Steps to Run
------------ 


Method 1: 
Using just .pyz file
.pyz present in the rootdirectory(simulator)
.pyz and all the text files(inst.txt, reg.txt,config,txt etc) should be present in the same root directory
Typical folder structure

C:\Users\divya\Desktop\simulator

	tabulate.py
	simulator.pyz
	inst.txt 
	data.txt 
	reg.txt 
	config.txt 
	result.txt

Assuming 
python installed ? Yes  (python 3.7)
pip installed ? Yes
zipapp installed ? Yes

Step 1- In command prompt go to the directory(simulator)(e.g. Desktop, Downloads etc) which has the .pyz file and type

	simulator.pyz inst.txt data.txt reg.txt config.txt result.txt
	
			or

	python simulator.pyz inst.txt data.txt reg.txt config.txt result.txt


 	Check the result in result.txt present in the same directory

################################################################################################################################################################
								IF METHOD 1 DOESNOT WORK
################################################################################################################################################################

Method 2: Not using pyz file, instead creating a new pyz file from the directory of source code 

Packages are installed into simulator before packaging (pip install tabulate)
If it doesnot work then 
Step 1- Get the name of the directory containing the source (containing all the 3 .py files) and run the below command to install the package required (eg tabulate)
	In cmd navigate to the parent directory of simulator then type

	python -m pip install tabulate --target simulator

Step 2- Zip the file into executable archive using the below command(create .pyz file)
	python -m zipapp NameoftheDirectory -m "main:main"
        e.g. python -m zipapp simulator -m "main:main"
	IMPORTANT: place the generated .pyz file, inside the directory 'simulator' directory

Step 3- Run the below command

	python NameoftheDirectory.pyz inst.txt data.txt reg.txt config.txt result.txt (same as Method 1)
	e.g. simulator.pyz inst.txt data.txt reg.txt config.txt result.txt
	
			or

	python simulator.pyz inst.txt data.txt reg.txt config.txt result.txt

	Check the result in result.txt present in the same directory