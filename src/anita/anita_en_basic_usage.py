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