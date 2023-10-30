import argparse
from anita.anita_pt_fo import check_proof as check_pt
from anita.anita_en_fo import check_proof as check_en
import os

def main():
    parser = argparse.ArgumentParser(description='Analytic Tableau Proof Assistant (ANITA).')
    parser.add_argument("-i", type=str, required=True, help="Arquivo de entrada com a prova em ANITA.")
    parser.add_argument("-l", type=str, default="pt", help="Digite pt para Português (default) ou en para Inglês.")
    parser.add_argument("-t", type=str, help="Entre com o teorema a ser analisado.")
    parser.add_argument("-dl", type=int, default=0, help="Digite 1 para exibir o código LaTeX.")
    parser.add_argument("-dt", type=int, default=0, help="Digite 1 para exibir o teorema.")
    parser.add_argument("-dc", type=int, default=0, help="Digite 1 para exibir o contra-exemplo do teorema.")
    args = parser.parse_args()
    input_theorem = None
    input_lang = "pt"
    input_display_latex = False
    input_display_theorem = False
    input_display_countermodel = False
    if args.i is not None: fileName = args.i
    if args.t is not None: input_theorem = args.t
    if args.l is not None: input_lang = args.l
    if args.dl is not None: input_display_latex = (args.dl==1)
    if args.dt is not None: input_display_theorem = (args.dt==1)
    if args.dc is not None: input_display_countermodel = (args.dc==1)

    if not os.path.isfile(fileName):
        return "Arquivo não encontradao"
    f = open(fileName, 'r')

    input_proof = f.read()
    if input_lang=="pt":
        print(check_pt(input_proof,input_theorem=input_theorem,display_latex=input_display_latex, display_theorem=input_display_theorem, display_countermodel=input_display_countermodel))
    elif input_lang=="en":
        print(check_en(input_proof,input_theorem=input_theorem,display_latex=input_display_latex, display_theorem=input_display_theorem, display_countermodel=input_display_countermodel))
    else:
        print("Você deve escolher pt para Português (default) ou en para Inglês.")
    

if __name__ == '__main__':
    main()
