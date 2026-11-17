"""Rebuild a pinned upstream source with reviewed module locks and a pinned Go SDK."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def file_hash(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def unpack(url, expected, archive, destination):
    if not archive.exists():
        with tempfile.NamedTemporaryFile(dir=archive.parent) as staged:
            with urllib.request.urlopen(url, timeout=90) as source:
                shutil.copyfileobj(source, staged)
            staged.flush()
            if file_hash(staged.name) != expected:
                raise ValueError('Build input download SHA256 mismatch')
            shutil.copyfile(staged.name, archive)
    if file_hash(archive) != expected:
        raise ValueError('Build input archive SHA256 mismatch')
    if not destination.exists():
        staging = Path(tempfile.mkdtemp(dir=archive.parent, prefix='extract-'))
        try:
            with tarfile.open(archive, 'r:gz') as tar:
                tar.extractall(staging, filter='data')
            staging.rename(destination)
        finally:
            shutil.rmtree(staging, ignore_errors=True)


def build_binary(lock, cache, binary):
    build = lock['build']
    work = cache.parent / 'cis-registry-build'
    work.mkdir(mode=0o700, exist_ok=True)
    if work.is_symlink() or work.stat().st_uid != os.getuid() or work.stat().st_mode & 0o077:
        raise ValueError('Build directory must be owned and private')
    unpack(build['sdk_url'], build['sdk_sha256'], work / 'sdk.tar.gz', work / 'sdk')
    unpack(build['source_url'], build['source_sha256'], work / 'source.tar.gz', work / 'source')
    roots = [p for p in (work / 'source').iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise ValueError('Unexpected upstream source root')
    source = roots[0]
    for name, expected in build['module_locks'].items():
        reviewed = ROOT / 'config/registry-source' / name
        if file_hash(reviewed) != expected:
            raise ValueError('Reviewed module lock SHA256 mismatch')
        shutil.copyfile(reviewed, source / name)
    go = work / 'sdk/go/bin/go'
    env = {'PATH': os.defpath, 'LANG': 'C.UTF-8', 'GOTOOLCHAIN': 'local',
           'GOOS': 'linux', 'GOARCH': 'amd64', 'GOAMD64': 'v1', 'CGO_ENABLED': '0',
           'GOMAXPROCS': '2', 'GOPROXY': 'https://proxy.golang.org', 'GOSUMDB': 'sum.golang.org',
           'GOCACHE': str(work / 'build-cache'), 'GOMODCACHE': str(work / 'modules'), 'GOPATH': str(work / 'gopath')}
    # Preserve only transport proxy/CA settings, not repository tokens/secrets.
    for name in ('HTTPS_PROXY', 'HTTP_PROXY', 'ALL_PROXY', 'NO_PROXY', 'SSL_CERT_FILE', 'SSL_CERT_DIR'):
        if name in os.environ:
            env[name] = os.environ[name]
    version = subprocess.check_output([str(go), 'version'], env=env, text=True)
    if version.split()[2] != build['go_version']:
        raise ValueError('Unexpected Go SDK version')
    flags = '-s -w -X github.com/distribution/distribution/v3/version.version=v' + lock['version']
    flags += ' -X github.com/distribution/distribution/v3/version.revision=' + build['source_commit']
    # Build logs are private; they are not exported with integration evidence.
    with (work / 'build.log').open('w') as log:
        subprocess.run([str(go), 'build', '-p=2', '-mod=readonly', '-trimpath', '-buildvcs=false',
                        '-ldflags=' + flags, '-o', str(binary), './cmd/registry'],
                       cwd=source, env=env, stdout=log, stderr=log, check=True, timeout=600)
        subprocess.run([str(go), 'mod', 'verify'], cwd=source, env=env,
                       stdout=log, stderr=log, check=True, timeout=120)
    binary.chmod(0o700)
    if file_hash(binary) != lock['binary_sha256']:
        raise ValueError('Rebuilt executable SHA256 differs from reviewed build')
    for name, expected in build['module_locks'].items():
        if file_hash(source / name) != expected:
            raise ValueError('Build changed reviewed module lock')
    return binary
