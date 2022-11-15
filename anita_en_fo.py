import traceback
from rply import LexerGenerator

## File formula.py
class BinaryFormula():
    def __init__(self, key = '', left = None, right = None):
        self.key = key
        self.left = left
        self.right = right

    def __eq__(self, other): 
        if not isinstance(other, BinaryFormula):
            return NotImplemented

        return self.key == other.key and self.left == other.left and self.right == other.right

    def __ne__(self, other): 
        if not isinstance(other, BinaryFormula):
            return NotImplemented

        return self.key != other.key or self.left != other.left or self.right != other.right

    def create_string_representation(self, formula, parentheses= False):
        if(parentheses):
          return formula.toString(parentheses=parentheses)
        elif isinstance(formula, BinaryFormula):
            return'({})'.format(formula.toString())
        else:
            return formula.toString()

    def create_latex_representation(self, formula, parentheses= False):
        if(parentheses):
          return formula.toLatex(parentheses=parentheses)
        elif isinstance(formula, BinaryFormula):
            return'({})'.format(formula.toLatex())
        else:
            return formula.toLatex()

    def is_implication(self):
      return self.key=='->'
    def is_conjunction(self):
      return self.key=='&'
    def is_disjunction(self):
      return self.key=='|'

    def toLatex(self, parentheses= False):
        operators = {
            '->': '\\rightarrow ',
            '&': '\\land ',
            '|': '\\lor ',
            '<->': '\\leftrightarrow ',
        }
        string = self.create_latex_representation(self.left, parentheses=parentheses)
        string += operators[self.key]
        string += self.create_latex_representation(self.right, parentheses=parentheses)
        if parentheses:
          return '('+string+')'
        return string

    def toString(self, parentheses= False):
        string = self.create_string_representation(self.left, parentheses=parentheses)
        string += self.key
        string += self.create_string_representation(self.right, parentheses=parentheses)
        if parentheses:
          return '('+string+')'
        return string

    def all_variables(self):
      return self.left.all_variables().union(self.right.all_variables())

    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      return self.left.free_variables().union(self.right.free_variables())

    def is_substitutable(self, x, y):
      return self.left.substitutable(x,y) and self.right.substitutable(x,y) 

    def substitution(self, var_x, a):
      return BinaryFormula(self.key, self.left.substitution(var_x, a), self.right.substitution(var_x, a))

    def get_values_x_substitution(self, var_x, formula):
      if not (isinstance(formula,BinaryFormula) and self.key==formula.key):
        return set()
      else:
        return self.left.get_values_x_substitution(var_x, formula.left).union(self.right.get_values_x_substitution(var_x, formula.right))

    def is_first_order_formula(self):
      return self.left.is_first_order_formula() or self.right.is_first_order_formula()

class AndFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '&', left=left, right = right)

class OrFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '|', left=left, right = right)

class ImplicationFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '->', left=left, right = right)

class BiImplicationFormula(BinaryFormula):
    def __init__(self, left = None, right = None):
        super().__init__(key = '<->', left=left, right = right)

class NegationFormula():
    def __init__(self, formula = None):
        self.formula = formula

    def __eq__(self, other): 
        if not isinstance(other, NegationFormula):
            return NotImplemented

        return self.formula == other.formula

    def __ne__(self, other): 
        if not isinstance(other, NegationFormula):
            return NotImplemented

        return self.formula != other.formula

    def toLatex(self, parentheses= False):
        if(parentheses):
          return '('+'\\lnot ' + self.formula.toLatex(parentheses=parentheses)+')'
        if not isinstance(self.formula, BinaryFormula):
            string = '\\lnot ' + self.formula.toLatex()
        else:
            string = '\\lnot({})'.format(self.formula.toLatex())
        return string   

    def toString(self, parentheses= False):
        if parentheses:
            string = '(~' + self.formula.toString()+')'
        elif not isinstance(self.formula, BinaryFormula):
            string = '~' + self.formula.toString()
        else:
            string = '~({})'.format(self.formula.toString())
        return string 

    def all_variables(self):
      return self.formula.all_variables()

    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      return self.formula.free_variables()

    def is_substitutable(self, x, y):
      return self.formula.substitutable(x,y)

    def substitution(self, var_x, a):
      return NegationFormula(self.formula.substitution(var_x, a))

    def get_values_x_substitution(self, var_x, formula):
      values = set()
      if not isinstance(formula,NegationFormula):
        return values
      else:
        return self.formula.get_values_x_substitution(var_x, formula.formula)

    def is_first_order_formula(self):
      return self.formula.is_first_order_formula()


class AtomFormula():
    def __init__(self, key = None):
        self.key = key

    def __eq__(self, other): 
        if not isinstance(other, AtomFormula):
            return NotImplemented

        return self.key == other.key
    
    def __ne__(self, other): 
        if not isinstance(other, AtomFormula):
            return NotImplemented

        return self.key != other.key

    def toLatex(self, parentheses= False):
        if(self.key != '@'):
            return self.key  
        else:
            return '\\bot' 

    def toString(self, parentheses= False):
        return self.key  

    def all_variables(self):
      return set()

    def bound_variables(self):
      return set()

    def free_variables(self):
      return set()

    def is_substitutable(self, x, y):
      return True 

    def substitution(self, var_x, a):
      return AtomFormula(self.key)

    def get_values_x_substitution(self, var_x, formula):
      return set()
    def is_first_order_formula(self):
      return False

class BottonFormula(AtomFormula):
    def __init__(self):
      super().__init__(key='@')


class PredicateFormula():
    def __init__(self, name = '', variables = []):
        self.variables = variables
        self.name = name

    def __eq__(self, other): 
        if not isinstance(other, PredicateFormula):
            return NotImplemented
        return self.variables == other.variables and self.name == other.name
    
    def __ne__(self, other): 
        if not isinstance(other, PredicateFormula):
            return NotImplemented

        return self.variables != other.variables or self.name != other.name

    def toLatex(self, parentheses= False):
        if self.variables: 
            return self.name+'('+','.join(self.variables)+')'
        else:
            return self.name

    def toString(self, parentheses= False):
        if self.variables: 
            return self.name+'('+','.join(self.variables)+')'
        else:
            return self.name

    def get_values_x_substitution(self, var_x, formula):
      values = set()
      if isinstance(formula, PredicateFormula) and formula.name==self.name and len(formula.variables)==len(self.variables):
        for i in range(len(self.variables)):
          if self.variables[i]==var_x:
            values.add(formula.variables[i])
      return values

    def all_variables(self):
      return set(self.variables)

    def bound_variables(self):
      return set()

    def free_variables(self):
      return set(self.variables)

    def is_substitutable(self, x, y):
      return True

    def substitution(self, var_x, a):
      aux_variables = []
      for v in self.variables:
        if(v==var_x): aux_variables.append(a)
        else: aux_variables.append(v)
      return PredicateFormula(self.name, aux_variables)

    def is_first_order_formula(self):
      return True

class QuantifierFormula():
    def __init__(self, forAll = True, variable=None, formula=None):
        self.forAll = forAll
        self.variable = variable
        self.formula = formula

    def __eq__(self, other): 
        if not isinstance(other, QuantifierFormula):
            return NotImplemented

        return self.forAll == other.forAll and self.variable == other.variable and self.formula == other.formula
    
    def __ne__(self, other): 
        if not isinstance(other, QuantifierFormula):
            return NotImplemented

        return self.forAll != other.forAll and self.variable != other.variable and self.formula != other.formula

    def is_universal(self):
      return self.forAll

    def is_existential(self):
      return not self.forAll

    def toLatex(self, parentheses= False):
        if parentheses:
          if self.forAll:        
              return '(\\forall {} {})'.format(self.variable, self.formula.toLatex(parentheses=parentheses))
          else:
              return '(\\exists {} {})'.format(self.variable, self.formula.toLatex(parentheses=parentheses))
        elif not isinstance(self.formula, BinaryFormula):
          if self.forAll:        
              return '\\forall {} {}'.format(self.variable, self.formula.toLatex())
          else:
              return '\\exists {} {}'.format(self.variable, self.formula.toLatex())
        else:
          if self.forAll:        
              return '\\forall {} ({})'.format(self.variable, self.formula.toLatex())
          else:
              return '\\exists {} ({})'.format(self.variable, self.formula.toLatex())

    def toString(self, parentheses= False):
        if parentheses:
          if self.forAll:        
              return '(A{} {})'.format(self.variable, self.formula.toString(parentheses=parentheses))
          else:
              return '(E{} {})'.format(self.variable, self.formula.toString(parentheses=parentheses))
        if not isinstance(self.formula, BinaryFormula):
          if self.forAll:        
              return 'A{} {}'.format(self.variable, self.formula.toString())
          else:
              return 'E{} {}'.format(self.variable, self.formula.toString())
        else:
          if self.forAll:        
              return 'A{} ({})'.format(self.variable, self.formula.toString())
          else:
              return 'E{} ({})'.format(self.variable, self.formula.toString())

    def all_variables(self):
      result = self.formula.all_variables()
      result.add(self.variable)
      return result
      
    def bound_variables(self):
      return self.all_variables().difference(self.free_variables())

    def free_variables(self):
      result = self.formula.free_variables()
      result.discard(self.variable)
      return result 

    def is_substitutable(self, x, y):
      if (self.variable == y and x in self.formula.free_variables()):
        return False
      return self.formula.is_substitutable(x,y)# and (self.variable == y or x in self.formula.free_variables())

    def valid_substitution(self, formula):
      free_vars = formula.free_variables()
      for v in free_vars:
        fAux = self.formula.substitution(self.variable, v)
        if (fAux==formula):
          return True
      return False

    def substitution(self, var_x, a):
      if self.variable == var_x:
        return self#.formula#.clone()
      else:
        return QuantifierFormula(self.forAll,self.variable, self.formula.substitution(var_x, a))

    def get_values_x_substitution(self, var_x, formula):
      if not (isinstance(formula,QuantifierFormula) and self.forAll==formula.forAll):
        return set()
      #elif self.variable != var_x:
      #  return set()
      else:
        return self.formula.get_values_x_substitution(var_x, formula.formula)
    def is_first_order_formula(self):
      return True

class UniversalFormula(QuantifierFormula):
    def __init__(self, variable=None, formula=None):
      super().__init__( forAll = True, variable=variable, formula=formula)

class ExistentialFormula(QuantifierFormula):
    def __init__(self, variable=None, formula=None):
      super().__init__( forAll = False, variable=variable, formula=formula)


## File lexer.py
class Lexer():
    def __init__(self):
        self.lexer = LexerGenerator()

    def _add_tokens(self):
        #Comma
        self.lexer.add('COMMA', r'\,')

        # Dot
        self.lexer.add('DOT', r'\.')

        # Vdash
        self.lexer.add('V_DASH', r'\|-|\|=')

        # Parentheses
        self.lexer.add('OPEN_PAREN', r'\(')
        self.lexer.add('CLOSE_PAREN', r'\)')

        #Brackets
        self.lexer.add('OPEN_BRACKET', r'\{')
        self.lexer.add('CLOSE_BRACKET', r'\}')

        #rules
        self.lexer.add('IMP_FALSE', r'->F')
        self.lexer.add('IMP_TRUE', r'->T')
        self.lexer.add('OR_FALSE', r'\|F')
        self.lexer.add('OR_TRUE', r'\|T')
        self.lexer.add('AND_TRUE', r'&T')
        self.lexer.add('AND_FALSE', r'&F')
        self.lexer.add('NEG_TRUE', r'~T')
        self.lexer.add('NEG_FALSE', r'~F')

        # Connectives
        self.lexer.add('BOTTOM', r'@')
        self.lexer.add('NOT', r'~')
        self.lexer.add('AND', r'&')
        self.lexer.add('OR', r'\|')
        self.lexer.add('IMPLIE', r'->')
        self.lexer.add('IFF', r'<->')

        #First order rules
        self.lexer.add('EXT_FALSE', r'EF')
        self.lexer.add('EXT_TRUE', r'ET')
        self.lexer.add('ALL_FALSE', r'AF')
        self.lexer.add('ALL_TRUE', r'AT')

        #First order connectives
        self.lexer.add('EXT', r'E[a-z][a-z0-9]*')
        self.lexer.add('ALL', r'A[a-z][a-z0-9]*')

        # definitions
        self.lexer.add('TRUE', r'T')
        self.lexer.add('FALSE', r'F')

        # Number
        self.lexer.add('NUM', r'\d+')

        #justification
        self.lexer.add('PREMISSE', r'pre')
        self.lexer.add('CONCLUSION', r'conclusion')
        self.lexer.add('CLOSED', r'closed')

        #Variable
        self.lexer.add('VAR', r'(?!pre)[a-z][a-z0-9]*')

        # Atom
        self.lexer.add('ATOM', r'[A-Z][A-Z0-9]*' )

        # Ignore spaces and comments
        self.lexer.ignore('##[^##]*##')
        self.lexer.ignore('#[^\n]*\n?')
        self.lexer.ignore('\s+')  

        # Detect symbols out of grammar
        self.lexer.add('OUT', r'.*' )      

    def get_lexer(self):
        self._add_tokens()
        return self.lexer.build()


