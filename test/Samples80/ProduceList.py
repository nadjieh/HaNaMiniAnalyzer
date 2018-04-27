import Samples as sss

for sample in sss.MiniAOD80Samples:
    if "DYMG" in sample.Name:
        print  'dasgoclient --query="file dataset=%s" > %s.list' % (sample.DSName ,  sample.Name)
