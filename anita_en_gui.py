import ipywidgets as widgets
from IPython.display import display, Markdown
import traceback
from anita_pt_fo import ParserAnita, ParserTheorem, ParserFormula

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
          result = ParserAnita.getProof(input.value)
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
  run = widgets.Button(description="Check")
  input = widgets.Textarea(
      value=input_proof,
      placeholder='Digite sua demonstração:',
      description='',
      layout=layout
      )
  premisses, conclusion = ParserTheorem.getTheorem(input_theorem)
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
          result = ParserAnita.getProof(input.value)
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



def is_substitutable(input_formula='', input_var ='x', input_term='a'):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Check")
  cResult = widgets.RadioButtons(
    options=['Yes', 'No'],
    value=None, 
    description='Answer:',
    disabled=False
)
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**The variable {input_var} is substitutable by the term {input_term} in the formula {input_formula}:**'))
  display(cResult, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          if(f!=None):
            if (f.is_substitutable(input_var,input_term) and cResult.value=='Yes'):
              display(Markdown(r'**<font color="blue">Congratulations you got the question right!</font>**'))              
              display(Markdown(rf'The variable {input_var} **is substitutable** by the term {input_term} in the formula {input_formula}.'))              
            elif not f.is_substitutable(input_var,input_term) and cResult.value=='No':
              display(Markdown(r'**<font color="blue">Congratulations you got the question right!</font>**'))              
              display(Markdown(rf'The variable {input_var} **is not substitutable** by the term {input_term} in the formula {input_formula}.')) 
            else:
              display(Markdown(rf'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Enter the variables separated by ; (semicolon)',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Enter the set of variables of the formula {input_formula}:**'))
  display(Markdown(r'Each element of your set must be separated by ; (semicolon)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.all_variables():
              display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)


def verify_free_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Enter the variables separated by ; (semicolon)',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Enter the set of the free variables of the formula {input_formula}:**'))
  display(Markdown(r'Each element of your set must be separated by ; (semicolon)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.free_variables():
              display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_bound_variables(input_string='', input_formula = ''):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Enter the variables separated by ; (semicolon)',
      description='',
      layout=layout
      )
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  
  display(Markdown(rf'**Enter the set of bound variables of the formula {input_formula}:**'))
  display(Markdown(r'Each element of your set must be separated by ; (semicolon)'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          result = ParserFormula.getFormula(input_formula)
          variables = set([x.strip() for x in input.value.strip().split(";")])
          if(result!=None):
            if variables==result.bound_variables():
              display(Markdown(r'**<font color="blue">Congratulations, you got the question right!</font>**'))              
            else:
              display(Markdown(rf'**<font color="red">Unfortunately, you got the question wrong.</font>**'))
          else:
            display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_substitution(input_string='', input_formula = '', input_var ='x', input_term='a'):
  layout = widgets.Layout(width='90%')
  run = widgets.Button(description="Check")
  input = widgets.Text(
      value=input_string,
      placeholder='Enter your formula:',
      description='',
      layout=layout
      )
  cParentheses = widgets.Checkbox(value=False, description='Display Formula with Parentheses')
  cLatex = widgets.Checkbox(value=False, description='Display Formula in Latex')
  output = widgets.Output()
  wButtons = widgets.HBox([run, cParentheses, cLatex])
  
  display(Markdown(rf'**Enter the formula that results from substitution the variable {input_var} with the term {input_term} in the formula {input_formula}:**'))
  display(input, wButtons, output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      try:
          f = ParserFormula.getFormula(input_formula)
          result = ParserFormula.getFormula(input.value)
          if(result!=None):
            if result==f.substitution(input_var,input_term):
              display(Markdown(r'**<font color="blue">Congratulations this is the correct substitution:</font>**'))              
              if(cLatex.value):
                s = result.toLatex(parentheses=cParentheses.value)
                display(Markdown(rf'${s}$'))
              else:
                display(Markdown(rf'{result.toString(parentheses=cParentheses.value)}'))
            else:
              display(Markdown(rf'**<font color="red">The formula {result.toString()} is not the result of substitution {input_var} with {input_term} in the formula {input_formula}.</font>**'))
          else:
            display(Markdown(r'**<font color="red">Formula definition is not correct, check if all rules are applied correctly. Remember that a formula is defined by the following BNF: F :== P | ~ P | Q & Q | P | Q | P -> Q | P <-> Q | (P), where P,Q (in capital letters) are atoms.</font>**'))
      except ValueError:
          s = traceback.format_exc()
          result = (s.split("@@"))[-1]
          print (f'{result}')
      else:
          pass
  run.on_click(on_button_run_clicked)

def verify_valid_conclusion(input_assumptions, input_conclusion, result_value=False):
  layout = widgets.Layout(width='40%')
  run = widgets.Button(description="Check")
  output = widgets.Output()
  wButtons = widgets.HBox([run])
  cResult = widgets.RadioButtons(
    options=['Yes', 'No'],
    value=None, 
    description='Answer:',
    disabled=False
)
  questao = '**Consider the following statements:**'
  i = 1
  for assumption in input_assumptions:
    questao += f'\n1. {assumption}'
    i+=1
  questao+='\n**Can we conclude that the statement below follows logically from the statements above?**'
  questao+=f'\n{i}. {input_conclusion}'
  display(Markdown(questao))
  display(widgets.HBox([cResult,wButtons]), output)

  def on_button_run_clicked(_):
    output.clear_output()
    with output:
      if (cResult.value==None):
        display(Markdown('<font color="red">**Choose one of the alternatives! Try again!**</font>'))
      elif(result_value==(cResult.value=='Yes')):
        display(Markdown('<font color="blue">**Congratulations, you got the question right.**</font>'))
      else:
        display(Markdown('<font color="red">**Unfortunately, you got the question wrong. Try again!**</font>'))
  run.on_click(on_button_run_clicked)
