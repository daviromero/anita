# Analytic Tableau Proof Assistant (ANITA)

The ANITA is a tool written in Python that can be used as a desktop application, or in a [web platform](https://sistemas.quixada.ufc.br/anita/en/). The main idea is that the students can write their proofs as similar as possible to what is available in the textbooks and to what the students would usually write on paper. ANITA allows the students to automatically check whether a proof in the analytic tableaux is valid. If the proof is not correct, ANITA will display the errors of the proof. So, the students may make mistakes and learn from the errors. The web interface is very easy-to-use and has: 
- An area for editing the proof in plain text. The students should write a proof in the Fitch-style (see [AT Rules](AT-Rules.pdf)).
- A message area to display whether the proof is valid, the countermodel, or the errors on the proof.
- And the following links: 
  - Check, to check the correctness of the proof; 
  - Manual, to view a document with the inference rules and examples; 
  - LaTeX, to generate the LaTeX code of the trees from a valid proof. Use the `qtree` package in your LaTeX code; 
  - LaTeX in Overleaf, to open the proof source code directly in [Overleaf](http://overleaf.com/) that is a collaborative platform for editing LaTeX

To facilitate the writing of the proofs, we made the following conventions in ANITA:
- The Atoms are written in capital letters (e.g. `A, B,  H(x)`);
- Variables are written with the first letter in lowercase, followed by letters and numbers (e.g. `x, x0, xP0`);
- Formulas with $\forall x$ and $\exists x$ are represented by $Ax$ and $Ex$ ('A' and 'E' followed by the variable x). For instance, `Ax(H(x)->M(x))` represents $\forall x~(H(x)\rightarrow M(x))$.
- Table below shows the equivalence of logic symbols and those used in ANITA.
- The order of precedence of quantifiers and logical connectives is defined by $\lnot,\forall,\exists,\wedge,\vee,\rightarrow$ with right alignment. For example:
  - Formula `~A&B -> C` represents formula $(((\lnot A)\land B)\rightarrow C)$;
  - The theorem `~A|B |- A->C` represents $((\lnot A)\vee B)\vdash (A\rightarrow B)$.
- Each inference rule will be named by its respective connective and the truth value of the signed formula. For example, `&T` represents the conjunction rule when the formula is true. Optionally, the rule name can be omitted.
- The justifications for the premises and the conclusion use the reserved words `pre` and `conclusion`, respectively.

| Symbol |  $\lnot$ | $\land$ | $\lor$ | $\rightarrow$ | $\forall x$ | $\exists x$ | $\bot$ | branch | $\vdash$ |
| :---:  |  :---:  | :---: | :---:  | :---:  | :---:  | :---:  | :---:  | :---:  | :---: |
| LaTeX  |  $\backslash\textrm{lnot}$ | $\backslash\textrm{land}$ | $\backslash\textrm{lor}$ | $\backslash\textrm{rightarrow}$ | $\backslash\textrm{forall x}$ | $\backslash\textrm{exists x}$ | $\backslash\textrm{bot}$ | $[.~]$ | $\backslash\textrm{vdash}$ |
| ANITA |  ~  | \& | $\mid$ | -> | Ax | Ex | @  | { } | \|- |

![](ANITA-EXAMPLE.png)

## License
ANITA is available by a [**MIT License**](license.txt).

## Requirements:
- You must install the [rply 0.7.8 package](https://pypi.org/project/rply/)

## ANITA
You can run ANITA with the command line: 
```bash
python anita_en.py [-i input_file] [-o output_file]
```
## ANITA in Voila
You can run ANITA in Jupyter Nootebook or in a [Voilà](https://voila.readthedocs.io/) 
```bash
voila anita_en.ipynb
```
## ANITA in your code
You can import ANITA in your code (basic usage)
```bash
from anita.anita_en_fo import check_proof

print(check_proof('''1. T A|B		pre
2. T A->C		pre
3. T B->C		pre
4. F C			conclusion
5. {	T A		1
6.	{	F A	    2
7.		@	    5,6
	}
8.	{	T C	    2
9.		@	    8,4
	}
   }
10.{	T B		1
11.	{	F B	    3
12.		@	    10,11
	}
13.	{	T C 	3
14.		@	    13,4
	}
   }
'''))
```

## A Portuguese Version
We have a portuguese version:
- Run ANITA with
```bash
python anita.anita_pt.py [-i input_file] [-o output_file]
```
- Voilà with
```bash
voila anita_pt.ipynb
```
- In ANITA syntax, use `conclusao`instead of `conclusion`.

- You can import ANITA in your code (basic usage)
```bash
from anita.anita_pt_fo import check_proof

print(check_proof('''1. T A|B		pre
2. T A->C		pre
3. T B->C		pre
4. F C			conclusao
5. {	T A		1
6.	{	F A	    2
7.		@	    5,6
	}
8.	{	T C	    2
9.		@	    8,4
	}
   }
10.{	T B		1
11.	{	F B	    3
12.		@	    10,11
	}
13.	{	T C 	3
14.		@	    13,4
	}
   }
'''))
```
