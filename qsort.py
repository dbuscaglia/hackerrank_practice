global_count = 0

def qsort(qlist):
    if len(qlist) <= 1:
        return qlist

    pivot = qlist[len(qlist) - 1]  # right most element
    qlist.pop(len(qlist) - 1)
    lesslist = []
    greaterlist = []
    for element in qlist:
        if element <= pivot:
            lesslist.append(element)
        else:
            greaterlist.append(element)

    lesslist = qsort(lesslist)
    greaterlist = qsort(greaterlist)

    final_list = []
    for element in lesslist:
        final_list.append(element)
    final_list.append(pivot)
    for element in greaterlist:
        final_list.append(element)
    return final_list

sortable = [9, 6, 3, 1, 7, 0, 4]
# should be 0, 1, 3, 4, 6, 7, 9]
# pivot should be 4
print qsort(sortable)
