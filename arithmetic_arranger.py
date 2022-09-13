def space_len(i_problem,i):
    maxlen = max(len(problem[i].split()[0]),len(problem[i].split()[2]))
    space_len = 2 if len(i_problem) == maxlen else maxlen - len(i_problem) + 2
    return space_len

    #first_line = [' '*space_len(problem[i].split()[0],i) + problem[i].split()[0] + ' '*3 for i in range(len(problem))]
    #second_line = [problem[i].split()[1] + ' '*(space_len(problem[i].split()[2],i)-1) + problem[i].split()[2] + ' '*3 for i in range(len(problem))]
    #third_line = [(2 + max(len(problem[i].split()[0]),len(problem[i].split()[2]))) * '-' + ' '*3 for i in range(len(problem))]
    #result_line = [int(problem[i].split()[0]) + int(problem[i].split()[2]) if problem[i].split()[1] == '+' else int(problem[i].split()[0]) - int(problem[i].split()[2]) for i in range(len(problem))]


def arithmetic_arranger(problem, result=False):

    first_line, second_line, third_line, result_line = list(), list(), list(), list()
    
    for i in range(len(problem)):
        max_len = max(len(problem[i].split()[0]),len(problem[i].split()[2]))

        if len(problem[i].split()[0]) == max_len:
            space_len1 = 2
            space_len2 = max_len - len(problem[i].split()[2]) + 1
        else:
            space_len1 = max_len - len(problem[i].split()[0]) + 2
            space_len2 = 1
            
        first_line.append(' '*space_len1 + problem[i].split()[0] + ' '*4)
        second_line.append(problem[i].split()[1] + ' '*space_len2 + problem[i].split()[2] + ' '*4)
        third_line.append('-'*(max_len + 2) + ' '*4)

        if result:
            if problem[i].split()[1] == '+':
                result_line.append(int(problem[i].split()[0]) + int(problem[i].split()[2]))
            else:
                result_line.append(int(problem[i].split()[0]) - int(problem[i].split()[2]))
            
            if len(str(result_line[i])) > max_len:
                result_line[i] = f' {str(result_line[i])}   '
            else:
                result_line[i] = ' '* (max_len + 2 - len(str(result_line[i]))) + str(result_line[i]) + ' '*4 

    for l in (first_line, second_line, third_line):
        l[-1] = l[-1].rstrip()
    arithmetic_arranger = '\n'.join([''.join(first_line), ''.join(second_line), ''.join(third_line)])
    return arithmetic_arranger 

problem = ["3801 - 2", "123 + 49"]

print([arithmetic_arranger(problem)])#, True)

#arguments = [['3801 - 2', '123 + 49']]
#expected_output = '  3801      123\n-    2    +  49\n------    -----'

#'  3801      123\n-    2    +  49\n------    -----\n' == 
#'  3801      123\n-    2    +  49\n------    -----'
