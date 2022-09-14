def space_len(i_problem,i):
    maxlen = max(len(problem[i].split()[0]),len(problem[i].split()[2]))
    space_len = 2 if len(i_problem) == maxlen else maxlen - len(i_problem) + 2
    return space_len

    #first_line = [' '*space_len(problem[i].split()[0],i) + problem[i].split()[0] + ' '*3 for i in range(len(problem))]
    #second_line = [problem[i].split()[1] + ' '*(space_len(problem[i].split()[2],i)-1) + problem[i].split()[2] + ' '*3 for i in range(len(problem))]
    #third_line = [(2 + max(len(problem[i].split()[0]),len(problem[i].split()[2]))) * '-' + ' '*3 for i in range(len(problem))]
    #result_line = [int(problem[i].split()[0]) + int(problem[i].split()[2]) if problem[i].split()[1] == '+' else int(problem[i].split()[0]) - int(problem[i].split()[2]) for i in range(len(problem))]
 
def find_trubles(problems):

    trubles = {'too_many_problems' : False, 'incorrect_operators' : False, 'too_many_digits' : False, 'not_digit' : False}

    if len(problems) > 5:
        trubles['too_many_problems'] = True

    for problem in problems:
        x1, operator, x2 = problem.split()
        if operator != '+' and operator != '-':
            trubles['incorrect_operators'] = True
        if len(x1) > 4 or len(x2) > 4:
            trubles['too_many_digits'] = True
        if not x1.isdigit() or not x2.isdigit():
            trubles['not_digit'] = True
    return trubles


def arithmetic_arranger(problems, result=False):

    trubles = find_trubles(problems)
    if trubles['too_many_problems']: return "Error: Too many problems."
    if trubles['incorrect_operators']: return "Error: Operator must be '+' or '-'."
    if trubles['too_many_digits']: return "Error: Numbers cannot be more than four digits."
    if trubles['not_digit']: return "Error: Numbers must only contain digits."

    first_line, second_line, third_line, result_line = list(), list(), list(), list()
    intend = ' '*4
    
    for problem in problems:
        x1, operation, x2 = problem.split()
        max_x_len = max(len(x1), len(x2))
        full_line_len = max_x_len + 2
        underline = '-'*full_line_len

        if len(x1) == max_x_len:
            space_1 = ' '*2
            space_2 = ' '*(full_line_len - len(x2) - 1)
        else:
            space_1 = ' '*(full_line_len - len(x1))
            space_2 = ' '
            
        first_line.append(f'{space_1}{x1}{intend}')
        second_line.append(f'{operation}{space_2}{x2}{intend}')
        third_line.append(f'{underline}{intend}')

        if result:
            if operation == '+':
                result_str = str(int(x1) + int(x2))
            else:
                result_str = str(int(x1) - int(x2))
            if len(result_str) > max_x_len:
                result_line.append(f' {result_str}{intend}')
            else:
                result_line.append(f'{" "*(full_line_len - len(result_str))}{result_str}{intend}')
        else:
            result_line.append(' ')
            
    arithmetic_arranger = '\n'.join([''.join(first_line).rstrip(), ''.join(second_line).rstrip(), ''.join(third_line).rstrip(), ''.join(result_line)]).rstrip()
    return arithmetic_arranger 

problems = ['98 + 3g5', '3801 - 2', '45 + 43', '123 + 49']

print(arithmetic_arranger(problems, True))

#arguments = [['3801 - 2', '123 + 49']]
#expected_output = '  3801      123\n-    2    +  49\n------    -----'

#'  3801      123\n-    2    +  49\n------    -----\n' == 
#'  3801      123\n-    2    +  49\n------    -----'
