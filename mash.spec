#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
#
Summary:	A library for using real 3D models within a Clutter scene
Summary(pl.UTF-8):	Biblioteka pozwalająca na używanie prawdziwych modeli 3D wewnątrz sceny Clutter
Name:		mash
Version:	0.2.0
Release:	6
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://source.clutter-project.org/sources/mash/0.2/%{name}-%{version}.tar.xz
# Source0-md5:	9eda552784291707e667be4d55917794
URL:		http://wiki.clutter-project.org/wiki/Mash
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.9
BuildRequires:	clutter-devel >= 1.6.0
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mash is a small library for using real 3D models within a Clutter
scene. Models can be exported from Blender or other 3D modeling
software as PLY files and then used as actors. It also supports a
lighting model with animatable lights.

%description -l pl.UTF-8
Mash to mała biblioteka pozwalająca na używanie prawdziwych modeli 3D
wewnątrz sceny Clutter. Modele można eksportować z Blendera lub innego
programu do modelowania 3D w postaci plików PLY, a następnie używać
ich jako aktorów. Obsługiwane są także modele oświetlenia z ruchomymi
światłami.

%package devel
Summary:	Header files for mash library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki mash
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	clutter-devel >= 1.6.0

%description devel
Header files for mash library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki mash.

%package static
Summary:	Static mash library
Summary(pl.UTF-8):	Statyczna biblioteka mash
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static mash library.

%description static -l pl.UTF-8
Statyczna biblioteka mash.

%package apidocs
Summary:	mash API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki mash
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API and internal documentation for mash library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki mash.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{__enable_disable static_libs static} \
	%{__enable_disable apidocs gtk-doc} \
	--with-html-dir=%{_gtkdocdir} \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libmash-0.2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmash-0.2.so.0
%{_libdir}/girepository-1.0/Mash-0.2.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmash-0.2.so
%{_datadir}/gir-1.0/Mash-0.2.gir
%{_includedir}/mash-0.2
%{_pkgconfigdir}/mash-0.2.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmash-0.2.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mash
%endif
