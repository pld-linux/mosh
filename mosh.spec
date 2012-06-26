#
# Conditional build:
%bcond_without	verbose		# verbose build (V=1)

%include	/usr/lib/rpm/macros.perl
Summary:	Mosh mobile shell
Name:		mosh
Version:	1.2.2
Release:	1
License:	GPL v3+
Group:		X11/Applications
Source0:	https://github.com/downloads/keithw/mosh/%{name}-%{version}.tar.gz
# Source0-md5:	7ed5b857307685794dcd120afe5bdf52
URL:		http://mosh.mit.edu/
BuildRequires:	libutempter-devel
BuildRequires:	ncurses-devel
BuildRequires:	protobuf
BuildRequires:	protobuf-devel
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
