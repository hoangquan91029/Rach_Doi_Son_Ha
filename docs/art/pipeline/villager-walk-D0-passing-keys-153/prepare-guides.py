from pathlib import Path
import json,hashlib
p=Path(__file__).parent
base=Path('docs/art/pipeline/villager-walk-D0-clothed-guide-152/clothed-F04-guide.svg').read_text()
# Each output is a complete original vector drawing, no pixel/limb asset extraction.
legs={
'F02':'''<!-- FAR LEFT flexed swing passes beside the NEAR RIGHT stance. -->
<path d="M534 577Q580 595 598 667L624 728Q617 762 581 779L552 810L534 845Q508 851 492 830L511 790L552 737L533 695L493 625Z" fill="url(#brown)"/>
<path d="M495 823Q512 839 535 837L524 868Q505 879 486 861Z" fill="url(#cream)"/>
<path d="M493 854L520 861Q549 868 565 885Q568 897 551 899L514 890L482 877Z" fill="#b5865d"/>
<path d="M483 874L552 893L564 891Q564 903 549 905L511 896L480 885Z" fill="#6b4b30"/>
<path d="M496 860L526 890M510 864L543 891" stroke="#493626" stroke-width="8" fill="none"/>
<!-- NEAR RIGHT weight-bearing leg directly beneath its hip. -->
<path d="M463 579Q509 586 526 647L516 744L525 833Q508 864 479 851L466 771L453 701L423 617Z" fill="url(#brown)"/>
<path d="M478 836Q501 849 525 838L529 915Q509 930 483 919Z" fill="url(#cream)"/>
<path d="M485 910L521 908Q552 923 588 945Q596 958 578 966L523 967Q498 963 480 947Z" fill="#b5865d"/>
<path d="M480 944Q522 957 584 950L596 960Q592 973 573 977L523 977Q496 973 476 959Z" fill="#6b4b30"/>
<path d="M493 924L545 954M518 920L562 947" stroke="#493626" stroke-width="9" fill="none"/>
''',
'F06':'''<!-- FAR LEFT weight-bearing leg directly beneath its hip. -->
<path d="M534 577Q579 587 591 647L575 744L588 834Q570 864 541 850L525 768L508 699L493 625Z" fill="url(#brown)"/>
<path d="M541 836Q564 848 588 838L591 915Q573 930 548 919Z" fill="url(#cream)"/>
<path d="M548 910L584 908Q615 923 651 945Q659 958 641 966L586 967Q561 963 543 947Z" fill="#b5865d"/>
<path d="M543 944Q585 957 647 950L659 960Q655 973 636 977L586 977Q559 973 539 959Z" fill="#6b4b30"/>
<path d="M556 924L608 954M581 920L625 947" stroke="#493626" stroke-width="9" fill="none"/>
<!-- NEAR RIGHT flexed swing passes in front of far stance, raised sandal. -->
<path d="M463 579Q505 586 505 649L463 718Q451 740 468 758L512 790L536 825Q522 851 495 843L466 818L416 781Q393 754 408 721L423 617Z" fill="url(#brown)"/>
<path d="M497 822Q516 839 536 825L552 851Q546 875 524 873L502 852Z" fill="url(#cream)"/>
<path d="M528 857L548 850Q578 865 592 882Q593 897 577 899L544 887L516 874Z" fill="#b5865d"/>
<path d="M516 871L579 892L592 888Q595 901 579 906L542 895L514 882Z" fill="#6b4b30"/>
<path d="M534 860L558 889M547 862L575 891" stroke="#493626" stroke-width="8" fill="none"/>
'''}
for key in ['F02','F06']:
 out=base.replace('<g stroke=', '<g transform="translate(0 -74.4727272727) scale(1 1.08)" stroke=')
 start=out.index(' <!-- FAR/actor LEFT leg');end=out.index(' <!-- One whole tunic silhouette')
 out=out[:start]+legs[key]+out[end:]
 # Replace complete near-arm drawing with relaxed passing swing close to body.
 start=out.index(' <!-- NEAR arm swings');end=out.index(' <!-- Same ESE head')
 dx=-10 if key=='F02' else 10
 arm=f'''<!-- NEAR arm neutral passing swing, small anti-phase offset. -->
<path d="M407 330Q439 345 447 388L435 435L416 453L386 438L383 376Z" fill="url(#cream)"/>
<path d="M388 430L418 438L{425+dx} 491L{437+dx} 543Q{438+dx} 559 {423+dx} 561L{412+dx} 548L{408+dx} 519L386 473Z" fill="#b98a5c"/>
<path d="M384 423L420 435L414 457L383 445Z" fill="#ddd0b4"/>
'''
 out=out[:start]+arm+out[end:]
 out=out.replace('M580 318Q630 333 638 380L624 431L564 489Q548 501 535 489L545 470L579 413L576 367Z','M580 318Q630 333 638 380L632 434L625 490Q624 507 610 508L598 491L604 429L576 367Z')
 (p/f'{key}-clothed-guide.svg').write_text(out)
refs=['docs/art/pipeline/villager-walk-ESE-033/F00-raw.png','docs/art/pipeline/villager-walk-D0-clothed-guide-152/F04-raw.png']
(p/'work-order.json').write_text(json.dumps({'jobId':p.name,'status':'PREP_ONLY_ROOT_GUIDE_INTAKE_AND_NEW_DISPATCH_REQUIRED','model':'gpt-6.1-sol','reasoningEffort':'low','callsMade':0,'callOpen':False,'maxCalls':2,'retries':0,'slots':[{'frame':key,'primaryTarget':f'{key}-clothed-guide.png','status':'UNCALLED'} for key in ['F02','F06']],'secondaryReferences':[{'path':r,'sha256':hashlib.sha256(Path(r).read_bytes()).hexdigest(),'role':'selected contact identity/camera continuity ONLY, not passing pose target'} for r in refs],'canvas':[1254,1254],'pivot':[654,1140],'transform':'whole1254→128 uniform Lanczos, game89 wholecanvas; no fitting/shift/mirror','pose':{'F02':'nearRIGHT stance underbody; farLEFT flexed knee swing passes, raised sandal','F06':'farLEFT stance underbody; nearRIGHT flexed knee swing passes, raised sandal'},'laterGate':'No F1/F3/F5/F7/export/runtime/fanout until parent actual F2/F6 intake/new finite order','toolControl':'whole clothed PNG visual primary edit target; no guaranteed pose/pixel-lock control','note':'contact body proportions vary slightly; eventual actual whole loop look decides visible issues, no perframefit/footpolish'},indent=2)+'\n')
