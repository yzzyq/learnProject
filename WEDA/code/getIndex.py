


if __name__ == '__main__':
    all_file_name = []
    with open('C:/Users/Administrator/Desktop/8202/8202-all-fileName.txt', 'r') as f:
        for one_file in f.readlines():
            file_name = one_file.strip('\n')
            all_file_name.append(file_name)
    print(len(all_file_name))

    true_file_name = []
    with open('C:/Users/Administrator/Desktop/8202/8202-true-file.txt', 'r') as f:
        for one_file in f.readlines():
            file_name = one_file.strip('\n')
            true_file_name.append(file_name)
    print(len(true_file_name))

    true_index = []
    for one_file in true_file_name:
        index = all_file_name.index(one_file)
        true_index.append(index)
    
    with open('C:/Users/Administrator/Desktop/8202/8202-true-index.txt', 'w') as f:
        f.write(str(true_index))



