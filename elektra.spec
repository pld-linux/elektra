# TODO: use system nickel (1.1.0, in src/plugins/ni), inih (r29, src/plugins/ini)
#
# Conditonal build:
%bcond_with	full		# "full" variant (libelektra-full with all plugins linked in)
%bcond_without	glib		# GLib/GObject/GSetttings (+ GI) bindings
%bcond_with	gsettings	# GSetttings module (experimental)
%bcond_without	java		# Java support: JNA binding and JNI plugin (needs Java 8)
%bcond_without	lua		# Lua (5.2) support: bindings and plugin
%bcond_without	python2		# Python 2 support: bindings and plugin
%bcond_without	python3		# Python 3 support: bindings and plugin
%bcond_without	qt		# Qt GUI
%bcond_without	ruby		# Ruby binding

Summary:	A key/value pair database to store software configurations
Summary(pl.UTF-8):	Baza kluczy/wartości do przechowywania konfiguracji oprogramowania
Name:		elektra
Version:	0.8.19
Release:	4
License:	BSD
Group:		Applications/System
Source0:	http://www.libelektra.org/ftp/elektra/releases/%{name}-%{version}.tar.gz
# Source0-md5:	6669e765c834e259fb7570f126b85d7e
Patch0:		%{name}-zsh.patch
Patch1:		%{name}-no-markdown.patch
Patch2:		%{name}-no-deb.patch
URL:		http://www.libelektra.org/
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
BuildRequires:	cmake >= 2.8.11
BuildRequires:	curl-devel
BuildRequires:	dbus-devel
BuildRequires:	doxygen
BuildRequires:	gettext-tools
%{?with_glib:BuildRequires:	glib2-devel >= 1:2.36}
%{?with_glib:BuildRequires:	gobject-introspection-devel >= 1.38}
# for binding
%{?with_java:BuildRequires:	java-jna}
%{?with_java:BuildRequires:	jdk >= 1.8}
# jawt for plugin
%{?with_java:BuildRequires:	jre-X11 >= 1.8}
BuildRequires:	libgcrypt-devel
BuildRequires:	libgit2-devel >= 0.24.1
%{?with_qt:BuildRequires:	libmarkdown-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-progs
%{?with_lua:BuildRequires:	lua52-devel >= 5.2}
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 1:2.7}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	ronn
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%{?with_ruby:BuildRequires:	ruby-devel}
BuildRequires:	swig >= 2
%if %{with python2} || %{with python3}
BuildRequires:	swig-python >= 2
%endif
%{?with_ruby:BuildRequires:	swig-ruby}
BuildRequires:	systemd-devel
BuildRequires:	tcl-devel
BuildRequires:	yajl-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mktemp
Obsoletes:	registry
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
Requires:	jre-X11 >= 1.8

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

%package plugin-python2
Summary:	Python 2 plugin for Elektra
Summary(pl.UTF-8):	Wtyczka Python 2 dla Elektry
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python-libs >= 1:2.7

%description plugin-python2
Python 2 plugin for Elektra. It allows to use plugins written in
Python 2.

%description plugin-python2 -l pl.UTF-8
Wtyczka 2 Python dla Elektry. Pozwala na używanie wtyczek napisanych w
Pythonie 2.

%package plugin-python3
Summary:	Python 3 plugin for Elektra
Summary(pl.UTF-8):	Wtyczka Python 3 dla Elektry
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	python3-libs >= 1:3.2

%description plugin-python3
Python 3 plugin for Elektra. It allows to use plugins written in
Python 3.

%description plugin-python3 -l pl.UTF-8
Wtyczka Python 3 dla Elektry. Pozwala na używanie wtyczek napisanych w
Pythonie 3.

%package -n bash-completion-elektra
Summary:	Bash completion for Elektra commands
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów dla poleceń z pakietu Elektra
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n bash-completion-elektra
Bash completion for Elektra kdb command.

%description -n bash-completion-elektra -l pl.UTF-8
Bashowe uzupełnianie parametrów dla polecenai kdb z pakietu Elektra.

%package -n zsh-completion-elektra
Summary:	ZSH completion for Elektra commands
Summary(pl.UTF-8):	Uzupełnianie parametrów dla poleceń z pakietu Elektra w powłoce ZSH
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n zsh-completion-elektra
ZSH completion for Elektra kdb command.

%description -n zsh-completion-elektra -l pl.UTF-8
Uzupełnianie parametrów dla polecenai kdb z pakietu Elektra w powłoce
ZSH.

