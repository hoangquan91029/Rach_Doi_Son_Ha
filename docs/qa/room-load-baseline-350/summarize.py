import json,pathlib,statistics,hashlib
out=pathlib.Path(__file__).resolve().parent
r=json.loads((out/'receipt.json').read_text())
def q(a,p):return sorted(a)[min(len(a)-1,int((len(a)-1)*p))]
summary={'status':r['status'],'phases':[],'limitations':['Server and Playwright coordinator share process: CPU, memory and event-loop figures are combined.','Initial armies idle, no combat or dense army measurement.','Headless Chromium on one host, not WAN or external desktop evidence.','frameMs is sampled renderer execution cost, not RAF interval or FPS; sampling does not establish missed frame rate.','Sequential increasing load; older rooms run longer. Both maps are present beyond one-room phase.','Read-only diagnostics snapshot clones displayed state, contributing measurement overhead.']}
for p in r['phases']:
 f=[c['frameMs'] for s in p['samples'] for c in s['clients']];ping=[c['pingMs'] for s in p['samples'] for c in s['clients'] if c['pingMs'] is not None];reads=[s['readDurationMs'] for s in p['samples']]
 summary['phases'].append({'rooms':p['target'],'connections':sum(x['connections'] for x in p['before']),'livingEntities':sum(x['living'] for x in p['before']),'perRoomLiving':[x['living'] for x in p['before']],'seconds':p['elapsedMs']/1000,'tickRateMin':min(x['ticksPerSecond'] for x in p['tickRates']),'tickRateMax':max(x['ticksPerSecond'] for x in p['tickRates']),'tickAdvance':[x['ticks'] for x in p['tickRates']],'frameCostMs':{'samples':len(f),'median':statistics.median(f),'p95':q(f,.95),'max':max(f)},'pingMs':{'median':statistics.median(ping),'p95':q(ping,.95),'max':max(ping)},'visibilityStates':sorted({c['visibility'] for s in p['samples'] for c in s['clients']}),'diagnosticReadMs':{'median':statistics.median(reads),'max':max(reads)},'eventLoopDelayMs':p['eventLoopDelayMs'],'eventLoopUtilization':p['eventLoopUtilization']['utilization'],'rssMiB':p['memoryAfter']['rss']/1024**2,'cpuSeconds':sum(p['cpu'].values())/1e6})
summary.update({k:r.get(k) for k in ['errors','networkErrors','httpErrors','commands','cleanup','afterMenus','preservation','menuCleanupErrors']})
summary['responsePinsCount']=len(r['responsePins'])
summary['conclusion']='No concrete simulation bottleneck demonstrated within these idle baseline windows. Measurements do not close final room/dense/browser performance.'
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
