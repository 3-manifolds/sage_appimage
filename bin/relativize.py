import os
import sys
import subprocess

ELF_magic = b'\x7fELF'
# These libraries are deemed to be compatible by the manylinux2014
# specification in PEP 599.

ok_libs = [ 'libgcc_s.so.1', 'libstdc++.so.6', 'libm.so.6',
            'libdl.so.2', 'librt.so.1', 'libc.so.6', 'libnsl.so.1',
            'libutil.so.1', 'libpthread.so.0', 'libresolv.so.2', 'libX11.so.6',
            'libXext.so.6', 'libXrender.so.1', 'libICE.so.6', 'libSM.so.6',
            'libGL.so.1', 'libgobject-2.0.so.0', 'libgthread-2.0.so.0',
            'libglib-2.0.so.0' ]

symlink_lib = '/var/tmp/sage-10.7/local/lib' 

def is_ELF(filepath):
    if os.path.islink(filepath):
        return False
    with open(filepath, 'rb') as file_instance:
        magic = file_instance.read(4)
    return magic == ELF_magic

def relpath(start, end):
    # start is the path to an ELF binary;
    # end is a path to a library it loads.
    # The directory "local" is the common root of the entire tree,
    # but our paths start above "local"
    start_nodes = os.path.abspath(start).split(os.path.sep)
    end_nodes = os.path.abspath(end).split(os.path.sep)
    start_nodes = start_nodes[start_nodes.index('local'):]
    end_nodes = end_nodes[end_nodes.index('local'):]
    n = 0
    while start_nodes[n] == end_nodes[n]:
        n += 1
    up = [os.path.pardir] * (len(start_nodes) - n - 1)
    down = end_nodes[n:]
    return os.path.join('$ORIGIN', *(up + down[:-1]))

class ELFBinary:
    def __init__(self, filepath):
        assert is_ELF(filepath)
        self.filepath = os.path.abspath(filepath)
        self.origin, self.filename = os.path.split(self.filepath)
        result = subprocess.run(['patchelf', '--print-rpath', self.filepath],
                                capture_output=True, text=True)
        self.rpath = result.stdout.strip()
        self.abs_rpaths = [
            x.replace('$ORIGIN', self.origin) for x in self.rpath.split(':')]
        self.loadable_libs = []
        self.external_libs = []
        self.symlink_libs = []
        self.missing_libs = []
        self.illegal_libs = []
        result = subprocess.run(['ldd', self.filepath],
                                capture_output=True, text=True)
        for line in result.stdout.split('\n'):
           if line.find('not found') > 0:
               self.missing_libs.append(line)
           elif line.find('=>') > 0:
               lib = line.split('=>')[1].split()[0].strip()
               self.loadable_libs.append(lib)
        for lib in self.loadable_libs:
            libdir, libfile = os.path.split(lib)
            if libfile not in ok_libs:
                if libdir.startswith(symlink_lib):
                    self.symlink_libs.append(lib)
                elif lib.startswith('/usr') or lib.startswith('/lib') :
                    self.illegal_libs.append(lib)

def check_dir(dir):
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            path = os.path.abspath(os.path.join(dirpath, filename))
            if is_ELF(path):
                b = ELFBinary(path)
                for lib in b.illegal_libs:
                    print(path, 'uses illegal:', lib)
                for lib in b.missing_libs:
                    print('%s:'%path, lib)

def get_rpath(elfpath):
    """Inputs a path to an ELF binary; outputs a relative rpath which
    will find all libraries in /var/tmp/sage-X.Y which are needed.

    """
    abs_path = os.path.abspath(elfpath)
    b = ELFBinary(abs_path)
    rpaths = set()
    # The symlink_libs are the libraries /var/tmp/sage-X.Y/...
    for symlink_lib in b.symlink_libs:
        abs_symlink_libpath = os.path.abspath(symlink_lib)
        rpaths.add(relpath(abs_path, abs_symlink_libpath))
    return ':'.join(rpaths) 

def add_rpaths(dir):
    for dirpath, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            path = os.path.abspath(os.path.join(dirpath, filename))
            if is_ELF(path):
                rpath = get_rpath(path)
                if rpath:
                    result = subprocess.run(['patchelf', '--set-rpath', rpath, path])
                    if result.returncode:
                        print('Failed to set rpath for', path)
    
if __name__ == '__main__':
    check_dir(sys.argv[1])
#    add_rpaths(sys.argv[1])
