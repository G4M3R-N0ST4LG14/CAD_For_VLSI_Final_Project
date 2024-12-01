# CAD_For_VLSI_Final_Project
## Prompt 1: Implement QM in a Language of Choice (Python)
### By Arturo Lara, UCF Computer Engineering Undergrad

This project implements the Quine-McCluskey Algorithm to minimize BLIF files and return a SOP in the form of a PLA file.
The source code for the program can be found in quine_mccluskey.py.
The program will take in a .blif file which in this directory can be found in input.blif.
When the program has successfully minimized the minterms to an SOP a file formatted in PLA called output.pla will be generated.

The following code is how the BLIF file should be formatted where everything modifiable is in []:
.model [file name]
.inputs [character inputs (ex. A B C D)]
.outputs [character output]
(Please note I only accounted for the input file to have only one output)
(This program is designed for QM Algorithm minimization so there should be only one output)
.names [character inputs and outputs listed like in inputs example]
[minterms and don't cares where 1 indicates a minterm and - indicates a don't care]
(example of minterm 1 with 4 inputs: 0001 1)
(example of don't care 9 with 4 inputs: 1001 -)
.end

The following code is how the PLA output will look like:
.i [number of inputs]
.o F (Simply because I don't like it otherwise the output of the PLA will always be F)
(This is because I prefer the output SOP format to be F(inputs) = SOP)
(If you would like to change it to match whatever the input file has listed go to read_blif_file() and add it there)
.ilb [list of inputs]
.ob [character of outputs]
[minterms]
(0s indicate 'not', 1s indicate true, - indicate don't cares)
(example of A'D: 0--1
.e

## Issues with creating project
The biggest issue with tackling this project was dealing with the Prime Implicants as making the algorithm find the essential implicants would require a lot of effort.
Adding the working code in step 3 of the simplify function would help find the essential prime implicants much easier in step 4. 
Once the prime implicants would be properly in the coverage table the simplify function would work smoothly.

Another annoying issue was dealing with the input file, reading the minterms would for some reason cause issues if tried to find the exact number of inputs and count until they pass and the output is available. Also what was very useful for this section was splitting the inputs and the outputs so that the output can be read to determine if it is a minterm or don't care. This allows me to search for them in case they are out of order and avoid any outputs of 0.

Before attemping this version of the project C was going to be used as the language but before I could get too far I couldn't get the BLIF files to be read. This lead me to choose Python since its environment is overall easier

#Credit to GeekyBoy here on Github and his own QM solver
Made verifying that my algorithm was correct a lot easier as AI like ChatGPT proved useless since it kept returning wrong answers
https://geeekyboy.github.io/Quine-McCluskey-Solver/