%package libs
Summary:	Elektra Project libraries
Summary(pl.UTF-8):	Biblioteki projektu Elektra
Group:		Libraries
Obsoletes:	elektra-cpp < 0.8
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
Requires:	glib2 >= 1:2.36

%description glib
GLib/GObject binding for Elektra.

%description glib -l pl.UTF-8
Wiązanie GLib/GObject do Elektry.

%package glib-devel
Summary:	GLib/GObject binding for Elektra - development files
Summary(pl.UTF-8):	Wiązanie GLib/GObject do Elektry - pliki programistyczne
Group:		Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36

%description glib-devel
GLib/GObject binding for Elektra - development files.

%description glib-devel -l pl.UTF-8
Wiązanie GLib/GObject do Elektry - pliki programistyczne.

%package -n java-elektra
Summary:	Java binding for Elektra
Summary(pl.UTF-8):	Wiązanie języka Java dla Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	java-jna
Requires:	jre >= 1.8

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

%package -n lua-elektra-glib
Summary:	Lua/GI binding for Elektra
Summary(pl.UTF-8):	Wiązanie Lua/GI dla Elektry
Group:		Libraries
Requires:	%{name}-glib = %{version}-%{release}
Requires:	lua52-libs >= 5.2
#R: lua52-lgi ?

%description -n lua-elektra-glib
Lua/GI binding for Elektra. Note: this bindings is deprecated, it's
better to use SWIG (lua-elektra) binding.

%description -n lua-elektra-glib -l pl.UTF-8
Wiązanie Lua/GI dla Elektry. Uwaga: to wiązanie jest przestarzałe,
lepiej używać wiązania SWIG (lua-elektra).

%package -n python-elektra
Summary:	Python 2 binding for Elektra
Summary(pl.UTF-8):	Wiązanie Pythona 2 dla Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python-libs >= 1:2.7

%description -n python-elektra
Python 2 binding for Elektra.

%description -n python-elektra -l pl.UTF-8
Wiązanie Pythona 2 dla Elektry.

%package -n python3-elektra
Summary:	Python 3 binding for Elektra
Summary(pl.UTF-8):	Wiązanie Pythona 3 dla Elektry
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	python3-libs >= 1:3.2

%description -n python3-elektra
Python 3 binding for Elektra.

%description -n python3-elektra -l pl.UTF-8
Wiązanie Pythona 3 dla Elektry.

%package -n python3-elektra-glib
Summary:	Python 3 GI binding for Elektra
Summary(pl.UTF-8):	Wiązanie Pythona 3 GI dla Elektry
Group:		Libraries
Requires:	%{name}-glib = %{version}-%{release}
Requires:	python3-pygobject3 >= 3

%description -n python3-elektra-glib
Python 3 GI binding for Elektra. Note: this bindings is deprecated,
it's better to use SWIG (python*-elektra) binding.


%description -n python3-elektra-glib -l pl.UTF-8
Wiązanie Pythona 3 GI dla Elektry. Uwaga: to wiązanie jest
przestarzałe, lepiej używać wiązania SWIG (python*-elektra).

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
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
	-DBINDINGS="INTERCEPT;cpp%{?with_glib:;glib%{?with_gsettings:;gsettings}%{?with_lua:;gi_lua}%{?with_python3:;gi_python}}%{?with_java:;jna}%{?with_lua:;swig_lua}%{?with_python2:;swig_python2}%{?with_python3:;swig_python}%{?with_ruby:;swig_ruby}" \
	%{!?with_full:-DBUILD_FULL=OFF} \
	-DINSTALL_TESTING=FALSE \
	-DPLUGINS=ALL \
	-DTARGET_CMAKE_FOLDER=%{_datadir}/cmake/Modules \
	-DTOOLS="kdb;race%{?with_gen:;gen}%{?with_qt:;qt-gui}" \
	-DBUILD_STATIC=ON

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# unneeded compat symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libelektragetenv.so.0

install -D src/plugins/xmltool/xmlschema/elektra.xsd $RPM_BUILD_ROOT%{_datadir}/sgml/elektra/elektra.xsd

%if %{with python2}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean
%endif

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

