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
        line_len = max(len(x1), len(x2)) + 2
        underline = '-'*line_len
        
        first_line.append(f"{x1:>{line_len}}")
        second_line.append(f'{operation}{x2:>{line_len-1}}')
        third_line.append(f'{underline}')

        if result:
            if operation == '+':
                result_str = str(int(x1) + int(x2))
            else:
                result_str = str(int(x1) - int(x2))
            result_line.append(f'{result_str:>{line_len}}')

    first_line = (intend).join(first_line)
    second_line = (intend).join(second_line)
    third_line = (intend).join(third_line)
    result_line = (intend).join(result_line)
    
    arithmetic_arranger = '\n'.join([first_line, second_line, third_line, result_line]).rstrip()
    return arithmetic_arranger 

problems = ['98 + 35', '3801 - 2', '45 + 43', '123 + 49']

print(arithmetic_arranger(problems))

#arguments = [['3801 - 2', '123 + 49']]
#expected_output = '  3801      123\n-    2    +  49\n------    -----'

#'  3801      123\n-    2    +  49\n------    -----\n' == 
#'  3801      123\n-    2    +  49\n------    -----'
