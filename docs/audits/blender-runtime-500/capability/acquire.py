import subprocess,pathlib,json,hashlib,re,urllib.request,tarfile,io,shutil
p=pathlib.Path('docs/audits/blender-runtime-500/capability'); a=json.loads((p/'assignment.json').read_text());root=pathlib.Path(a['externalInstallRoot'])
for i in a['inputs']:assert hashlib.sha256(pathlib.Path(i['path']).read_bytes()).hexdigest()==i['sha256']
assert root.exists(),'resume existing owned root'
indexes={}; signatures=[]
for suite in ['resolute','resolute-updates','resolute-security']:
 host='security.ubuntu.com' if suite.endswith('security') else 'archive.ubuntu.com'
 release=pathlib.Path(f'/var/lib/apt/lists/{host}_ubuntu_dists_{suite}_InRelease');v=subprocess.run(['gpgv','--keyring','/usr/share/keyrings/ubuntu-archive-keyring.gpg',str(release)],capture_output=True,text=True);signatures.append(v.stdout+v.stderr);assert v.returncode==0
 sha=release.read_text().split('SHA256:\n')[1].split('\nSHA512:')[0]
 for component in ['main','universe']:
  key=f'{component}/binary-amd64/Packages';expected=re.search(r'^ ([0-9a-f]{64}) +\d+ '+re.escape(key)+r'$',sha,re.M).group(1)
  f=f'/var/lib/apt/lists/{host}_ubuntu_dists_{suite}_{component}_binary-amd64_Packages'
  if not pathlib.Path(f).exists():continue
  data=subprocess.check_output(['/usr/lib/apt/apt-helper','cat-file',f]);assert hashlib.sha256(data).hexdigest()==expected
  for para in data.decode().split('\n\n'):
   d=dict(x.split(': ',1) for x in para.splitlines() if ': ' in x and not x.startswith(' '))
   if 'Package' in d:indexes[(d['Package'],d['Version'])]=d|{'publisherHost':host}
(p/'signature.log').write_text('\n'.join(signatures))
pairs=re.findall(r'^Inst (\S+) \((\S+) ',(p/'apt-simulation.log').read_text(),re.M);packages=[]
for name,version in pairs:
 d=indexes[(name,version)];packages.append({'name':name,'version':version,'size':int(d['Size']),'sha256':d['SHA256'],'url':'https://'+d['publisherHost']+'/ubuntu/'+d['Filename']})
total=sum(x['size'] for x in packages);assert total<800*1024**2;assert shutil.disk_usage(root.parent.parent).free>total*8
(p/'package-plan.json').write_text(json.dumps({'downloadBytes':total,'packages':packages,'signedIndexHashesVerified':True},indent=2)+'\n');print('estimate',len(packages),total,flush=True)
debdir=root/'debs';dest=root/'root'
for d in packages:
 f=debdir/d['url'].rsplit('/',1)[1];data=f.read_bytes() if f.exists() else urllib.request.urlopen(d['url'],timeout=60).read(d['size']+1);assert len(data)==d['size'];assert hashlib.sha256(data).hexdigest()==d['sha256'];f.write_bytes(data)
 tdata=subprocess.check_output(['dpkg-deb','--fsys-tarfile',str(f)])
 with tarfile.open(fileobj=io.BytesIO(tdata)) as t:
  for m in t.getmembers():
   path=pathlib.PurePosixPath(m.name);assert not path.is_absolute() and '..' not in path.parts
   if m.issym() or m.islnk():
    assert not pathlib.PurePosixPath(m.linkname).is_absolute()
    target=(dest/path.parent/m.linkname).resolve() if m.issym() else (dest/m.linkname).resolve()
    assert target.is_relative_to(dest.resolve()),(d['name'],m.name,m.linkname)
  t.extractall(dest,filter='data')
 print('extracted',d['name'],flush=True)
