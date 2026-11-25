"""Fill Nature Portfolio's XFA Reporting Summary from these answers.
Blank form: https://www.nature.com/documents/nr-reporting-summary.pdf
python fill_reporting_summary.py BLANK.pdf OUT.pdf"""
import sys, re, pypdf
from pypdf.generic import NameObject, ArrayObject
from xml.etree import ElementTree as ET
SRC, OUT = sys.argv[1], sys.argv[2]
T = {
 'author': 'Animesh Acharjee',
 'lastupdate': '2026-11-25',
 'collectioninfo': 'Custom Python scripts queried the Omics Discovery Index, NCBI GEO, BioStudies and ArrayExpress, CZ CELLxGENE Discover and the Human Cell Atlas Data Portal APIs; CNGBdb was searched by hand. The code is in the ELAJ repository (data_collation/), https://github.com/AtharvaOnGitHub/ELAJ.',
 'analysisinfo': 'ELAJ training and evaluation: Python 3.12, PyTorch 2.7.1 (CUDA 12.6), NumPy 1.26.4, SciPy 1.13.1, pandas 2.2.2, scanpy 1.9.8, anndata 0.10.9, h5py 3.12.1, scikit-learn 1.9.0 and R 4.5.0. Comparison methods and integration metrics: scvi-tools 1.2.1 (scVI, scANVI), harmonypy 0.2.0, Scanorama 1.7.4, scib-metrics 0.5.10, scib 1.1.7 and umap-learn 0.5.12. Foundation models were run from their published checkpoints with PyTorch 2.6.0 (CUDA 12.4): scGPT 0.2.5, Geneformer 0.1.0 with transformers 4.57.6, SCimilarity 0.4.1, and scFoundation from its published repository. ELAJ is available at https://github.com/AtharvaOnGitHub/ELAJ under the MIT licence; an archived release will be deposited on Zenodo with a DOI on acceptance.',
 'DAS': 'This study analysed previously published data and generated no new primary data. All datasets are publicly available. Gene Expression Omnibus: GSE266265, GSE247695, GSE214411, GSE218044, GSE213216, GSE203191 and GSE179640. ArrayExpress: E-MTAB-14039. CZ CELLxGENE Discover: collections 9ddea8d9 and 968885c5. CNGBdb: CNP0006183. No restrictions apply beyond each deposit\'s own terms. Source data are provided with this paper.',
 'human': [
  'All data come from the source studies\' public deposits. The tissue is endometrial or endometriosis-related, and the source studies report donors of female sex. Gender was not reported. Sex was not a variable in the analysis because it does not vary across the corpus.',
  'Race, ethnicity and other socially relevant groupings were not reported consistently by the source studies and were not used in the analysis.',
  '254 donors, deposited as 269 donor identifiers (one study pair deposits the same fifteen people twice). By donor record: 108 control, 99 eutopic endometrium from patients, 58 ectopic lesion and 4 adenomyosis, across six anatomical sites. Age and ancestry are not available consistently across studies.'],
 'recruitment': 'No participants were recruited for this study. Donors were recruited by the eleven source studies under their own protocols. Patients and many controls were undergoing surgery, which is how endometriosis is diagnosed, so the corpus over-represents surgically managed disease.',
 'ethics': 'This study is a secondary analysis of publicly available, de-identified single-cell data, and no new samples were collected. Each source study reports ethical approval and informed consent from its donors in its publication. No further ethical approval was required for this analysis.',
 'life': {
  'howselectedsamplesize': 'No sample-size calculation was performed. The corpus is every eligible public single-cell dataset of endometriosis found by a systematic search (Extended Data Fig. 1): 1,577,728 cells from 254 donors in eleven studies.',
  'exclusions': 'Of 553 records identified, 11 studies met the three pre-stated inclusion criteria (single-cell RNA data, biopsied human tissue, relevance to endometriosis; Methods, Data collection). Deposits of placental tissue and of organoids were excluded. Fifteen people deposited under two identifiers were merged before splitting. Within each study, genes detected in fewer than three cells were removed, as were cells with fewer than 200 counts, fewer than 100 detected genes or more than 25% of counts from mitochondrial genes. Doublets were not removed.',
  'limitations': 'Each reported configuration is a single training run at seed 24; one configuration was retrained at a second seed (Supplementary Note 5). The six frontier models and five ablations reproduce the trade-off across configurations. Published claims were retested across all studies that carry the relevant labels.',
  'methodrandomization': 'There was no experimental allocation. Donors were assigned to training, validation and test partitions (70/15/15) at random, with every cell from a donor in a single partition.',
  'blindinggroupallocation': 'There was no group allocation to blind. The model was never given disease status, severity, cell family or cell type; only menstrual phase was supervised, so every biological readout is measured on labels the model did not see.'}}
