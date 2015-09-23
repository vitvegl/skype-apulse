%define __os_install_post %{nil}
%define debug_package %{nil}
%define __name skype

Summary:	Free Internet telephony that just works
Name:		skype-apulse
Version:	4.3.0.37
Release:	1%{?dist}
Group:		Applications/Internet
License:	Proprietary
URL:		http://www.skype.com
Source0:	http://download.skype.com/linux/%{__name}-%{version}-fedora.i586.rpm
Source1:	%{__name}.sh
BuildRoot:	%{_tmppath}/%{__name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	desktop-file-utils
Requires:       /usr/lib/apulse/libpulse.so.0
Requires:	/usr/lib/libtiff.so.5
Provides:	libtiff.so.4
Conflicts:      skype

ExclusiveArch:	i586


%description
Skype - Take a deep breath

Skype is a little piece of software that lets you make free calls
to anyone else on Skype, anywhere in the world. And even though
the calls are free, they are really excellent quality.

 * Make free Skype-to-Skype calls to anyone else, anywhere in the world.
 * Call ordinary phones and mobiles at pretty cheap rates per minute.
 * Group chat with up to 100 people or conference call with up to nine others.
 * See who you are talking to with free video calls.
 * Free to download.

%prep
%setup -q -c -T

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
pushd %{buildroot}
rpm2cpio %{SOURCE0} | cpio -idV --quiet
popd

mv %{buildroot}%{_bindir}/%{__name} %{buildroot}%{_bindir}/%{__name}-bin

install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/%{__name}

sed -i 's!Icon=skype.png!Icon=skype!g' %{buildroot}%{_datadir}/applications/%{__name}.desktop

desktop-file-install \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --add-category Telephony			\
  --add-category Qt				\
  --remove-category Application			\
  --delete-original				\
  %{buildroot}%{_datadir}/applications/%{__name}.desktop

echo "StartupWMClass=Skype-bin" >> %{buildroot}%{_datadir}/applications/skype.desktop

mkdir -p %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf libtiff.so.5 libtiff.so.4
popd

sed -i 's!skype!skype-bin!g' \
	%{buildroot}%{_sysconfdir}/prelink.conf.d/skype.conf

%post
update-desktop-database &> /dev/null || :
touch --no-create /usr/share/icons/hicolor &>/dev/null || :
if [ -x /usr/bin/gtk-update-icon-cache ]; then
  /usr/bin/gtk-update-icon-cache --quiet /usr/share/icons/hicolor || :
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create /usr/share/icons/hicolor &>/dev/null
    gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache /usr/share/icons/hicolor &>/dev/null || :


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root)
%doc %{_docdir}/%{__name}-%{version}
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/skype.conf
%config(noreplace) %{_sysconfdir}/prelink.conf.d/skype.conf
%{_bindir}/%{__name}
%{_bindir}/%{__name}-bin
%{_libdir}/libtiff.so.4
%{_datadir}/%{__name}
%{_datadir}/pixmaps/%{__name}.png
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{__name}.png

%changelog
* Wed Sep 23 2015 vitvegl@quintagroup.org - 4.3.0.37-1
- initial build
