# Stellarium_DSO_catalog
fix with NI2019



#6059 fix NI2019's M20(NGC6514) pos error







version Control:

base on: Fixed errors in DSO catalog (SNR G subsystem; fix #1208)



put catalog.dat into C:\Program Files\Stellarium\nebulae\default



My fixing note:

1.source

catalog
https://github.com/Stellarium/stellarium/blob/master/nebulae/default/catalog.txt #1208

Dr. Wolfgang Steinicke

http://www.klima-luft.de/steinicke/index_e.htm

2.fix Bug

①dup ID：such as NGC3626=NGC3632, however stellarium's logic does not permit, so just remove one.

②unmarked type：EN+OCL = C+N，GxyP = PoG。

③NGC/IC in stellarium only allow int， however extended id is string.

3.solving way：

①binding error:

PGC is position good. NGC is position bad. build a correct map.

②fix RA、Dec、Vmag

③two IC object = one NGC. delete one IC.

④No binding ID in origin, build a new one.

⑤write the undata 99、0。

⑥warning! Excel's format auto bug, text format is good.