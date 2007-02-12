Summary:	An efficient alternative to syslogd
Summary(pl.UTF-8):   Wydajny zamiennik syslogd
Name:		metalog
Version:	0.7
Release:	2
Epoch:		0
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/metalog/%{name}-%{version}.tar.gz
# Source0-md5:	40940eb9829de7d5776b9bbd514f9d7e
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
URL:		http://metalog.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Provides:	syslogdaemon
Obsoletes:	klogd
Obsoletes:	syslog
Obsoletes:	syslog-ng
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Metalog is a modern replacement for syslogd and klogd. The logged
messages can be dispatched according to their facility, urgency,
program name and/or Perl-compatible regular expressions. Log files can
be automatically rotated when they exceed a certain size or age.
External shell scripts (e.g., mail) can be launched when specific
patterns are found. Metalog is easier to configure than syslogd and
syslog-ng, accepts unlimited number of rules and has (switchable)
memory bufferization for maximal performance.

%description -l pl.UTF-8
Metalog jest nowoczesnym zamiennikiem syslogd i klogd. Logowane
komunikaty mogą być rozsyłane zależnie od facility, wagi, priorytetu,
nazwy programu i/lub perlowych wyrażeń regularnych. Pliki logów mogą
podlegać automatycznej rotacji kiedy przekroczą określony rozmiar lub
wiek. Zewnętrzne skrypty shellowe (np. poczta) mogą być uruchamiane
przy znalezieniu określonych wzorców. Metalog jest łatwiejszy do
skonfigurowania niż syslogd i syslog-ng, akceptuje nieskończoną liczbę
regułek i ma (przełączalne) buforowanie pamięci dla osiągnięcia
najwyższej wydajności.

%prep
%setup -q

%build
rm -f missing
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{rc.d/init.d,sysconfig},%{_sbindir},%{_mandir}/man8,}

install	src/metalog 	$RPM_BUILD_ROOT%{_sbindir}
install man/metalog.8*	$RPM_BUILD_ROOT%{_mandir}/man8

install %{SOURCE1}      $RPM_BUILD_ROOT/etc/rc.d/init.d/metalog
install %{SOURCE2}      $RPM_BUILD_ROOT/etc/sysconfig/metalog
install %{SOURCE3}	$RPM_BUILD_ROOT%{_sysconfdir}/metalog.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add metalog
%service metalog restart "metalog daemon"

%preun
if [ "$1" = "0" ]; then
	%service metalog stop
	/sbin/chkconfig --del metalog
fi

%files
%defattr(644,root,root,755)
%doc README AUTHORS NEWS metalog.conf
%attr(755,root,root) %{_sbindir}/metalog
%attr(640,root,root) %config %verify(not md5 mtime size) %{_sysconfdir}/metalog.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/metalog
%attr(754,root,root) /etc/rc.d/init.d/metalog
%{_mandir}/man8/*
