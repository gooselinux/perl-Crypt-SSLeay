Name:           perl-Crypt-SSLeay
Summary:        Crypt::SSLeay - OpenSSL glue that provides LWP https support
Version:        0.57
Release:        16%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
Source0:        http://www.cpan.org/authors/id/D/DL/DLAND/Crypt-SSLeay-%{version}.tar.gz
Patch1:         perl-Crypt-SSLeay-cryptdef.patch
Patch2:         perl-Crypt-SSLeay-0.57-live-tests.patch
Patch3:		perl-Crypt-SSLeay-Makefile_ssl1.patch
URL:            http://search.cpan.org/dist/Crypt-SSLeay/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  openssl-devel
BuildRequires:  perl(URI)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(ExtUtils::MakeMaker::Coverage)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(LWP::UserAgent)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This perl module provides support for the https protocol under LWP, so
that a LWP::UserAgent can make https GET & HEAD & POST
requests. Please see perldoc LWP for more information on POST
requests.

The Crypt::SSLeay package contains Net::SSL, which is automatically
loaded by LWP::Protocol::https on https requests, and provides the
necessary SSL glue for that module to work.


%prep
%setup -q -n Crypt-SSLeay-%{version} 
%patch1 -p1 -b .cryptdef
%patch2 -p1
%patch3 -p1 -b .make

# Filter unwanted Provides:
cat << EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(DB)/d'
EOF

%define __perl_provides %{_builddir}/Crypt-SSLeay-%{version}/%{name}-prov
chmod +x %{__perl_provides}


%build
if pkg-config openssl ; then
  export INC="$CFLAGS `pkg-config --cflags-only-I openssl`"
  export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi

%{__perl} Makefile.PL --default --no-live-tests INC="$INC" \
          LDFLAGS="$LDFLAGS" INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}


%clean 
rm -rf $RPM_BUILD_ROOT


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*
chmod -R 644 eg/*
chmod -R 644 certs/*

%check
make test


%files
%defattr(-,root,root,-)
%doc README Changes eg/* certs/*
%{perl_vendorarch}/auto/Crypt/
%{perl_vendorarch}/Crypt/
%{perl_vendorarch}/Net/
%{_mandir}/man3/*.3*


%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.57-16
- rebuild against perl 5.10.1

* Wed Nov 25 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.57-14
- change Makefile for openssl 1.0, which couldn't be found properly before

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.57-13
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.57-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 0.57-10
- rebuild with new openssl

* Mon Oct  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 0.57-9
- add examples into doc

* Wed Sep 24 2008 Marcela Maslanova <mmaslano@redhat.com> - 0.57-8
- fix patches for fuzz

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.57-7
- rebuild for new perl

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.57-6
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 0.57-5
 - Rebuild for deps

* Wed Dec  5 2007 Robin Norwood <rnorwood@redhat.com> - 0.57-4
- Rebuild for new openssl

* Sat Oct 27 2007 Robin Norwood <rnorwood@redhat.com> - 0.57-3
- Remove unnecessary BR: pkgconfig

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 0.57-2
- Fix buildroot per package review
- Resolves: bz#226248

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 0.57-1
- Update to latest upstream version.
- Remove old patch (patch applied to upstream)
- Several fixes for package review:
- Fixed BuildRequires (added Test::Pod and LWP::UserAgent)
- Apply patch to avoid prompting for input when building Makefile
- Fix defattr line
- Resolves: bz#226248

* Mon Aug 27 2007 Robin Norwood <rnorwood@redhat.com> - 0.56-2
- perl(ExtUtils::MakeMaker::Coverage) is now available

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 0.56-1
- 0.56 is the latest CPAN version, not 0.55

* Mon Aug 13 2007 Robin Norwood <rnorwood@redhat.com> - 0.55-2
- Update to latest version from CPAN: 0.55
- Remove two old patches, update lib64 patch for Makefile.PL changes.

* Tue Feb 13 2007 Robin Norwood <rnorwood@redhat.com> - 0.53-1
- New version: 0.53

* Mon Nov 27 2006 Robin Norwood <rnorwood@redhat.com> - 0.51-12
- Resolves: bug#217138
- fix a segfault on x86_64

* Tue Oct 17 2006 Robin Norwood <rnorwood@redhat.com> - 0.51-10
- Filter out Provides perl(DB)
- bug #205562

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.51-9.2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.51-9.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.51-9.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.51-9.2
- rebuild for new perl-5.8.8 / gcc / glibc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 0.51-9
- rebuilt against new openssl
- added missing SSL_library_init()

* Sat Sep 24 2005 Ville Skyttä <ville.skytta at iki.fi> 0.51-8
- Own more installed dirs (#73908).
- Enable rpmbuild's internal dependency generator, drop unneeded dependencies.
- Require perl(:MODULE_COMPAT_*).
- Run tests in the %%check section.
- Fix License, Source0, URL, and Group tags.

* Wed Mar 30 2005 Warren Togami <wtogami@redhat.com> 0.51-7
- remove brp-compress

* Tue Mar  8 2005 Joe Orton <jorton@redhat.com> 0.51-6
- rebuild

* Tue Aug 31 2004 Chip Turner <cturner@redhat.com> 0.51-5
- build for FC3

* Tue Aug 31 2004 Chip Turner <cturner@redhat.com> 0.51-4
- build for RHEL3 U4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 0.51-1
- update to upstream 0.51

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com>
- pass openssl includes to make as INC and ldflags in as LDFLAGS

* Thu Nov 21 2002 Chip Turner <cturner@redhat.com>
- patch to support /usr/lib64 before /usr/lib

* Wed Nov 20 2002 Chip Turner <cturner@redhat.com>
- rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Thu Jun 27 2002 Chip Turner <cturner@redhat.com>
- description update

* Tue Jun 25 2002 Chip Turner <cturner@redhat.com>
- move to 0.39

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 
