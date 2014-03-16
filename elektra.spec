# TODO: use system nickel (in src/plugins/ni)
#
# Conditonal build:
%bcond_with	full	# "full" variant (libelektra-full with all plugins linked in)
#
Summary:	A key/value pair database to store software configurations
Summary(pl.UTF-8):	Baza kluczy/wartości do przechowywania konfiguracji oprogramowania
Name:		elektra
Version:	0.8.5
Release:	1
License:	BSD
Group:		Applications/System
Source0:	http://www.libelektra.org/ftp/elektra/releases/%{name}-%{version}.tar.gz
# Source0-md5:	6fe4a48d70cefc04c04639e5d85a0ddc
Patch0:		%{name}-elektraenv.patch
URL:		http://www.libelektra.org/
BuildRequires:	cmake >= 2.6
BuildRequires:	dbus-devel
BuildRequires:	doxygen
BuildRequires:	gettext-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel}
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

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	%{!?with_full:-DBUILD_FULL=OFF} \
	-DPLUGINS=ALL \
	-DTARGET_CMAKE_FOLDER=%{_datadir}/cmake/Modules

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

echo 'RUN="no"' > $RPM_BUILD_ROOT/etc/sysconfig/elektra
install -D scripts/elektraenv.sh $RPM_BUILD_ROOT/etc/profile.d/elektraenv.sh
install -D src/plugins/xmltool/xmlschema/elektra.xsd $RPM_BUILD_ROOT%{_datadir}/sgml/elektra/elektra.xsd

# just tests
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/lib/elektra/tool_exec \
	$RPM_BUILD_ROOT%{_datadir}/elektra/test_data

# prepare docs
%{__rm} -rf installed-doc
install -d installed-doc
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-api installed-doc/elektra-api

# "static" variant (with libelektra-static and thus all plugins linked in);
# we don't need it
%{__rm} $RPM_BUILD_ROOT%{_bindir}/kdb-static

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,CHANGES,COPYING,DESIGN,GOALS,NEWS,README,SECURITY,SPECIFICATION,todo}
# doc/standards installed-doc/scripts
%attr(755,root,root) %{_bindir}/kdb
%if %{with full}
%attr(755,root,root) %{_bindir}/kdb-full
%endif
%dir %{_libdir}/elektra
%attr(755,root,root) %{_libdir}/elektra/libelektra-ccode.so
# R: dbus
%attr(755,root,root) %{_libdir}/elektra/libelektra-dbus.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-doc.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-dump.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-error.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-fstab.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-glob.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hexcode.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hidden.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-hosts.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-iconv.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-network.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-ni.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-null.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-path.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-resolver.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-simpleini.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-struct.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-success.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-syslog.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-tcl.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-template.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-timeofday.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-tracer.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-type.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-uname.so
%attr(755,root,root) %{_libdir}/elektra/libelektra-validation.so
# R: libxml2
%attr(755,root,root) %{_libdir}/elektra/libelektra-xmltool.so
# R: yajl
%attr(755,root,root) %{_libdir}/elektra/libelektra-yajl.so
%attr(755,root,root) /etc/profile.d/elektraenv.sh
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/elektra
%{_datadir}/sgml/elektra

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelektra.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra.so.4
%if %{with full}
%attr(755,root,root) %{_libdir}/libelektra-full.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-full.so.4
%endif

%files devel
%defattr(644,root,root,755)
%doc installed-doc/elektra-api/*
%attr(755,root,root) %{_libdir}/libelektra.so
%if %{with full}
%attr(755,root,root) %{_libdir}/libelektra-full.so
%endif
%dir %{_includedir}/elektra
%{_includedir}/elektra/*.h
%{_pkgconfigdir}/elektra.pc
%{_datadir}/cmake/Modules/FindElektra.cmake
%{_mandir}/man3/deprecated.3elektra*
%{_mandir}/man3/kdb*.3elektra*
%{_mandir}/man3/key*.3elektra*
%{_mandir}/man3/plugin.3elektra*

%files static
%defattr(644,root,root,755)
%{_libdir}/libelektra-static.a

%files cpp-devel
%defattr(644,root,root,755)
%{_includedir}/elektra/*.hpp
