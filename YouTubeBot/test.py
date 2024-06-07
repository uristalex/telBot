# import os
#
# s = 0
# for a, b, f in os.walk('videos/'):
#     print(os.path.getsize(f))
#
# print(s)

import os
from pathlib import Path

#Вычисляет размер папки, количество файлов и количество итераций функции
def folderSize(path):
    # fsize = 0
    # for file in Path(path).rglob('*'):
    #     if (os.path.isfile(file)):
    #         fsize += os.path.getsize(file)
    # return round((fsize/1024), 2)
    return round(sum([os.path.getsize(i) for i in Path(path).rglob('*')])/1024, 2)

print(folderSize('videos'))