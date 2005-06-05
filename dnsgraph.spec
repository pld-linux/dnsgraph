%include	/usr/lib/rpm/macros.perl
Summary:	Simple BIND statistics
Summary(pl):	Proste statystyki dla BINDa
Name:		dnsgraph
Version:	0.9
Release:	0.1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://dl.sourceforge.net/dnsgraph/%{name}-%{version}.tar.gz
# Source0-md5:	4847627fb3709bbe166d59e872225693
Source1:	%{name}.cron
Source2:	%{name}.conf
URL:		http://dnsgraph.sourceforge.net/
BuildRequires:	rpm-perlprov
Requires(post,preun):	grep
Requires(preun):	fileutils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_dnsgraphdir	%{_datadir}/%{name}

%description
Dnsgraph is a very simple DNS statistics RRDtool frontend for Bind
(named) that produces daily, weekly, monthly, and yearly graphs of
success/failure, recursion/referral, nxrrset/nxdomain.

%description -l pl
dnsgraph to bardzo prosty frontend dla RRDtoola do statystyk DNS dla
Binda (named) tworz±cy dzienne, tygodniowe, miesiêczne i roczne
wykresy powodzeñ/niepowodzeñ, rekurencji/odniesieñ, nxrrset/nxdomain.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{cron.d,httpd},%{_dnsgraphdir}/html/imgs}

install dnsanalise.pl dnsreport.pl $RPM_BUILD_ROOT%{_dnsgraphdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/httpd

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && \
	! grep -q "^Include.*/%{name}.conf" /etc/httpd/httpd.conf; then
		echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		apachectl restart
	fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	grep -E -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
		/etc/httpd/httpd.conf.tmp
	mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
	if [ -f /var/lock/subsys/httpd ]; then
		apachectl restart
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
/etc/cron.d/%{name}
%{_sysconfdir}/httpd/%{name}.conf
%dir %{_dnsgraphdir}
%{_dnsgraphdir}/html
%attr(755,root,root) %{_dnsgraphdir}/dns*.pl
