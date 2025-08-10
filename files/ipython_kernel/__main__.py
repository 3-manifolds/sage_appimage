# sage_setup: distribution = sagemath-repl
from ipykernel.kernelapp import IPKernelApp
from sage.repl.ipython_kernel.kernel import SageKernel
from cocoserver import StaticServer
import sys
import os
# Figure out where the documentation lives
real_argv0 = os.path.realpath(sys.argv[0])
sage_local = real_argv0[:real_argv0.find('/lib')]
doc_dir = os.path.join(sage_local, 'share', 'documentation')
# Start a cocoserver for viewing the documentation.
docserver = StaticServer(doc_dir)
docserver.start()
# Monkey patch the Sage Jupyter kernel
SageKernel.docserver = docserver
# Launch the kernel server
IPKernelApp.launch_instance(kernel_class=SageKernel)
