input_file_name = ['input_1.txt', 'input_2.txt', 'input_3.txt', 'input_4.txt', 'input_5.txt']
output_file_name = ['output_1.txt', 'output_2.txt', 'output_3.txt', 'output_4.txt', 'output_5.txt']

from propositional_logic import *

# Default that the input is in CNF form

def PL_RESOLUTION(knowledge, query):
    clauses = knowledge + [Not(query)]
    newList = []

    output_clause = []
    output_num = []

    while True:
        print('Current Clauses: ', end='')
        print(clausesPrint(clauses))

        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(0,n) for j in range(i+1,n)]
        for (ci, cj) in pairs:

            resolvents = PL_RESOLVE(ci, cj, clauses)
            for e in resolvents:
                if not e in newList:
                    newList.append(e)

        newIsSubset = True
        for e in newList:
            if not e in clauses:
                newIsSubset = False
        if newIsSubset:
            return [False, output_num, output_clause]

        count = 0
        for e in newList:
            if not e in clauses:
                clauses.append(e)
                output_clause.append(clausesPrint([e]))
                count += 1
        output_num.append(count)
        print(f'Number of clauses to add: {count}')

        if '{}' in clauses:
            return [True, output_num, output_clause]

        print('------------------------------------------------------------------------')

def PL_RESOLVE(ci, cj, PL_RESOLUTION_clauses):
    new_clauses = []
    ciList = ci.listOfLiterals()
    cjList = cj.listOfLiterals()

    if len(ciList) == 1 and len(cjList) == 1:
        if ciList[0] == Not(cjList[0]) or cjList[0] == Not(ciList[0]):
            new_clauses = ['{}']
    else:
        for e_ci in ciList:
            for e_cj in cjList:
                if e_ci == Not(e_cj) or Not(e_ci) == e_cj:
                    tempCi = ciList
                    tempCj = cjList
                    tempCi.remove(e_ci)
                    tempCj.remove(e_cj)
                    cur_new_clauses = list(set(tempCi + tempCj))

                    can_append = False
                    if len(cur_new_clauses) == 1:
                        cur_new_clause = cur_new_clauses[0]
                        can_append = True
                    elif len(cur_new_clauses) > 1:
                        flag = True
                        for ei in cur_new_clauses:
                            for ej in cur_new_clauses:
                                if ei == Not(ej) or Not(ei) == ej:
                                    flag = False
                        if flag:
                            cur_new_clause = Or(cur_new_clauses)
                            can_append = True
                    if can_append:
                        new_clauses.append(cur_new_clause)
    
    for ei in new_clauses:
        for ej in PL_RESOLUTION_clauses:
            if ei == ej or ei == Not(Not(ej)) or Not(Not(ei)) == ej:
                new_clauses.remove(ei)

    if len(new_clauses) != 0:
        print(f'> PL_RESOLVE: [{ci.printClause():<12}] and [{cj.printClause():<12}]\t->\t', end='')
        print('[' + clausesPrint(new_clauses) + ']')
    return new_clauses

def clausesPrint(ls):
    res_str = ''
    try:
        for e in ls:
            res_str += e.printClause() + '; '
        res_str = res_str[:-2]
    except:
        res_str = ls[0]
    return res_str

def splitSymbolsByOr(s_text):
    symbols = []
    s = s_text
    def countOr(s):
        return s.count('OR')
    for i in range(countOr(s)):
        idx = s.find('OR') - 1
        cur_symbol = s[:idx]
        symbols.append(cur_symbol)
        s = s[idx+4:]
    symbols.append(s)
    return symbols

def extractSymbols(lines):
    symbols = []
    for i, line in enumerate(lines):
        if i != 1:
            for symbol in splitSymbolsByOr(line):
                if symbol[0] == '-':
                    if not symbol[1:] in symbols:
                        symbols.append(symbol[1:])
                else:
                    if not symbol in symbols:
                        symbols.append(symbol)
    return symbols

def extractLines(lines):
    lns = []
    for line in lines:
        lns.append(line)
    return lns

def symStrToLogical(sym_string, symbols_string, symbols_logical):
    if sym_string[0] != '-':
        idx = symbols_string.index(sym_string)
        return symbols_logical[idx]
    else:
        idx = symbols_string.index(sym_string[1:])
        return Not(symbols_logical[idx])

def clauseStrToLogical(clause_string, symbols_string, symbols_logical):
    clause_logical = None

    syms_string_temp = splitSymbolsByOr(clause_string)
    if len(syms_string_temp) == 1:
        sym_string = syms_string_temp[0]
        clause_logical = symStrToLogical(sym_string, symbols_string, symbols_logical)
    else:
        temp_clause_list = []
        for sym_string in syms_string_temp:
            temp_clause_list.append(symStrToLogical(sym_string, symbols_string, symbols_logical))
        clause_logical = Or(temp_clause_list)

    return clause_logical



for i in range(len(input_file_name)):
    read_file_successfully = False
    with open(input_file_name[i], 'r') as f_input:
        lines = [line.rstrip() for line in f_input.readlines()]
        symbols_string = extractSymbols(lines)
        symbols_logical = []
        clauses_string = extractLines(lines)
        clauses_logical = []
        for sym in symbols_string:
            symbols_logical.append(Symbol(sym))

        n_kb = int(clauses_string[1])
        clauses_string.remove(clauses_string[1])
        
        for clause_string in clauses_string:
            clause_logical = clauseStrToLogical(clause_string, symbols_string, symbols_logical)
            clauses_logical.append(clause_logical)

        query = clauses_logical[0]
        knowledge = clauses_logical[1:]
        print('========================================================================')
        print(f"{'Knowledge:':<12}{clausesPrint(knowledge)}")
        print(f"{'Query:':<12}{clausesPrint([query])}")
        print('========================================================================')
        pl_res = PL_RESOLUTION(knowledge, query)
        print(f'\n>> Entailment: {pl_res[0]}')
        print('========================================================================')


        write_file_successfully = False
        with open(output_file_name[i], 'w') as f_output:
            j = 0
            for count in pl_res[1]:
                f_output.write(f'{count}\n')
                for i in range(count):
                    f_output.write(f'{pl_res[2][j]}\n')
                    j += 1
            if pl_res[0] == True:
                f_output.write(f'YES')
            else:
                f_output.write(f'0\nNO')
            write_file_successfully = True
            f_output.close()
        
        if not write_file_successfully:
            print('> Failed to write file!')

        read_file_successfully = True
        f_input.close()

    if not read_file_successfully:
        print('> Failed to read file!')