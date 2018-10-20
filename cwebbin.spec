# 'make fullmanual' requires TeX (pdflatex).
# use '--without doc' to exclude this step; default is 'with'.
%bcond_without doc
# By default CWEB and CWEBBIN are compiled and linked with optimization
# switched on. Use '--with debuginfo' to switch debugging on.
%bcond_with debuginfo
# Apply only the set of ANSI changes.
%bcond_with ansi_only

Name: cwebbin
Summary: The CWEBbin extension of the CWEB package
License: Public Domain
URL: http://www-cs-faculty.stanford.edu/~uno/cweb.html
Packager: Andreas Scherer <https://ascherer.github.io>

%if %{_vendor} == "debbuild"
Group: tex
Distribution: Kubuntu 16.04 (x86_64)
Requires: texlive
%if %{with doc}
BuildRequires: texlive
%endif
%else
Group: Productivity/Publishing/TeX/Base
Distribution: openSUSE 42 (x86_64)
%global __touch /usr/bin/touch
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Source0: https://www.ctan.org/tex-archive/web/c_cpp/cweb/cweb-3.64c.tar.gz
%if %{with ansi_only}
Version: 3.64c
Release: ansi
Source1: %{name}-2018.tar.gz
%else
Version: 2018
Release: 12
Source1: %{name}-%{version}.tar.gz
%endif

Patch: 0001-Update-CWEBbin-manpage.patch

%define texmf /opt/texlive/texmf-local

%description
The 'CWEBbin' package is an extension of the 'CWEB' package by Silvio Levy
and Donald Knuth for Literate Programming in C/C++.

%prep
%autosetup -c -a1
%{!?with_doc:%{__sed} -e "s/wmerge fullmanual/wmerge # fullmanual/" -i Makefile.unix}
%if ! %{with debuginfo}
%{__sed} -e "s/CFLAGS = -g/CFLAGS = -O/" -i Makefile.unix
%{__sed} -e "s/LINKFLAGS = -g/LINKFLAGS = -s/" -i Makefile.unix
%endif
%if %{with ansi_only}
%{__sed} -i Makefile.unix -e \
"/CHANGES):/{N;s/\(.*: [a-z.\/]*\)\( .*\)\? \(.*ansi[.ch]*\).*/\1 \3/}"
%{?with_doc:%{__sed} -e "s/wmerge fullmanual/wmerge docs/" -i Makefile.unix}
%endif

%build
%{__touch} *.cxx
%{__ln_s} catalogs/%{?_l_}%{!?_l_:e}cweb.h cweb.h
%{__make} -f Makefile.unix -e PDFTEX=pdftex boot cautiously all

%install
%{__rm} -rf %{buildroot}
%make_install -f Makefile.unix -e TEXMFDIR=%{texmf} -e CWEBINPUTS=%{_libdir}/cweb

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/emacs/site-lisp/cweb.el
%{_libdir}/cweb/*
%{_mandir}/man1/*
%{texmf}/tex/plain/cweb/*

%post
%{__texhash}

%postun
%{__texhash}

%changelog
* Sun Feb 19 2017 Andreas Scherer <https://ascherer.github.io>
- Update for the 2017 sources

* Tue Mar 08 2016 Andreas Scherer <https://ascherer.github.io>
- Prepare release for CTAN/Web2c/TeX Live

* Tue Feb 23 2016 Andreas Scherer <https://ascherer.github.io>
- Update for the updated 2016 sources

* Sun Jan 31 2016 Andreas Scherer <https://ascherer.github.io>
- Update for the 2016 sources

* Sat Jan 09 2016 Andreas Scherer <https://ascherer.github.io>
- Conditional Build Stuff for non-TeX systems

* Thu Oct 29 2015 Andreas Scherer <andreas_tex@freenet.de> 22p-5
- Fully parametrized specfile

* Sat Aug 22 2015 Andreas Scherer <andreas_tex@freenet.de> 22p-4
- Put the TeX stuff into the correct 'local texmf tree'

* Sat Aug 15 2015 Andreas Scherer <andreas_tex@freenet.de> 22p-3
- Provide consistent information in URL and Source0

* Mon Jul 06 2015 Andreas Scherer <andreas_tex@freenet.de> 22p-2
- Use a simpler %prep section

* Thu Aug 18 2011 Andreas Scherer <andreas_tex@freenet.de> 22p-1
- Compile the package on Kubuntu 10.04

* Sat Apr 21 2007 Andreas Scherer <andreas_tug@freenet.de> p21-4
- Update for the 2006 sources

* Sun Dec 18 2005 Andreas Scherer <andreas_tug@freenet.de> p21-3
- Install (and hide) cwebmac.tex

* Fri Nov 04 2005 Andreas Scherer <andreas_tug@freenet.de> p21-2
- Build from two source archives (CWEBbin + cweb)

* Sat Oct 29 2005 Andreas Scherer <andreas_tug@freenet.de> p21-1
- Initial build