# these don't belong to man3
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{README_md,doc_*_md,md_doc_*,md_src_*,md_scripts_README,src_libs_getenv_README_md}.3elektra
# internal, not part of API
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/doc.h.3elektra
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{array,backend,dl,doc,ease_keyname,elektra_{keyname,plugin,proposal},exportsymbols,functional,internal,kdbenum,log,markdownlinkconverter,meta,mount,nolog,owner,plugin_plugin,proposal_proposal,split,static,trie}.c.3elektra
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{benchmark_plugins,examples_backend}.cpp.3elektra
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/{internaldatastructs,std_hash_*_,trie,vheap,vstack}.3elektra

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	glib -p /sbin/ldconfig
%postun	glib -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,BIGPICTURE.md,DESIGN.md,GOALS.md,LICENSE.md,NEWS.md,SECURITY.md,WHY.md,todo}
# doc/standards installed-doc/scripts
%attr(755,root,root) %{_bindir}/kdb
%if %{with full}
%attr(755,root,root) %{_bindir}/kdb-full
%endif
%dir %{_libdir}/elektra
# R: augeas-libs libxml2
%attr(755,root,root) %{_libdir}/elektra/libelektra-augeas.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-base64.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-blockresolver.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-boolean.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-c.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-cachefilter.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-ccode.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-conditionals.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-constants.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-counter.so
# TODO: R: botan
#%attr(755,root,root) %{_libdir}/elektra/libelektra-crypto_botan.so
# R: libgcrypt
%attr(755,root,root) %{_libdir}/elektra/libelektra-crypto_gcrypt.so
# R: openssl
%attr(755,root,root) %{_libdir}/elektra/libelektra-crypto_openssl.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-csvstorage.so
# R: curl-libs
%attr(755,root,root) %{_libdir}/elektra/libelektra-curlget.so
# R: dbus
%attr(755,root,root) %{_libdir}/elektra/libelektra-dbus.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-desktop.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-doc.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-dpkg.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-dump.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-enum.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-error.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-fcrypt.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-filecheck.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-fstab.so
# R: libgit2 >= 0.24.1
%attr(755,root,root) %{_libdir}/elektra/libelektra-gitresolver.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-glob.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hexcode.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hidden.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hosts.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-iconv.so
# uses internal inih library
%attr(755,root,root) %{_libdir}/elektra/libelektra-ini.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-iterate.so
# R: systemd-libs
%attr(755,root,root) %{_libdir}/elektra/libelektra-journald.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-keytometa.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-line.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-lineendings.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-list.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-logchange.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-mathcheck.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-mozprefs.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-network.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-noresolver.so
# uses internal nickel library
%attr(755,root,root) %{_libdir}/elektra/libelektra-ni.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-null.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-passwd.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-path.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-profile.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-regexstore.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-rename.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-resolver.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-resolver_fm_*.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-required.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-semlock.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-shell.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-simplespeclang.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-simpleini.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-spec.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-storage.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-struct.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-sync.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-syslog.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-tcl.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-template.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-timeofday.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-tracer.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-type.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-uname.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-validation.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-wresolver.so
# R: libxml2
%attr(755,root,root) %{_libdir}/elektra/libelektra-xmltool.so
# R: yajl
%attr(755,root,root) %{_libdir}/elektra/libelektra-yajl.so
%dir %{_libdir}/elektra/tool_exec
%attr(755,root,root) %{_libdir}/elektra/tool_exec/benchmark-createtree
%attr(755,root,root) %{_libdir}/elektra/tool_exec/configure-firefox
%attr(755,root,root) %{_libdir}/elektra/tool_exec/convert-fstab
%attr(755,root,root) %{_libdir}/elektra/tool_exec/convert-hosts
%attr(755,root,root) %{_libdir}/elektra/tool_exec/convert-inittab
%attr(755,root,root) %{_libdir}/elektra/tool_exec/convert-users
%attr(755,root,root) %{_libdir}/elektra/tool_exec/elektra-merge
%attr(755,root,root) %{_libdir}/elektra/tool_exec/elektra-mount
%attr(755,root,root) %{_libdir}/elektra/tool_exec/elektra-umount
%attr(755,root,root) %{_libdir}/elektra/tool_exec/elektrify-open
%attr(755,root,root) %{_libdir}/elektra/tool_exec/elektrify-getenv
%attr(755,root,root) %{_libdir}/elektra/tool_exec/example-xorg
%dir %{_libdir}/elektra/tool_exec/ffconfig
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/setupConfig
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/setupHomepage
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/setupProxy
%attr(755,root,root) %{_libdir}/elektra/tool_exec/ffconfig/writeConfigFiles
%attr(755,root,root) %{_libdir}/elektra/tool_exec/find-tools
%attr(755,root,root) %{_libdir}/elektra/tool_exec/getenv
%attr(755,root,root) %{_libdir}/elektra/tool_exec/install-sh-completion
%attr(755,root,root) %{_libdir}/elektra/tool_exec/list-tools
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-augeas
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-info
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-kde
%attr(755,root,root) %{_libdir}/elektra/tool_exec/mount-openicc
%attr(755,root,root) %{_libdir}/elektra/tool_exec/race
%attr(755,root,root) %{_libdir}/elektra/tool_exec/umount-all
%attr(755,root,root) %{_libdir}/elektra/tool_exec/upgrade-bootstrap
%{_datadir}/sgml/elektra
%{_mandir}/man1/kdb.1*
%{_mandir}/man1/kdb-check.1*
%{_mandir}/man1/kdb-convert.1*
%{_mandir}/man1/kdb-cp.1*
%{_mandir}/man1/kdb-editor.1*
%{_mandir}/man1/kdb-elektrify-getenv.1*
%{_mandir}/man1/kdb-export.1*
%{_mandir}/man1/kdb-file.1*
%{_mandir}/man1/kdb-find-tools.1*
%{_mandir}/man1/kdb-fstab.1*
%{_mandir}/man1/kdb-get.1*
%{_mandir}/man1/kdb-getmeta.1*
%{_mandir}/man1/kdb-global-mount.1*
%{_mandir}/man1/kdb-help.1*
%{_mandir}/man1/kdb-import.1*
%{_mandir}/man1/kdb-info.1*
%{_mandir}/man1/kdb-introduction.1*
%{_mandir}/man1/kdb-list.1*
%{_mandir}/man1/kdb-list-tools.1*
%{_mandir}/man1/kdb-ls.1*
%{_mandir}/man1/kdb-lsmeta.1*
%{_mandir}/man1/kdb-merge.1*
%{_mandir}/man1/kdb-mount.1*
%{_mandir}/man1/kdb-mv.1*
%{_mandir}/man1/kdb-remount.1*
%{_mandir}/man1/kdb-rm.1*
%{_mandir}/man1/kdb-set.1*
%{_mandir}/man1/kdb-setmeta.1*
%{_mandir}/man1/kdb-sget.1*
%{_mandir}/man1/kdb-shell.1*
%{_mandir}/man1/kdb-spec-mount.1*
%{_mandir}/man1/kdb-test.1*
%{_mandir}/man1/kdb-umount.1*
%{_mandir}/man1/kdb-vset.1*
%{_mandir}/man7/elektra-*.7*

