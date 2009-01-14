Name:		transconnect
# indeed, the version is 1.3-Beta. But it is untouched since 2001 so
# I do not expect a final 1.3. Therefore, the 'Beta' is omitted
# completely instead of bothering around with a '0.Beta' release
# till end of days.
Summary:	A function imposter to allow transparent connection over HTTPS proxies
Version:	1.3
Release:	1
License:	GPL
Group:		Applications/Networking
URL:		http://transconnect.sourceforge.net/
Source0:	http://dl.sourceforge.net/transconnect/%{name}-%{version}-Beta.tar.gz
# Source0-md5:	50f75731e610fce00803cc7d98b301fd
Source1:	tconn
Patch0:		%{name}-fixup.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Transconnect is an implementation to allow network connections over a
HTTP proxy. This should work under almost all linux distributions
using glibc, and all proxies allowing https CONNECT (eg squid).

%prep
%setup -q -n %{name}-%{version}-Beta
%patch0 -p1
%{__sed} -i -e 's!\$HOME/\.tconn/!!g' tconn.cat

%build
for i in localres tcpdns localtcp; do
	%{__make} CFLAGS="%{rpmcflags} -fPIC" CC="%{__cc}" "$i"
	mv tconn.so tconn-$i.so
	%{__make} clean
done

%{__make} CFLAGS="%{rpmcflags} -fPIC" CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_bindir}}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}
install -p tconn*.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING INSTALL README TROUBLESHOOT tconn.cat tconn.conf
%attr(755,root,root) %{_bindir}/tconn
%attr(755,root,root) %{_libdir}/tconn-localres.so
%attr(755,root,root) %{_libdir}/tconn-localtcp.so
%attr(755,root,root) %{_libdir}/tconn-tcpdns.so
%attr(755,root,root) %{_libdir}/tconn.so
