Summary:	A registry to store general key-value pairs instead of text configuration files
Summary(pl):	Rejestr do przechowywania par klucz-warto¶æ u¿ywany zamiast plików konfiguracyjnych
Name:		registry
Version:	0.1.6
Release:	1
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	04f05693c7be8da6db64f59129b92cf3
Group:		Base
License:	LGPL
Vendor:		Avi Alkalay <avi@unix.sh>
URL:		http://registry.sf.net
Requires:	%{name}-libs = %{version}-%{release}
BuildRequires:	libxslt-progs
BuildRequires:	docbook-style-xsl
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Linux Registry is an alternative back-end for text configuration
files.

Instead of each program to have its own text configuration files, the
Registry tries to provide a universal, fast, consistent, robust,
thread-safe and transactional infrastructure to store configuration
parameters through a key-value pair mechanism.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

%description -l pl
Rejestr Linux jest alternatyw± dla zaplecza w postaci tekstowych
plików konfiguracyjnych.

Ka¿dy program, zamiast przechowywaæ informacje konfiguracyjne w swoim
w³asnym pliku mo¿e u¿yæ Rejestru, który udostêpnia uniwersaln±,
szybk±, spójn±, niezawodn±, bezpieczn± dla aplikacji opatrych na
w±tkach i transakcyjn± infrastrukturê s³u¿±c± do przechowwania
parametrów konfiguracyjnych poprzez mechanizm: klucz-warto¶æ.

W ten sposób ka¿da aplikacja mo¿e odczytaæ/zapisaæ swoj± konfiguracjê
u¿ywaj±c spójnego API. Co wiêcej, aplikacje mog± w ten sposób
wzajemnie zdawaæ sobie sprawê o swoich konfiguracjach co wspomaga
ich integrowanie.

%package devel
Summary:	Include files and API documentation for the Linux Registry
Summary(pl):	Pliki nag³ówkowe i dokumentacja API dla Rejestru Linux
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
The Linux Registry is an alternative back-end for text configuration
files.

Instead of each program to have its own text configuration files, the
Registry tries to provide a universal, fast, consistent, robust,
thread-safe and transactional infrastructure to store configuration
parameters through a key-value pair mechanism.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

This package contains the include files and API manual pages to use
the Registry API in C.

%description devel -l pl
Rejestr Linux jest alternatyw± dla zaplecza w postaci tekstowych
plików konfiguracyjnych.

Ka¿dy program, zamiast przechowywaæ informacje konfiguracyjne w swoim
w³asnym pliku mo¿e u¿yæ Rejestru, który udostêpnia uniwersaln±,
szybk±, spójn±, niezawodn±, bezpieczn± dla aplikacji opatrych na
w±tkach i transakcyjn± infrastrukturê s³u¿±c± do przechowwania
parametrów konfiguracyjnych poprzez mechanizm: klucz-warto¶æ.

W ten sposób ka¿da aplikacja mo¿e odczytaæ/zapisaæ swoj± konfiguracjê
u¿ywaj±c spójnego API. Co wiêcej, aplikacje mog± w ten sposób
wzajemnie zdawaæ sobie sprawê o swoich konfiguracjach co wspomaga
ich integrowanie.

Ten pakiet zawiera pliki nag³ówkowe i strony podrêcznika API, aby
u¿ywaæ Rejestru z poziomu programów pisanych w jêzyku C.

%package examples
Summary:	Example source files for the Linux Registry
Summary(pl):	Przyk³adowe pliki ¼ród³owe dla Rejestru Linux
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description examples
The Linux Registry is an alternative back-end for text configuration
files.

Instead of each program to have its own text configuration files, the
Registry tries to provide a universal, fast, consistent, robust,
thread-safe and transactional infrastructure to store configuration
parameters through a key-value pair mechanism.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

This package contains the example source files for the Linux Registry.

%description examples -l pl
Rejestr Linux jest alternatyw± dla zaplecza w postaci tekstowych
plików konfiguracyjnych.

Ka¿dy program, zamiast przechowywaæ informacje konfiguracyjne w swoim
w³asnym pliku mo¿e u¿yæ Rejestru, który udostêpnia uniwersaln±,
szybk±, spójn±, niezawodn±, bezpieczn± dla aplikacji opatrych na
w±tkach i transakcyjn± infrastrukturê s³u¿±c± do przechowwania
parametrów konfiguracyjnych poprzez mechanizm: klucz-warto¶æ.

W ten sposób ka¿da aplikacja mo¿e odczytaæ/zapisaæ swoj± konfiguracjê
u¿ywaj±c spójnego API. Co wiêcej, aplikacje mog± w ten sposób
wzajemnie zdawaæ sobie sprawê o swoich konfiguracjach co wspomaga
ich integrowanie.

Ten pakiet zawiera przyk³adowe pliki ¼ród³owe dla Rejestru Linux.

%package libs
Summary:	Library files for the Linux Registry
Summary(pl):	Pliki biblioteki dla Rejestru Linux
Group:		Base

%description libs
The Linux Registry is an alternative back-end for text configuration
files.

Instead of each program to have its own text configuration files, the
Registry tries to provide a universal, fast, consistent, robust,
thread-safe and transactional infrastructure to store configuration
parameters through a key-value pair mechanism.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

This package contains the library files, which are necessary for the
applications to work with the Registry.

%description libs -l pl
Rejestr Linux jest alternatyw± dla zaplecza w postaci tekstowych
plików konfiguracyjnych.

Ka¿dy program, zamiast przechowywaæ informacje konfiguracyjne w swoim
w³asnym pliku mo¿e u¿yæ Rejestru, który udostêpnia uniwersaln±,
szybk±, spójn±, niezawodn±, bezpieczn± dla aplikacji opatrych na
w±tkach i transakcyjn± infrastrukturê s³u¿±c± do przechowwania
parametrów konfiguracyjnych poprzez mechanizm: klucz-warto¶æ.

W ten sposób ka¿da aplikacja mo¿e odczytaæ/zapisaæ swoj± konfiguracjê
u¿ywaj±c spójnego API. Co wiêcej, aplikacje mog± w ten sposób
wzajemnie zdawaæ sobie sprawê o swoich konfiguracjach co wspomaga
ich integrowanie.

Ten pakiet zawiera pliki biblioteczne konieczne do dzia³ania
aplikacji wraz z Rejestrem.

%prep
%setup -q -n registry

%build
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/bin,/lib,%{_includedir},%{_examplesdir}} \
	   $RPM_BUILD_ROOT%{_docdir}/{%{name}-devel,%{name}} \
	   $RPM_BUILD_ROOT%{_mandir}/man{1,3,5,7}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_docdir}/%{name} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mv -f $RPM_BUILD_ROOT%{_docdir}/%{name}-devel $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
mv -f TODO VERSION ChangeLog $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/rg set -t dir system.sw

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) /bin/*
%doc %{_docdir}/%{name}-%{version}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_mandir}/man3/*

%files examples
%defattr(644,root,root,755)
%doc %{_examplesdir}/%{name}-%{version}/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) /lib/*
