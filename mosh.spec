#

# Conditional build:
%bcond_without	verbose		# verbose build (V=1)

%if "%{pld_release}" == "ac"
# add suffix, but allow ccache, etc in ~/.rpmmacros
%{expand:%%define	__cc	%(echo '%__cc' | sed -e 's,-gcc,-gcc4,')}
%{expand:%%define	__cxx	%(echo '%__cxx' | sed -e 's,-g++,-g++4,')}
%{expand:%%define	__cpp	%(echo '%__cpp' | sed -e 's,-gcc,-gcc4,')}
%endif

%include	/usr/lib/rpm/macros.perl
Summary:	Mosh mobile shell
Name:		mosh
Version:	1.2.2.95rc1
Release:	0.1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/downloads/keithw/mosh/%{name}-%{version}.tar.gz
# Source0-md5:	3bfba35b09a80c4a8f3bebd4dc6f8c94
URL:		http://mosh.mit.edu/
BuildRequires:	binutils >= 2.20.51.0.2
BuildRequires:	libstdc++-devel >= 5:4.0
BuildRequires:	libutempter-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	protobuf
BuildRequires:	protobuf-devel
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
# gcc4 might be installed, but not current __cc
%if "%(echo %{cc_version} | cut -d. -f1,2)" < "4.0"
BuildRequires:	__cc >= 4.0
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# PLD stack protector flags are weaker than upstream, filter them out
# https://github.com/keithw/mosh/issues/203
%define		filterout_cxx	-fstack-protector --param=ssp-buffer-size=4

%description
Remote terminal application that allows roaming, supports intermittent
connectivity, and provides intelligent local echo and line editing of
user keystrokes.

Mosh is a replacement for SSH. It's more robust and responsive,
especially over Wi-Fi, cellular, and long-distance links.

%prep
%setup -q
%{__sed} -i -e '1s,^#!.*perl,#!%{__perl},' scripts/mosh

%build
%configure \
	--enable-compile-warnings=error \
	CPPFLAGS="-I/usr/include/ncurses"
%{__make} \
	%{?with_verbose:V=1}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS THANKS
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-client
%attr(755,root,root) %{_bindir}/%{name}-server
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-client.1*
%{_mandir}/man1/%{name}-server.1*
