# TODO: PLDify init script
#
# Conditonal build:
%bcond_with	db	# BerkeleyDB backend [slightly outdated]
%bcond_with	gconf	# GConf backend [same as above]
%bcond_with	python	# Python binding [same as above]
#
Summary:	A key/value pair database to store software configurations
Summary(pl.UTF-8):	Baza kluczy/wartości do przechowywania konfiguracji oprogramowania
Name:		elektra
Version:	0.7.2
Release:	1
License:	BSD
Group:		Applications/System
Source0:	http://www.libelektra.org/ftp/elektra/releases/%{name}-%{version}.tar.gz
# Source0-md5:	29f14be7693ae627fb8cc30a079b10c9
Patch0:		%{name}-elektraenv.patch
Patch1:		%{name}-am.patch
URL:		http://www.libelektra.org/
%{?with_gconf:BuildRequires:	GConf2-devel}
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_db:BuildRequires:	db-devel}
BuildRequires:	doxygen
BuildRequires:	gettext-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libltdl-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
BuildRequires:	pkgconfig
%{?with_python:BuildRequires:	python-devel}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	mktemp
# for /usr/share/sgml dir
Requires:	sgml-common
Obsoletes:	registry
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_sbindir	/sbin

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

%package cpp
Summary:	C++ interface for Elektra library
Summary(pl.UTF-8):	Interfejs C++ do biblioteki Elektra
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description cpp
C++ interface for Elektra library.

%description cpp -l pl.UTF-8
Interfejs C++ do biblioteki Elektra.

%package cpp-devel
Summary:	Header files of C++ interface for Elektra library
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu C++ do biblioteki Elektra
Group:		Development/Libraries
Requires:	%{name}-cpp = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description cpp-devel
Header files of C++ interface for Elektra library.

%description cpp-devel -l pl.UTF-8
Pliki nagłówkowe interfejsu C++ do biblioteki Elektra.

%package cpp-static
Summary:	Static library of C++ interface for Elektra library
Summary(pl.UTF-8):	Biblioteka statyczna interfejsu C++ do biblioteki Elektra
Group:		Development/Libraries
Requires:	%{name}-cpp-devel = %{version}-%{release}

%description cpp-static
Static library of C++ interface for Elektra library.

%description cpp-static -l pl.UTF-8
Biblioteka statyczna interfejsu C++ do biblioteki Elektra.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/gettext/config.rpath .
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--libdir=/%{_lib} \
	--disable-ltdl-install \
	%{?with_db:--enable-berkeleydb} \
	%{?with_gconf:--enable-gconf} \
	--enable-passwd \
	%{?with_python:--enable-python}
# also outdated (as of 0.7.2): daemon, fstab
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	elektrainitdir=/etc/rc.d/init.d

%{!?with_berkeleydb:%{__rm} $RPM_BUILD_ROOT/%{_lib}/elektra/libelektra-ddefault.so}

# prepare docs
rm -rf installed-doc
install -d installed-doc
mv $RPM_BUILD_ROOT%{_docdir}/%{name}-devel installed-doc/elektra-api
mv $RPM_BUILD_ROOT%{_docdir}/%{name}/scripts installed-doc/scripts
rmdir $RPM_BUILD_ROOT%{_docdir}/%{name}

echo 'RUN="no"' > $RPM_BUILD_ROOT/etc/sysconfig/elektra

# move devel files to /usr
%{__mv} $RPM_BUILD_ROOT/%{_lib}/libelektra.a $RPM_BUILD_ROOT%{_libdir}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libelektra.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libelektra.so
%{__rm} $RPM_BUILD_ROOT/%{_lib}/libelektra.so

# dlopened modules
%{__rm} $RPM_BUILD_ROOT/%{_lib}/elektra/*.{la,a}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT/%{_lib}/lib*.la \
	$RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Create basic key structure for apps
kdb set -t dir system/sw || :
kdb set system/sw/kdb/schemapath "%{_datadir}/sgml/elektra-0.7.1/elektra.xsd"

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	cpp -p /sbin/ldconfig
%postun	cpp -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/standards installed-doc/scripts
%attr(755,root,root) /bin/kdb
%attr(755,root,root) /bin/kdb_static
%attr(755,root,root) /bin/preload
%attr(755,root,root) /bin/preload_static
%dir /%{_lib}/elektra
%attr(755,root,root) /%{_lib}/elektra/libelektra-default.so
%attr(755,root,root) /%{_lib}/elektra/libelektra-filesys.so*
%attr(755,root,root) /%{_lib}/elektra/libelektra-hosts.so*
%attr(755,root,root) /%{_lib}/elektra/libelektra-passwd.so*
%if %{with db}
%attr(755,root,root) /%{_lib}/elektra/libelektra-berkeleydb.so*
%attr(755,root,root) /%{_lib}/elektra/libelektra-ddefault.so
%endif
%if %{with gconf}
%attr(755,root,root) /%{_lib}/elektra/libelektra-gconf.so*
%endif
%attr(754,root,root) /etc/rc.d/init.d/kdbd
%attr(755,root,root) /etc/profile.d/elektraenv.sh
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/elektra
%{_datadir}/sgml/elektra-0.7.1
%{_mandir}/man1/kdb.1*
%{_mandir}/man5/elektra.5*
%{_mandir}/man7/elektra.7*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libelektra.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libelektra.so.3
%attr(755,root,root) %{_libdir}/libelektratools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektratools.so.2

%files devel
%defattr(644,root,root,755)
%doc installed-doc/elektra-api/*
%attr(755,root,root) %{_libdir}/libelektra.so
%attr(755,root,root) %{_libdir}/libelektratools.so
%{_includedir}/kdb*.h
%{_pkgconfigdir}/elektra.pc
%{_pkgconfigdir}/elektratools.pc
%{_mandir}/man3/kdb*.3*
%{_mandir}/man3/key*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libelektra.a
%{_libdir}/libelektratools.a

%files cpp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelektra-cpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libelektra-cpp.so.0

%files cpp-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libelektra-cpp.so
%{_includedir}/kdb
%{_includedir}/key
%{_includedir}/keyset
%{_pkgconfigdir}/elektracpp.pc

%files cpp-static
%defattr(644,root,root,755)
%{_libdir}/libelektra-cpp.a
