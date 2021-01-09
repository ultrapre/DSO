import re
def writealllines(lines,src,srccoding="utf-8",filetype="txt",crlf=True):
    rf = ''
    if crlf == True:
        rf = '\n'
    fp = open(src, "w", encoding=srccoding)
    fp.writelines([line + rf for line in lines])
    fp.close()

def skylistMake(src,ngcdat=None):
    lins = ['SkySafariObservingListVersion=3.0', 'SortedBy=Default Order']
    num = 0
    for line in open(src, "r").read().splitlines():
        it = line
        cm = ''
        if ',' in line:
            it = line.split(',',1)[0]
            cm = line.split(',',1)[1]
        elif '\t' in line:
            it = line.split(',',1)[0]
            cm = line.split(',',1)[1]
        itp = re.match('^([A-z]+)(.*)$', it)
        if itp:
            it = itp.group(1) + ' ' + itp.group(2)
        lins.append('SkyObject=BeginObject')
        lins.append('\tObjectID=4,-1,-1')
        lins.append('\tCatalogNumber=' + it)
        lins.append('\tDefaultIndex=' + str(num))
        if cm != '':
            lins.append('\tComment=' + cm)
        lins.append('EndObject=SkyObject')
        num += 1
    writealllines( lins,src.replace('.txt','.skylist'))
    return
if __name__ == '__main__':
    skylistMake('list.txt')