%if 0
%files gen ?
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/elektra/tool_exec/gen
%{py_sitescriptdir}/elektra_gen-%{version}-py*.egg-info
# FIXME: should be in elektra_gen subdir
%{py_sitescriptdir}/support
%{_datadir}/elektra/templates
%endif

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

%if %{with python2}
%files plugin-python2
%defattr(644,root,root,755)
# R: python-libs
%attr(755,root,root) %{_libdir}/elektra/libelektra-python2.so
%endif

%if %{with python3}
%files plugin-python3
%defattr(644,root,root,755)
# R: python3-libs
%attr(755,root,root) %{_libdir}/elektra/libelektra-python.so
%endif

%files -n bash-completion-elektra
%defattr(644,root,root,755)
%{bash_compdir}/kdb

%files -n zsh-completion-elektra
%defattr(644,root,root,755)
%{_datadir}/zsh/site-functions/_kdb

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelektra.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra.so.4
%attr(755,root,root) %{_libdir}/libelektra-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-core.so.4
%attr(755,root,root) %{_libdir}/libelektra-ease.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-ease.so.4
%attr(755,root,root) %{_libdir}/libelektra-kdb.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-kdb.so.4
%attr(755,root,root) %{_libdir}/libelektra-meta.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-meta.so.4
%attr(755,root,root) %{_libdir}/libelektra-plugin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-plugin.so.4
%attr(755,root,root) %{_libdir}/libelektra-proposal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-proposal.so.4
%attr(755,root,root) %{_libdir}/libelektraintercept-env.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektraintercept-env.so.0
%attr(755,root,root) %{_libdir}/libelektraintercept-fs.so
%attr(755,root,root) %{_libdir}/libelektratools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektratools.so.2
%if %{with full}
%attr(755,root,root) %{_libdir}/libelektra-full.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-full.so.4
%endif