## File symbol_table.py

class SymbolTable:
    def __init__(self):
        self.symbol_table = {
            'branch_0': {
                'name': 'branch_0',
                'parent': None,
                'children': [],
                'rules': [],
                'variable': None,
                'start_line': '1',
                'end_line': None
            }
        }
        self.current_branch = 'branch_0'

    def insert(self, rule):
        self.symbol_table[self.current_branch]['rules'].append(rule)

    def start_branch(self, branch):
        self.current_branch = branch

    def end_branch(self, end_line):
        self.symbol_table[self.current_branch]['end_line'] = end_line
        if(self.symbol_table[self.current_branch]['parent'] is not None):
            self.current_branch = self.symbol_table[self.current_branch]['parent']

    def add_branch(self, start_line, variable=None):
        branch = 'branch_{}'.format(len(self.symbol_table))
        self.symbol_table[branch] = {
            'name': branch,
            'parent': self.current_branch,
            'children': [],
            'rules': [],
            'variable': variable,
            'start_line': start_line,
            'end_line': None 
            }
        self.symbol_table[self.current_branch]['children'].append(self.symbol_table[branch])
        self.start_branch(branch)

    def branch_to_latex(self, branch, rules=[], color='red'):
      i = 0
      l = []
      initial_tableau = '[.{'
      n_rules = len(branch['rules']) 
      while i< n_rules:
        if isinstance(branch['rules'][i],PremisseRule):
          if (branch['rules'][i] in rules):
            initial_tableau += '\color{'+color+'}{$'+branch['rules'][i].toLatex(self)+'$} \\\\ '
          else:
            initial_tableau += '$'+branch['rules'][i].toLatex(self)+'$ \\\\ '
        elif isinstance(branch['rules'][i],ConclusionRule):
          if (branch['rules'][i] in rules):
            initial_tableau += '\color{'+color+'}{$'+branch['rules'][i].toLatex(self)+'$}}'
          else:
            initial_tableau += '$'+branch['rules'][i].toLatex(self)+'$}'
          l.append(initial_tableau)
        elif isinstance(branch['rules'][i],AndTrueRule):
          if (branch['rules'][i] in rules):
            s = '[.{{\color{'+color+'}$'+branch['rules'][i].toLatex(self)+'$}'
          else:
            s = '[.{$'+branch['rules'][i].toLatex(self)+'$'
          if i+1< n_rules and isinstance(branch['rules'][i+1],AndTrueRule) and branch['rules'][i].reference1==branch['rules'][i+1].reference1:            
            if (branch['rules'][i+1] in rules):
              s+=' \\\\ {\color{'+color+'}$'+branch['rules'][i+1].toLatex(self)+'$}'
            else:  
              s+=' \\\\ '+'$'+branch['rules'][i+1].toLatex(self)+'$'
            i+=1
          l.append(s+'}')
        elif isinstance(branch['rules'][i],OrFalseRule):
          if (branch['rules'][i] in rules):
            s = '[.{{\color{'+color+'}$'+branch['rules'][i].toLatex(self)+'$}'
          else:
            s = '[.{$'+branch['rules'][i].toLatex(self)+'$'
          if i+1< n_rules and isinstance(branch['rules'][i+1],OrFalseRule) and branch['rules'][i].reference1==branch['rules'][i+1].reference1:            
            if (branch['rules'][i+1] in rules):
              s+=' \\\\ {\color{'+color+'}$'+branch['rules'][i+1].toLatex(self)+'$}'
            else:  
              s+=' \\\\ '+'$'+branch['rules'][i+1].toLatex(self)+'$'
            i+=1
          l.append(s+'}')
        elif isinstance(branch['rules'][i],ImpFalseRule):
          if (branch['rules'][i] in rules):
            s = '[.{{\color{'+color+'}$'+branch['rules'][i].toLatex(self)+'$}'
          else:
            s = '[.{$'+branch['rules'][i].toLatex(self)+'$'
          if i+1< n_rules and isinstance(branch['rules'][i+1],ImpFalseRule) and branch['rules'][i].reference1==branch['rules'][i+1].reference1:            
            if (branch['rules'][i+1] in rules):
              s+=' \\\\ {\color{'+color+'}$'+branch['rules'][i+1].toLatex(self)+'$}'
            else:  
              s+=' \\\\ '+'$'+branch['rules'][i+1].toLatex(self)+'$'
            i+=1
          l.append(s+'}')
        else:
          if (branch['rules'][i] in rules):
            l.append('[.{\color{'+color+'}{$'+branch['rules'][i].toLatex(self)+'$}}') 

          else:
            l.append('[.{$'+branch['rules'][i].toLatex(self)+'$}') 
        i+=1
      s = ' '.join(l)
      for s_children in branch['children']:
        s+= ' '+self.branch_to_latex(s_children,rules=rules,color=color)
      s += ''.join([' ]' for r in range(len(l))])
      return s
    
    def toLatex(self, rules=[], color='red'):
      return '\Tree '+self.branch_to_latex(self.symbol_table['branch_0'],rules,color)

    def toString(self):
      for i in range(len(self.symbol_table)):
        print(self.symbol_table['branch_{}'.format(i)])

    def len_symbol_table(self):
      r = 0
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['branch_{}'.format(i)]['rules']:
          r+=1
      return r

    def find_token(self, line):
      for i in range(len(self.symbol_table)):
        for j in range(len(self.symbol_table['branch_{}'.format(i)]['rules'])):
          if (self.symbol_table['branch_{}'.format(i)]['rules'][j].line==line):
            return self.symbol_table['branch_{}'.format(i)]['rules'][j].line
      return None

    def find_branch(self, line):
        for key, branch in self.symbol_table.items():
            for rule in branch['rules']:
                if rule and (rule.line == line):
                    return key 
        #Verifica se a linha não tem fórmula (introdução do universal)
        for key, branch in self.symbol_table.items():
          if(int(branch['start_line'])==int(line)):
            return key
        return None

    def lookup_formula_by_line(self, rule_line, line):
    # Returns only if the line is visible
        branch = self.find_branch(rule_line)
        while branch != None:
            for rule in self.symbol_table[branch]['rules']:
                if rule.line == line:
                    return rule.formula
            branch = self.symbol_table[branch]['parent']
        return None

    def lookup_true_value_by_line(self, rule_line, line):
    # Returns only if the line is visible
        branch = self.find_branch(rule_line)
        while branch != None:
            for rule in self.symbol_table[branch]['rules']:
                if rule.line == line:
                  if (isinstance(rule,ClosedRule)):
                    return None
                  else:
                    return rule.true_value
            branch = self.symbol_table[branch]['parent']
        return None        

    def check_branch_delimiter(self, line1, line2):
        for key, branch in self.symbol_table.items():
            if key != 'branch_0':
                if(branch['start_line'] == line1 and branch['end_line'] == line2):
                    start_rule = branch['rules'][0].formula if branch['rules'][0] is not None else None
                    end_rule = branch['rules'][-1].formula if branch['rules'][-1] is not None else None
                    return (start_rule, end_rule)
        return None, None

    def get_box_start(self):
        if self.current_branch != 'branch_0':
            return self.symbol_table[self.current_branch]['start_line']
        return None

    def get_box_end(self):
        if self.current_branch != 'branch_0':
            return self.symbol_table[self.current_branch]['end_line']
        return None        

    def get_box_end(self, line):
        branch = self.find_branch(line)
        if branch != 'branch_0':
            return self.symbol_table[branch]['end_line']
        return None        

    def get_last_rule_from_branch(self):
        if self.symbol_table[self.current_branch]['rules']==[]: return None
        return self.symbol_table[self.current_branch]['rules'][-1]

    def get_rule(self, rule_line):
      for i in range(len(self.symbol_table)):
        for j in range(len(self.symbol_table['branch_{}'.format(i)]['rules'])):
          if (self.symbol_table['branch_{}'.format(i)]['rules'][j].line==rule_line):
            return self.symbol_table['branch_{}'.format(i)]['rules'][j]
      return None

    def check_is_visible(self, formula1_line, formula2_line):
      #Find formula1_line branch.
      if (int(formula1_line) <= int(formula2_line)): return False
      current_branch = None
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['branch_{}'.format(i)]['rules']:
          if rule and (rule.line == formula1_line):
            current_branch = self.symbol_table['branch_{}'.format(i)]
            break
        if current_branch != None: break
      #Check if formula2_line in formula1_line branch 
      while current_branch != None:
        for rule in current_branch['rules']:
          if rule and (rule.line == formula2_line):
            return True
        current_branch = self.symbol_table[current_branch['parent']] if 'parent' in current_branch else None
      return False


    # Returns True if the variable of the line is a fresh variable, i.e., it did not occur before this branch. 
    def is_fresh_variable(self, line, variable):
      return not variable in self.get_free_variables_before_branch(line)

    def get_free_variables_before_branch(self, line):
      free_variables = set()
      #Find formula1_line branch.
      branch = self.find_branch(line)
      while branch != None:
          for rule in self.symbol_table[branch]['rules']:
            if (int(rule.line) < int(line)):
              free_variables = free_variables.union(rule.formula.free_variables())
            #Adds the variable for the universal introduction rule, i.e., if the line does not have a formula
            if (int(self.symbol_table[branch]['start_line'])<int(line) and self.symbol_table[branch]['variable']):
              free_variables = free_variables.union(set(self.symbol_table[branch]['variable']))
          branch = self.symbol_table[branch]['parent']
      return free_variables
      
    def get_branch_rules(self, line):
      rules = []
      current_branch = self.find_branch(line)
      while current_branch != None:
        aux_rules = []
        for rule in self.symbol_table[current_branch]['rules']:
          if rule and (int(rule.line) <= int(line)):
            aux_rules.append(rule)
        aux_rules.reverse()        
        rules =  rules + aux_rules
        current_branch = self.symbol_table[current_branch]['parent']# if self.symbol_table[current_branch] else None
      return rules

    def count_used_rule_in_the_branch(self, rule):
      rules = self.get_branch_rules(rule.line)
      i = 0
      for r in rules:
        if hasattr(rule, 'reference1') and hasattr(r, 'reference1'):
          if(rule.reference1==r.reference1):
            i+= 1
      return i

    def branch_not_used_rules(self, rules):
      not_used_rules = []
      for rule in rules:
        if(not (isinstance(rule, ClosedRule) or isinstance(rule.formula,AtomFormula) or isinstance(rule.formula,PredicateFormula))):
          rule_used = False
          for rule_reference in rules:
            # Se a regra não for uma premissa, conclusão ou um átomo
            if(not (isinstance(rule_reference, PremisseRule) or isinstance(rule_reference, ConclusionRule)) ):
              if(rule_reference.reference1== rule.line):
                rule_used = True
                break
              if(isinstance(rule_reference, ClosedRule)):
                if(rule_reference.reference2== rule.line):
                  rule_used = True
                  break
          if(not rule_used):
            not_used_rules.append(rule)
      return not_used_rules

    def branch_has_contradiction(self, rules):
      for rule in rules:
        for rule_aux in rules:
          if(rule.formula==rule_aux.formula and rule.true_value!=rule_aux.true_value):
            return True
      return False

    def branch_is_saturaded(self,rules):
      return self.branch_not_used_rules(rules)==[]

    def get_open_tableau_branches(self):
      open = []
      for branch in self.get_last_branch_branchs():
        if(not isinstance(branch['rules'][-1], ClosedRule)): 
          open.append(branch)
      return open

    def get_closed_rule_branches(self):
      closed = []
      for branch in self.get_last_branch_branchs():
        if(isinstance(branch['rules'][-1], ClosedRule)): 
          closed.append(branch['rules'][-1])
      return closed

    def get_reference_closed_rule(self):
      reference_rules = []
      closed_rules = self.get_closed_rule_branches()
      for c in closed_rules:
        r1 = self.get_rule(c.reference1)
        r2 = self.get_rule(c.reference2)
        if not r1 in reference_rules:
          reference_rules.append(r1)
        if not r2 in reference_rules:
          reference_rules.append(r2)
      return reference_rules


    def get_open_saturated_branches(self):
      saturated_branches = []
      nonsaturated_branches = []
      branchs = self.get_open_tableau_branches()
      for branch in branchs:
        rules = self.get_branch_rules(branch['rules'][-1].line)
        # Test if a first-order branch
        is_first_order = False
        for r in rules:
          if(r.formula.is_first_order_formula()):
            is_first_order = True
            break
        if is_first_order:
          nonsaturated_branches.append(rules)
        elif self.branch_is_saturaded(rules) and not self.branch_has_contradiction(rules):
          saturated_branches.append(rules)
        else:
          nonsaturated_branches.append(rules)
      return saturated_branches, nonsaturated_branches

    def truth_values_toString(self,v):
      v.keys()
      return ''.join(v)

    def get_truth_values(self, saturated_branch):
      v = {}
      for rule in saturated_branch:
        if(isinstance(rule.formula, AtomFormula)):
          v[rule.formula.toString()] = rule.true_value
      return v

    def get_counter_examples_toString(self):
      return [self.counter_example_toString(v) for v in self.get_counter_examples()]
    
    def counter_example_toString(self, v):
      return ', '.join(['v('+key+')='+v[key] for key in sorted(list(v.keys()))])

    def get_counter_examples(self):
      counter_examples = []
      saturated_branches, nonsaturated_branches = self.get_open_saturated_branches()
      for rules in saturated_branches:
        counter_examples.append(self.get_truth_values(rules))
      return counter_examples

    def is_closed_tableau(self):
      return self.get_open_tableau_branches()==[]

    def get_last_branch_branchs(self):
      result = []
      for key, branch in self.symbol_table.items():
        is_last = True
        for key_aux, branch_aux in self.symbol_table.items():
          if(branch_aux['parent']==key and branch_aux!=branch):
            is_last = False
            break
        if is_last :
          result.append(branch)
      return result

    def is_valid_initial_tableau(self):
      has_conclusion = False
      for key, branch in self.symbol_table.items():
        if (key=='branch_0'):# O Tableau inicial deve ter uma sequência de premissas seguida da conclusão.
          for rule in branch['rules']:
              if(isinstance(rule, PremisseRule)): 
                if(has_conclusion):
                  return False
              elif(isinstance(rule, ConclusionRule)):
                has_conclusion = True
        else: # Premissas ou conclusão só podem ocorrer no tableau inicial.
          for rule in branch['rules']:
              if(isinstance(rule, PremisseRule) or isinstance(rule, ConclusionRule)): 
                return False
      return has_conclusion
      
    def getPremisses(self):
      lines = []
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['branch_{}'.format(i)]['rules']:
          if(isinstance(rule, PremisseRule) ):
            lines.append(rule.line)
      return lines

    def getPremissesFormulas(self):
      formulas = []
      for i in range(len(self.symbol_table)):
        for rule in self.symbol_table['branch_{}'.format(i)]['rules']:
          if(isinstance(rule, PremisseRule) and rule.formula not in formulas):
            formulas.append(rule.formula)
      return formulas

    def getConclusionFormula(self):
      for rule in self.symbol_table['branch_0']['rules']:
          if(isinstance(rule, ConclusionRule)):
            return rule.formula
      return None
    
    def theoremToString(self,parentheses=False):
      premissas = sorted([p.toString(parentheses=parentheses) for p in self.getPremissesFormulas()])
      fConclusion = self.getConclusionFormula()
      if(fConclusion):
        return (', '.join(premissas)+' |- '+fConclusion.toString(parentheses=parentheses))

    def theoremToLatex(self,parentheses=False):
      premisses = ([p.toLatex(parentheses=parentheses) for p in self.getPremissesFormulas()])
      fConclusion = self.getConclusionFormula()
      if(fConclusion):
        return (', '.join(premisses)+' \\vdash '+fConclusion.toLatex(parentheses=parentheses))

    def is_closed_branchs(self):
      for key, branch in self.symbol_table.items():
        if (key=='branch_0'): continue
        if(branch['end_line']==None): return False
      return True

    def find_branch_variable(self, line):
        branch = self.find_branch(line)
        if branch != None:
          return self.symbol_table[branch]['variable']
        #Verifica se a linha não tem fórmula (introdução do universal)
        for key, branch in self.symbol_table.items():
          if(int(branch['start_line'])==int(line)):
            return branch['variable']          
        return None

    def check_branch_is_valid(self, branch):
        current_branch = self.current_branch
        while current_branch != None:
            if current_branch == branch:
                return True
            current_branch = self.symbol_table[current_branch]['parent']
        return False


