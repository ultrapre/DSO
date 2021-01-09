
def jsondump(dic,dst,sort=False):
    f = open(dst, "w", encoding='utf-8')
    json.dump(dic, f, ensure_ascii=False, sort_keys=sort, indent=4)
    f.close()

def makebookmark(src,dst):
    import uuid
    dic = {'bookmarks': {}}
    for line in open(src, "r" ).read().splitlines():
        name = line.split('\t')[0]
        desp = ''
        if '\t' in line:
            desp = line.split('\t')[1] + ','
        u1 = str(uuid.uuid1())
        dic['bookmarks'][u1] = {}
        dic['bookmarks'][u1]['name'] = name.replace('NGC', 'NGC ').replace('IC', 'IC ')
        dic['bookmarks'][u1]["nameI18n"] = desp
    jsondump(dic, dst)
	
makebookmark('list.txt','list.json')