STATS = {'samplesize':'2','collection':'2','statstests':'2','covariates':'2','assumptions':'2','descstats':'2','nullhypothesis':'2','bayesian':'1','hierarchical':'2','effectsizes':'2'}
NA = ['antibodies','celllines','palaeontology','animals','clinical','durc','plants','chip-seq','flowcytometry','mri']
HIDE = ['Behavioural','EEE','Antibodies','Celllines','Palaeontology','Animals','Clinical','DURC','Plants','ChIPseq','FlowCytometry','MRI']

r = pypdf.PdfReader(SRC); w = pypdf.PdfWriter(clone_from=r)
af = w._root_object['/AcroForm']; xfa = af['/XFA']
pk = {str(xfa[i]): xfa[i+1].get_object() for i in range(0, len(xfa), 2)}

ET.register_namespace('xfa', 'http://www.xfa.org/schema/xfa-data/1.0/')
ds = ET.fromstring(pk['datasets'].get_data())
form = ds.find('{http://www.xfa.org/schema/xfa-data/1.0/}data/form')
mc = form.find('Maincontent')
def setp(path, val):
    e = mc.find(path); assert e is not None, path; e.text = val
setp('Header/author', T['author']); setp('Header/lastupdate', T['lastupdate'])
for k, v in STATS.items(): setp(f'Universal/Statistics/questions/{k}', v)
setp('Universal/Software/collectioninfo', T['collectioninfo']); setp('Universal/Software/analysisinfo', T['analysisinfo'])
setp('Universal/Dataavail/DAS/howselectedsamplesize', T['DAS'])
hd = mc.find('Humans').findall('humandetails'); assert len(hd) == 3
for e, v in zip(hd, T['human']): e.text = v
setp('Humans/recruitment', T['recruitment']); setp('Humans/ethics', T['ethics'])
setp('SelectField/Type', '1')
for k, v in T['life'].items(): setp(f'Life/{k}', v)
for k in NA[:7]: setp(f'MethodModules/MethodspecificReporting/materials/{k}', '1')
for k in NA[7:]: setp(f'MethodModules/MethodspecificReporting/methods/{k}', '1')
newds = ET.tostring(ds, encoding='utf-8')

tx = pk['template'].get_data().decode('utf-8')
for name in HIDE:
    pat = re.compile(r'<subform(\s[^>]*?)name="' + name + r'"')
    m = pat.findall(tx); assert len(m) == 1 and 'presence' not in m[0], (name, m)
    tx = pat.sub(lambda mm: '<subform presence="hidden"' + mm.group(1) + 'name="' + name + '"', tx)

pk['datasets'].set_data(newds); pk['template'].set_data(tx.encode('utf-8'))
# drop the saved form state so Reader re-merges template + data; drop the broken Reader-rights signature
arr = ArrayObject()
for i in range(0, len(xfa), 2):
    if str(xfa[i]) == 'form': continue
    arr += [xfa[i], xfa[i+1]]
af[NameObject('/XFA')] = arr
if '/Perms' in w._root_object: del w._root_object['/Perms']
w.write(OUT)
print('ok')
