%bcond_with tests

# disable docs for now since doxygen 1.9.0 build issue
%bcond_with dox

# Not yet fully ready, wxQt is missing the
# wxPen::wxPen(const wxPenInfo&)
# constructor
%bcond_with qt

Name:		python-wxpython
Version:	4.2.3
Release:	1
Summary:	Python wrapper around wxWidgets
License:	wxWidgets and BSD
Group:		Development/Python
URL:		https://www.wxpython.org/
Source0:	https://files.pythonhosted.org/packages/source/w/wxPython/wxPython-%{version}.tar.gz
#Patch0:		sip5.patch
#Patch1:		sip6.patch
#Patch3:		unbundle-sip.patch
Patch5:		fix-build.patch
# (debian)
#Patch10:	fix-ftbfs-doxygen-197.patch
# (upstream) fix compatibility with Cython 3.0.0
#Patch100:	https://github.com/wxWidgets/Phoenix/commit/aeb557d01e7cd37176ebbf0f1ae6d0b53c115378.patch

BuildRequires:	locales-extra-charsets
BuildRequires:	doxygen
BuildRequires:	waf
%if %{with qt}
BuildRequires:	wxqt3.2-devel
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Widgets)
%else
BuildRequires:	wxgtk3.2-devel
BuildRequires:	pkgconfig(gtk+-3.0)
%endif

%{?python_provide:%python_provide python-wxpython4}
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(attrdict)
BuildRequires:	python%{pyver}dist(numpy)
# Available in unsupported, so disable for now.
#BuildRequires:	python%{pyver}dist(pathlib2)
BuildRequires:	python%{pyver}dist(pillow)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(six)
#BuildRequires:	python%{pyver}dist(sip)
BuildRequires:	python%{pyver}dist(requests)
Requires:		python%{pyver}dist(pillow)
Requires:		python%{pyver}dist(six)

# For tests
%if %{with tests}
BuildRequires:	locales-en
BuildRequires:	x11-server-xvfb
BuildRequires:	python%{pyver}dist(numpy)
# Available in Cooker but in unsupported repo. Disable for now.
#BuildRequires:	python%{pyver}dist(pypdf2)
BuildRequires:	python%{pyver}dist(pytest)
# Not imported yet
#BuildRequires:	python-pytest-timeout
#BuildRequires:	python-pytest-xdist
#BuildRequires:	python-wx-siplib
%endif

%rename python-wxpython4

%description
wxPython wraps the wxWidgets C++ toolkit and provides access to the user
interface portions of the wx API, enabling Python applications to have a
GUI on Windows, Macs or Unix systems with a native look and feel and
requiring very little (if any) platform specific code.

%files
%license license/*
%{python_sitearch}/*
%exclude %{python_sitearch}/wx/*html2*
%exclude %{python_sitearch}/wx/*media*

#---------------------------------------------------------------------------

%package media
Summary:	New implementation of wxPython, a GUI toolkit for Python (media module)
Group:		Development/Python
%{?python_provide:%python_provide python-wxpython4-media}
Requires:	%{name} = %{EVRD}
%rename python-wxpython4-media

%description media
wxPython wraps the wxWidgets C++ toolkit and provides access to the user
interface portions of the wx API, enabling Python applications to have a
GUI on Windows, Macs or Unix systems with a native look and feel and
requiring very little (if any) platform specific code.

This package provides the wx.media module.

%files media
%{python_sitearch}/wx/*media*

#---------------------------------------------------------------------------

%package webview
Summary:	New implementation of wxPython, a GUI toolkit for Python (webview module)
Group:		Development/Python
%{?python_provide:%python_provide python-wxpython4-webview}
Requires:	%{name} = %{EVRD}
%rename python-wxpython4-webview

%description webview
wxPython wraps the wxWidgets C++ toolkit and provides access to the user
interface portions of the wx API, enabling Python applications to have a
GUI on Windows, Macs or Unix systems with a native look and feel and
requiring very little (if any) platform specific code.

This package provides the wx.html2 module.

%files webview
%{python_sitearch}/wx/*html2*

#---------------------------------------------------------------------------

%package doc
Summary:	Documentation and samples for wxPython
Group:		Development/Python
BuildArch:	noarch

%description doc
Documentation, samples and demo application for wxPython.

%files doc
%doc docs demo samples
%license license/*

#----------------------------------------------

%prep
%autosetup -p1 -n wxPython-%{version}

#rm -rf sip/siplib
#rm -rf wx/py/tests
#rm -f docs/sphinx/_downloads/i18nwxapp/i18nwxapp.zip
#cp -a wx/lib/pubsub/LICENSE_BSD_Simple.txt license
# Remove env shebangs from various files
#sed -i -e '/^#!\//, 1d' demo/*.py{,w}
#sed -i -e '/^#!\//, 1d' demo/agw/*.py
#sed -i -e '/^#!\//, 1d' docs/sphinx/_downloads/i18nwxapp/*.py
#sed -i -e '/^#!\//, 1d' samples/floatcanvas/*.py
#sed -i -e '/^#!\//, 1d' samples/mainloop/*.py
#sed -i -e '/^#!\//, 1d' samples/ribbon/*.py
#sed -i -e '/^#!\//, 1d' wx/py/*.py
#sed -i -e '/^#!\//, 1d' wx/tools/*.py
# Fix end of line encodings
sed -i 's/\r$//' docs/sphinx/_downloads/*.py
sed -i 's/\r$//' docs/sphinx/rest_substitutions/snippets/python/contrib/*.py
sed -i 's/\r$//' docs/sphinx/rest_substitutions/snippets/python/converted/*.py
sed -i 's/\r$//' docs/sphinx/_downloads/i18nwxapp/locale/I18Nwxapp.pot
sed -i 's/\r$//' docs/sphinx/make.bat
sed -i 's/\r$//' samples/floatcanvas/BouncingBall.py
# Remove spurious executable perms
chmod -x demo/*.py
chmod -x samples/mainloop/mainloop.py
chmod -x samples/printing/sample-text.txt
# Remove empty files
find demo -size 0 -delete
find docs/sphinx/rest_substitutions/snippets/python/converted -size 0 -delete

%build
#Generate sip module code to replace bundled version 
#sip-module --abi-version 12.14 --sdist wx.siplib
#tar -xf wx_siplib-12.14.0.tar.gz
#mv wx_siplib-12.14.0 sip/siplib
#cp -p /usr/share/common-licenses/GPLv2 sip/siplib/LICENSE
#SIP=%{_bindir}/sip --nodoc sip
DOXYGEN=%{_bindir}/doxygen WAF=%{_bindir}/waf \
%{__python} -u build.py %{?with_dox:dox touch etg} build_py --use_syswx %{?with_qt:--qt}%{?!with_qt:--gtk3}

%install
%py_install
#{__python} build.py install_py --destdir=%{buildroot}
rm -f %{buildroot}%{_bindir}/*
# Remove locale files (they are provided by wxWidgets)
rm -rf %{buildroot}%{python_sitearch}/wx/locale

%check
%if %{with tests}
SKIP_TESTS="'not (display_Tests or glcanvas_Tests or mousemanager_Tests or numdlg_Tests or uiaction_MouseTests or uiaction_KeyboardTests or unichar_Tests or valtext_Tests or test_frameRestore or test_grid_pi)'"
ln -sf %{python_sitearch}/wx/siplib.so wx/siplib.so
xvfb-run -a %{__python} build.py test --pytest_timeout=60 --extra_pytest="-k $SKIP_TESTS" --verbose || true
%endif
