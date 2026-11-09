#!/usr/bin/env python3
"""Build six genuine editable Novaly content families; never references third-party faces."""
from __future__ import annotations
import json
from copy import deepcopy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
base=json.loads((ROOT/'examples/color-pair-looks/project.json').read_text())

FAMILIES={
'autumn-capsule':{
 'title':'Eight pieces that turn a small autumn capsule into many outfits',
 'series':'Autumn Capsule Foundations',
 'hooks':'The trick is repeating your base pieces while rotating one visible layer.',
 'rows':[
 ('Chocolate over oatmeal','Chocolate and oatmeal','#503B35','#DBCCB5','Chocolate soft cardigan, oatmeal high-rise tailored trousers, brown tote and loafers','Chocolate wool overshirt, oatmeal pleated trousers, dark loafers','present cardigan neckline'),
 ('Stone trench and navy','Stone and navy','#BDB1A0','#243852','Light stone trench over navy fine-knit top with navy straight trousers','Stone trench over navy poplin shirt and navy trousers','turn lapel gently'),
 ('Burgundy point of interest','Burgundy and beige','#713B47','#CCBDA8','Deep burgundy vest, oatmeal column skirt, brown belt and boots','Burgundy fine-knit sweater with tan chinos and dark brown shoes','indicate vest hem once'),
 ('Olive soft layer','Olive and cream','#5A664D','#ECE3D4','Olive utility jacket over cream tee and ivory wide trousers','Olive relaxed overshirt over cream polo with cream tailored trousers','one small cuff adjustment'),
 ('Charcoal and stone','Charcoal and stone','#45464B','#CDC9C1','Charcoal wool blazer, stone pleated trousers, simple black shoes','Charcoal suit jacket over stone knit and light grey trousers','stand almost still'),
 ('Camel over denim','Camel and indigo','#B98B62','#4E6484','Camel long wool layer, fitted white crew top, dark straight indigo jeans','Camel overshirt, indigo jeans, pale cotton shirt, suede shoes','show denim silhouette'),
 ('Forest and oat','Forest and oatmeal','#3D5446','#E4D5BF','Forest cardigan over oyster top and oatmeal trouser','Forest knit polo with oatmeal tailored trousers','relaxed palms down'),
 ('All-neutral finale','Ivory and cocoa','#EFE6D7','#58483E','Ivory textured jacket, cocoa trousers, dark suede bag and loafers','Ivory knitwear with dark cocoa trousers and tan loafers','finish with subtle nod')]
},
'office-casual':{
 'title':'Work outfits that feel polished without looking overdressed',
 'series':'Smart Casual Studio',
 'hooks':'One structured piece and one relaxed piece can balance the entire look.',
 'rows':[
 ('Blazer plus clean denim','Navy and mid-blue','#27394E','#50729A','Navy relaxed blazer, light shirt, straight mid-blue jeans, loafers','Navy overshirt, clean mid-blue jeans, white shirt','point to structured shoulder'),
 ('Knit with pleats','Oat and charcoal','#D6C8B0','#434750','Oat fitted knit top and charcoal tailored pleated trousers','Oat crew-neck knit and charcoal tapered pleated trousers','natural weight shift'),
 ('White shirt and cocoa','White and cocoa','#F4EFE8','#563E37','White oversized cotton shirt tucked into cocoa fluid trouser, simple belt','White Oxford shirt, brown tailored chino and dark loafer','brief cuff adjustment'),
 ('Soft pink with grey','Pink and slate','#CC9FAA','#737D89','Dusty rose fine-knit top and slate-grey straight trouser','Dusty pink shirt under grey relaxed jacket and grey trouser','small relaxed smile'),
 ('Olive with black','Olive and black','#526044','#24252B','Olive fitted top, tailored black wide trousers, low boots','Olive polo shirt with tailored black trousers and black shoes','hands rest at sides'),
 ('Blue over ecru','Powder blue and ecru','#A6C4D7','#EBE5D5','Powder-blue blazer over ecru shell with cream long trousers','Powder-blue shirt, ecru trousers, grey-brown loafers','open palm toward trousers'),
 ('Cream with burgundy','Cream and burgundy','#E8DFC9','#6C3442','Cream poplin shirt under burgundy knit vest with charcoal skirt','Cream Oxford under burgundy sweater with charcoal wool trousers','blink and slight head turn'),
 ('Monochrome charcoal','Charcoal and graphite','#3D424A','#6F727A','Charcoal sleeveless blazer and graphite tailored trousers','Charcoal open-collar shirt, graphite jacket and matching trousers','finish stable posture')]
},
'one-blazer-six-ways':{
 'title':'One navy blazer, six genuinely different styling formulas',
 'series':'One Piece, Six Ways',
 'hooks':'Keep the same navy blazer, and change only the proportions around it.',
 'rows':[
 ('White tee and denim','Navy and denim','#24364B','#547295','Same navy unstructured blazer over white cotton tee, straight mid-blue jeans and white sneakers','Same navy blazer over white tee, clean straight denim and dark low sneakers','indicate blazer front'),
 ('Soft trouser pairing','Navy and cream','#24364B','#ECE5D4','Same navy blazer over ivory crew top, cream tailored trousers and pointed beige flats','Same navy blazer over white knit and cream chinos with loafers','small one-hand presenting gesture'),
 ('Skirt and belt','Navy and stone','#24364B','#A5A69C','Same navy blazer over white fitted shell, stone column skirt and slim brown belt','Same navy blazer with stone straight trousers and crisp white shirt','very small cuff movement'),
 ('Dress layering','Navy and beige','#24364B','#D5BC97','Same navy blazer over beige midi knit dress, dark leather shoes','Same navy blazer over beige polo and dark tailored trousers','stand quietly, breathe'),
 ('Evening black','Navy and black','#24364B','#25272A','Same navy blazer over black satin blouse, black fluid trousers and neat heels','Same navy blazer over black open-collar shirt and black trousers','one subtle chin movement'),
 ('Color accent','Navy and burgundy','#24364B','#753948','Same navy blazer over burgundy fine-knit shell, cream tailored trouser','Same navy blazer over burgundy knit and cream pleated trousers','complete with faint nod')]
},
'denim-color-matching':{
 'title':'Choose top colors that make different denim washes feel intentional',
 'series':'Denim Color Match',
 'hooks':'Different denim washes respond to different shirt colors; watch the contrasts.',
 'rows':[
 ('Pale denim with espresso','Light denim and espresso','#8AB0CF','#4B302B','Pale straight jeans, espresso fitted cotton tee and tan handbag','Pale relaxed jeans, espresso polo and loafers','point briefly to jean fabric'),
 ('Pale denim with rust','Light denim and rust','#8AB0CF','#A74D33','Light blue jeans, rust sweater, simple ivory flats','Light blue relaxed jeans, rust sweater and dark sneakers','tiny head turn'),
 ('Mid-blue with ivory','Mid denim and ivory','#547BA1','#F1E8D8','Mid-blue wide-leg jeans with ivory slim crew top','Mid-blue straight jeans with ivory open-collar Oxford','indicate white top hem'),
 ('Mid-blue with forest','Mid denim and forest','#547BA1','#3C5B48','Mid-blue jeans with deep forest-green structured blouse','Mid-blue jeans with forest-green short-sleeve knit polo','natural small hand movement'),
 ('Dark indigo with cocoa','Indigo and cocoa','#2C4568','#634A41','Dark-indigo straight jeans with cocoa satin-look blouse','Dark-indigo denim with cocoa open-collar shirt and suede loafers','relax shoulders'),
 ('Dark indigo with oatmeal','Indigo and oat','#2C4568','#DACAB2','Dark-indigo jeans and oatmeal relaxed cashmere sweater','Dark-indigo jeans and oatmeal fine-gauge knit','brief half-smile'),
 ('Black denim with stone','Black denim and stone','#242424','#C0BAB1','Black fitted jeans with soft stone grey blazer and white shell','Black straight denim with stone knit and structured grey jacket','show jacket hem with open palm'),
 ('Black denim with burgundy','Black denim and burgundy','#242424','#703542','Black straight jeans with rich burgundy fine knit and black boots','Black denim with burgundy textured shirt and black loafers','small finishing nod')]
},
'weekend-travel-capsule':{
 'title':'A compact weekend wardrobe with seven reliable outfit combinations',
 'series':'Carry-on Wardrobe Planning',
 'hooks':'These seven combinations work from a small repeatable clothing capsule.',
 'rows':[
 ('Travel base','Navy and beige','#30405A','#CFBA9C','Navy crew tee, beige comfortable tailored trouser, white low-profile sneakers','Navy tee, beige relaxed chino and low-profile sneakers','small calm hand wave'),
 ('Daytime layers','Cream and dark denim','#E8DCCB','#344C70','Cream cardigan over white top and dark straight denim','Cream knit cardigan over white shirt and dark jeans','touch cardigan lapel'),
 ('Evening restaurant','Black and camel','#242326','#B69272','Black soft wrap top, camel trouser and structured small bag','Black open-collar linen shirt, camel tailored trouser and dark loafers','natural upright pose'),
 ('Light weather','Olive and stone','#5D6858','#C8C3B9','Olive utility shirt, stone trousers and ivory shoes','Olive utility overshirt, stone trousers and sneakers','gesture toward overshirt'),
 ('Cool morning','Burgundy and oatmeal','#713643','#D9CBB9','Burgundy soft knit sweater with oat trousers and loafers','Burgundy crew neck sweater and oat chinos','small head turn'),
 ('Casual stroll','Powder blue and white','#A8C6E2','#EEE7DE','Light blue shirt over white tee, straight dark denim, minimal sneakers','Light blue linen overshirt over white tee and denim','unbuttoned layer movement'),
 ('Return look','Chocolate and cream','#60463D','#E9E2D4','Chocolate cardigan, cream long trousers and comfortable slip-on flats','Chocolate polo sweater with cream chinos and suede loafers','final relaxed smile')]
}}

