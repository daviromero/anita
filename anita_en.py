import anita_en_fo
import argparse
import traceback

parser = argparse.ArgumentParser(description='Analytic Tableau Proof Assistant (ANITA).')
parser.add_argument("-i", type=str,help="Input file with the proof in ANITA.")
parser.add_argument("-o", type=str,help="Output file of result of the checking of the proof in ANITA.")
args = parser.parse_args()
fileName = 'example_anita.txt'
fileSave = 'result_anita.txt'
if args.i is not None: fileName = args.i
if args.o is not None: fileSave = args.o
try:
    f = open(fileName, 'r')
    input_proof = f.read()
    result = anita_en_fo.ParserAnita.getProof(input_proof)
    with open(fileSave, "w", encoding='utf8') as fs:
        if(result.errors==[]):
            if(result.is_closed):
                fs.write("The proof below is valid.\n")
                fs.write(result.theorem) 
                fs.write("\n;"+str(result.latex))
                fs.write(";The proof of theorem ${}$ is valid.\n".format(result.latex_theorem))
                fs.write("\n"+str(result.colored_latex))
            else:
                if result.saturared_branches != []:
                    fs.write("The theorem is not valid.\n")
                    fs.write(result.theorem) 
                    fs.write("\nCountermodels:")
                    for s_v in result.counter_examples:
                        fs.write('\n  '+s_v)
                    fs.write("\n;"+str(result.latex))
                    fs.write(";Theorem ${}$ is not valid.\n".format(result.latex_theorem))
                    fs.write("\nCountermodels:")
                    fs.write("\n\\begin{itemize}")
                    for s_v in result.counter_examples:
                        fs.write('\n  \item $'+s_v+'$')
                    fs.write("\n\end{itemize}")
                    fs.write("\n"+str(result.colored_latex))
                else: 
                    fs.write("The proof below is not complete.\n")
                    fs.write(result.theorem) 
                    fs.write("\nThe branches below are not saturated:")
                    for rules in result.open_branches:
                        fs.write("\nBranch:\n  ")
                        fs.write('\n  '.join([r.toString() for r in reversed(rules)]))
                    fs.write("\n;"+str(result.latex))
                    fs.write(";The proof of theorem ${}$ is not complete.\n".format(result.latex_theorem))
                    fs.write("\n"+str(result.colored_latex))

        else:
            fs.write("The following errors were found:\n\n")
            for error in result.errors:
                fs.write(str(error))
    fs.close()
except ValueError:
    s = traceback.format_exc()
    result = (s.split("@@"))[-1]
    with open(fileSave, "w", encoding='utf8') as fs:
        fs.write("The following errors were found:\n\n")
        fs.write(result)
    print (f'{result}')
else:
    pass
