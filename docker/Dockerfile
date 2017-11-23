# Dockerfile
FROM ubuntu:14.04

EXPOSE 80
RUN apt-get clean && apt-get update \
 && apt-get install -y wget

RUN echo "deb http://www.yade-dem.org/packages/ trusty/" >> /etc/apt/sources.list
RUN wget -O - http://www.yade-dem.org/packages/yadedev_pub.gpg |apt-key add -

RUN apt-get clean && apt-get update && apt-get install -y \
    build-essential \
    cmake \
    debhelper \
    devscripts \
    dpkg-dev \
    dvipng \
    fakeroot \
    freeglut3-dev \
    g++ \
    git \
    git-buildpackage \
    gnuplot \
    gtk2-engines-pixbuf \
    help2man \
    ipython \
    libboost-all-dev \
    libbz2-dev \
    libcgal-dev \
    libeigen3-dev \
    libgts-dev \
    libjs-jquery \
    libloki-dev \
    libmetis-dev \
    libopenblas-dev \
    libqglviewer-dev \
    libsqlite3-dev \
    libsuitesparse-dev \
    libvtk5-dev \
    libxi-dev \
    libxmu-dev \
    lmodern \
    pyqt4-dev-tools \
    python-all-dev \
    python-argparse \
    python-bibtex \
    python-dev \
    python-git \
    python-gts \
    python-imaging \
    python-matplotlib \
    python-minieigen \
    python-numpy \
    python-numpy \
    python-pygraphviz \
    python-qt4 \
    python-sphinx \
    python-tk \
    python-xlib \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-latex-recommended \
    texlive-pictures \
    texlive-xetex \
    tipa \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install yadedayly
RUN apt-get update && apt-get install -y yadedaily
# Add symbolic link to yadedaily
RUN mkdir /home/yade && mkdir /home/yade/YadePythonImport
RUN ln -s /usr/bin/yadedaily /home/yade/YadePythonImport/yadeimport.py
# COPY build-yade-package /usr/local/bin/