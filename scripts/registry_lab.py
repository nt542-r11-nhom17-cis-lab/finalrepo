#!/usr/bin/env python3
"""Offline registry policy model. Fixture roles/MFA are NOT real IdP or registry security."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from types import MappingProxyType

ROLES = MappingProxyType({'fixture-ci': 'uploader', 'fixture-reader': 'reader', 'fixture-admin': 'admin'})

class Registry:
    def __init__(self, root, public_key):
        self.root=Path(root)
        self.key=Path(public_key)
        self.events=[]
        self.head='0'*64

    def event(self, kind, detail):
        item={'index':len(self.events),'kind':kind,'detail':detail,'previous':self.head}
        self.head=hashlib.sha256(json.dumps(item,sort_keys=True).encode()).hexdigest()
        self.events.append({**item,'digest':self.head})

    def authorize(self, actor, mfa_claim, role=None):
        # Supplied claims are fixtures. No authentication server is implemented here.
        if actor not in ROLES or mfa_claim is not True:
            self.event('denied','missing fixture identity/MFA claim')
            raise PermissionError('Identity or MFA fixture missing')
        if role and ROLES[actor]!=role:
            self.event('denied','wrong fixture role')
            raise PermissionError('Wrong fixture role')

    def verify(self, artifact, signature):
        p=subprocess.run(['openssl','dgst','-sha256','-verify',str(self.key),'-signature',str(signature),str(artifact)],capture_output=True)
        if p.returncode:
            self.event('signature_rejected','invalid signature')
            raise ValueError('Invalid artifact signature')

    def upload(self, actor, mfa_claim, version, artifact, signature):
        self.authorize(actor,mfa_claim,'uploader')
        if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+',version):
            raise ValueError('Only numeric semantic versions allowed')
        target=self.root/version
        if target.exists():
            raise FileExistsError('Immutable version already exists')
        self.verify(artifact,signature)
        target.mkdir(mode=0o700)
        shutil.copyfile(artifact,target/'application.zip')
        shutil.copyfile(signature,target/'application.zip.sig')
        self.event('upload',version)

    def download(self, actor, mfa_claim, version):
        self.authorize(actor,mfa_claim)
        if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+',version):
            raise ValueError('Invalid version')
        target=self.root/version
        self.verify(target/'application.zip',target/'application.zip.sig')
        self.event('download',version)
        return (target/'application.zip').read_bytes()

    def configure(self, actor, mfa_claim, webhook):
        self.authorize(actor,mfa_claim,'admin')
        from urllib.parse import urlparse
        u=urlparse(webhook)
        if u.scheme!='https' or not u.hostname or u.username or u.password:
            raise ValueError('HTTPS webhook without embedded credentials required')
        self.event('configuration','validated HTTPS webhook metadata; no network request sent')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',default='reports/supply-chain')
    p.add_argument('--output',default='reports/registry-lab')
    args=p.parse_args()
    source=Path(args.input);out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    results=[]
    def reject(name,exception,fn):
        try:fn()
        except exception:results.append({'test':name,'result':'PASS','expectation':'operation rejected'})
        else:raise RuntimeError('Unsafe operation accepted: '+name)
    with tempfile.TemporaryDirectory(prefix='registry-fixture-') as temp:
        reg=Registry(Path(temp)/'storage',source/'lab-public-key.pem');reg.root.mkdir(mode=0o700)
        artifact=source/'application.zip';sig=source/'application.zip.sig'
        reject('anonymous upload',PermissionError,lambda:reg.upload(None,False,'1.0.0',artifact,sig))
        reject('reader upload',PermissionError,lambda:reg.upload('fixture-reader',True,'1.0.0',artifact,sig))
        reject('upload without MFA claim',PermissionError,lambda:reg.upload('fixture-ci',False,'1.0.0',artifact,sig))
        reject('version path traversal',ValueError,lambda:reg.upload('fixture-ci',True,'../../escape',artifact,sig))
        reg.upload('fixture-ci',True,'1.0.0',artifact,sig)
        reg.upload('fixture-ci',True,'1.0.1',artifact,sig)
        results.append({'test':'valid signed uploads, two immutable versions','result':'PASS'})
        reject('overwrite existing version',FileExistsError,lambda:reg.upload('fixture-ci',True,'1.0.0',artifact,sig))
        reject('anonymous download',PermissionError,lambda:reg.download(None,False,'1.0.0'))
        for version in ['1.0.0','1.0.1']:
            assert reg.download('fixture-reader',True,version)==artifact.read_bytes()
        results.append({'test':'all stored versions verified on read','result':'PASS'})
        altered=Path(temp)/'altered.zip';altered.write_bytes(artifact.read_bytes()+b'changed')
        reject('tampered upload',ValueError,lambda:reg.upload('fixture-ci',True,'1.0.2',altered,sig))
        (reg.root/'1.0.1/application.zip').write_bytes(b'corrupted')
        reject('tampered stored version download',ValueError,lambda:reg.download('fixture-reader',True,'1.0.1'))
        reject('reader configuration change',PermissionError,lambda:reg.configure('fixture-reader',True,'https://example.invalid/hook'))
        reject('unencrypted webhook configuration',ValueError,lambda:reg.configure('fixture-admin',True,'http://example.invalid/hook'))
        reg.configure('fixture-admin',True,'https://example.invalid/hook')
        results.append({'test':'admin HTTPS-only configuration and chained audit events','result':'PASS'})
        (out/'audit-events.json').write_text(json.dumps({'events':reg.events,'head':reg.head,'scope':'local in-memory chain; not externally anchored or immutable audit service'},indent=2)+'\n')
    report={'scope':'offline policy fixture, no real IdP, MFA, CA, package registry or production control',
            'tests':results,'real_world_compliance':'NOT_ASSESSED'}
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'scope':report['scope'],'tests':len(results),'result':'PASS'}))

if __name__=='__main__':main()
