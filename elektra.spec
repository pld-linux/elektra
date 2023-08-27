# TODO:
# - subpackage crypto modules? (-plugin-crypto_{botan,gcrypt,openssl} or so)
# - force maven to work without network, enable java_mvn
# - rest-backend (BR: cppcms boost >= 1.45 libjwt openssl)
# - rest-frontend, web (BR: npm)
# - use system nickel (1.1.0, in src/plugins/ni)
#
# Conditonal build:
%bcond_with	full		# "full" variant (libelektra-full with all plugins linked in)
%bcond_without	glib		# GLib/GObject/GSetttings (+ GI) bindings
%bcond_without	gsettings	# GSetttings module
%bcond_without	java		# Java support: JNA binding and JNI plugin (needs Java 8)
%bcond_with	java_mvn	# Java JNA binding (needs Java 8 and maven)
%bcond_without	lua		# Lua (5.2) support: bindings and plugin
%bcond_without	python3		# Python 3 support: bindings and plugin
%bcond_without	qt		# Qt GUI
%bcond_without	ruby		# Ruby binding and plugin

%if %{without glib}
%undefine	with_gsettings
%endif
%if %{without java}
%undefine	with_java_mvn
%endif
Summary:	A key/value pair database to store software configurations
Summary(pl.UTF-8):	Baza kluczy/wartości do przechowywania konfiguracji oprogramowania
Name:		elektra
Version:	0.9.14
Release:	1
License:	BSD
Group:		Applications/System
Source0:	https://www.libelektra.org/ftp/elektra/releases/%{name}-%{version}.tar.gz
# Source0-md5:	eb0f1d2e5d93bbae122999b5a27be343
Patch0:		%{name}-zsh.patch
Patch1:		%{name}-no-markdown.patch
Patch4:		%{name}-gpgme.patch
Patch5:		%{name}-jni.patch
Patch6:		%{name}-system-gtest.patch
Patch7:		libgit2-detect.patch
URL:		https://www.libelektra.org/
%if %{with qt}
BuildRequires:	Qt5Core-devel >= 5.3
BuildRequires:	Qt5Gui-devel >= 5.3
BuildRequires:	Qt5Qml-devel >= 5.3
BuildRequires:	Qt5Quick-devel >= 5.3
BuildRequires:	Qt5Svg-devel >= 5.3
BuildRequires:	Qt5Test-devel >= 5.3
BuildRequires:	Qt5Widgets-devel >= 5.3
%endif
BuildRequires:	augeas-devel >= 1.0
BuildRequires:	boost-devel
BuildRequires:	botan2-devel
BuildRequires:	cmake >= 3.0
BuildRequires:	curl-devel >= 7.28.0
BuildRequires:	dbus-devel
BuildRequires:	doxygen
BuildRequires:	gcc >= 6:4.8
BuildRequires:	gettext-tools
%{?with_glib:BuildRequires:	glib2-devel >= 1:2.36}
%{?with_gsettings:BuildRequires:	glib2-devel >= 1:2.42}
%{?with_glib:BuildRequires:	gobject-introspection-devel >= 1.38}
BuildRequires:	gpgme-devel >= 1.10
# for binding
%{?with_java_mvn:BuildRequires:	java-jna >= 4.5.0}
%{?with_java_mvn:BuildRequires:	java-junit >= 4.12}
%{?with_java:BuildRequires:	jdk >= 10}
# jawt for plugin
%{?with_java:BuildRequires:	jre-X11 >= 1.10}
BuildRequires:	libev-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libgit2-devel >= 0.24.1
%{?with_qt:BuildRequires:	libmarkdown-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libuv-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-progs
%{?with_lua:BuildRequires:	lua52-devel >= 5.2}
%{?with_java_mvn:BuildRequires:	maven}
%{?with_java_mvn:BuildRequires:	maven-plugin-compiler >= 3.6.0}
%{?with_java_mvn:BuildRequires:	maven-plugin-surefire >= 2.19.1}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	ronn
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	sed >= 4.0
BuildRequires:	swig >= 3
%if %{with python3}
BuildRequires:	swig-python >= 3
%endif
%{?with_ruby:BuildRequires:	swig-ruby >= 3.0.8}
BuildRequires:	systemd-devel
BuildRequires:	tcl-devel
BuildRequires:	xerces-c-devel >= 3.0.0
BuildRequires:	yajl-devel
BuildRequires:	yaml-cpp-devel >= 0.5
BuildRequires:	zeromq-devel >= 3.2
BuildRequires:	zlib-devel
BuildConflicts:	java-gnu-classpath
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mktemp
# plugins dependencies (move to individual plugin subpackage if created)
Requires:	augeas-libs >= 1.0
Requires:	curl-libs >= 7.28.0
Requires:	libgit2 >= 0.24.1
Requires:	yaml-cpp >= 0.5
Obsoletes:	elektra-gen < 0.9
Obsoletes:	registry < 0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Elektra Project provides a framework to store generic
configuration data in an hierarchical key-value pair database, instead
of a human-readable only text file.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

%description -l pl.UTF-8
Projekt Elektra dostarcza szkielet do przechowywania typowych danych
konfiguracyjnych w postaci klucz-wartość w hierarchicznej bazie
danych, zamiast w pliku tekstowym czytelnym tylko dla człowieka.

W ten sposób oprogramowanie może odczytywać/zapisywać konfigurację za
pomocą spójnego API. Dodatkowo aplikacje mogą być zorientowane w
konfiguracji innych aplikacji, ułatwiając ich integrację.

%package gui
Summary:	Qt based GUI for Elektra
Summary(pl.UTF-8):	Oparty na Qt graficzny interfejs do Elektry
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
Qt based GUI for Elektra.

%description gui -l pl.UTF-8
Oparty na Qt graficzny interfejs do Elektry.

%package plugin-jni
Summary:	Java JNI plugin for Elektra
Summary(pl.UTF-8):	Wtyczka Java JNI dla Elektry
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
# jawt
Requires:	jre-X11 >= 1.10

%description plugin-jni
Java JNI plugin for Elektra. It allows to use plugins written in Java.

%description plugin-jni -l pl.UTF-8
Wtyczka Java JNI dla Elektry. Pozwala na używanie wtyczek napisanych w
Javie.

%package plugin-lua
Summary:	Lua plugin for Elektra
Summary(pl.UTF-8):	Wtyczka Lua dla Elektry
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	lua52-libs >= 5.2

%description plugin-lua
Lua plugin for Elektra. It allows to use plugins written in Lua.

%description plugin-lua -l pl.UTF-8
Wtyczka Lua dla Elektry. Pozwala na używanie wtyczek napisanych w Lua.

%package plugin-python3
Summary:	Python 3 plugin for Elektra
Summary(pl.UTF-8):	Wtyczka Python 3 dla Elektry
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.2
Obsoletes:	elektra-plugin-python2 < 0.9

%description plugin-python3
Python 3 plugin for Elektra. It allows to use plugins written in
Python 3.

%description plugin-python3 -l pl.UTF-8
Wtyczka Python 3 dla Elektry. Pozwala na używanie wtyczek napisanych w
Pythonie 3.

%package plugin-ruby
Summary:	Ruby plugin for Elektra
Summary(pl.UTF-8):	Wtyczka Ruby dla Elektry
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ruby

%description plugin-ruby
Ruby plugin for Elektra. It allows to use plugins written in Ruby.

%description plugin-ruby -l pl.UTF-8
Wtyczka Ruby dla Elektry. Pozwala na używanie wtyczek napisanych w
języku Ruby.

%package -n bash-completion-elektra
Summary:	Bash completion for Elektra commands
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla poleceń z pakietu Elektra
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2
BuildArch:	noarch

%description -n bash-completion-elektra
Bash completion for Elektra kdb command.

%description -n bash-completion-elektra -l pl.UTF-8
Bashowe uzupełnianie parametrów dla polecenia kdb z pakietu Elektra.

%package -n fish-completion-elektra
Summary:	Fish completion for Elektra commands
Summary(pl.UTF-8):	Uzupełnianie parametrów w fish dla poleceń z pakietu Elektra
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	fish
BuildArch:	noarch

%description -n fish-completion-elektra
Fish completion for Elektra kdb command.

%description -n fish-completion-elektra -l pl.UTF-8
Uzupełnianie parametrów w fish dla polecenia kdb z pakietu Elektra.

%package -n zsh-completion-elektra
Summary:	ZSH completion for Elektra commands
Summary(pl.UTF-8):	Uzupełnianie parametrów dla poleceń z pakietu Elektra w powłoce ZSH
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-elektra
ZSH completion for Elektra kdb command.

%description -n zsh-completion-elektra -l pl.UTF-8
Uzupełnianie parametrów dla polecenia kdb z pakietu Elektra w powłoce
ZSH.

%package libs
Summary:	Elektra Project libraries
Summary(pl.UTF-8):	Biblioteki projektu Elektra
Group:		Libraries
Obsoletes:	elektra-cpp < 0.8
Obsoletes:	registry-libs < 0.4
Conflicts:	elektra < 0.7

%description libs
The Elektra Project provides a framework to store generic
configuration data in an hierarchical key-value pair database, instead
of a human-readable only text file.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

This package contains Elektra shared libraries.

%description libs -l pl.UTF-8
Projekt Elektra dostarcza szkielet do przechowywania typowych danych
konfiguracyjnych w postaci klucz-wartość w hierarchicznej bazie
danych, zamiast w pliku tekstowym czytelnym tylko dla człowieka.

W ten sposób oprogramowanie może odczytywać/zapisywać konfigurację za
pomocą spójnego API. Dodatkowo aplikacje mogą być zorientowane w
konfiguracji innych aplikacji, ułatwiając ich integrację.

Ten pakiet zawiera biblioteki współdzielone Elektry.

%package devel
Summary:	Include files and API documentation for Elektra Project
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja API projektu Elektra
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Obsoletes:	registry-devel < 0.4
Obsoletes:	registry-examples < 0.4

%description devel
This package contains the include files and API manual pages to use
the Elektra API in C.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe oraz strony podręcznika
systemowego opisującego sposób użycia API Elektry w C.

%package static
Summary:	Static libraries for Elektra Project
Summary(pl.UTF-8):	Statyczne biblioteki projektu Elektra
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libraries for Elektra Project.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczne biblioteki projektu Elektra.

%package cpp-devel
Summary:	Header files of C++ interface for Elektra library
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu C++ do biblioteki Elektra
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel
Obsoletes:	elektra-cpp-static < 0.8

%description cpp-devel
Header files of C++ interface for Elektra library.

%description cpp-devel -l pl.UTF-8
Pliki nagłówkowe interfejsu C++ do biblioteki Elektra.

%package glib
Summary:	GLib/GObject binding for Elektra
Summary(pl.UTF-8):	Wiązanie GLib/GObject do Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
%if %{with gsettings}
Requires:	glib2 >= 1:2.42
%else
Requires:	glib2 >= 1:2.36
%endif
Obsoletes:	lua-elektra-glib < 0.9
Obsoletes:	python3-elektra-glib < 0.9

%description glib
GLib/GObject binding for Elektra.

%description glib -l pl.UTF-8
Wiązanie GLib/GObject do Elektry.

%package glib-devel
Summary:	GLib/GObject binding for Elektra - development files
Summary(pl.UTF-8):	Wiązanie GLib/GObject do Elektry - pliki programistyczne
Group:		Libraries
Requires:	%{name}-devel = %{version}-%{release}
%if %{with gsettings}
Requires:	glib2-devel >= 1:2.42
%else
Requires:	glib2-devel >= 1:2.36
%endif

%description glib-devel
GLib/GObject binding for Elektra - development files.

%description glib-devel -l pl.UTF-8
Wiązanie GLib/GObject do Elektry - pliki programistyczne.

%package io-ev
Summary:	Elektra I/O binding using libev
Summary(pl.UTF-8):	Wiązanie we/wy Elektry wykorzystujące libev
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description io-ev
Elektra I/O binding using libev.

%description io-ev -l pl.UTF-8
Wiązanie we/wy Elektry wykorzystujące libev.

%package io-ev-devel
Summary:	Development files for Elektra I/O ev binding
Summary(pl.UTF-8):	Pliki programistyczne wiązania we/wy Elektry ev
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-io-ev = %{version}-%{release}
Requires:	libev-devel

%description io-ev-devel
Development files for Elektra I/O ev binding.

%description io-ev-devel -l pl.UTF-8
Pliki programistyczne wiązania we/wy Elektry ev.

%package io-glib
Summary:	Elektra I/O binding using GLib
Summary(pl.UTF-8):	Wiązanie we/wy Elektry wykorzystujące GLib
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description io-glib
Elektra I/O binding using GLib.

%description io-glib -l pl.UTF-8
Wiązanie we/wy Elektry wykorzystujące GLib.

%package io-glib-devel
Summary:	Development files for Elektra I/O GLib binding
Summary(pl.UTF-8):	Pliki programistyczne wiązania we/wy Elektry GLib
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-io-glib = %{version}-%{release}
Requires:	glib2-devel >= 2.0

%description io-glib-devel
Development files for Elektra I/O GLib binding.

%description io-glib-devel -l pl.UTF-8
Pliki programistyczne wiązania we/wy Elektry GLib.

%package io-uv
Summary:	Elektra I/O binding using uv
Summary(pl.UTF-8):	Wiązanie we/wy Elektry wykorzystujące uv
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description io-uv
Elektra I/O binding using uv.

%description io-uv -l pl.UTF-8
Wiązanie we/wy Elektry wykorzystujące uv.

%package io-uv-devel
Summary:	Development files for Elektra I/O uv binding
Summary(pl.UTF-8):	Pliki programistyczne wiązania we/wy Elektry uv
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	%{name}-io-uv = %{version}-%{release}
Requires:	libuv-devel

%description io-uv-devel
Development files for Elektra I/O uv binding.

%description io-uv-devel -l pl.UTF-8
Pliki programistyczne wiązania we/wy Elektry uv.

%package -n java-elektra
Summary:	Java binding for Elektra
Summary(pl.UTF-8):	Wiązanie języka Java dla Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	java-jna >= 4.5.0
Requires:	jre >= 1.10

%description -n java-elektra
Java binding for Elektra.

%description -n java-elektra -l pl.UTF-8
Wiązanie języka Java dla Elektry.

%package -n lua-elektra
Summary:	Lua binding for Elektra
Summary(pl.UTF-8):	Wiązanie języka Lua dla Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	lua52-libs >= 5.2

%description -n lua-elektra
Lua binding for Elektra.

%description -n lua-elektra -l pl.UTF-8
Wiązanie języka Lua dla Elektry.

%package -n python3-elektra
Summary:	Python 3 binding for Elektra
Summary(pl.UTF-8):	Wiązanie Pythona 3 dla Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python3-libs >= 1:3.2
Obsoletes:	python-elektra < 0.9

%description -n python3-elektra
Python 3 binding for Elektra.

%description -n python3-elektra -l pl.UTF-8
Wiązanie Pythona 3 dla Elektry.

%package -n ruby-elektra
Summary:	Ruby binding for Elektra
Summary(pl.UTF-8):	Wiązanie języka Ruby dla Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n ruby-elektra
Ruby binding for Elektra.

%description -n ruby-elektra -l pl.UTF-8
Wiązanie języka Ruby dla Elektry.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' $(grep -l '/usr/bin/env bash' -r scripts)
%{__sed} -i -e '1s,/usr/bin/env sh,/bin/sh,' scripts/check-env-dep scripts/kdb/mount-list-all-files
%{__sed} -i -e '1s,/usr/bin/env python,%{__python},' scripts/dev/update-infos-status
%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' scripts/kdb/find-tools

%{__rm} -r src/bindings/io/test
%{__rm} src/bindings/io/uv/testio_uv.c
%{__rm} src/bindings/io/glib/testio_glib.c

%build
install -d build
cd build
%cmake .. \
	-DBINDINGS="INTERCEPT;cpp;io_ev;io_uv%{?with_glib:;glib;io_glib}%{?with_gsettings:;gsettings}%{?with_java_mvn:;jna}%{?with_lua:;lua}%{?with_python3:;python}%{?with_ruby:;ruby}" \
	%{!?with_full:-DBUILD_FULL=OFF} \
	-DBUILD_TESTING=OFF \
	-DENABLE_TESTING=OFF \
	-DINSTALL_SYSTEM_FILES=ON \
	-DINSTALL_TESTING=OFF \
	-DPLUGINS=ALL \
	-DTARGET_CMAKE_FOLDER=%{_datadir}/cmake/Modules \
	-DTOOLS="kdb;race%{?with_gen:;pythongen}%{?with_qt:;qt-gui}" \
	-DBUILD_STATIC=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# unneeded compat symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libelektragetenv.so.0

install -D src/plugins/xmltool/xmlschema/elektra.xsd $RPM_BUILD_ROOT%{_datadir}/sgml/elektra/elektra.xsd

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

# "static" variant (with libelektra-static and thus all plugins linked in);
# we don't need it
%{__rm} $RPM_BUILD_ROOT%{_bindir}/kdb-static

# prepare docs
%{__rm} -rf installed-doc
install -d installed-doc
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-api installed-doc/elektra-api
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

# these don't belong to man3
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{CODING.md,README_md,doc_*_md,md_doc_*,md_src_*,scripts_README_md,src_libs{,_highlevel,_merge}_README_md,src_plugins_README_md}.3elektra
# internal or example, not part of API
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{DocBindingData,DocOperationData,SomeIoLibHandle}.3elektra
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/doc.h.3elektra
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{array,dl,doc,ease_keyname,elektra_{keyname,plugin},functional,internal,kdbenum,log,markdownlinkconverter,meta,nolog,plugin_plugin,static,testio_doc,testlib_notification,testlib_pluginprocess,try_compile_{dbus,zeromq}}.c.3elektra
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{benchmark_plugins,examples_backend}.cpp.3elektra
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/std_hash_*_.3elektra

%if %{without java_mvn}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/org_libelektra*.3elektra
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	glib -p /sbin/ldconfig
%postun	glib -p /sbin/ldconfig

%post	io-ev -p /sbin/ldconfig
%postun	io-ev -p /sbin/ldconfig

%post	io-glib -p /sbin/ldconfig
%postun	io-glib -p /sbin/ldconfig

%post	io-uv -p /sbin/ldconfig
%postun	io-uv -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md doc/{AUTHORS.md,BIGPICTURE.md,DESIGN.md,GOALS.md,SECURITY.md,WHY.md,todo} build/doc/NEWS.md
# doc/standards installed-doc/scripts
%attr(755,root,root) %{_bindir}/kdb
%if %{with full}
%attr(755,root,root) %{_bindir}/kdb-full
%endif
%dir %{_libdir}/elektra
# R: augeas-libs >= 1.0 libxml2
%attr(755,root,root) %{_libdir}/elektra/libelektra-augeas.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-backend.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-base64.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-blacklist.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-blockresolver.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-c.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-ccode.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-conditionals.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-constants.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-counter.so
# R: libstdc++
%attr(755,root,root) %{_libdir}/elektra/libelektra-cpptemplate.so
# R: libgcrypt
%attr(755,root,root) %{_libdir}/elektra/libelektra-crypto.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-csvstorage.so
# R: curl-libs >= 7.28.0
%attr(755,root,root) %{_libdir}/elektra/libelektra-curlget.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-date.so
# R: dbus
%attr(755,root,root) %{_libdir}/elektra/libelektra-dbus.so
# R: dbus
%attr(755,root,root) %{_libdir}/elektra/libelektra-dbusrecv.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-desktop.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-directoryvalue.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-doc.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-dpkg.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-dump.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-email.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-error.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-fcrypt.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-file.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-filecheck.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-fstab.so
# R: libgit2 >= 0.24.1
%attr(755,root,root) %{_libdir}/elektra/libelektra-gitresolver.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-glob.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-gopts.so
# R: gpgme
%attr(755,root,root) %{_libdir}/elektra/libelektra-gpgme.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hexcode.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hexnumber.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hosts.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-iconv.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-internalnotification.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-ipaddr.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-iterate.so
# R: systemd-libs
%attr(755,root,root) %{_libdir}/elektra/libelektra-journald.so
# R: libstdc++
%attr(755,root,root) %{_libdir}/elektra/libelektra-kconfig.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-keytometa.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-length.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-line.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-lineendings.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-logchange.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-macaddr.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-mathcheck.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-mini.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-missing.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-modules.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-mozprefs.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-multifile.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-network.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-noresolver.so
# uses internal nickel library
%attr(755,root,root) %{_libdir}/elektra/libelektra-ni.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-passwd.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-path.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-process.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-profile.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-quickdump.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-range.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-reference.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-rename.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-resolver.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-resolver_fm_*.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-rgbcolor.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-shell.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-simpleini.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-spec.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-specload.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-storage.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-sync.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-syslog.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-template.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-timeofday.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-toml.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-tracer.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-type.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-unit.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-uname.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-validation.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-version.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-wresolver.so
# R: xerces-c >= 3.0.0
%attr(755,root,root) %{_libdir}/elektra/libelektra-xerces.so
# R: glib xfconf
%attr(755,root,root) %{_libdir}/elektra/libelektra-xfconf.so
# R: libxml2
%attr(755,root,root) %{_libdir}/elektra/libelektra-xmltool.so
# R: yajl
%attr(755,root,root) %{_libdir}/elektra/libelektra-yajl.so
# R: yaml-cpp >= 0.5
%attr(755,root,root) %{_libdir}/elektra/libelektra-yamlcpp.so
# R: zeromq
%attr(755,root,root) %{_libdir}/elektra/libelektra-zeromqrecv.so
# R: zeromq
%attr(755,root,root) %{_libdir}/elektra/libelektra-zeromqsend.so
%dir %{_libdir}/elektra/tool_exec
%attr(755,root,root) %{_libdir}/elektra/tool_exec/backup
%attr(755,root,root) %{_libdir}/elektra/tool_exec/benchmark-createtree
%attr(755,root,root) %{_libdir}/elektra/tool_exec/change-resolver-symlink
%attr(755,root,root) %{_libdir}/elektra/tool_exec/change-storage-symlink
%attr(755,root,root) %{_libdir}/elektra/tool_exec/check-env-dep
%attr(755,root,root) %{_libdir}/elektra/tool_exec/cmerge-config-files
%attr(755,root,root) %{_libdir}/elektra/tool_exec/configure-firefox
%attr(755,root,root) %{_libdir}/elektra/tool_exec/elektrify-open
%attr(755,root,root) %{_libdir}/elektra/tool_exec/elektrify-getenv
%dir %{_libdir}/elektra/tool_exec/ffconfig
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/setupConfig
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/setupHomepage
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/setupProxy
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/writeConfigFiles
%attr(755,root,root) %{_libdir}/elektra/tool_exec/find-tools
%attr(755,root,root) %{_libdir}/elektra/tool_exec/getenv
%attr(755,root,root) %{_libdir}/elektra/tool_exec/install-config-file
%attr(755,root,root) %{_libdir}/elektra/tool_exec/install-sh-completion
%attr(755,root,root) %{_libdir}/elektra/tool_exec/list-tools
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-augeas
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-info
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-list-all-files
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-openicc
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mountpoint-info
%attr(755,root,root) %{_libdir}/elektra/tool_exec/process-testapp.sh
%attr(755,root,root) %{_libdir}/elektra/tool_exec/race
%attr(755,root,root) %{_libdir}/elektra/tool_exec/reset
%attr(755,root,root) %{_libdir}/elektra/tool_exec/reset-elektra
%attr(755,root,root) %{_libdir}/elektra/tool_exec/restore
%attr(755,root,root) %{_libdir}/elektra/tool_exec/stash
%attr(755,root,root) %{_libdir}/elektra/tool_exec/umount-all
%attr(755,root,root) %{_libdir}/elektra/tool_exec/update-snippet-repository
%attr(755,root,root) %{_libdir}/elektra/tool_exec/upgrade-bootstrap
%{_datadir}/sgml/elektra
%{_mandir}/man1/kdb.1*
%{_mandir}/man1/kdb-backup.1*
%{_mandir}/man1/kdb-basename.1*
%{_mandir}/man1/kdb-cache.1*
%{_mandir}/man1/kdb-change-resolver-symlink.1*
%{_mandir}/man1/kdb-change-storage-symlink.1*
%{_mandir}/man1/kdb-check-env-dep.1*
%{_mandir}/man1/kdb-cmerge.1*
%{_mandir}/man1/kdb-complete.1*
%{_mandir}/man1/kdb-convert.1*
%{_mandir}/man1/kdb-cp.1*
%{_mandir}/man1/kdb-dirname.1*
%{_mandir}/man1/kdb-editor.1*
%{_mandir}/man1/kdb-elektrify-getenv.1*
%{_mandir}/man1/kdb-export.1*
%{_mandir}/man1/kdb-file.1*
%{_mandir}/man1/kdb-find.1*
%{_mandir}/man1/kdb-find-tools.1*
%{_mandir}/man1/kdb-gen.1*
%{_mandir}/man1/kdb-gen-highlevel.1*
%{_mandir}/man1/kdb-get.1*
%{_mandir}/man1/kdb-help.1*
%{_mandir}/man1/kdb-import.1*
%{_mandir}/man1/kdb-install-config-file.1*
%{_mandir}/man1/kdb-list-commands.1*
%{_mandir}/man1/kdb-list-tools.1*
%{_mandir}/man1/kdb-ls.1*
%{_mandir}/man1/kdb-merge.1*
%{_mandir}/man1/kdb-meta-get.1*
%{_mandir}/man1/kdb-meta-ls.1*
%{_mandir}/man1/kdb-meta-rm.1*
%{_mandir}/man1/kdb-meta-set.1*
%{_mandir}/man1/kdb-meta-show.1*
%{_mandir}/man1/kdb-mount.1*
%{_mandir}/man1/kdb-mount-java.1*
%{_mandir}/man1/kdb-mount-list-all-files.1*
%{_mandir}/man1/kdb-mountpoint-info.*
%{_mandir}/man1/kdb-mv.1*
%{_mandir}/man1/kdb-namespace.1*
%{_mandir}/man1/kdb-plugin-check.1*
%{_mandir}/man1/kdb-plugin-info.1*
%{_mandir}/man1/kdb-plugin-list.1*
%{_mandir}/man1/kdb-remount.1*
%{_mandir}/man1/kdb-reset.1*
%{_mandir}/man1/kdb-reset-elektra.1*
%{_mandir}/man1/kdb-restore.1*
%{_mandir}/man1/kdb-rm.1*
%{_mandir}/man1/kdb-set.1*
%{_mandir}/man1/kdb-sget.1*
%{_mandir}/man1/kdb-shell.1*
%{_mandir}/man1/kdb-spec-mount.1*
%{_mandir}/man1/kdb-stash.1*
%{_mandir}/man1/kdb-static.1*
%{_mandir}/man1/kdb-test.1*
%{_mandir}/man1/kdb-umount.1*
%{_mandir}/man1/kdb-umount-all.1*
%{_mandir}/man1/kdb-validate.1*
%{_mandir}/man7/elektra-*.7*

%files gui
%defattr(644,root,root,755)
%doc src/tools/qt-gui/README.md
%attr(755,root,root) %{_bindir}/elektra-qt-editor
%attr(755,root,root) %{_libdir}/elektra/tool_exec/qt-gui
%{_datadir}/appdata/org.libelektra.elektra-qt-editor.appdata.xml
%{_desktopdir}/org.libelektra.elektra-qt-editor.desktop
%{_iconsdir}/hicolor/scalable/apps/elektra-symbolic.svg
%{_iconsdir}/hicolor/scalable/apps/elektra.svg
%{_mandir}/man1/kdb-qt-gui.1*

%if %{with java}
%files plugin-jni
%defattr(644,root,root,755)
# R: jre with jawt
%attr(755,root,root) %{_libdir}/elektra/libelektra-jni.so
%endif

%if %{with lua}
%files plugin-lua
%defattr(644,root,root,755)
# R: lua52-libs
%attr(755,root,root) %{_libdir}/elektra/libelektra-lua.so
%endif

%if %{with python3}
%files plugin-python3
%defattr(644,root,root,755)
# R: python3-libs
%attr(755,root,root) %{_libdir}/elektra/libelektra-python.so
%endif

%if %{with ruby}
%files plugin-ruby
%defattr(644,root,root,755)
# R: ruby
%attr(755,root,root) %{_libdir}/elektra/libelektra-ruby.so
%endif

%files -n bash-completion-elektra
%defattr(644,root,root,755)
%{bash_compdir}/kdb

%files -n fish-completion-elektra
%defattr(644,root,root,755)
%{_datadir}/fish/vendor_completions.d/kdb.fish

%files -n zsh-completion-elektra
%defattr(644,root,root,755)
%{_datadir}/zsh/site-functions/_kdb

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelektra-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-core.so.5
%attr(755,root,root) %{_libdir}/libelektra-ease.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-ease.so.5
%attr(755,root,root) %{_libdir}/libelektra-globbing.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-globbing.so.5
%attr(755,root,root) %{_libdir}/libelektra-highlevel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-highlevel.so.5
%attr(755,root,root) %{_libdir}/libelektra-invoke.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-invoke.so.5
%attr(755,root,root) %{_libdir}/libelektra-io.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-io.so.5
%attr(755,root,root) %{_libdir}/libelektra-kdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-kdb.so.5
%attr(755,root,root) %{_libdir}/libelektra-merge.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-merge.so.5
%attr(755,root,root) %{_libdir}/libelektra-meta.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-meta.so.5
%attr(755,root,root) %{_libdir}/libelektra-notification.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-notification.so.5
%attr(755,root,root) %{_libdir}/libelektra-opts.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-opts.so.5
%attr(755,root,root) %{_libdir}/libelektra-plugin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-plugin.so.5
%attr(755,root,root) %{_libdir}/libelektra-pluginprocess.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-pluginprocess.so.5
%attr(755,root,root) %{_libdir}/libelektra-utility.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-utility.so.5
%attr(755,root,root) %{_libdir}/libelektraintercept-env.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektraintercept-env.so.0
%attr(755,root,root) %{_libdir}/libelektraintercept-fs.so
%attr(755,root,root) %{_libdir}/libelektratools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektratools.so.2
%if %{with full}
%attr(755,root,root) %{_libdir}/libelektra-full.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-full.so.5
%endif

%files devel
%defattr(644,root,root,755)
%doc doc/API.md installed-doc/elektra-api/html
%attr(755,root,root) %{_libdir}/libelektra-core.so
%attr(755,root,root) %{_libdir}/libelektra-ease.so
%attr(755,root,root) %{_libdir}/libelektra-globbing.so
%attr(755,root,root) %{_libdir}/libelektra-highlevel.so
%attr(755,root,root) %{_libdir}/libelektra-invoke.so
%attr(755,root,root) %{_libdir}/libelektra-io.so
%attr(755,root,root) %{_libdir}/libelektra-kdb.so
%attr(755,root,root) %{_libdir}/libelektra-meta.so
%attr(755,root,root) %{_libdir}/libelektra-merge.so
%attr(755,root,root) %{_libdir}/libelektra-notification.so
%attr(755,root,root) %{_libdir}/libelektra-opts.so
%attr(755,root,root) %{_libdir}/libelektra-plugin.so
%attr(755,root,root) %{_libdir}/libelektra-pluginprocess.so
%attr(755,root,root) %{_libdir}/libelektra-utility.so
%attr(755,root,root) %{_libdir}/libelektragetenv.so
%attr(755,root,root) %{_libdir}/libelektraintercept-env.so
%attr(755,root,root) %{_libdir}/libelektraintercept.so
%attr(755,root,root) %{_libdir}/libelektratools.so
%if %{with full}
%attr(755,root,root) %{_libdir}/libelektra-full.so
%endif
%dir %{_includedir}/elektra
%{_includedir}/elektra/elektra.h
%{_includedir}/elektra/elektra
%{_includedir}/elektra/kdb.h
%{_includedir}/elektra/kdbease.h
%{_includedir}/elektra/kdbendian.h
%{_includedir}/elektra/kdbextension.h
%{_includedir}/elektra/kdbgetenv.h
%{_includedir}/elektra/kdbglobbing.h
%{_includedir}/elektra/kdbgopts.h
%{_includedir}/elektra/kdbhelper.h
%{_includedir}/elektra/kdbinvoke.h
%{_includedir}/elektra/kdbio.h
%dir %{_includedir}/elektra/kdbio
%{_includedir}/elektra/kdbmacros.h
%{_includedir}/elektra/kdbmerge.h
%{_includedir}/elektra/kdbmeta.h
%{_includedir}/elektra/kdbmodule.h
%{_includedir}/elektra/kdbnotification.h
%{_includedir}/elektra/kdbopts.h
%{_includedir}/elektra/kdbos.h
%{_includedir}/elektra/kdbplugin.h
%{_includedir}/elektra/kdbpluginprocess.h
%{_includedir}/elektra/kdbprivate.h
%{_includedir}/elektra/kdbtypes.h
%{_includedir}/elektra/kdbutility.h
%{_includedir}/elektra/kdbversion.h
%{_pkgconfigdir}/elektra.pc
%{_pkgconfigdir}/elektra-codegen.pc
%{_pkgconfigdir}/elektra-highlevel.pc
%{_pkgconfigdir}/elektra-io.pc
%{_pkgconfigdir}/elektra-merge.pc
%{_pkgconfigdir}/elektra-notification.pc
%{_datadir}/cmake/Modules/ElektraConfig*.cmake
%{_datadir}/cmake/Modules/ElektraTargetsLibelektra*.cmake
# FIXME: x86_64 doxygen uses lower case, while the other use upper, needs investigation
%{_mandir}/man3/[Ii]nvoke.3elektra*
%{_mandir}/man3/Opmphm*.3elektra*
%{_mandir}/man3/backends.c.3elektra*
%{_mandir}/man3/contracts.c.3elektra*
%{_mandir}/man3/conversion.c.3elektra*
%{_mandir}/man3/conversion.h.3elektra*
%{_mandir}/man3/cow.c.3elektra*
%{_mandir}/man3/dbus.c.3elektra*
%{_mandir}/man3/dbus.h.3elektra*
%{_mandir}/man3/deprecated.3elektra*
%{_mandir}/man3/elektra.c.3elektra*
%{_mandir}/man3/elektra.h.3elektra*
%{_mandir}/man3/elektra_array_value.c.3elektra*
%{_mandir}/man3/elektra_error.c.3elektra*
%{_mandir}/man3/elektra_value.c.3elektra*
%{_mandir}/man3/error.h.3elektra*
%{_mandir}/man3/errors.c.3elektra*
%{_mandir}/man3/ev.h.3elektra*
%{_mandir}/man3/globbing.c.3elektra*
%{_mandir}/man3/highlevel.3elektra*
%{_mandir}/man3/hooks.c.3elektra*
%{_mandir}/man3/invoke.c.3elektra*
%{_mandir}/man3/io.c.3elektra*
%{_mandir}/man3/io_doc.c.3elektra*
%{_mandir}/man3/hash.c.3elektra*
%{_mandir}/man3/kdb.3elektra*
%{_mandir}/man3/kdb.c.3elektra*
%{_mandir}/man3/kdb_*.3elektra*
%{_mandir}/man3/kdb*.h.3elektra*
%{_mandir}/man3/kdbio.3elektra*
%{_mandir}/man3/kdbnotification.3elektra*
%{_mandir}/man3/key.3elektra*
%{_mandir}/man3/keymeta.3elektra*
%{_mandir}/man3/keyname.3elektra*
%{_mandir}/man3/keyset.3elektra*
%{_mandir}/man3/keytest.3elektra*
%{_mandir}/man3/keyvalue.3elektra*
%{_mandir}/man3/key.c.3elektra*
%{_mandir}/man3/keyhelpers.c.3elektra*
%{_mandir}/man3/keymeta.c.3elektra*
%{_mandir}/man3/keyset.c.3elektra*
%{_mandir}/man3/keytest.c.3elektra*
%{_mandir}/man3/keyvalue.c.3elektra*
%{_mandir}/man3/meta.3elektra*
%{_mandir}/man3/modules.3elektra*
%{_mandir}/man3/notification.c.3elektra*
%{_mandir}/man3/opmphm.c.3elektra*
%{_mandir}/man3/opmphmpredictor.c.3elektra*
%{_mandir}/man3/opts.c.3elektra*
%{_mandir}/man3/plugin.3elektra*
%{_mandir}/man3/pluginprocess.c.3elektra*
%{_mandir}/man3/proposal.c.3elektra*
%{_mandir}/man3/rand.c.3elektra*
%{_mandir}/man3/reference.c.3elektra*
%{_mandir}/man3/zeromq.c.3elektra*
%{_mandir}/man3/zeromq.h.3elektra*

%files static
%defattr(644,root,root,755)
%{_libdir}/libelektra-static.a
%{_libdir}/libelektratools-static.a

%files cpp-devel
%defattr(644,root,root,755)
%doc src/bindings/cpp/README.md
%{_includedir}/elektra/*.hpp
%{_includedir}/elektra/errors
%{_includedir}/elektra/helper
%{_includedir}/elektra/merging
# libelektratools API man pages
%{_mandir}/man3/automergeconfiguration.cpp.3elektra*
%{_mandir}/man3/automergeconfiguration.hpp.3elektra*
%{_mandir}/man3/automergestrategy.cpp.3elektra*
%{_mandir}/man3/automergestrategy.hpp.3elektra*
%{_mandir}/man3/backend.hpp.3elektra*
%{_mandir}/man3/backendbuilder.cpp.3elektra*
%{_mandir}/man3/backendbuilder.hpp.3elektra*
%{_mandir}/man3/backendparser.cpp.3elektra*
%{_mandir}/man3/backendparser.hpp.3elektra*
%{_mandir}/man3/backends.cpp.3elektra*
%{_mandir}/man3/backends.hpp.3elektra*
%{_mandir}/man3/comparison.cpp.3elektra*
%{_mandir}/man3/comparison.hpp.3elektra*
%{_mandir}/man3/importmergeconfiguration.cpp.3elektra*
%{_mandir}/man3/importmergeconfiguration.hpp.3elektra*
%{_mandir}/man3/interactivemergestrategy.cpp.3elektra*
%{_mandir}/man3/interactivemergestrategy.hpp.3elektra*
%{_mandir}/man3/kdb*.hpp.3elektra*
%{_mandir}/man3/key*.hpp.3elektra*
%{_mandir}/man3/keyhelper.cpp.3elektra*
%{_mandir}/man3/mergeconfiguration.hpp.3elektra*
%{_mandir}/man3/mergeconflict.hpp.3elektra*
%{_mandir}/man3/mergeconflictstrategy.cpp.3elektra*
%{_mandir}/man3/mergeconflictstrategy.hpp.3elektra*
%{_mandir}/man3/mergeresult.cpp.3elektra*
%{_mandir}/man3/mergeresult.hpp.3elektra*
%{_mandir}/man3/mergetask.hpp.3elektra*
%{_mandir}/man3/mergetestutils.cpp.3elektra*
%{_mandir}/man3/merging.cpp.3elektra*
%{_mandir}/man3/mergingkdb.cpp.3elektra*
%{_mandir}/man3/mergingkdb.hpp.3elektra*
%{_mandir}/man3/metamergestrategy.cpp.3elektra*
%{_mandir}/man3/metamergestrategy.hpp.3elektra*
%{_mandir}/man3/newkeystrategy.cpp.3elektra*
%{_mandir}/man3/newkeystrategy.hpp.3elektra*
%{_mandir}/man3/onesidemergeconfiguration.cpp.3elektra*
%{_mandir}/man3/onesidemergeconfiguration.hpp.3elektra*
%{_mandir}/man3/onesidestrategy.cpp.3elektra*
%{_mandir}/man3/onesidestrategy.hpp.3elektra*
%{_mandir}/man3/onesidevaluestrategy.cpp.3elektra*
%{_mandir}/man3/onesidevaluestrategy.hpp.3elektra*
%{_mandir}/man3/overwritemergeconfiguration.cpp.3elektra*
%{_mandir}/man3/overwritemergeconfiguration.hpp.3elektra*
%{_mandir}/man3/modules.cpp.3elektra*
%{_mandir}/man3/modules.hpp.3elektra*
%{_mandir}/man3/plugin.cpp.3elektra*
%{_mandir}/man3/plugin.hpp.3elektra*
%{_mandir}/man3/plugindatabase.cpp.3elektra*
%{_mandir}/man3/plugindatabase.hpp.3elektra*
%{_mandir}/man3/plugins.cpp.3elektra*
%{_mandir}/man3/plugins.hpp.3elektra*
%{_mandir}/man3/pluginspec.cpp.3elektra*
%{_mandir}/man3/pluginspec.hpp.3elektra*
%{_mandir}/man3/specreader.hpp.3elektra*
%{_mandir}/man3/src_backend.cpp.3elektra*
%{_mandir}/man3/testtool_*.cpp.3elektra*
%{_mandir}/man3/threewaymerge.cpp.3elektra*
%{_mandir}/man3/threewaymerge.hpp.3elektra*
%{_mandir}/man3/toolexcept.hpp.3elektra*

%if %{with glib}
%files glib
%defattr(644,root,root,755)
%doc src/bindings/glib/README.md
%attr(755,root,root) %{_libdir}/libgelektra-5.0.so
%if %{with gsettings}
%attr(755,root,root) %{_libdir}/gio/modules/libelektrasettings.so
%endif

%files glib-devel
%defattr(644,root,root,755)
%{_includedir}/elektra/gelektra-*.h
%{_pkgconfigdir}/gelektra-5.0.pc
%endif

%files io-glib
%defattr(644,root,root,755)
%doc src/bindings/io/glib/README.md
%attr(755,root,root) %{_libdir}/libelektra-io-glib.so

%files io-ev
%defattr(644,root,root,755)
%doc src/bindings/io/ev/README.md
%attr(755,root,root) %{_libdir}/libelektra-io-ev.so

%files io-ev-devel
%defattr(644,root,root,755)
%{_includedir}/elektra/kdbio/ev.h
%{_pkgconfigdir}/elektra-io-ev.pc

%files io-glib-devel
%defattr(644,root,root,755)
%{_includedir}/elektra/kdbio/glib.h
%{_pkgconfigdir}/elektra-io-glib.pc
%{_mandir}/man3/glib.h.3elektra*

%files io-uv
%defattr(644,root,root,755)
%doc src/bindings/io/uv/README.md
%attr(755,root,root) %{_libdir}/libelektra-io-uv.so

%files io-uv-devel
%defattr(644,root,root,755)
%{_includedir}/elektra/kdbio/uv.h
%{_pkgconfigdir}/elektra-io-uv.pc
%{_mandir}/man3/uv.h.3elektra*

%if %{with java_mvn}
%files -n java-elektra
%defattr(644,root,root,755)
%doc src/bindings/jna/README.md
%{_javadir}/libelektra-1.jar
%{_javadir}/libelektra.jar
%{_mandir}/man3/org_libelektra_*.3elektra*
%endif

%if %{with lua}
%files -n lua-elektra
%defattr(644,root,root,755)
%doc src/bindings/swig/lua/README.md
%attr(755,root,root) %{_libdir}/lua/5.2/kdb.so
%endif

%if %{with python3}
%files -n python3-elektra
%defattr(644,root,root,755)
%doc src/bindings/swig/python/README.md
%dir %{py3_sitedir}/kdb
%attr(755,root,root) %{py3_sitedir}/kdb/_kdb.so
%attr(755,root,root) %{py3_sitedir}/kdb/_merge.so
%attr(755,root,root) %{py3_sitedir}/kdb/_tools.so
%{py3_sitedir}/kdb/*.py
%{py3_sitedir}/kdb/__pycache__
%endif

%if %{with ruby}
%files -n ruby-elektra
%defattr(644,root,root,755)
%doc src/bindings/swig/ruby/README.md
%attr(755,root,root) %{ruby_vendorarchdir}/_kdb.so
%attr(755,root,root) %{ruby_vendorarchdir}/_kdbtools.so
%{ruby_vendorlibdir}/kdb.rb
%{ruby_vendorlibdir}/kdbtools.rb
%endif
