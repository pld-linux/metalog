Summary:	An efficient alternative to syslogd
Summary(pl):	Wydajny zamiennik syslogd
Name:		metalog
Version:	0.7beta
Release:	0.1
License:	GPL
Group:		Daemons
Source0:	http://prdownloads.sourceforge.net/metalog/%{name}-%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.conf
URL:		http://metalog.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pcre-devel
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
Provides:	syslogdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	klogd syslog syslog-ng

%description
Metalog is a modern replacement for syslogd and klogd. The logged
messages can be dispatched according to their facility, urgency,
program name and/or Perl-compatible regular expressions. Log files can
be automatically rotated when they exceed a certain size or age.
External shell scripts (e.g., mail) can be launched when specific
patterns are found. Metalog is easier to configure than syslogd and
syslog-ng, accepts unlimited number of rules and has (switchable)
memory bufferization for maximal performance.

%description -l pl
Metalog jest nowoczesnym zamiennikiem syslogd i klogd. Logowane
komunikaty mog± byæ rozsy³ane zale¿nie od facility, wagi, priorytetu,
nazwy programu i/lub perlowych wyra¿eñ regularnych. Pliki logów mog±
podlegaæ automatycznej rotacji kiedy przekrocz± okre¶lony rozmiar lub
wiek. Zewnêtrzne skrypty shellowe (np. poczta) mog± byæ uruchamiane
przy znalezieniu okre¶lonych wzorców. Metalog jest ³atwiejszy do
skonfigurowania ni¿ syslogd i syslog-ng, akceptuje nieskoñczon± liczbê
regu³ek i ma (prze³±czalne) buforowanie pamiêci dla osi±gniêcia
najwy¿szej wydajno¶ci.

%prep
%setup -q

%build
rm -f missing
aclocal
autoconf
automake -a -c -f
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

gzip -9nf README AUTHORS NEWS metalog.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add metalog
if [ -f /var/lock/subsys/metalog ]; then
	/etc/rc.d/init.d/metalog restart &>/dev/null
else
	echo "Run \"/etc/rc.d/init.d/metalog start\" to start metalog daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/metalog ]; then
		/etc/rc.d/init.d/metalog stop >&2
	fi
	/sbin/chkconfig --del metalog
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/metalog
%attr(640,root,root) %config %verify(not size mtime md5) %{_sysconfdir}/metalog.conf
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/metalog
%attr(754,root,root) /etc/rc.d/init.d/metalog
%{_mandir}/man8/*
