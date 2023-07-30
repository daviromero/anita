import argparse
from anita.anita_pt_fo import check_proof as check_pt
from anita.anita_en_fo import check_proof as check_en
import os

parser = argparse.ArgumentParser(description='Analytic Tableau Proof Assistant (ANITA).')
parser.add_argument("-i", type=str, required=True, help="Arquivo de entrada com a prova em ANITA.")
parser.add_argument("-l", type=str, default="pt", help="Digite pt para Português (default) ou en para Inglês.")
parser.add_argument("-t", type=str, help="Entre com o teorema a ser analisado.")
parser.add_argument("-dl", type=int, default=0, help="Digite 1 para exibir o código LaTeX.")
args = parser.parse_args()
input_theorem = None
input_lang = "pt"
input_display_latex = False
if args.i is not None: fileName = args.i
if args.t is not None: input_theorem = args.t
if args.l is not None: input_lang = args.l
if args.dl is not None: input_display_latex = (args.dl==1)


def app(fileName, input_theorem, input_lang, input_display_latex):
    if not os.path.isfile(fileName):
        return "Arquivo não encontradao"
    f = open(fileName, 'r')

    input_proof = f.read()
    if input_lang=="pt":
        return check_pt(input_proof,input_theorem=input_theorem,display_latex=input_display_latex)
    elif input_lang=="en":
        return check_en(input_proof,input_theorem=input_theorem,display_latex=input_display_latex)
    else:
        return "Você deve escolher pt para Português (default) ou en para Inglês."
    
print(app(fileName,input_theorem,input_lang,input_display_latex))