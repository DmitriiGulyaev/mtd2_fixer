import os


def block_from_mtd(file, start, end):
    end = hex(int(end, 16) + 1)
    with open(file, "rb") as file:
        file.seek(int(start, 16), 0)
        size = int(end, 16) - int(start, 16)
        byte = file.read(size)
        return byte


need_names = ['mtd2', 'factory']
need_files = []
open_file = False
folder = [i.lower() for i in os.listdir()]
for i in range(len(folder)):
    for j in need_names:
        if j in folder[i]:
            need_files.append(os.listdir()[i])

while True:
    index_lst = []
    for i, item in enumerate(need_files):
        print(i*' ' + str(i) + '. ' + item)
        index_lst.append(i)
    q = input('Укажите нужный mtd2/factory (число)\t')
    if q.isdigit():
        if int(q) in index_lst:
            open_file = need_files[int(q)]
            break
    else:
        print('----------Некорректный ввод----------\n----------Попробуйте снова-----------')

if open_file:
    if '.' in open_file:
        name_new_file = open_file.split('.')[0] + 'FIXED' + '.' + open_file.split('.')[1]
    else:
        name_new_file = open_file + 'FIXED'
    new_file = open('bin' + ('\\' if '\\' in os.getcwd() else '/') + name_new_file, 'wb')
    before_pass = block_from_mtd(open_file, '0', '210DF')
    wifi_pass = block_from_mtd(open_file, '210a0', '210a8')
    after_pass = block_from_mtd(open_file, '210e9', 'fffff  ')
    new_file.write(before_pass + wifi_pass + after_pass)
    new_file.close()
    print(f'создан {name_new_file}\n admin:{str(wifi_pass)[2:-5]}')
else:
    print('mtd2/factory не обнаружен')
