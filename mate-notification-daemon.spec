Summary:	MATE notification daemon
Name:		mate-notification-daemon
Version:	1.8.1
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	305d64a23982479575dfd169a00ff398
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	libnotify-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libwnck2-devel
BuildRequires:	pkg-config
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires:	dbus
Obsoletes:	xdg-desktop-notification-daemon
Provides:	xdg-desktop-notification-daemon
BuildRoot:	%{_tmppath}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
A daemon that displays passive pop-up notifications as per the Desktop
Notifications spec.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*/*/*.la
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-notification-daemon.convert

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_gsettings_cache

%postun
%update_icon_cache hicolor
%update_gsettings_cache

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-notification-properties
%dir %{_libexecdir}
%dir %{_libdir}/mate-notification-daemon
%dir %{_libdir}/mate-notification-daemon/engines
%attr(755,root,root) %{_libexecdir}/mate-notification-daemon
%attr(755,root,root) %{_libdir}/mate-notification-daemon/engines/*.so
%{_datadir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/org.mate.NotificationDaemon.gschema.xml
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/apps/*.*
%{_mandir}/man1/mate-notification-properties.1*