## dados_json.py
import json

class tableau_deduction_return:
    def __init__(self):
        self.latex = ''
        self.is_closed = False,
        self.errors = []
        self.premisses = []
        self.conclusion = None
        self.latex_theorem = ''
        self.theorem = ''
        self.counter_examples = None
        self.colored_latex = ''
        self.saturared_branches = []
        self.open_branches = []

    def add_error(self, error):
        self.errors.append(error)

    def to_json(self):
        result = {
            'latex': self.latex,
            'errors': self.errors,
            'premisses': self.premisses,
            'conclusion': self.conclusion,
            'is_closed': self.is_closed,
            'theorem':self.theorem,
            'latex_theorem': self.latex_theorem,
            'colored_latex': self.colored_latex,
            'counter_examples': self.counter_examples,
        }
        # with open("result.json", "w", encoding='utf8') as f:
        #     f.write(json.dumps(result, sort_keys=True, indent=3, ensure_ascii=False))

## File constants.py
class constants:
  INVALID_RESULT = 1 # Conclusão inválida da regra
  UNEXPECT_RESULT = 2 # Escolha errada de regra
  USING_DESCARTED_RULE = 3
  REFERENCED_LINE_NOT_DEFINED = 4
  CLOSE_BRACKET_WITHOUT_BOX = 5
  BOX_MUST_BE_DISPOSED = 6
  INVALID_SUBSTITUTION_UNIVERSAL = 7
  INVALID_UNIVERSAL_FORMULA = 8
  INVALID_EXISTENCIAL_FORMULA = 9
  INVALID_SUBSTITUTION_EXISTENCIAL = 10
  VARIABLE_IS_NOT_FRESH_VARIABLE = 11
  BOX_MUST_BE_DISPOSED_BY_RULE = 12
  IS_NOT_DISJUNCTION_TRUE = 13
  IS_NOT_DISJUNCTION_FALSE = 14
  IS_NOT_NEGATION_TRUE = 15
  IS_NOT_NEGATION_FALSE = 16
  IS_NOT_CONJUNCTION_TRUE = 17
  IS_NOT_CONJUNCTION_FALSE = 18
  IS_NOT_IMPLICATION = 19
  INVALID_LEFT_CONJUNCTION = 20
  INVALID_RIGHT_CONJUNCTION = 21
  INVALID_NEGATION = 22
  INVALID_LEFT_OR_RIGHT_DISJUNCTION = 23
  INVALID_LEFT_OR_RIGHT_CONJUNCTION = 24
  INVALID_LEFT_IMPLICATION = 25
  INVALID_RIGHT_IMPLICATION = 26
  INVALID_LEFT_RIGHT_IMPLICATION = 27
  INVALID_INITIAL_TABLEAU = 28
  INVALID_TRUE_CONJUNCTION_NEXT = 29
  INVALID_TRUE_CONJUNCTION_PREVIOUS = 30
  INVALID_FALSE_DISJUNCTION_NEXT = 31
  INVALID_FALSE_DISJUNCTION_PREVIOUS = 32
  INVALID_FALSE_IMPLICATION_NEXT = 33
  INVALID_FALSE_IMPLICATION_PREVIOUS = 34
  INVALID_FALSE_CONJUNCTION_NEXT = 35
  INVALID_FALSE_CONJUNCTION_PREVIOUS = 36
  INVALID_TRUE_DISJUNCTION_NEXT = 37
  INVALID_TRUE_DISJUNCTION_PREVIOUS = 38
  INVALID_TRUE_IMPLICATION_NEXT = 39
  INVALID_TRUE_IMPLICATION_PREVIOUS = 40
  INVALID_BETA_RULE = 41
  ALREADY_USED_RULE_IN_BRANCH = 42
  PREMISSE_SHOULD_BE_TRUE = 43
  CONCLUSION_SHOULD_BE_FALSE = 44
  WRONG_TRUE_VALUE = 45
  RULE_MUST_BE_BETA = 46
  RULE_MUST_BE_ALPHA = 47
  RULE_CANNOT_BE_APPLIED = 48


## File ast.py
class PremisseRule():
    def __init__(self, token_line, token_true_value, token_formula):
        self.token_line = token_line
        self.token_formula = token_formula[0]
        self.token_true_value = token_true_value
        self.line = token_line.value
        self.formula = token_formula[1]
        self.true_value = token_true_value.value

    def evaluation(self,parser,deduction_result):
        return

    def toLatex(self, symbol_table):
      return '{}~{}'.format(self.true_value, self.formula.toLatex())

    def toString(self):
      return '{}. {} {} pre'.format(self.line, self.true_value, self.formula.toString())

class ConclusionRule():
    def __init__(self, token_line, token_true_value, token_formula):
      self.token_line = token_line
      self.token_formula = token_formula[0]
      self.token_true_value = token_true_value
      self.line = token_line.value
      self.formula = token_formula[1]
      self.true_value = token_true_value.value

    def evaluation(self,parser,deduction_result):
      return

    def toLatex(self, symbol_table):
      return '{}~{}'.format(self.true_value, self.formula.toLatex())

    def toString(self):
      return '{}. {} {} conclusion'.format(self.line, self.true_value, self.formula.toString())

class BasicRule():
    def __init__(self, token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=True):
      self.token_line = token_line
      self.token_formula = token_formula[0]
      self.token_true_value = token_true_value
      self.token_reference1 = token_reference1
      self.token_symbol_rule = token_symbol_rule
      self.line = token_line.value
      self.formula = token_formula[1]
      self.true_value = token_true_value.value
      self.reference1 = token_reference1.value
      self.show_token_symbol = show_token_symbol
      
    def toLatex(self, symbol_table):
      return '{}~{}'.format(self.true_value, self.formula.toLatex())
   
    def toString(self):
      if self.show_token_symbol:
        return '{}. {} {} {} {}'.format(self.line, self.true_value, self.formula.toString(), self.token_symbol_rule.value, self.reference1)
      else:
        return '{}. {} {} {}'.format(self.line, self.true_value, self.formula.toString(), self.reference1)

class AndTrueRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return
      # If the formula (reference 1) is not a conjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_conjunction()) 
              or true_value!='T'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_CONJUNCTION_TRUE, self.token_reference1, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(not (formula1.left == self.formula or formula1.right == self.formula)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_OR_RIGHT_CONJUNCTION, self.token_reference1, self))

class AndFalseRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return
      # If the formula (reference 1) is not a conjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_conjunction()) 
        or true_value!='F'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_CONJUNCTION_FALSE, self.token_reference1, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(not (formula1.left == self.formula or formula1.right == self.formula)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_OR_RIGHT_CONJUNCTION, self.token_formula, self))

class OrTrueRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return
      # If the formula (reference 1) is not a conjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_disjunction())
       or true_value!='T'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_DISJUNCTION_TRUE, self.token_reference1, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(not (formula1.left == self.formula or formula1.right == self.formula)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_OR_RIGHT_DISJUNCTION, self.token_formula, self))

class OrFalseRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return
      # If the formula (reference 1) is not a disjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_disjunction())
         or true_value!='F'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_DISJUNCTION_FALSE, self.token_reference1, self))
      else:
          # If the left formula of conclusion (the disjunction) is one of the references 
          if(not (formula1.left == self.formula or formula1.right == self.formula)):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_OR_RIGHT_DISJUNCTION, self.token_reference1, self))

class ImpTrueRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return
      # If the formula (reference 1) is not a conjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_implication())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_IMPLICATION, self.token_reference1, self))
      else:
          # If the left formula of conclusion (the conjunction) is one of the references 
          if(formula1.left == self.formula):
            if(true_value==self.true_value):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_IMPLICATION, self.token_line, self))
          elif(formula1.right == self.formula):
            if(true_value!=self.true_value):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_RIGHT_IMPLICATION, self.token_true_value, self))
          else:
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_RIGHT_IMPLICATION, self.token_true_value, self))

class ImpFalseRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return
      # If the formula (reference 1) is not a conjunction formula
      if(not isinstance(formula1, BinaryFormula) or (isinstance(formula1, BinaryFormula) and not formula1.is_implication())):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_IMPLICATION, self.token_reference1, self))
      else:
          # If the left formula of conclusion is one of the references 
          if(self.token_true_value.gettokentype()=='TRUE'):
            if(formula1.left != self.formula):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_LEFT_IMPLICATION, self.token_line, self))
          # If the right formula of conclusion (the conjunction) is one of the references 
          elif(self.token_true_value.gettokentype()=='FALSE'):
            if(formula1.right != self.formula):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_RIGHT_IMPLICATION, self.token_true_value, self))

class NegationRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula1= parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return

      # If the formula is not a negation formula or the true value is not different
      if(formula1 != NegationFormula(self.formula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_RESULT, self.token_reference1, self))
      elif (true_value=='F' and self.token_symbol_rule.gettokentype() == 'NEG_TRUE'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_NEGATION_TRUE, self.token_reference1, self))
      elif (true_value=='T' and self.token_symbol_rule.gettokentype() == 'NEG_FALSE'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.IS_NOT_NEGATION_FALSE, self.token_reference1, self))


class ClosedRule():
    def __init__(self, token_line, token_formula, token_reference1, token_reference2, show_token_symbol=True):
        self.token_line = token_line
        self.token_formula = token_formula
        self.token_reference1 = token_reference1
        self.token_reference2 = token_reference2
        self.line = token_line.value
        self.formula = token_formula[1]
        self.reference1 = token_reference1.value
        self.reference2 = token_reference2.value
        self.show_token_symbol = show_token_symbol

    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True, reference2=True)      

      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value1 = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      formula2 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference2)
      true_value2 = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference2)

      if(formula1==None or formula2==None or self.formula==None):
        return

      # If the formula (reference 1) is not a contradiction
      if(self.formula.toString()!='@'):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_RESULT, self.token_formula, self))
      else:
          # if both formulas are the same and one contradicts the other.
          if(formula2 != formula1 or true_value1==true_value2):
              parser.has_error = True
              deduction_result.add_error(parser.get_error(constants.INVALID_NEGATION, self.token_reference1, self))

    def toLatex(self, symbol_table):
      return '\\times'
    
    def toString(self):
      if self.show_token_symbol:
        return '{}. {} closed {},{}'.format(self.line, self.formula.toString(), self.reference1, self.reference2)
      else:
        return '{}. {} {},{}'.format(self.line, self.formula.toString(), self.reference1, self.reference2)
      


class ForAllTrueRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return

      # If the formula is not a existential formula
      if(not isinstance(formula1, QuantifierFormula) or (isinstance(formula1, QuantifierFormula) and not formula1.is_universal()) or (true_value!=self.true_value)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_UNIVERSAL_FORMULA, self.token_reference1, self))

      # If the conclusion is a valid substitution of the universal formula (referecence 1)
      if(isinstance(formula1, QuantifierFormula) and not formula1.valid_substitution(self.formula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_SUBSTITUTION_UNIVERSAL, self.token_formula, self))

class ExistsFalseRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)
      if(formula1==None):
        return

      # If the formula is not a existential formula
      if(not isinstance(formula1, QuantifierFormula) or (isinstance(formula1, QuantifierFormula) and not formula1.is_existential()) or (true_value!=self.true_value)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_EXISTENCIAL_FORMULA, self.token_formula, self))

      # If the conclusion is a valid substitution of the universal formula (referecence 1)
      if(isinstance(formula1, QuantifierFormula) and not formula1.valid_substitution(self.formula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_SUBSTITUTION_EXISTENCIAL, self.token_formula, self))

class ForAllFalseRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)

      if(formula1==None):
        return

      # If the formula is not an universal formula
      if(not isinstance(formula1, QuantifierFormula) or (isinstance(formula1, QuantifierFormula) and not formula1.is_universal()) or (true_value!=self.true_value)):
        parser.has_error = True
        deduction_result.add_error(parser.get_error(constants.INVALID_UNIVERSAL_FORMULA, self.token_reference1, self))

      # If the conclusion is a valid substitution of the universal formula (referecence 1)
      if(isinstance(formula1, QuantifierFormula) and not formula1.valid_substitution(self.formula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_SUBSTITUTION_UNIVERSAL, self.token_formula, self))
      # If the variable is not a fresh variable 
      elif(isinstance(formula1, QuantifierFormula)):
        variables = formula1.get_values_x_substitution(formula1.variable, UniversalFormula(formula1.variable, self.formula))
        if not parser.symbol_table.is_fresh_variable(self.line, list(variables)[0]):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.VARIABLE_IS_NOT_FRESH_VARIABLE, self.token_formula,self))


class ExistsTrueRule(BasicRule):
    def evaluation(self,parser,deduction_result):
      # If the references lines occur before the rule line 
      before = parser.check_line_reference_before_rule_error(deduction_result,self)
      # If the reference1 line occurs in the branch of the rule line 
      if before:
        parser.check_line_branch_reference_error(deduction_result,self, reference1=True)      

      formula_reference = parser.symbol_table.find_token(self.line)
      formula1 = parser.symbol_table.lookup_formula_by_line(self.line, self.reference1)
      true_value = parser.symbol_table.lookup_true_value_by_line(self.line, self.reference1)

      if(formula1==None):
        return

      # If the formula is not an universal formula
      if(not isinstance(formula1, QuantifierFormula) or (isinstance(formula1, QuantifierFormula) and not formula1.is_existential()) or (true_value!=self.true_value)):
        parser.has_error = True
        deduction_result.add_error(parser.get_error(constants.INVALID_EXISTENCIAL_FORMULA, self.token_reference1, self))

      # If the conclusion is a valid substitution of the existencial formula (referecence 1)
      if(isinstance(formula1, QuantifierFormula) and not formula1.valid_substitution(self.formula)):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.INVALID_SUBSTITUTION_UNIVERSAL, self.token_formula, self))
      # If the variable is not a fresh variable 
      elif(isinstance(formula1, QuantifierFormula)):
        variables = formula1.get_values_x_substitution(formula1.variable, ExistentialFormula(formula1.variable, self.formula))
        if not parser.symbol_table.is_fresh_variable(self.line, list(variables)[0]):
          parser.has_error = True
          deduction_result.add_error(parser.get_error(constants.VARIABLE_IS_NOT_FRESH_VARIABLE, self.token_formula,self))


## File analisys.py

from rply import ParserGenerator
from rply import Token
import sys

deduction_result = tableau_deduction_return()

def value_error_handle(exctype, value, tb):
    deduction_result.add_error(str(value))
    deduction_result.to_json()

sys.excepthook = value_error_handle

