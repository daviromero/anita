import ipywidgets as widgets
from IPython.display import display, Markdown
import traceback
import anita_en_fo

def anita(input_string='', height_layout='300px'):
  layout = widgets.Layout(width='90%', height=height_layout)
  run = widgets.Button(description="Check")
  input = widgets.Textarea(
      value=input_string,
      placeholder='Enter you proof',
      description='',
      layout=layout
      )
  cLatex = widgets.Checkbox(value=False, description='Display Latex')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cLatex])
  
  display(widgets.HTML('<h3>Enter your proof in Analytic Tableau:</h3>'), 
          input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = anita_en_fo.ParserAnita.getProof(input.value)
          if(result.errors==[]):
            msg = []
            if(result.is_closed):
              display(Markdown(rf'**<font color="blue">Congratulations! The proof of {result.theorem} is valid.</font>**'))
            else:
              if result.saturared_branches!=[]:
                display(Markdown(rf'**<font color="blue">Theorem {result.theorem} is not valid.</font>**'))              
                msg.append("Countermodels:")
                for s_v in result.counter_examples:
                  msg.append(s_v)                  
              else:
                display(Markdown(rf'**<font color="red">The proof of {result.theorem} is not complete.</font>**'))              
                msg.append("The branches below are not saturated:")
                for rules in result.open_branches:
                  msg.append("Branch:")
                  msg.append('<br>'.join([r.toString() for r in reversed(rules)]))
            if(cLatex.value):
              msg.append("LaTeX Code:")
              msg.append("%"+result.latex_theorem)
              msg.append(result.colored_latex)
            display(widgets.HTML('<br>'.join(msg)))       
          else:
            display(Markdown(rf'**<font color="red">The proof is not correct:</font>**'))
            for error in result.errors:
                print(error)
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def anita_theorem(input_theorem, input_proof='', height_layout='300px',default_gentzen=False, default_fitch=False):
  layout = widgets.Layout(width='90%', height=height_layout)
  run = widgets.Button(description="Verificar")
  input = widgets.Textarea(
      value=input_proof,
      placeholder='Digite sua demonstração:',
      description='',
      layout=layout
      )
  premisses, conclusion = anita_en_fo.ParserTheorem.getTheorem(input_theorem)
  if conclusion == None:
    display(Markdown(rf'**<font color="red">{input_theorem} não é um teorema válido!</font>**'))
    return
  cLatex = widgets.Checkbox(value=False, description='Exibir Latex')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cLatex])
  
  display(widgets.HTML(f'<h3>Digite a demonstração de {input_theorem} em Tableau Analítico:</h3>'), 
          input, wButtons, output)
  
  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = anita_en_fo.ParserAnita.getProof(input.value)
          if(result.errors==[]):
              set_premisses = set([p.toString() for p in premisses])
              set_premisses_result = set([p.toString() for p in result.premisses])
              if(conclusion==result.conclusion and set_premisses==set_premisses_result):
                msg = []
                if(result.is_closed):
                  display(Markdown(rf'**<font color="blue">Parabéns! A demonstraçãoo de {result.theorem} está correta.</font>**'))
                else:
                  if result.saturared_branches!=[]:
                    display(Markdown(rf'**<font color="blue">O teorema {result.theorem} não é válido.</font>**'))              
                    msg.append("São contra-exemplos:")
                    for s_v in result.counter_examples:
                      msg.append(s_v)                  
                  else:
                    display(Markdown(rf'**<font color="red">A demonstração de {result.theorem} não está completa.</font>**'))              
                    msg.append("Os ramos abaixo não estão saturados:")
                    for rules in result.open_branches:
                      msg.append("Ramo:")
                      msg.append('<br>'.join([r.toString() for r in reversed(rules)]))
                if(cLatex.value):
                  msg.append("Código Latex:")
                  msg.append("%"+result.latex_theorem)
                  msg.append(result.colored_latex)
                display(widgets.HTML('<br>'.join(msg)))       
              else:
                display(Markdown(rf'**<font color="red">Sua demostração de {result.theorem} é válida, mas é diferente da demonstração solicitada {input_theorem}!</font>**'))
          else:
            display(Markdown(rf'**<font color="red">Sua demonstração contém os seguintes erros:</font>**'))
            for error in result.errors:
                print(error)
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)




from random import randrange

lTheorems = [' |- (A|(A&B))->A', ' |- (A&(A|B))->A', ' |- (A->(B->C))->(B->(A->C))', ' |- (A->(A->B))->(A->B)', ' |- (~A->B)->((~A->~B)->A)', ' |- A|~A', ' |- (A->B)|(B->A)', ' |- A->A', ' |- (A->B)->((C->A)->(C->A))', 'A&B->C |- B->(A->C)', 'B->(A->C) |- A&B->C', ' |- (A->(B->C))->((A->B)->(A->C))', ' |- A->(B->A)', ' |- ((A->B)->A)->A', 'A->C, A|B, B->C |- C', 'A |- ~~A', '~~A |- A', 'A->B, ~B |- ~A', '~B->~A |- A->B', 'A->B |- ~B->~A', '~(A|B) |- ~A&~B', '~A&~B |- ~(A|B)', '~(A&B) |- ~A|~B', '~A|~B |- ~(A&B)', 'A|(B&C) |- (A|B)&(A|C)', '(A|B)&(A|C) |- A|(B&C)', 'A&(B|C) |- (A&B)|(A&C)', '(A&B)|(A&C) |- A&(B|C)', 'A|B, ~B |- A', 'A|B |- ~A->B', '~A->B |- A|B', 'A&B |- ~(A->~B)', '~(A->~B) |- A&B', 'A|B |- ~(~A&~B)', '~(~A&~B) |- A|B', 'A->B |- ~(A&~B)', '~(A&~B) |- A->B', 'A&B |- ~(~A|~B)', '~(~A|~B) |- A&B', 'A->B |- ~A|B', '~A|B |- A->B', ' |- Ax P(x)->~Ex ~P(x)', ' |- ~Ex ~P(x)->Ax P(x)', ' |- ~Ex ~P(x)->Ax P(x)', ' |- Ex P(x)->~Ax ~P(x)', ' |- Ax (P(x)&Q(x))->(Ax P(x)&Ax Q(x))', ' |- Ax Ay P(x,y)->Ay Ax P(x,y)', ' |- Ax (P->Q(x))->(P->Ax Q(x))', ' |- Ex (P(x)|Q(x))->(Ex P(x)|Ex Q(x))', ' |- ~Ax P(x)->Ex ~P(x)', ' |- Ex ~P(x)->~Ax P(x)', ' |- ~Ex P(x)->Ax ~P(x)', ' |- Ax ~P(x)->~Ex P(x)', ' |- Ex (P(x)&Q)->(Ex P(x)&Q)', ' |- (Ex P(x)&Q)->Ex (P(x)&Q)', ' |- Ax (P(x)|Q)->(Ax P(x)|Q)', ' |- (Ax P(x)|Q)->Ax (P(x)|Q)', ' |- Ex (P(x)->Q)->(Ax P(x)->Q)', ' |- (Ax P(x)->Q)->Ex (P(x)->Q)', ' |- Ex (P->Q(x))->(P->Ex Q(x))', ' |- (P->Ex Q(x))->Ex (P->Q(x))', ' |- Ex (P(x)->Ax P(x))']

