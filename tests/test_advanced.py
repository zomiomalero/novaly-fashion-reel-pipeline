"""Regression tests for v2 source inspection, word sync and background controls."""
from __future__ import annotations
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
from fashionreel.audio_qc import audio_report
from fashionreel.config import read_project,ProjectError
from fashionreel.demo import create_demo
from fashionreel.continuity import anchor_metrics,compare_project
from fashionreel.preflight import sha256_file,inspect_assets
from fashionreel.prompt_audit import lint,audit_folder
from fashionreel.word_timing import load_words,make_sync_map

ROOT=Path(__file__).resolve().parents[1]

class PromptAuditTests(unittest.TestCase):
    def test_clean_generation_prompt(self):
        self.assertEqual(lint('Photorealistic 9:16 vertical video. Keep the same original models and unchanged studio.'),[])
    def test_catches_duration(self):
        self.assertTrue(any('Duration' in x for x in lint('9:16 same models. Make 10 seconds.')))
    def test_catches_wardrobe_morph(self):
        self.assertTrue(any('wardrobe' in x.lower() for x in lint('Vertical 9:16, same models, change outfit at end')))
    def test_catches_missing_continuity(self):
        self.assertTrue(any('continuity' in x for x in lint('A lovely 9:16 fashion montage')))
    def test_still_skips_duration(self):
        self.assertFalse(any('Duration' in x for x in lint('A 9:16 photo at 8 seconds, same people',kind='still')))
    def test_pack_is_clean(self):
        r=audit_folder(ROOT/'examples/color-pair-looks/prompts-generated')
        self.assertEqual(r['issues'],0)
        self.assertEqual(r['files'],20)

class ContinuityTests(unittest.TestCase):
    def test_identical_image_score(self):
        im=Image.new('RGB',(100,100),'#4f575e')
        score=anchor_metrics(im,im,(.1,.1,.9,.9))
        self.assertAlmostEqual(score['mean_abs_difference_8bit'],0.)
    def test_different_image_score(self):
        a=Image.new('RGB',(100,100),'#151515');b=Image.new('RGB',(100,100),'#f0f0f0')
        self.assertGreater(anchor_metrics(a,b,(.1,.1,.9,.9))['mean_abs_difference_8bit'],100)
    def test_tiny_region_rejected(self):
        im=Image.new('RGB',(100,100),'black')
        with self.assertRaises(ValueError):anchor_metrics(im,im,(.1,.1,.12,.12))

class PreflightTests(unittest.TestCase):
    def test_hash_agrees(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'a.txt';p.write_text('abc')
            self.assertEqual(sha256_file(p),'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
    def test_missing_sources_reported_without_crashing(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'project.json'
            data=json.loads((ROOT/'examples/jeans-styling/project.json').read_text())
            data['scenes']=data['scenes'][:1]
            path.write_text(json.dumps(data))
            result=inspect_assets(path,Path(d)/'report')
            self.assertEqual(result['status'],'FAIL')
            self.assertGreater(len(result['errors']),0)
    def test_real_demo_images(self):
        with tempfile.TemporaryDirectory() as d:
            demo=create_demo(Path(d)/'demo').parent/'project.json'
            result=inspect_assets(demo,Path(d)/'report')
            self.assertFalse(result['errors'])
            self.assertTrue((Path(d)/'report/preflight.json').exists())
    def test_source_rights_are_not_auto_approved(self):
        with tempfile.TemporaryDirectory() as d:
            demo=create_demo(Path(d)/'demo').parent/'project.json'
            report=inspect_assets(demo,Path(d))
            self.assertTrue(any('rights declaration' in s for s in report['warnings']))

class WordSyncTests(unittest.TestCase):
    def test_words_normalized(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'w.json';file.write_text('[{"text":"Hello","start":0.05,"end":0.22}]')
            self.assertEqual(len(load_words(file)),1)
    def test_invalid_timing(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'w.json';file.write_text('[{"text":"x","start":0.4,"end":0.3}]')
            with self.assertRaises(ValueError):load_words(file)
    def test_timing_map(self):
        with tempfile.TemporaryDirectory() as d:
            wd=Path(d);words=wd/'words.json'
            words.write_text(json.dumps({'words':[{'text':'Look','start':0.1,'end':0.3},{'text':'good','start':0.4,'end':0.9}]}))
            report=make_sync_map(ROOT/'examples/jeans-styling/project.json',words,wd/'result')
            self.assertEqual(report['segments'][0]['word_count'],2)
            self.assertTrue((wd/'result/word_sync.csv').exists())
    def test_word_order_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'w.json';file.write_text('[{"text":"a","start":1,"end":2},{"text":"b","start":0.2,"end":0.3}]')
            with self.assertRaises(ValueError):load_words(file)

class ProjectCollectionTests(unittest.TestCase):
    def test_all_examples_are_valid(self):
        folders=list((ROOT/'examples').glob('*/project.json'))
        self.assertGreaterEqual(len(folders),7)
        for p in folders:
            with self.subTest(name=p.parent.name):self.assertGreater(len(read_project(p)['scenes']),3)
    def test_private_study_ignored_by_git(self):
        ignore=(ROOT/'.gitignore').read_text()
        self.assertIn('private_reference_lab/',ignore)
    def test_original_material_manifest(self):
        mf=ROOT/'assets/original-material-studies/manifest.csv'
        self.assertTrue(mf.exists())
        self.assertEqual(len(mf.read_text().splitlines())-1,48)

if __name__=='__main__':unittest.main()
