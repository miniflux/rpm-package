%undefine _disable_source_fetch

Name:    miniflux
Version: 2.0.15
Release: 1.0
Summary: Minimalist feed reader
URL: https://miniflux.app/
License: ASL 2.0
Source0: https://github.com/miniflux/miniflux/releases/download/%{version}/miniflux-linux-amd64
Source1: miniflux.service
Source2: miniflux.conf
Source3: https://raw.githubusercontent.com/miniflux/miniflux/master/miniflux.1
Source4: https://raw.githubusercontent.com/miniflux/miniflux/%{version}/LICENSE
Source5: https://raw.githubusercontent.com/miniflux/miniflux/%{version}/ChangeLog
BuildRoot: %{_topdir}/BUILD/%{name}-%{version}-%{release}
BuildArch: x86_64
Requires(pre): shadow-utils

%{?systemd_requires}
BuildRequires: systemd

%description
%{summary}

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 %{SOURCE0} %{buildroot}%{_bindir}/miniflux
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/miniflux.service
install -D -m 600 %{SOURCE2} %{buildroot}%{_sysconfdir}/miniflux.conf
install -D -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man1/miniflux.1
install -D -m 644 %{SOURCE4} %{buildroot}%{_docdir}/miniflux/LICENSE
install -D -m 644 %{SOURCE5} %{buildroot}%{_docdir}/miniflux/ChangeLog

%files
%defattr(755,root,root)
%{_bindir}/miniflux
%{_docdir}/miniflux
%defattr(644,root,root)
%{_unitdir}/miniflux.service
%{_mandir}/man1/miniflux.1*
%{_docdir}/miniflux/LICENSE
%{_docdir}/miniflux/ChangeLog
%defattr(600,root,root)
%config(noreplace) %{_sysconfdir}/miniflux.conf

%pre
getent group miniflux >/dev/null || groupadd -r miniflux
getent passwd miniflux >/dev/null || \
    useradd -r -g miniflux -d /dev/null -s /sbin/nologin \
    -c "Miniflux Daemon" miniflux
exit 0

%post
%systemd_post miniflux.service

%preun
%systemd_preun miniflux.service

%postun
%systemd_postun_with_restart miniflux.service

%changelog
