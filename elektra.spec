Summary:	A key/value pair database to store software configurations
Summary(pl):	Baza kluczy/warto¶ci do przechowywania konfiguracji oprogramowania
Name:		elektra
Version:	0.4.6
Release:	0.1
Epoch:		0
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/elektra/%{name}-%{version}.tar.gz
# Source0-md5:	f032ec83ffe91f2e7c2a0d70f67749eb
Patch0:		%{name}-Makefile_CFLAGS.patch
Patch1:		%{name}-libdir.patch
Patch2:		%{name}-not_implemented_func_hack.patch
Patch3:		%{name}-elektraenv.patch
URL:		http://elektra.sourceforge.net/
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-progs
Requires(post):	/sbin/ldconfig
Requires:	mktemp
# for /usr/share/sgml dir
Requires:	sgml-common
Obsoletes:	registry
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Elektra Project provides a framework to store generic
configuration data in an hierarchical key-value pair database, instead
of a human-readable only text file.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

%description -l pl
Projekt Elektra dostarcza szkielet do przechowywania typowych danych
konfiguracyjnych w postaci klucz-warto¶æ w hierarchicznej bazie
danych, zamiast w pliku tekstowym czytelnym tylko dla cz³owieka.

W ten sposób oprogramowanie mo¿e odczytywaæ/zapisywaæ konfiguracjê za
pomoc± spójnego API. Dodatkowo aplikacje mog± byæ zorientowane w
konfiguracji innych aplikacji, u³atwiaj±c ich integracjê.

%package devel
Summary:	Include files and API documentation for Elektra Project
Summary(pl):	Pliki nag³ówkowe i dokumentacja API projektu Elektra
Group:		Development/Libraries
Requires:	elektra = %{epoch}:%{version}-%{release}

%description devel
The Elektra Project provides a framework to store generic
configuration data in an hierarchical key-value pair database, instead
of a human-readable only text file.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

This package contains the include files and API manual pages to use
the Elektra API in C.

%description devel -l pl
Projekt Elektra dostarcza szkielet do przechowywania typowych danych
konfiguracyjnych w postaci klucz-warto¶æ w hierarchicznej bazie
danych, zamiast w pliku tekstowym czytelnym tylko dla cz³owieka.

W ten sposób oprogramowanie mo¿e odczytywaæ/zapisywaæ konfiguracjê za
pomoc± spójnego API. Dodatkowo aplikacje mog± byæ zorientowane w
konfiguracji innych aplikacji, u³atwiaj±c ich integracjê.

Ten pakiet zawiera pliki nag³ówkowe oraz strony podrêcznika
systemowego opisuj±cego sposób u¿ycia API Elektry w C.

%package static
Summary:	Static library for Elektra Project
Summary(pl):	Statyczna wersja biblioteki projektu Elektra
Group:		Development/Libraries
Requires:	elektra-devel = %{epoch}:%{version}-%{release}

%description static
The Elektra Project provides a framework to store generic
configuration data in an hierarchical key-value pair database, instead
of a human-readable only text file.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

This package contains static library for Elektra Project.

%description static -l pl
Projekt Elektra dostarcza szkielet do przechowywania typowych danych
konfiguracyjnych w postaci klucz-warto¶æ w hierarchicznej bazie
danych, zamiast w pliku tekstowym czytelnym tylko dla cz³owieka.

W ten sposób oprogramowanie mo¿e odczytywaæ/zapisywaæ konfiguracjê za
pomoc± spójnego API. Dodatkowo aplikacje mog± byæ zorientowane w
konfiguracji innych aplikacji, u³atwiaj±c ich integracjê.

Ten pakiet zawiera wersjê statyczn± biblioteki projektu Elektra.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__make} all \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig

%{__make} install \
	 LIB=/%{_lib} \
	 DESTDIR=$RPM_BUILD_ROOT

cp -a $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel elektra-api

echo 'RUN="no"' > $RPM_BUILD_ROOT/etc/sysconfig/elektra

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# Create basic key structure for apps
kdb set -t dir system/sw || :

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc articles doc/standards example scripts AUTHORS ChangeLog README TODO
%attr(755,root,root) /bin/*
%attr(755,root,root) /%{_lib}/lib*.so
%attr(755,root,root) /etc/profile.d/*
%{_datadir}/sgml/*
%{_mandir}/man[157]/*
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}

%files devel
%defattr(644,root,root,755)
%doc bindings elektra-api
%{_includedir}/*
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