def slug(s):return ''.join(ch if ch.isalnum() else '_' for ch in s.lower()).strip('_')


def main():
    from sys import path as sys_path
    sys_path.insert(0,str(ROOT/'src'))
    from fashionreel.config import read_project
    from fashionreel.prompts import build_prompt_pack
    from fashionreel.storyboard import write_storyboard
    for family,desc in FAMILIES.items():
        p=deepcopy(base)
        p['project'].update(title=desc['title'],series=desc['series'])
        p['scenes']=[]
        for i,(title,label,c1,c2,woman,man,gesture) in enumerate(desc['rows'],1):
            p['scenes'].append({'id':f'{i:02}_{slug(title)}','title':title,'duration':3.25 if i==1 else 2.85,
               'asset':f"assets/{i:02}_{slug(title)}.mp4",'colors':[{'name':label.split(' and ')[0].lower(),'hex':c1},{'name':label.split(' and ')[-1].lower(),'hex':c2}],
               'woman_outfit':woman,'man_outfit':man,
               'action':f'Both models stand in fixed floor marks. Woman {gesture}; man makes one minimal natural reaction.',
               'rights':'original_or_permission_required'})
        folder=ROOT/'examples'/family;folder.mkdir(parents=True,exist_ok=True)
        (folder/'project.json').write_text(json.dumps(p,indent=2)+'\n')
        read_project(folder/'project.json')
        (folder/'voiceover.txt').write_text(desc['hooks']+'\n\n'+ '\n'.join(f"{s['title']}: {s['woman_outfit'].split(',')[0].lower()}, paired with a consistent, simple silhouette." for s in p['scenes'])+'\n\n(Voiceover is a starting draft only; edit for natural delivery and verify against audio length.)\n')
        build_prompt_pack(read_project(folder/'project.json'),folder/'prompts-generated')
        write_storyboard(read_project(folder/'project.json'),folder/'STORYBOARD.md')
        print('NEW',family,len(p['scenes']),'looks')

if __name__=='__main__':main()
