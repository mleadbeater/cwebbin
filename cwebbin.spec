# 'make fullmanual' requires TeX (pdflatex).
# use '--without doc' to exclude this step; default is 'with'.
%bcond_without doc
# By default CWEB and CWEBBIN are compiled and linked with optimization
# switched on. Use '--with debuginfo' to switch debugging on.
%bcond_with debuginfo
# Apply only the set of ANSI changes.
%bcond_with ansi_only
# Prepare CWEBbin as base for TeXLive.
%bcond_with texlive

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
%define __msgfmt /usr/bin/msgfmt
%define __pax /bin/pax
%define __touch /usr/bin/touch
%endif
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Source0: ftp://ftp.cs.stanford.edu/pub/ctwill/ctwill.tar.gz
Source1: https://www.ctan.org/tex-archive/web/c_cpp/cweb/cweb-3.64c.tar.gz
Source2: %{name}-2018.tar.gz

Patch1: 0001-Update-CWEBbin-manpage.patch
Patch2: 0001-Make-clean-twinx.patch
Patch3: 0002-Make-clean-refsort.patch

%if %{with ansi_only}
Version: 3.64c
Release: ansi
%else
Version: 2018
Release: 16
%endif

%define texmf /opt/texlive/texmf-local

%global __make %{__make} -f Makefile.unix \\\
	-e PDFTEX=pdftex \\\
	-e TEXMFDIR=%{texmf} \\\
	%{!?with_texlive:-e CWEBINPUTS=%{_libdir}/cweb}

%description
The 'CWEBbin' package is an extension of the 'CWEB' package by Silvio Levy
and Donald Knuth for Literate Programming in C/C++.

%prep
%autosetup -c -a1 -a2

%if %{with texlive}
%{__sed} -e "s/# \(.*-texlive\)/\1/" -i Makefile.unix

%else

%{!?with_doc:%{__sed} -e "s/cweave fullmanual/cweave # fullmanual/" -i Makefile.unix}

%if ! %{with debuginfo}
%{__sed} -e "s/CFLAGS = -g/CFLAGS = -O/" -i Makefile.unix
%{__sed} -e "s/LINKFLAGS = -g/LINKFLAGS = -s/" -i Makefile.unix
%endif

%if %{with ansi_only}
%{__sed} -i Makefile.unix -e \
"/CHANGES):/{N;s/\(.*: [a-z.\/]*\)\( .*\)\? \(.*ansi[.ch]*\).*/\1 \3/}"
%{?with_doc:%{__sed} -e "s/cweave fullmanual/cweave docs/" -i Makefile.unix}
%{__sed} -i ctang-ansi.ch -e "/case not_eq/ s/@+/ /"
%{__sed} -i cweav-ansi.ch -e "0,/char \*b/ s/, where/,where/"
%endif

%endif

%build
%if %{with texlive}

%{__make} -e CCHANGES=comm-w2c.ch comm-w2c.ch
%{__make} -e HCHANGES=comm-w2c.h comm-w2c.h
%{__make} -e TCHANGES=ctang-w2c.ch ctang-w2c.ch
%{__make} -e WCHANGES=cweav-w2c.ch cweav-w2c.ch
%{__make} -e LCHANGES=ctwill-w2c.ch ctwill-w2c.ch

%{__make} prod-twill.w

for m in comm ctang cweav ctwill
do %{__sed} -e "1r texlive.w" -e "1d" -i $m-w2c.ch; done

# Use system CWEB, most likely from TeXLive
%{__make} -e CTANGLE=ctangle -e CCHANGES=comm-w2c.ch common.cxx
%{__make} -e CTANGLE=ctangle -e TCHANGES=ctang-w2c.ch ctangle.cxx

%{__msgfmt} po/de/cweb.po -o po/de/cweb.mo
%{__msgfmt} po/de/cweb-tl.po -o po/de/cweb-tl.mo
%{__msgfmt} po/de/web2c-help.po -o po/de/web2c-help.mo
%{__msgfmt} po/it/cweb.po -o po/it/cweb.mo

%else

%{__touch} *.cxx
%{__make} boot cautiously all

%endif

%install
%if %{with texlive}

%{__pax} *-w2c.ch comm-w2c.h prod-twill.w ctwimac.tex proofmac.tex \
	po cwebinputs texinputs refsort.w twinx.w \
	-wzf %{getenv:PWD}/cweb-texlive.tar.gz

%else

%{__rm} -rf %{buildroot}

%make_install

%{__install} -d %{buildroot}%{_datadir}/locale/de/LC_MESSAGES \
	%{buildroot}%{_datadir}/locale/it/LC_MESSAGES
%{__msgfmt} po/de/cweb.po -o %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/cweb.mo
%{__msgfmt} po/de/cweb-tl.po -o %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/cweb-tl.mo
%{__msgfmt} po/de/web2c-help.po -o %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/web2c-help.mo
%{__msgfmt} po/it/cweb.po -o %{buildroot}%{_datadir}/locale/it/LC_MESSAGES/cweb.mo

%endif

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_datadir}/emacs/site-lisp/cweb.el
%{_libdir}/cweb/*
%{_mandir}/man1/*
%{texmf}/tex/plain/cweb/*
%{_datadir}/locale/de/LC_MESSAGES/cweb.mo
%{_datadir}/locale/de/LC_MESSAGES/cweb-tl.mo
%{_datadir}/locale/de/LC_MESSAGES/web2c-help.mo
%{_datadir}/locale/it/LC_MESSAGES/cweb.mo

%post
%{__texhash}

%postun
%{__texhash}

%changelog
* Sun Dec 30 2018 Andreas Scherer <https://ascherer.github.io>
- Add CTWILL and its utiliy programs and macros

* Fri Nov 09 2018 Andreas Scherer <https://ascherer.github.io>
- Add internationalization (i18n)

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
