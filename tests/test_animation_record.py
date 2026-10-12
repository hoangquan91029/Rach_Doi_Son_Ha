"""Synthetic custody fixtures only; no visual or public gameplay evidence."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image
from jsonschema import ValidationError

spec=importlib.util.spec_from_file_location('record_validator',Path(__file__).resolve().parents[1]/'scripts/validate-animation-record.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RecordTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        image=Image.new('RGBA',(8,8),(0,0,0,0))
        image.putpixel((4,4),(255,0,0,255))
        image.save(self.root/'source.png')
        Image.new('RGBA',(132,132),(0,0,0,0)).save(self.root/'atlas.png')
        def pin(name):
            return {'path':name,'sha256':hashlib.sha256((self.root/name).read_bytes()).hexdigest()}
        def rgba(name):
            with Image.open(self.root/name) as im:
                return hashlib.sha256(im.tobytes()).hexdigest()
        source={**pin('source.png'),'rgbaSha256':rgba('source.png')}
        job={'schemaVersion':2,'id':'fixture','family':'fixture','action':'idle','direction':0,'master':source,'fixedCanvas':{'width':8,'height':8},'cell':{'width':128,'height':128},'render':{'width':42,'height':42},'pivot':{'x':4,'y':7,'space':'source'},'loop':True,'frameCount':1,'frames':[{'input':source,'status':'selected','phase':0,'durationMs':90}]}
        descriptor={'id':'fixture','family':'fixture','state':'idle','direction':0,'cell':job['cell'],'render':job['render'],'pivot':job['pivot'],'loop':True,'frames':[{'source':source,'x':2,'y':2,'width':128,'height':128,'durationMs':90}],'runtime':{**pin('atlas.png'),'rgbaSha256':rgba('atlas.png'),'width':132,'height':132}}
        for name,data in [('job.json',job),('descriptor.json',descriptor)]:
            (self.root/name).write_text(json.dumps(data))
        self.record={'schema':'rds-animation-record/v1','identityId':'fixture','unitId':'fixture','assetId':'fixture','version':'1','archetype':'biped','action':'idle','direction':0,'canonicalReference':pin('source.png'),'job':pin('job.json'),'descriptor':pin('descriptor.json'),'sources':[{'pin':pin('source.png'),'status':'selected'}],'tool':{'name':'synthetic-test','model':None,'promptVersion':None,'poseVersion':None,'timestamp':None},'geometry':{'sourceWidth':8,'sourceHeight':8,'cellWidth':128,'cellHeight':128,'pivotX':4,'pivotY':7,'renderWidth':42,'renderHeight':42,'padding':2},'frameSequence':[{'sourceIndex':0,'phase':0,'durationMs':90}],'loop':True,'mirrorSource':None,'qualification':{k:{'status':'UNREVIEWED','evidence':[]} for k in ['technical','motion','runtime','owner','release']},'scope':'candidate','distancePerCycle':None,'limitations':['Synthetic fixture, not art approval']}
    def test_candidate_valid_never_approval(self):
        result=module.validate(self.record,self.root)
        self.assertFalse(result['visualApproval'])
        self.assertFalse(result['productionAuthorized'])
    def test_wrong_sha(self):
        self.record['canonicalReference']['sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'SHA mismatch'):module.validate(self.record,self.root)
    def test_unknown_field(self):
        self.record['tool']['invented']=True
        with self.assertRaises(ValidationError):module.validate(self.record,self.root)
    def test_empty_pass_evidence(self):
        self.record['qualification']['motion']['status']='PASS'
        with self.assertRaises(ValidationError):module.validate(self.record,self.root)
    def test_missing_qualification(self):
        self.record['qualification']={}
        with self.assertRaises(ValidationError):module.validate(self.record,self.root)
    def test_held_production(self):
        job=json.loads((self.root/'job.json').read_text())
        job['frames'][0]['status']='held'
        (self.root/'job.json').write_text(json.dumps(job))
        self.record['job']['sha256']=hashlib.sha256((self.root/'job.json').read_bytes()).hexdigest()
        self.record['sources'][0]['status']='held'
        self.record['scope']='production'
        with self.assertRaisesRegex(ValueError,'rejects held'):module.validate(self.record,self.root)
    def test_production_cannot_invent_approval(self):
        self.record['scope']='production'
        for stage in ['technical','motion','runtime']:
            self.record['qualification'][stage]={'status':'PASS','evidence':[copy.deepcopy(self.record['job'])]}
        with self.assertRaisesRegex(ValueError,'trusted qualification'):module.validate(self.record,self.root)
    def test_duration_binding(self):
        self.record['frameSequence'][0]['durationMs']=91
        with self.assertRaisesRegex(ValueError,'Duration mismatch'):module.validate(self.record,self.root)
    def test_nested_relative_job_and_descriptor_pins(self):
        for folder, name in [('jobs','job.json'),('compiled','descriptor.json')]:
            nested=self.root/folder
            nested.mkdir()
            data=json.loads((self.root/name).read_text())
            if name=='job.json':
                data['master']['path']='../source.png'
                data['frames'][0]['input']['path']='../source.png'
            else:
                data['frames'][0]['source']['path']='../source.png'
                data['runtime']['path']='../atlas.png'
            target=nested/name
            target.write_text(json.dumps(data))
            field='job' if name=='job.json' else 'descriptor'
            self.record[field]={'path':f'{folder}/{name}','sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
        result=module.validate(self.record,self.root)
        self.assertEqual(result['status'],'VALID_CANDIDATE_CUSTODY')
        self.assertFalse(result['visualApproval'])
    def test_direction_binding(self):
        self.record['direction']=1
        with self.assertRaisesRegex(ValueError,'Direction mismatch'):module.validate(self.record,self.root)
    def test_source_order(self):
        self.record['frameSequence'][0]['sourceIndex']=1
        with self.assertRaisesRegex(ValueError,'Source indices'):module.validate(self.record,self.root)

if __name__=='__main__':unittest.main()
