import os



if __name__ == '__main__':
    all_file = os.listdir('19411')
    with open('19411-all-fileName.txt', 'a') as f:
        for one_file in all_file:
            f.write(one_file + '\n')
    


