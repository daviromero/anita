import anita_pt_fo
import argparse
import traceback

parser = argparse.ArgumentParser(description='Analytic Tableau Proof Assistant (ANITA).')
parser.add_argument("-i", type=str,help="Arquivo de entrada com a prova em ANITA.")
parser.add_argument("-o", type=str,help="Arquivo de saída do resultado da verificação da prova na ANITA")
args = parser.parse_args()
fileName = 'example_anita.txt'
fileSave = 'result_anita.txt'
if args.i is not None: fileName = args.i
if args.o is not None: fileSave = args.o

try:
    f = open(fileName, 'r')
    input_proof = f.read()
    result = anita_pt_fo.ParserAnita.getProof(input_proof)
    with open(fileSave, "w", encoding='utf8') as fs:
        if(result.errors==[]):
            if(result.is_closed):
                fs.write("A demonstração abaixo está correta.\n")
                fs.write(result.theorem) 
                fs.write("\n;"+str(result.latex))
                fs.write(";A demonstração do teorema ${}$ está correta.\n".format(result.latex_theorem))
                fs.write("\n"+str(result.colored_latex))
            else:
                if result.saturared_branches != []:
                    fs.write("O Teorema abaixo não é válido.\n")
                    fs.write(result.theorem) 
                    fs.write("\nSão contra-exemplos:")
                    for s_v in result.counter_examples:
                        fs.write('\n  '+s_v)
                    fs.write("\n;"+str(result.latex))
                    fs.write(";O Teorema ${}$ não é válido.\n".format(result.latex_theorem))
                    fs.write("\nSão contra-exemplos:")
                    fs.write("\n\\begin{itemize}")
                    for s_v in result.counter_examples:
                        fs.write('\n  \item $'+s_v+'$')
                    fs.write("\n\end{itemize}")
                    fs.write("\n"+str(result.colored_latex))
                else: 
                    fs.write("A demonstração do teorema abaixo não está completa.\n")
                    fs.write(result.theorem) 
                    fs.write("\nOs ramos abaixo não estão saturados:")
                    for rules in result.open_branches:
                        fs.write("\nRamo:\n  ")
                        fs.write('\n  '.join([r.toString() for r in reversed(rules)]))
                    fs.write("\n;"+str(result.latex))
                    fs.write(";A demonstração do teorema ${}$ não está completa.\n".format(result.latex_theorem))
                    fs.write("\n"+str(result.colored_latex))

        else:
            fs.write("Os seguintes erros foram encontrados:\n\n")
            for error in result.errors:
                fs.write(str(error))
    fs.close()
except ValueError:
    s = traceback.format_exc()
    result = (s.split("@@"))[-1]
    with open(fileSave, "w", encoding='utf8') as fs:
        fs.write("Os seguintes erros foram encontrados:\n\n")
        fs.write(result)
    print (f'{result}')
else:
    pass
