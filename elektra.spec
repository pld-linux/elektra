Summary:	A key/value pair database to store software configurations
#Summary(pl):
Name:		elektra
Version:	0.4.6
Release:	0.1
Epoch:		0
License:	BSD
Group:		Applications/System
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	f032ec83ffe91f2e7c2a0d70f67749eb
Patch0:		%{name}-Makefile_CFLAGS.patch
URL:		http://elektra.sf.net
BuildRequires:	libxslt-progs
Obsoletes:	registry
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Elektra Project provides a framework to store generic
configuration data in an hierarchical key-value pair database, instead
of a human-readable only text file.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

#%%description -l pl

%package devel
Summary:	Include files and API documentation for Elektra Project
#Summary(pl):
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

#%%description devel -l pl

%package static
Summary:        Static library for Elektra Project
#Summary(pl):
Group:          Libraries
Requires:	elektra-devel = %{epoch}:%{version}-%{release}

%description static
The Elektra Project provides a framework to store generic
configuration data in an hierarchical key-value pair database, instead
of a human-readable only text file.

This way any software can read/save his configuration using a
consistent API. Also, applications can be aware of other applications
configurations, leveraging easy application integration.

This package contains static library for Elektra Project.

#%%description static -l pl

%prep
%setup -q -n elektra
%patch0 -p1

%build
%{__make} all CC="%{__cc}" CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

cp -a $RPM_BUILD_ROOT%{_datadir}/doc/%{name}-devel elektra-api

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
# Create basic key structure for apps
kdb set -t dir system/sw

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc articles doc/standards example scripts AUTHORS ChangeLog README TODO
%attr(755,root,root) /bin/*
%attr(755,root,root) /lib/lib*.so
%attr(755,root,root) /etc/profile.d/*
%{_includedir}/*
%{_datadir}/sgml
%{_mandir}/man[157]/*

%files devel
%defattr(644,root,root,755)
%doc bindings elektra-api
%{_includedir}/*
%{_mandir}/man3/*

%files static
%{_libdir}/lib*.a