class ParserAnita():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['NUM', 'DOT', 'COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT', 'BOTTOM',
             'AND', 'OR', 'AND_TRUE', 'AND_FALSE', 'NEG_TRUE', 'NEG_FALSE','OR_FALSE', 'OR_TRUE', 'IMP_FALSE', 'IMP_TRUE', 
             'PREMISSE', 'ATOM', 'OPEN_BRACKET', 'CLOSE_BRACKET', 'IMPLIE', 'CONCLUSION', 'CLOSED',
             'VAR', 'EXT', 'ALL', 'ALL_TRUE', 'EXT_FALSE', 'EXT_TRUE', 'ALL_FALSE', 'TRUE', 'FALSE' ],
            #The precedence $\lnot,\forall,\exists,\land,\lor,\rightarrow,\leftrightarrow$
            precedence=[
                ('right', ['IMPLIE']),
                ('right', ['OR']),
                ('right', ['AND']),
                ('right', ['EXT']),
                ('right', ['ALL']),
                ('right', ['NOT']),
            ]
        )
        self.symbol_table = SymbolTable()
        self.has_error = False


    def verify_sequence_lines_error(self, deduction_result):
        productions = self.state.splitlines()
        i = 1
        for p in productions:
          x = p.split('.')[0]
          if x.isdigit():
            if int(x)!=i: 
              self.has_error = True
              if(i==1): deduction_result.add_error('{}\n^, The number of line {} should be {}, becacuse the numbering of the proof should be sequencial and start with 1.\n'.format(p,x,i))
              else: deduction_result.add_error('{}\n^, The number of line {} should be {}, becacuse the numbering of the proof should be sequencial.\n'.format(p,x,i))
              break
            i+=1

    def check_is_closed_branches_by_rule(self,deduction_result):
      if(not self.symbol_table.is_closed_branchs()):
        self.has_error = True
        for key, branch in self.symbol_table.symbol_table.items():
          if (key=='branch_0'): continue
          if(branch['end_line']==None): 
            begin_rule = branch["rules"][0]
            begin_token = branch["rules"][0].token_formula
            deduction_result.add_error(self.get_error(constants.BOX_MUST_BE_DISPOSED, begin_token, begin_rule))

    def check_is_valid_initial_tableau(self,deduction_result):
      if (not self.symbol_table.is_valid_initial_tableau()):
        self.has_error = True
        begin_rule = self.symbol_table.symbol_table['branch_0']["rules"][0]
        begin_token = self.symbol_table.symbol_table['branch_0']["rules"][0].token_formula
        deduction_result.add_error(self.get_error(constants.INVALID_INITIAL_TABLEAU, begin_token, begin_rule))

    def check_line_reference_before_rule_error(self, deduction_result, rule):
      result = True
      if hasattr(rule, 'reference1'):
        if(int(rule.reference1) >= int(rule.line)):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.REFERENCED_LINE_NOT_DEFINED, rule.token_reference1, rule))
            result = False
      if hasattr(rule, 'reference2'):
        if(int(rule.reference2) >= int(rule.line)):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.REFERENCED_LINE_NOT_DEFINED, rule.token_reference2, rule))
            result = False
      return result

    def check_line_branch_reference_error(self, deduction_result, rule, reference1=False, reference2=False):
      result = True
      if reference1:
        if (self.symbol_table.lookup_formula_by_line(rule.line, rule.reference1)==None):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, rule.token_reference1, rule))
            result = False
      if reference2:
        if (self.symbol_table.lookup_formula_by_line(rule.line, rule.reference2)==None):
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.USING_DESCARTED_RULE, rule.token_reference2, rule))
            result = False
      return result


    def parse(self):
        deduction_result = tableau_deduction_return()
        @self.pg.production('program : steps')
        def program(p):
            self.verify_sequence_lines_error(deduction_result)
            self.check_is_closed_branches_by_rule(deduction_result)
            self.check_is_valid_initial_tableau(deduction_result)

            rule_info = p[0]
            for i in rule_info:
                rule_line, formula_reference = rule_info[i]

                formula_reference = self.symbol_table.find_token(rule_line.value)

                rule = self.symbol_table.get_rule(rule_line.value)
                if(isinstance(rule, PremisseRule) ):
                    pass
                elif(isinstance(rule, ConclusionRule) ):
                    pass
                elif(isinstance(rule, NegationRule)):
                    rule.evaluation(self, deduction_result)
                    #Verifica se a regra já foi utilizada anteriormente
                    if self.symbol_table.count_used_rule_in_the_branch(rule)>1:
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.ALREADY_USED_RULE_IN_BRANCH, rule.token_reference1, rule))
                elif(isinstance(rule, ClosedRule)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, AndTrueRule)):
                    rule.evaluation(self, deduction_result)

                    #Verifica se ambas as fórmulas da conjunção estão definidas
                    formula1 = self.symbol_table.lookup_formula_by_line(rule.line,rule.reference1)
                    if formula1==None or not isinstance(formula1, BinaryFormula):
                      continue
                    rule_AndTrue = self.symbol_table.get_rule(rule.reference1)
                    rule_previous = self.symbol_table.get_rule(str(int(rule.line)-1))
                    rule_next = self.symbol_table.get_rule(str(int(rule.line)+1))
                    if(formula1.left==rule.formula):    
                      if not ( rule_previous!=None and isinstance(rule_previous, AndTrueRule) and formula1.left==rule_previous.formula):                  
                        if( rule_next==None or (not isinstance(rule_next, AndTrueRule)) or formula1.right!=rule_next.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_TRUE_CONJUNCTION_NEXT, rule.token_line, rule_AndTrue))
                    elif(formula1.right==rule.formula):                      
                      if( rule_previous==None or (not isinstance(rule_previous, AndTrueRule)) or formula1.left!=rule_previous.formula):
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.INVALID_TRUE_CONJUNCTION_PREVIOUS, rule.token_line, rule_AndTrue))

                    #Verifica se a regra já foi utilizada anteriormente
                    if self.symbol_table.count_used_rule_in_the_branch(rule)>2:
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.ALREADY_USED_RULE_IN_BRANCH, rule.token_reference1, rule))
                elif(isinstance(rule, AndFalseRule)):
                    rule.evaluation(self, deduction_result)
                    branch = self.symbol_table.find_branch(rule.line)
                    branch_parent = self.symbol_table.symbol_table[branch]['parent']
                    branchs = self.symbol_table.symbol_table[branch_parent]['children']
                    last_rule_parent =self.symbol_table.symbol_table[branch_parent]['rules'][-1]
                    first_branch_rule =branchs[0]['rules'][0]
                    if(last_rule_parent.line!=str(int(first_branch_rule.line)-1) or len(branchs)!=2):
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.INVALID_BETA_RULE, rule.token_line, rule))
                    else:
                      formula1 = self.symbol_table.lookup_formula_by_line(rule.line,rule.reference1)
                      if formula1==None or not isinstance(formula1, BinaryFormula):
                        continue
                      rule_AndFalse = self.symbol_table.get_rule(rule.reference1)
                      if(formula1.left==rule.formula):                      
                        rule_next = branchs[1]['rules'][0]
                        if( rule_next==None or (not isinstance(rule_next, AndFalseRule)) or formula1.right!=rule_next.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_FALSE_CONJUNCTION_NEXT, rule.token_line, rule_AndFalse))
                      elif(formula1.right==rule.formula):                      
                        rule_previous = branchs[0]['rules'][0]
                        if( rule_previous==None or (not isinstance(rule_previous, AndFalseRule)) or formula1.left!=rule_previous.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_FALSE_CONJUNCTION_PREVIOUS, rule.token_line, rule_AndFalse))
                    #Verifica se a regra já foi utilizada anteriormente
                    if self.symbol_table.count_used_rule_in_the_branch(rule)>1:
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.ALREADY_USED_RULE_IN_BRANCH, rule.token_reference1, rule))

                elif(isinstance(rule, OrFalseRule)):
                    rule.evaluation(self, deduction_result)
                    #Verifica se ambas as fórmulas da disjunção estão definidas
                    formula1 = self.symbol_table.lookup_formula_by_line(rule.line,rule.reference1)
                    if formula1==None or not isinstance(formula1, BinaryFormula):
                      continue
                    rule_OrFalse = self.symbol_table.get_rule(rule.reference1)
                    rule_previous = self.symbol_table.get_rule(str(int(rule.line)-1))
                    rule_next = self.symbol_table.get_rule(str(int(rule.line)+1))
                    if(formula1.left==rule.formula):    
                      if not (rule_previous!=None and isinstance(rule_previous, OrFalseRule) and formula1.left==rule_previous.formula):
                        if( rule_next==None or (not isinstance(rule_next, OrFalseRule)) or formula1.right!=rule_next.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_FALSE_DISJUNCTION_NEXT, rule.token_line, rule_OrFalse))
                    elif(formula1.right==rule.formula):                      
                      if( rule_previous==None or (not isinstance(rule_previous, OrFalseRule)) or formula1.left!=rule_previous.formula):
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.INVALID_FALSE_DISJUNCTION_PREVIOUS, rule.token_line, rule_OrFalse))
                    #Verifica se a regra já foi utilizada anteriormente
                    if self.symbol_table.count_used_rule_in_the_branch(rule)>2:
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.ALREADY_USED_RULE_IN_BRANCH, rule.token_reference1, rule))
                
                elif(isinstance(rule, OrTrueRule)):
                    rule.evaluation(self, deduction_result)
                    branch = self.symbol_table.find_branch(rule.line)
                    branch_parent = self.symbol_table.symbol_table[branch]['parent']
                    branchs = self.symbol_table.symbol_table[branch_parent]['children']
                    last_rule_parent =self.symbol_table.symbol_table[branch_parent]['rules'][-1]
                    first_branch_rule =branchs[0]['rules'][0]
                    if(last_rule_parent.line!=str(int(first_branch_rule.line)-1) or len(branchs)!=2):
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.INVALID_BETA_RULE, rule.token_line, rule))
                    else:
                      formula1 = self.symbol_table.lookup_formula_by_line(rule.line,rule.reference1)
                      if formula1==None or not isinstance(formula1, BinaryFormula):
                        continue
                      rule_OrTrue = self.symbol_table.get_rule(rule.reference1)
                      if(formula1.left==rule.formula):                      
                        rule_next = branchs[1]['rules'][0]
                        if( rule_next==None or (not isinstance(rule_next, OrTrueRule)) or formula1.right!=rule_next.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_TRUE_DISJUNCTION_NEXT, rule.token_line, rule_OrTrue))
                      elif(formula1.right==rule.formula):                      
                        rule_previous = branchs[0]['rules'][0]
                        if( rule_previous==None or (not isinstance(rule_previous, OrTrueRule)) or formula1.left!=rule_previous.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_TRUE_DISJUNCTION_PREVIOUS, rule.token_line, rule_OrTrue))
                    #Verifica se a regra já foi utilizada anteriormente
                    if self.symbol_table.count_used_rule_in_the_branch(rule)>1:
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.ALREADY_USED_RULE_IN_BRANCH, rule.token_reference1, rule))

                elif(isinstance(rule, ImpTrueRule)):
                    rule.evaluation(self, deduction_result)
                    branch = self.symbol_table.find_branch(rule.line)
                    branch_parent = self.symbol_table.symbol_table[branch]['parent']
                    branchs = self.symbol_table.symbol_table[branch_parent]['children']
                    last_rule_parent =self.symbol_table.symbol_table[branch_parent]['rules'][-1]
                    first_branch_rule =branchs[0]['rules'][0]
                    if(last_rule_parent.line!=str(int(first_branch_rule.line)-1) or len(branchs)!=2):
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.INVALID_BETA_RULE, rule.token_line, rule))
                    else:
                      formula1 = self.symbol_table.lookup_formula_by_line(rule.line,rule.reference1)
                      if formula1==None or not isinstance(formula1, BinaryFormula):
                        continue
                      rule_ImpTrue = self.symbol_table.get_rule(rule.reference1)
                      if(formula1.left==rule.formula):                      
                        rule_next = branchs[1]['rules'][0]
                        if( rule_next==None or (not isinstance(rule_next, ImpTrueRule)) or formula1.right!=rule_next.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_TRUE_IMPLICATION_NEXT, rule.token_line, rule_ImpTrue))
                      elif(formula1.right==rule.formula):                      
                        rule_previous = branchs[0]['rules'][0]
                        if( rule_previous==None or (not isinstance(rule_previous, ImpTrueRule)) or formula1.left!=rule_previous.formula):
                          self.has_error = True
                          deduction_result.add_error(self.get_error(constants.INVALID_TRUE_IMPLICATION_PREVIOUS, rule.token_line, rule_ImpTrue))
                     #Verifica se a regra já foi utilizada anteriormente
                    if self.symbol_table.count_used_rule_in_the_branch(rule)>1:
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.ALREADY_USED_RULE_IN_BRANCH, rule.token_reference1, rule))

                elif(isinstance(rule, ImpFalseRule)):
                    rule.evaluation(self, deduction_result)
                    #Verifica se ambas as fórmulas da implicação estão definidas
                    formula1 = self.symbol_table.lookup_formula_by_line(rule.line,rule.reference1)
                    if formula1==None or not isinstance(formula1, BinaryFormula):
                      continue
                    rule_ImpFalse = self.symbol_table.get_rule(rule.reference1)
                    if(formula1.left==rule.formula and rule.token_true_value.gettokentype()=='TRUE'):                      
                      rule_next = self.symbol_table.get_rule(str(int(rule.line)+1))
                      if( rule_next==None or (not isinstance(rule_next, ImpFalseRule)) or formula1.right!=rule_next.formula):
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.INVALID_FALSE_IMPLICATION_NEXT, rule.token_line, rule_ImpFalse))
                    elif(formula1.right==rule.formula and rule.token_true_value.gettokentype()=='FALSE'):                      
                      rule_previous = self.symbol_table.get_rule(str(int(rule.line)-1))
                      if( rule_previous==None or (not isinstance(rule_previous, ImpFalseRule)) or formula1.left!=rule_previous.formula):
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.INVALID_FALSE_IMPLICATION_PREVIOUS, rule.token_line, rule_ImpFalse))
                    #Verifica se a regra já foi utilizada anteriormente
                    if self.symbol_table.count_used_rule_in_the_branch(rule)>2:
                        self.has_error = True
                        deduction_result.add_error(self.get_error(constants.ALREADY_USED_RULE_IN_BRANCH, rule.token_reference1, rule))
                elif(isinstance(rule, ForAllTrueRule)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, ForAllFalseRule)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, ExistsTrueRule)):
                    rule.evaluation(self, deduction_result)
                elif(isinstance(rule, ExistsFalseRule)):
                    rule.evaluation(self, deduction_result)

            if(not self.has_error):
                deduction_result.latex = self.symbol_table.toLatex()
                deduction_result.premisses = self.symbol_table.getPremissesFormulas()
                deduction_result.conclusion = self.symbol_table.getConclusionFormula()
                deduction_result.theorem = ParserAnita.toString(deduction_result.premisses, deduction_result.conclusion)
                deduction_result.latex_theorem = ParserAnita.toLatex(deduction_result.premisses, deduction_result.conclusion)
                deduction_result.counter_examples = self.symbol_table.get_counter_examples_toString()
                deduction_result.is_closed = self.symbol_table.is_closed_tableau()
                deduction_result.saturared_branches, deduction_result.open_branches = self.symbol_table.get_open_saturated_branches()
                if(deduction_result.saturared_branches!=[]):
                  rules = []
                  for branch in deduction_result.saturared_branches:
                    rules = rules+ branch
                  deduction_result.colored_latex = self.symbol_table.toLatex(rules=rules,color="red")
                elif(deduction_result.open_branches!=[]):
                  rules = []
                  for branch in deduction_result.open_branches:
                    rules = rules+ branch
                  deduction_result.colored_latex = self.symbol_table.toLatex(rules=rules,color="red")
                else:
                  rules = self.symbol_table.get_reference_closed_rule()
                  deduction_result.colored_latex = self.symbol_table.toLatex(rules=rules,color="blue")
            return deduction_result

        @self.pg.production('steps : steps step')
        @self.pg.production('steps : step')
        def steps(p):
            if len(p) == 1:
                result = p[0]
                return {result[0].value: result}
            else:
                result = p[1]
                p[0][result[0].value] = result
                return p[0]

        # Premisse Rule without rule's name
        # @self.pg.production('step : NUM DOT TRUE formula')
        # def Premisse_rule(p):
        #   token_line = p[0]
        #   token_true_value = p[2]
        #   token_formula = p[3]
        #   premisse = PremisseRule(token_line, token_true_value, token_formula)
        #   self.symbol_table.insert(premisse)
        #   return token_line, formula

        # # Conclusion Rule without rule's name
        # @self.pg.production('step : NUM DOT FALSE formula')
        # def Conclusion_rule(p):
        #     token_line = p[0]
        #     token_true_value = p[2]
        #     token_formula = p[3]
        #     formula = token_formula[1]
        #     conclusion = ConclusionRule(token_line, token_true_value, token_formula)
        #     self.symbol_table.insert(conclusion)
        #     return token_line, formula

        # Alpha Rules without rule's name
        @self.pg.production('step : NUM DOT FALSE formula NUM')
        @self.pg.production('step : NUM DOT TRUE formula NUM')
        def Rule_alpha(p):
            token_line = p[0]
            token_true_value = p[2]
            token_formula = p[3]
            token_reference1 = p[4]
            formula = token_formula[1] 
            true_value = token_true_value.value
            formula1 = self.symbol_table.lookup_formula_by_line(token_reference1.value, token_reference1.value)
            true_value_formula1 = self.symbol_table.lookup_true_value_by_line(token_reference1.value, token_reference1.value)
            if(isinstance(formula1, BinaryFormula) and formula1.is_conjunction() and true_value_formula1=='T'):
              token_symbol_rule = Token('AND_TRUE', '&T')
              f = AndTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'FALSE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_conjunction() and true_value_formula1=='F'):
              token_symbol_rule = Token('AND_FALSE', '&F')
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_BETA, token_reference1, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_disjunction() and true_value_formula1=='F'):
              token_symbol_rule = Token('OR_FALSE', '|F')
              f = OrFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'TRUE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_disjunction() and true_value_formula1=='T'):
              token_symbol_rule = Token('OR_TRUE', '|T')
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_BETA, token_reference1, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_implication() and true_value_formula1=='F'):
              token_symbol_rule = Token('IMP_FALSE', '->F')
              f = ImpFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
            elif(isinstance(formula1, BinaryFormula) and formula1.is_implication() and true_value_formula1=='T'):
              token_symbol_rule = Token('IMP_TRUE', '->T')
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_BETA, token_reference1, f))              
            elif(isinstance(formula1, NegationFormula)):
              if true_value_formula1=='T':
                token_symbol_rule = Token('NEG_TRUE', '~T')
              elif true_value_formula1=='F':
                token_symbol_rule = Token('NEG_FALSE', '~F')
              negation = NegationRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(negation)
            elif(isinstance(formula1, UniversalFormula) and true_value_formula1=='T'):
              token_symbol_rule = Token('ALL_TRUE', 'AT')
              f = ForAllTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'FALSE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            elif(isinstance(formula1, UniversalFormula)  and true_value_formula1=='F'):
              token_symbol_rule = Token('ALL_FALSE', 'AF')
              f = ForAllFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'TRUE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            elif(isinstance(formula1, ExistentialFormula)  and true_value_formula1=='T'):
              token_symbol_rule = Token('EXT_TRUE', 'ET')
              f = ExistsTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'FALSE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            elif(isinstance(formula1, ExistentialFormula)  and true_value_formula1=='F'):
              token_symbol_rule = Token('EXT_FALSE', 'EF')
              f = ExistsFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'TRUE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            else:
              token_symbol_rule = None
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_CANNOT_BE_APPLIED, token_reference1, f))              

            return token_line, formula

        # Beta Rules without rule's name
        @self.pg.production('step : NUM DOT OPEN_BRACKET TRUE formula NUM')
        @self.pg.production('step : NUM DOT OPEN_BRACKET FALSE formula NUM')
        def Rule_beta(p):
            token_line = p[0]
            token_true_value = p[3]
            token_formula = p[4]
            token_reference1 = p[5]
            formula = token_formula[1] 
            true_value = token_true_value.value
            formula1 = self.symbol_table.lookup_formula_by_line(token_reference1.value, token_reference1.value)
            true_value_formula1 = self.symbol_table.lookup_true_value_by_line(token_reference1.value, token_reference1.value)
            if(isinstance(formula1, BinaryFormula) and formula1.is_conjunction() and true_value_formula1=='T'):
              token_symbol_rule = Token('AND_TRUE', '&T')
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_conjunction() and true_value_formula1=='F'):
              token_symbol_rule = Token('AND_FALSE', '&F')
              f = AndFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'TRUE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_disjunction() and true_value_formula1=='F'):
              token_symbol_rule = Token('OR_FALSE', '|F')
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_disjunction() and true_value_formula1=='T'):
              token_symbol_rule = Token('OR_TRUE', '|T')
              f = OrTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              if token_true_value.gettokentype() == 'FALSE':  
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_implication() and true_value_formula1=='F'):
              token_symbol_rule = Token('IMP_FALSE', '->F')
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            elif(isinstance(formula1, BinaryFormula) and formula1.is_implication() and true_value_formula1=='T'):
              token_symbol_rule = Token('IMP_TRUE', '->T')
              f = ImpTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
            elif(isinstance(formula1, NegationFormula)):
              if true_value_formula1=='T':
                token_symbol_rule = Token('NEG_TRUE', '~T')
              elif true_value_formula1=='F':
                token_symbol_rule = Token('NEG_FALSE', '~F')
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            elif(isinstance(formula1, UniversalFormula) and true_value_formula1=='T'):
              token_symbol_rule = Token('ALL_TRUE', 'AT')
              f = ForAllTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            elif(isinstance(formula1, UniversalFormula)  and true_value_formula1=='F'):
              token_symbol_rule = Token('ALL_FALSE', 'AF')
              f = ForAllFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            elif(isinstance(formula1, ExistentialFormula)  and true_value_formula1=='T'):
              token_symbol_rule = Token('EXT_TRUE', 'ET')
              f = ExistsTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            elif(isinstance(formula1, ExistentialFormula)  and true_value_formula1=='F'):
              token_symbol_rule = Token('EXT_FALSE', 'EF')
              f = ExistsFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.add_branch(token_line.value)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_ALPHA, token_reference1, f))              
            else:
              token_symbol_rule = None
              f = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1, show_token_symbol=False)
              self.symbol_table.insert(f)
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_CANNOT_BE_APPLIED, token_reference1, f))              
            return token_line, formula

        @self.pg.production('step : NUM DOT formula NUM COMMA NUM')
        def Rule_closed_rule(p):
            token_line = p[0]
            token_formula = p[2]
            token_reference1 = p[3]
            token_reference2 = p[5]
            formula = token_formula[1] 
            closed = ClosedRule(token_line, token_formula, token_reference1, token_reference2)
            self.symbol_table.insert(closed)
            return token_line, formula


