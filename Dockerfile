FROM quay.io/pypa/manylinux2014_x86_64
RUN yum install -y less.x86_64
RUN yum install -y zip.x86_64
RUN yum install -y perl-IPC-Cmd
RUN yum install -y perl-Time-Piece
RUN yum install -y bzip2-devel.x86_64
RUN yum install -y ncurses-devel.x86_64
RUN yum install -y libXft-devel.x86_64
RUN yum install -y libXfont2-devel.x86_64
RUN yum install -y xorg-x11-fonts-Type1.noarch
RUN yum install -y readline-devel.x86_64
RUN yum install -y openblas-devel.x86_64
RUN yum install -y gmp-devel.x86_64
RUN yum install -y libmpc-devel.x86_64
RUN yum install -y mpfr-devel.x86_64
RUN yum install -y xz-devel.x86_64
RUN yum install -y libffi-devel.x86_64