%files devel
%defattr(644,root,root,755)
%doc doc/API.md installed-doc/elektra-api/html
%attr(755,root,root) %{_libdir}/libelektra.so
%attr(755,root,root) %{_libdir}/libelektra-core.so
%attr(755,root,root) %{_libdir}/libelektra-ease.so
%attr(755,root,root) %{_libdir}/libelektra-kdb.so
%attr(755,root,root) %{_libdir}/libelektra-meta.so
%attr(755,root,root) %{_libdir}/libelektra-plugin.so
%attr(755,root,root) %{_libdir}/libelektra-proposal.so
%attr(755,root,root) %{_libdir}/libelektragetenv.so
%attr(755,root,root) %{_libdir}/libelektraintercept-env.so
%attr(755,root,root) %{_libdir}/libelektraintercept.so
%attr(755,root,root) %{_libdir}/libelektratools.so
%if %{with full}
%attr(755,root,root) %{_libdir}/libelektra-full.so
%endif
%dir %{_includedir}/elektra
%{_includedir}/elektra/kdb*.h
%{_pkgconfigdir}/elektra.pc
%{_datadir}/cmake/Modules/ElektraConfig*.cmake
%{_datadir}/cmake/Modules/ElektraTargetsLibelektra*.cmake
%{_mandir}/man3/api.3elektra*
%{_mandir}/man3/deprecated.3elektra*
%{_mandir}/man3/kdb.3elektra*
%{_mandir}/man3/kdb.c.3elektra*
%{_mandir}/man3/kdb_*.3elektra*
%{_mandir}/man3/kdb*.h.3elektra*
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
%{_mandir}/man3/plugin.3elektra*
%{_mandir}/man3/proposal.3elektra*

%files static
%defattr(644,root,root,755)
%{_libdir}/libelektra-static.a
%{_libdir}/libelektratools-static.a

%files cpp-devel
%defattr(644,root,root,755)
%doc src/bindings/cpp/README.md
%{_includedir}/elektra/*.hpp
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
%attr(755,root,root) %{_libdir}/libgelektra-4.0.so
%if %{with gsettings}
%attr(755,root,root) %{_libdir}/gio/modules/libelektrasettings.so
%endif
%{_libdir}/girepository-1.0/GElektra-4.0.typelib

%files glib-devel
%defattr(644,root,root,755)
%{_datadir}/gir-1.0/GElektra-4.0.gir
%{_includedir}/elektra/gelektra-*.h
%{_pkgconfigdir}/gelektra-4.0.pc
%endif

%if %{with java}
%files -n java-elektra
%defattr(644,root,root,755)
%doc src/bindings/jna/README.md
%{_javadir}/libelektra-1.jar
%{_javadir}/libelektra.jar
%endif

%if %{with lua}
%files -n lua-elektra
%defattr(644,root,root,755)
%doc src/bindings/swig/lua/README.md
%attr(755,root,root) %{_libdir}/lua/5.2/kdb.so

%if %{with glib}
%files -n lua-elektra-glib
%defattr(644,root,root,755)
%doc src/bindings/gi/lua/README.md
%dir %{_datadir}/lua/5.2/lgi
%dir %{_datadir}/lua/5.2/lgi/override
%{_datadir}/lua/5.2/lgi/override/GElektra.lua
%endif
%endif

%if %{with python2}
%files -n python-elektra
%defattr(644,root,root,755)
%doc src/bindings/swig/python2/README.md
%attr(755,root,root) %{py_sitedir}/_kdb.so
%{py_sitedir}/kdb.py[co]
%endif

%if %{with python3}
%files -n python3-elektra
%defattr(644,root,root,755)
%doc src/bindings/swig/python/README.md
%attr(755,root,root) %{py3_sitedir}/_kdb.so
%{py3_sitedir}/kdb.py
%{py3_sitedir}/__pycache__/kdb.cpython-*.py[co]

%if %{with glib}
%files -n python3-elektra-glib
%defattr(644,root,root,755)
%doc src/bindings/gi/python/README.md
%{py3_sitedir}/gi/overrides/GElektra.py
%{py3_sitedir}/gi/overrides/__pycache__/GElektra.cpython-*.py[co]
%endif
%endif

%if %{with ruby}
%files -n ruby-elektra
%defattr(644,root,root,755)
%doc src/bindings/swig/ruby/README.md
%attr(755,root,root) %{ruby_vendorarchdir}/_kdb.so
%{ruby_vendorlibdir}/kdb.rb
%endif
