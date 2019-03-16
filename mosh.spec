#
# Conditional build:
%bcond_with	agent		# with ssh agent forwarding patch

%define		protobuf_ver	2.6.1
%include	/usr/lib/rpm/macros.perl
Summary:	Mosh mobile shell
Summary(pl.UTF-8):	Mosh - przenośna powłoka
Name:		mosh
Version:	1.3.2
Release:	6
License:	GPL v3+
Group:		Applications/Networking
Source0:	https://mosh.org/%{name}-%{version}.tar.gz
# Source0-md5:	5122f4d2b973ab7c38dcdac8c35cb61e
Patch0:		https://github.com/keithw/mosh/pull/583.patch
Patch1:		%{name}-Werror.patch
# Patch0-md5:	7eb14665ef06072591e5bcd80780c0e4
Patch2:		%{name}-gcc8.patch
URL:		https://mosh.org/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	binutils >= 2.20.51.0.2
BuildRequires:	libstdc++-devel >= 5:4.0
BuildRequires:	libtool
BuildRequires:	libutempter-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	patchutils
BuildRequires:	perl-base >= 1:5.14
BuildRequires:	pkgconfig
BuildRequires:	protobuf >= %{protobuf_ver}
BuildRequires:	protobuf-devel >= %{protobuf_ver}
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Requires:	protobuf-libs >= %{protobuf_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# PLD stack protector flags are weaker than upstream, filter them out
# https://github.com/keithw/mosh/issues/203
%define		_ssp_cflags	%{nil}

%define		specflags	-Wno-error=non-virtual-dtor

%description
Remote terminal application that allows roaming, supports intermittent
connectivity, and provides intelligent local echo and line editing of
user keystrokes.

Mosh is a replacement for SSH. It's more robust and responsive,
especially over Wi-Fi, cellular, and long-distance links.

%description -l pl.UTF-8
Zdalna aplikacja terminala, pozwalająca na przemieszczanie,
obsługująca przerywaną łączność i zapewniająca inteligentne lokalne
echo oraz edycję linii.

Mosh to zamiennik SSH. Jest potężniejszy i responsywny, w
szczególności po połączeniach Wi-Fi, komórkowych i długodystansowych.

%prep
%setup -q
%if %{with agent}
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%{__sed} -i -e '1s,^#!.*perl,#!%{__perl},' scripts/mosh.pl

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-compile-warnings=error
%{__make}

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