### Rules with Rule's name
        @self.pg.production('step : NUM DOT FALSE formula PREMISSE')
        @self.pg.production('step : NUM DOT TRUE formula PREMISSE')
        def Premisse(p):
          token_line = p[0]
          token_true_value = p[2]
          token_formula = p[3]
          token_symbol_rule = p[4]
          premisse = PremisseRule(token_line, token_true_value, token_formula)
          self.symbol_table.insert(premisse)
          if token_true_value.gettokentype() == 'FALSE':  
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.PREMISSE_SHOULD_BE_TRUE, token_true_value, premisse))              
          return token_line, formula


        @self.pg.production('step : NUM DOT TRUE formula CONCLUSION')
        @self.pg.production('step : NUM DOT FALSE formula CONCLUSION')
        def Conclusion(p):
            token_line = p[0]
            token_true_value = p[2]
            token_formula = p[3]
            formula = token_formula[1]
            conclusion = ConclusionRule(token_line, token_true_value, token_formula)
            self.symbol_table.insert(conclusion)
            if token_true_value.gettokentype() == 'TRUE':  
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.CONCLUSION_SHOULD_BE_FALSE, token_true_value, conclusion))              
            return token_line, formula


        @self.pg.production('step : NUM DOT FALSE formula AND_TRUE NUM')
        @self.pg.production('step : NUM DOT TRUE formula AND_TRUE NUM')
        def And_true(p):
            token_line = p[0]
            token_true_value = p[2]
            token_formula = p[3]
            token_symbol_rule = p[4]
            token_reference1 = p[5]
            formula = token_formula[1] 
            true_value = token_true_value.value
            andTrue = AndTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.insert(andTrue)
            if token_true_value.gettokentype() == 'FALSE':  
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, andTrue))              

            return token_line, formula

        @self.pg.production('step : NUM DOT OPEN_BRACKET TRUE formula AND_FALSE NUM')
        @self.pg.production('step : NUM DOT OPEN_BRACKET FALSE formula AND_FALSE NUM')
        def And_false(p):
            token_line = p[0]
            token_true_value = p[3]
            token_formula = p[4]
            token_symbol_rule = p[5]
            token_reference1 = p[6]
            formula = token_formula[1] 
            true_value = token_true_value.value
            
            andFalse = AndFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.add_branch(token_line.value)
            self.symbol_table.insert(andFalse)
            if token_true_value.gettokentype() == 'TRUE':  
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, andFalse))              
            return token_line, formula

        @self.pg.production('step : NUM DOT OPEN_BRACKET FALSE formula OR_TRUE NUM')
        @self.pg.production('step : NUM DOT OPEN_BRACKET TRUE formula OR_TRUE NUM')
        def Or_true(p):
            token_line = p[0]
            token_true_value = p[3]
            token_formula = p[4]
            token_symbol_rule = p[5]
            token_reference1 = p[6]
            formula = token_formula[1] 
            true_value = token_true_value.value
            
            OrTrue = OrTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.add_branch(token_line.value)
            self.symbol_table.insert(OrTrue)
            if token_true_value.gettokentype() == 'FALSE':  
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, OrTrue))              
            return token_line, formula

        @self.pg.production('step : NUM DOT TRUE formula OR_FALSE NUM')
        def Or_false_wrong(p):
            token_line = p[0]
            token_true_value = p[2]
            token_formula = p[3]
            token_symbol_rule = p[4]
            token_reference1 = p[5]
            formula = token_formula[1] 
            true_value = token_true_value.value
            
            orFalse = BasicRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.insert(orFalse)
            if token_true_value.gettokentype() == 'TRUE':  
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.RULE_MUST_BE_BETA, token_reference1, orFalse))              
            return token_line, formula

        @self.pg.production('step : NUM DOT FALSE formula OR_FALSE NUM')
        def Or_false(p):
            token_line = p[0]
            token_true_value = p[2]
            token_formula = p[3]
            token_symbol_rule = p[4]
            token_reference1 = p[5]
            formula = token_formula[1] 
            true_value = token_true_value.value
            
            orFalse = OrFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.insert(orFalse)
            return token_line, formula

        @self.pg.production('step : NUM DOT OPEN_BRACKET TRUE formula IMP_TRUE NUM')
        @self.pg.production('step : NUM DOT OPEN_BRACKET FALSE formula IMP_TRUE NUM')
        def Imp_true(p):
            token_line = p[0]
            token_true_value = p[3]
            token_formula = p[4]
            token_symbol_rule = p[5]
            token_reference1 = p[6]
            formula = token_formula[1] 
            true_value = token_true_value.value
            
            ImpTrue = ImpTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.add_branch(token_line.value)
            self.symbol_table.insert(ImpTrue)
            return token_line, formula

        @self.pg.production('step : NUM DOT FALSE formula IMP_FALSE NUM')
        @self.pg.production('step : NUM DOT TRUE formula IMP_FALSE NUM')
        def Imp_false(p):
            token_line = p[0]
            token_true_value = p[2]
            token_formula = p[3]
            token_symbol_rule = p[4]
            token_reference1 = p[5]
            formula = token_formula[1] 
            true_value = token_true_value.value
            
            impFalse = ImpFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.insert(impFalse)
            return token_line, formula

        
        @self.pg.production('step : NUM DOT TRUE formula NEG_TRUE NUM')
        @self.pg.production('step : NUM DOT FALSE formula NEG_TRUE NUM')
        @self.pg.production('step : NUM DOT FALSE formula NEG_FALSE NUM')
        @self.pg.production('step : NUM DOT TRUE formula NEG_FALSE NUM')
        def Neg(p):
            token_line = p[0]
            token_true_value = p[2]
            token_formula = p[3]
            token_symbol_rule = p[4]
            token_reference1 = p[5]
            formula = token_formula[1] 
            true_value = token_true_value.value
            
            negation = NegationRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
            self.symbol_table.insert(negation)
            if (token_true_value.gettokentype() == 'TRUE' and token_symbol_rule.gettokentype() == 'NEG_TRUE') or (token_true_value.gettokentype() == 'FALSE' and token_symbol_rule.gettokentype() == 'NEG_FALSE') :  
              self.has_error = True
              deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, negation))              
            return token_line, formula

        @self.pg.production('step : NUM DOT formula CLOSED NUM COMMA NUM')
        def Rule_closed(p):
            token_line = p[0]
            token_formula = p[2]
            token_reference1 = p[4]
            token_reference2 = p[6]
            formula = token_formula[1] 
            closed = ClosedRule(token_line, token_formula, token_reference1, token_reference2)
            self.symbol_table.insert(closed)
            return token_line, formula


        @self.pg.production('step : CLOSE_BRACKET')
        def close_box(p):
            token = p[0]
            rule = self.symbol_table.get_last_rule_from_branch()
            if rule==None:
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.BOX_MUST_BE_DISPOSED_BY_RULE, token, rule))              
                return p[0], rule
            elif(self.symbol_table.get_box_start()):
                self.symbol_table.end_branch(rule.line)
            else:
                self.has_error = True
                deduction_result.add_error(self.get_error(constants.CLOSE_BRACKET_WITHOUT_BOX, token, rule))
            return token, None


        @self.pg.production('step : NUM DOT FALSE formula ALL_TRUE NUM')
        @self.pg.production('step : NUM DOT TRUE formula ALL_TRUE NUM')
        def For_ALL_TRUE(p):
          token_line = p[0]
          token_true_value = p[2]
          token_formula = p[3]
          token_symbol_rule = p[4]
          token_reference1 = p[5]
          formula = token_formula[1] 
          true_value = token_true_value.value
          
          forall = ForAllTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
          self.symbol_table.insert(forall)
          if token_true_value.gettokentype() == 'FALSE':  
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, forall))              
          return token_line, formula

        @self.pg.production('step : NUM DOT TRUE formula EXT_FALSE NUM')
        @self.pg.production('step : NUM DOT FALSE formula EXT_FALSE NUM')
        def Exists_FALSE(p):
          token_line = p[0]
          token_true_value = p[2]
          token_formula = p[3]
          token_symbol_rule = p[4]
          token_reference1 = p[5]
          formula = token_formula[1] 
          true_value = token_true_value.value
          
          exists = ExistsFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
          self.symbol_table.insert(exists)
          if token_true_value.gettokentype() == 'TRUE':  
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, exists))              
          return token_line, formula

        @self.pg.production('step : NUM DOT TRUE formula ALL_FALSE NUM')
        @self.pg.production('step : NUM DOT FALSE formula ALL_FALSE NUM')
        def For_ALL_FALSE(p):
          token_line = p[0]
          token_true_value = p[2]
          token_formula = p[3]
          token_symbol_rule = p[4]
          token_reference1 = p[5]
          formula = token_formula[1] 
          true_value = token_true_value.value
          
          forall = ForAllFalseRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
          self.symbol_table.insert(forall)
          if token_true_value.gettokentype() == 'TRUE':  
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, forall))              
          return token_line, formula

        @self.pg.production('step : NUM DOT FALSE formula EXT_TRUE NUM')
        @self.pg.production('step : NUM DOT TRUE formula EXT_TRUE NUM')
        def Exists_TRUE(p):
          token_line = p[0]
          token_true_value = p[2]
          token_formula = p[3]
          token_symbol_rule = p[4]
          token_reference1 = p[5]
          formula = token_formula[1] 
          true_value = token_true_value.value
          
          existsTrue = ExistsTrueRule(token_line, token_true_value, token_formula, token_symbol_rule, token_reference1)
          self.symbol_table.insert(existsTrue)
          if token_true_value.gettokentype() == 'FALSE':  
            self.has_error = True
            deduction_result.add_error(self.get_error(constants.WRONG_TRUE_VALUE, token_true_value, existsTrue))              
          return token_line, formula


        @self.pg.production('formula : EXT formula')
        @self.pg.production('formula : ALL formula')
        @self.pg.production('formula : formula OR formula')
        @self.pg.production('formula : formula AND formula')
        @self.pg.production('formula : formula IMPLIE formula')
        @self.pg.production('formula : NOT formula')
        @self.pg.production('formula : ATOM OPEN_PAREN variableslist CLOSE_PAREN')
        @self.pg.production('formula : ATOM')
        @self.pg.production('formula : BOTTOM')
        def formula(p):
            #print(p)
            if len(p) < 3:
                if p[0].gettokentype() == 'ATOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    result = p[1]
                    return p[0], NegationFormula(formula=result[1])  
                elif( not type(p[0]) is tuple):
                  result1 = p[0]
                  result2 = p[1]
                  # Universal Formula
                  if p[0].gettokentype() == 'EXT':  
                    var = p[0].value.split('E')[1]
                    return p[0], ExistentialFormula(variable=var, formula=p[1][1])
                  elif p[0].gettokentype() == 'ALL':  
                    var = p[0].value.split('A')[1]
                    return p[0], UniversalFormula(variable=var, formula=p[1][1])
            elif len(p)==4:
              # Predicate Formula
              name = p[0]
              varlist = p[2]
              return p[0], PredicateFormula(name=p[0].value,variables=varlist[1])            
            elif len(p) == 3:
              # Binary Formula
              result1 = p[0]
              result2 = p[2]
              if(p[1].value=='&'):
                return result1[0], AndFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='|'):
                return result1[0], OrFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='->'):
                return result1[0], ImplicationFormula(left=result1[1], right=result2[1])
              else:
                return result1[0], BinaryFormula(key=p[1].value, left=result1[1], right=result2[1])


        @self.pg.production('variableslist : VAR')
        @self.pg.production('variableslist : VAR COMMA variableslist')
        def variablesList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]



        @self.pg.production('formula : OPEN_PAREN formula CLOSE_PAREN')
        def paren_formula(p):
            result = p[1]
            return p[0], result[1]

        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'None proof was submitted.'
            if token.gettokentype() == '$end':
                error = 'One of definitions are not completed. Please, check whether all rules are correctly written.\nRecall that a rule of inference starts with a numeber, followed by . (reference line), the truth value of the formula (T or F), has a formula and the justification (premise, conclusion or one of the inference rules with its formula references).'
            else:
                source_position = token.getsourcepos()
                error = 'One of definitions are not completed. Please, check whether all rules are correctly written.\nRecall that a rule of inference starts with a numeber, followed by . (reference line), the truth value of the formula (T or F), has a formula and the justification (premise, conclusion or one of the inference rules with its formula references).'
                error += "Sintax error:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Symbol does not belongs to the language.'
                error += string
                
            raise ValueError("@@"+error)

    def get_error(self, type_error, token_error, rule):
        productions = self.state.splitlines()
        column_error = token_error.getsourcepos().colno
        erro = "Error in line {}:\n".format(token_error.getsourcepos().lineno)
        erro += productions[token_error.getsourcepos().lineno-1] + "\n"
        for i in range(column_error-1):
            erro += ' '
        if type_error == constants.INVALID_INITIAL_TABLEAU:
            erro += "^, The initial tableau should start with the premises followed by the conclusion. After the initial tableau, it is not allowed to add premises or conclusion."
        elif type_error == constants.INVALID_RESULT:
            erro += "^, Formula {} is not a valid result for this rule.".format(rule.formula.toString())
        elif type_error == constants.UNEXPECT_RESULT:
            erro += "^, Formula {} is not a valid result for this rule.".format(rule.formula.toString())
        elif type_error == constants.IS_NOT_DISJUNCTION_FALSE:
            erro += "^, The formula referenced in line {} is not a signed formula F with a disjunction.".format(token_error.value)
        elif type_error == constants.IS_NOT_DISJUNCTION_TRUE:
            erro += "^, The formula referenced in line {} is not a signed formula T with a disjunction.".format(token_error.value)
        elif type_error == constants.IS_NOT_CONJUNCTION_FALSE:
            erro += "^, The formula referenced in line {} is not a signed formula F with a conjunction.".format(token_error.value)
        elif type_error == constants.IS_NOT_CONJUNCTION_TRUE:
            erro += "^, The formula referenced in line {} is not a signed formula T with a conjunction.".format(token_error.value)
        elif type_error == constants.IS_NOT_NEGATION_FALSE:
            erro += "^, The formula referenced in line {} is not a signed formula F with a negation.".format(token_error.value)
        elif type_error == constants.IS_NOT_NEGATION_TRUE:
            erro += "^, The formula referenced in line {} is not a signed formula T with a negation.".format(token_error.value)
        elif type_error == constants.IS_NOT_IMPLICATION:
            erro += "^,  The formula referenced in line {} is not a implication.".format(token_error.value)
        elif type_error == constants.INVALID_NEGATION:
            erro += "^, None of the formulas referenced by the lines contradict the other formula."
        elif type_error == constants.INVALID_LEFT_IMPLICATION:
            erro += "^, Formula {} (conclusion of the rule) must be the antecedent of the implication of the referenced formula with truth-value T.".format(rule.formula.toString())
        elif type_error == constants.INVALID_RIGHT_IMPLICATION:
            erro += "^, Formula {} (conclusion of the rule) must be the consequent of the implication of the referenced formula with truth-value F.".format(rule.formula.toString())
        elif type_error == constants.INVALID_LEFT_RIGHT_IMPLICATION:
            erro += "^, Formula {} (conclusion of the rule) must be the antecedent or consequent of the implication of the referenced formula.".format(rule.formula.toString())
        elif type_error == constants.INVALID_LEFT_CONJUNCTION:
            erro += "^, Formula on the left formula of the conclusion is not proof by any of the lines referenced in this rule."
        elif type_error == constants.INVALID_RIGHT_CONJUNCTION:
            erro += "^, Formula on the right formula of the conclusion is not proof by any of the lines referenced in this rule."
        elif type_error == constants.INVALID_LEFT_OR_RIGHT_DISJUNCTION:
            erro += "^, Formula to the right or left of the conclusion formula must be the same as the formula reference in line {}.".format(token_error.value)
        elif type_error == constants.INVALID_LEFT_OR_RIGHT_CONJUNCTION:
            erro += "^, Formula {} (conclusion of rule) must be the same as the right or left formula of line {}.".format(rule.formula.toString(),token_error.value)
        elif type_error == constants.USING_DESCARTED_RULE:
            erro += "^, The reference to the line formula {} cannot be used, as this formula does not belong to this branch.".format(token_error.value)
        elif type_error == constants.REFERENCED_LINE_NOT_DEFINED:
            erro += "^, The reference to the line formula {} cannot be used, as all references must occur before this rule.".format(token_error.value)
        elif type_error == constants.CLOSE_BRACKET_WITHOUT_BOX:
            erro += "^, Closing branches without an open branch."
        elif type_error == constants.BOX_MUST_BE_DISPOSED:
            erro += "^,The open branch must be closed."
        elif type_error == constants.BOX_MUST_BE_DISPOSED_BY_RULE:
            erro += "^, This branch must be closed after applying at least one rule."
        elif type_error == constants.INVALID_SUBSTITUTION_UNIVERSAL:
            erro += "^, Formula {} is not a valid substitution for the universal formula referenced in line {}.".format(rule.formula.toString(), rule.reference1)
        elif type_error == constants.INVALID_UNIVERSAL_FORMULA:
            erro += "^, Formula referenced in line {} is not a universal formula with truth-value {}.".format(rule.reference1, rule.true_value)
        elif type_error == constants.INVALID_EXISTENCIAL_FORMULA:
            erro += "^, Formula referenced in line {} is not a existential formula with truth-value {}.".format(rule.reference1, rule.true_value)
        elif type_error == constants.INVALID_SUBSTITUTION_EXISTENCIAL:
            erro += "^, Formula {} is not a valid substitutuion for the existential formula referenced in the line {}.".format(rule.formula.toString(), rule.reference1)
        elif type_error == constants.VARIABLE_IS_NOT_FRESH_VARIABLE:
            erro += "^, The variable used in this formula {} is not a new variable and therefore cannot be used in this rule.".format(rule.formula.toString())
        elif type_error == constants.INVALID_TRUE_CONJUNCTION_NEXT:
            erro += "^, The next line should be the &T rule with the formula {}.".format(rule.formula.right.toString())
        elif type_error == constants.INVALID_TRUE_CONJUNCTION_PREVIOUS:
            erro += "^, The previous line should be the &T rule with the formula {}.".format(rule.formula.left.toString())
        elif type_error == constants.INVALID_FALSE_DISJUNCTION_NEXT:
            erro += "^, The next line should be the rule |F with the formula {}.".format(rule.formula.right.toString())
        elif type_error == constants.INVALID_FALSE_DISJUNCTION_PREVIOUS:
            erro += "^, The previous line should be the |F rule with the formula {}.".format(rule.formula.left.toString())
        elif type_error == constants.INVALID_FALSE_IMPLICATION_NEXT:
            erro += "^, The next line should be the rule ->F with the formula {}.".format(rule.formula.right.toString())
        elif type_error == constants.INVALID_FALSE_IMPLICATION_PREVIOUS:
            erro += "^, The previous line should be the rule ->F with the formula {}.".format(rule.formula.left.toString())
        elif type_error == constants.INVALID_TRUE_DISJUNCTION_NEXT:
            erro += "^, There should be a next branch, starting with rule |T with formula {}.".format(rule.formula.right.toString())
        elif type_error == constants.INVALID_TRUE_DISJUNCTION_PREVIOUS:
            erro += "^, There should be a previous branch, starting with the rule |T with the formula {}.".format(rule.formula.left.toString())
        elif type_error == constants.INVALID_TRUE_IMPLICATION_NEXT:
            erro += "^, There should be a next branch, starting with rule ->T with formula {}.".format(rule.formula.right.toString())
        elif type_error == constants.INVALID_TRUE_IMPLICATION_PREVIOUS:
            erro += "^, There should be a previous branch, starting with the rule ->T with the formula {}.".format(rule.formula.left.toString())
        elif type_error == constants.INVALID_FALSE_CONJUNCTION_NEXT:
            erro += "^, There should be a next branch, starting with the rule &F with the formula {}.".format(rule.formula.right.toString())
        elif type_error == constants.INVALID_FALSE_CONJUNCTION_PREVIOUS:
            erro += "^, There should be a previous branch, starting with the rule &F with the formula {}.".format(rule.formula.left.toString())
        elif type_error == constants.INVALID_BETA_RULE:
            erro += "^, A beta rule must have exactly two branches."
        elif type_error == constants.ALREADY_USED_RULE_IN_BRANCH:
            erro += "^, The reference rule on the {} line can only be used once in this branch.".format(rule.line)
        elif type_error == constants.PREMISSE_SHOULD_BE_TRUE:
            erro += "^, The premise must have a truth value T."
        elif type_error == constants.CONCLUSION_SHOULD_BE_FALSE:
            erro += "^, The conclusion must have a truth value F."
        elif type_error == constants.RULE_CANNOT_BE_APPLIED:
            erro += "^, Cannot apply rule to an atom or predicate."
        elif type_error == constants.RULE_MUST_BE_BETA:
            erro += "^, The rule must be a beta-rule."
        elif type_error == constants.RULE_MUST_BE_ALPHA:
            erro += "^, The rule must be a alpha-rule."
        elif type_error == constants.WRONG_TRUE_VALUE:
            if rule.token_true_value.gettokentype() == 'FALSE':  
              erro += "^, The truth value should be T for this rule."
            else:
              erro += "^, The truth value should be F for this rule."

        return erro
    
    def get_parser(self):
        return self.pg.build()

    @staticmethod
    def getProof(input_text=''):
      lexer = Lexer().get_lexer()
      tokens = lexer.lex(input_text)

      pg = ParserAnita(state=input_text)
      pg.parse()
      parser = pg.get_parser()
      result = parser.parse(tokens)
      return result


    @staticmethod
    def toString(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '|- '+conclusion.toString(parentheses=parentheses)
      else:
        return ", ".join(f.toString(parentheses=parentheses) for f in premisses)+' |- '+conclusion.toString(parentheses=parentheses)

    @staticmethod
    def toLatex(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '\\vdash '+conclusion.toLatex(parentheses=parentheses)
      else:
        return ", ".join(f.toLatex(parentheses=parentheses) for f in premisses) +' \\vdash '+conclusion.toLatex(parentheses=parentheses)

def check_proof(input_proof, latex=True):
  try:
      result = ParserAnita.getProof(input_proof)
      r = ''
      if(result.errors==[]):
        if(result.is_closed):
            r += "The proof below is valid.\n"
            r += result.theorem
            if latex: 
              r += "\nLatex:\n"+str(result.latex)
              r += "\nColored Latex:\n"+str(result.colored_latex)
        else:
            if result.saturared_branches != []:
              r += "The theorem is not valid.\n"
              r += result.theorem 
              r += "\nCountermodels:"
              for s_v in result.counter_examples:
                  r += '\n  '+s_v
              r += "\n"+str(result.latex)
              if latex: 
                r += "\nLatex:\nTheorem ${}$ is not valid.\n".format(result.latex_theorem)
                r += "\nCountermodels:"
                r += "\n\\begin{itemize}"
                for s_v in result.counter_examples:
                    r += '\n  \item $'+s_v+'$'
                r += "\n\end{itemize}"
                r += "\n"+str(result.colored_latex)
            else: 
                r += "\nThe proof below is not complete.\n"
                r += result.theorem
                r += "\nThe branches below are not saturated:"
                for rules in result.open_branches:
                  r += "\nBranch:\n  "
                  r += '\n  '.join([r.toString() for r in reversed(rules)])
                if latex: 
                  r += "\nLatex:\n"+str(result.latex)
                  r += "\nColored Latex:\n"+str(result.colored_latex)
      else:
        r += "The following errors were found:\n\n"
        for error in result.errors:
          r += str(error)
      return r
  except ValueError:
      s = traceback.format_exc()
      result = (s.split("@@"))[-1]
      r = "The following errors were found:\n\n"
      r += result
      return r
  else:
    pass


# Parser of Theorem
class ParserTheorem():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT',
             'AND', 'OR',  'BOTTOM','ATOM', 'IMPLIE', 'IFF',
             'VAR','EXT','ALL', 'V_DASH' ],
            #The precedence $\lnot,\forall,\exists,\land,\lor,\rightarrow,\leftrightarrow$
            precedence=[
                ('right', ['IFF']),
                ('right', ['IMPLIE']),
                ('right', ['OR']),
                ('right', ['AND']),
                ('right', ['EXT']),
                ('right', ['ALL']),
                ('right', ['NOT']),
            ]
        )

    def parse(self):
        @self.pg.production('program : formulaslist V_DASH formula')
        @self.pg.production('program : V_DASH formula')
        def program(p):
            if len(p) == 2:
              return [], p[1][1]
            else:
              return p[0][1], p[2][1]

        @self.pg.production('formula : EXT formula')
        @self.pg.production('formula : ALL formula')
        @self.pg.production('formula : formula OR formula')
        @self.pg.production('formula : formula AND formula')
        @self.pg.production('formula : formula IMPLIE formula')
        @self.pg.production('formula : formula IFF formula')
        @self.pg.production('formula : NOT formula')
        @self.pg.production('formula : ATOM OPEN_PAREN variableslist CLOSE_PAREN')
        @self.pg.production('formula : ATOM')
        @self.pg.production('formula : BOTTOM')
        def formula(p):
            if len(p) < 3:
                if p[0].gettokentype() == 'ATOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    result = p[1]
                    return p[0], NegationFormula(formula=result[1])  
                elif( not type(p[0]) is tuple):
                  result1 = p[0]
                  result2 = p[1]
                  # Universal Formula
                  if p[0].gettokentype() == 'EXT':  
                    var = p[0].value.split('E')[1]
                    return p[0], ExistentialFormula(variable=var, formula=p[1][1])
                  elif p[0].gettokentype() == 'ALL':  
                    var = p[0].value.split('A')[1]
                    return p[0], UniversalFormula(variable=var, formula=p[1][1])
            elif len(p)==4:
              # Predicate Formula
              name = p[0]
              varlist = p[2]
              return p[0], PredicateFormula(name=p[0].value,variables=varlist[1])            
            elif len(p) == 3:
              # Binary Formula
              result1 = p[0]
              result2 = p[2]
              if(p[1].value=='&'):
                return result1[0], AndFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='|'):
                return result1[0], OrFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='->'):
                return result1[0], ImplicationFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='<->'):
                return result1[0], BiImplicationFormula(left=result1[1], right=result2[1])
              else:
                return result1[0], BinaryFormula(key=p[1].value, left=result1[1], right=result2[1])

        @self.pg.production('formula : OPEN_PAREN formula CLOSE_PAREN')
        def paren_formula(p):
            result = p[1]
            return p[0], result[1]

        @self.pg.production('variableslist : VAR')
        @self.pg.production('variableslist : VAR COMMA variableslist')
        def variablesList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]

        @self.pg.production('formulaslist : formula')
        @self.pg.production('formulaslist : formula COMMA formulaslist')
        def formulasList(p):
             if len(p) == 1:
                 return p[0], [p[0][1]]
             else:
                result = p[2]
             return p[0], [p[0][1]] + result[1]


        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'None formula was submitted.'
            if token.gettokentype() == '$end':
                error = 'None formula was submitted.'
            else:
                source_position = token.getsourcepos()
                error = 'The formula definition is not correct, check that all rules were applied correctly.\n Remember that a formula is defined by the following BNF:\nF :== P | ~ P | Q&A | P | Q | P -> Q | P <-> Q | (P), where P,Q are atoms'
                error += "Sintax error:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Symbol does not belong to language.'
                error += string
                
            raise ValueError("@@"+error)

    def get_error(self, type_error, token_error, rule):
        productions = self.state.splitlines()
        column_error = token_error.getsourcepos().colno
        erro = "Syntax error in line {}:\n".format(token_error.getsourcepos().lineno)
        erro += productions[token_error.getsourcepos().lineno-1] + "\n"
        for i in range(column_error-1):
            erro += ' '
        
        return erro
    
    def get_parser(self):
        return self.pg.build()
    
    @staticmethod
    def getTheorem(input_text=''):
        try:
          lexer = Lexer().get_lexer()
          tokens = lexer.lex(input_text)
          pg = ParserTheorem(state=input_text)
          pg.parse()
          parser = pg.get_parser()
          premises, conclusion = parser.parse(tokens)
          return premises, conclusion
        except ValueError:
            s = traceback.format_exc()
            return [], None
        else:
            return [], None
            pass

    @staticmethod
    def toString(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '|- '+conclusion.toString(parentheses=parentheses)
      else:
        return ", ".join(f.toString(parentheses=parentheses) for f in premisses)+' |- '+conclusion.toString(parentheses=parentheses)

    @staticmethod
    def toLatex(premisses,conclusion,parentheses=False):
      if (premisses==[]):
        return '\\vdash '+conclusion.toLatex(parentheses=parentheses)
      else:
        return ", ".join(f.toLatex(parentheses=parentheses) for f in premisses) +' \\vdash '+conclusion.toLatex(parentheses=parentheses)



# PARSER of a Formula
class ParserFormula():
    def __init__(self, state):
        self.state = state
        self.pg = ParserGenerator(
            # A list of all token names accepted by the parser.
            ['COMMA', 'OPEN_PAREN', 'CLOSE_PAREN', 'NOT',
             'AND', 'OR',  'BOTTOM','ATOM', 'IMPLIE', 'IFF',
             'VAR','EXT','ALL' ],
            #The precedence $\lnot,\forall,\exists,\land,\lor,\rightarrow,\leftrightarrow$
            precedence=[
                ('right', ['IFF']),
                ('right', ['IMPLIE']),
                ('right', ['OR']),
                ('right', ['AND']),
                ('right', ['EXT']),
                ('right', ['ALL']),
                ('right', ['NOT']),
            ]
        )

    def parse(self):
        @self.pg.production('program : formula')
        def program(p):
            rule_info = p[0]
            return p[0][1]

        @self.pg.production('formula : EXT formula')
        @self.pg.production('formula : ALL formula')
        @self.pg.production('formula : formula OR formula')
        @self.pg.production('formula : formula AND formula')
        @self.pg.production('formula : formula IMPLIE formula')
        @self.pg.production('formula : formula IFF formula')
        @self.pg.production('formula : NOT formula')
        @self.pg.production('formula : ATOM OPEN_PAREN variableslist CLOSE_PAREN')
        @self.pg.production('formula : ATOM')
        @self.pg.production('formula : BOTTOM')
        def formula(p):
            #print(p)
            if len(p) < 3:
                if p[0].gettokentype() == 'ATOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'BOTTOM':
                    return p[0], AtomFormula(key=p[0].value)
                elif p[0].gettokentype() == 'NOT':
                    result = p[1]
                    return p[0], NegationFormula(formula=result[1])  
                elif( not type(p[0]) is tuple):
                  result1 = p[0]
                  result2 = p[1]
                  # Universal Formula
                  if p[0].gettokentype() == 'EXT':  
                    var = p[0].value.split('E')[1]
                    return p[0], ExistentialFormula(variable=var, formula=p[1][1])
                  elif p[0].gettokentype() == 'ALL':  
                    var = p[0].value.split('A')[1]
                    return p[0], UniversalFormula(variable=var, formula=p[1][1])
            elif len(p)==4:
              # Predicate Formula
              name = p[0]
              varlist = p[2]
              return p[0], PredicateFormula(name=p[0].value,variables=varlist[1])            
            elif len(p) == 3:
              # Binary Formula
              result1 = p[0]
              result2 = p[2]
              if(p[1].value=='&'):
                return result1[0], AndFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='|'):
                return result1[0], OrFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='->'):
                return result1[0], ImplicationFormula(left=result1[1], right=result2[1])
              elif(p[1].value=='<->'):
                return result1[0], BiImplicationFormula(left=result1[1], right=result2[1])
              else:
                return result1[0], BinaryFormula(key=p[1].value, left=result1[1], right=result2[1])

        @self.pg.production('formula : OPEN_PAREN formula CLOSE_PAREN')
        def paren_formula(p):
            result = p[1]
            return p[0], result[1]

        @self.pg.production('variableslist : VAR')
        @self.pg.production('variableslist : VAR COMMA variableslist')
        def variablesList(p):
             if len(p) == 1:
                 return p[0], [p[0].value]
             else:
                result = p[2]
             return p[0], [p[0].value] + result[1]


        @self.pg.error
        def error_handle(token):
            productions = self.state.splitlines()
            error = ''  

            if(productions == ['']):
                error = 'None formula was submitted.'
            if token.gettokentype() == '$end':
                error = 'None formula was submitted.'
            else:
                source_position = token.getsourcepos()
                error = 'The formula definition is not correct, check that all rules were applied correctly.\nRemember that a formula is defined by the following BNF:\nF :== P | ~ P | Q&A | P | Q | P -> Q | P <-> Q | (P), where P,Q are atoms.\n'
                error += "Sintax error:\n"
                error += productions[source_position.lineno - 1]
                string = '\n'
                for i in range(source_position.colno -1):
                    string += ' '
                string += '^'
                if token.gettokentype() == 'OUT':
                    string += ' Symbol does not belong to the language.'
                error += string
                
            raise ValueError("@@"+error)

    def get_error(self, type_error, token_error, rule):
        productions = self.state.splitlines()
        column_error = token_error.getsourcepos().colno
        erro = "Syntax error in line {}:\n".format(token_error.getsourcepos().lineno)
        erro += productions[token_error.getsourcepos().lineno-1] + "\n"
        for i in range(column_error-1):
            erro += ' '
        
        return erro
    
    def get_parser(self):
      return self.pg.build()
    @staticmethod
    def getFormula(input_text=''):
      lexer = Lexer().get_lexer()
      tokens = lexer.lex(input_text)

      pg = ParserFormula(state=input_text)
      pg.parse()
      parser = pg.get_parser()
      result = parser.parse(tokens)
      return result
