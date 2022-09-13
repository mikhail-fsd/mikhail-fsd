def space_len(i_problem,i):
    maxlen = max(len(problem[i].split()[0]),len(problem[i].split()[2]))
    #if len(i_problem) == maxlen:
    #    space_len = 2
    #else:
    #    space_len = maxlen - len(i_problem) + 2


    space_len = 2 if len(i_problem) == maxlen else maxlen - len(i_problem) + 2
    return space_len



def arithmetic_arranger(problem):

    first_line = [' '*space_len(problem[i].split()[0],i) + problem[i].split()[0] + ' '*3 for i in range(len(problem))]
    second_line = [problem[i].split()[1] + ' '*(space_len(problem[i].split()[2],i)-1) + problem[i].split()[2] + ' '*3 for i in range(len(problem))]
    third_line = [(2 + max(len(problem[i].split()[0]),len(problem[i].split()[2]))) * '-' + ' '*3 for i in range(len(problem))]
    result_line = [int(problem[i].split()[0]) + int(problem[i].split()[2]) if problem[i].split()[1] == '+' else int(problem[i].split()[0]) - int(problem[i].split()[2]) for i in range(len(problem))]
    result_line = list()
    
    for i in range(len(problem)):
        max_len = max(len(problem[i].split()[0]),len(problem[i].split()[2]))

        if len(problem[i].split()[0]) == max_len:
            space_len1 = 2
            space_len2 = max_len - len(problem[i].split()[2]) + 1
        else:
            space_len1 = max_len - len(problem[i].split()[0]) + 2
            space_len2 = 1
            
        first_line.append(' '*space_len1 + problem[i].split()[0] + ' '*3)
        second_line.append(problem[i].split()[1] + ' '*space_len2 + problem[i].split()[2] + ' '*3)
        print(i)

    print(*first_line)
    print(*second_line)
    print(*third_line)
    print(*result_line)
    return None

problem = ["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]

arithmetic_arranger(problem)

