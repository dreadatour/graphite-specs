%define __prefix /usr/local

Summary:       Simple daemon for easy stats aggregation
Name:          statsd
Version:       0.6.0
Release:       1%{?dist}
Group:         MAILRU
License:       LGPL
Url:           https://github.com/etsy/statsd
Source0:       statsd.init
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
BuildRequires: nodejs
Requires:      nodejs


%description
Simple daemon for easy stats aggregation


%prep
# clean build directory
%{__rm} -rf %{buildroot}%{__prefix}/%{name}


%build
# clone repo
git clone --depth=1 --branch=v%{version} https://github.com/etsy/statsd.git %{buildroot}%{__prefix}/%{name}

# clean repository files
%{__rm} -rf %{buildroot}%{__prefix}/%{name}/{.git,.gitignore,debian,.travis.yml,Changelog.md,LICENSE,README.md,package.json}


%install
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}%{_initrddir}/statsd
chmod +x %{buildroot}%{__prefix}/%{name}/bin/*


%post
# create default statsd config if not exists
if [ ! -f %{__prefix}/%{name}/localConfig.js ];
then
    cp %{__prefix}/%{name}/exampleConfig.js %{__prefix}/%{name}/localConfig.js
fi


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_initrddir}/statsd
%defattr(-,mail,mail,-)
%{__prefix}/%{name}/
