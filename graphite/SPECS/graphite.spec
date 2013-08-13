%define __prefix /usr/local

Summary:       Enterprise scalable realtime graphing
Name:          graphite
Version:       0.9.10
Release:       1%{?dist}
License:       Apache Software License 2.0
Group:         MAILRU
Prefix:        %{_prefix}
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root

Url:           https://launchpad.net/graphite
Source0:       carbon-cache.init
Source1:       graphite-uwsgi.init
Source2:       graphite-uwsgi.ini
Source3:       graphite-wsgi.py
Source4:       graphite-nginx.conf
Source5:       graphite-settings.py

BuildRequires: python2.7
BuildRequires: python2.7-devel
BuildRequires: python2.7-tools
BuildRequires: openldap-devel
BuildRequires: cairo == 1.8.8
BuildRequires: cairo-devel == 1.8.8
Requires:      python2.7
Requires:      cairo == 1.8.8
Requires:      bitmap-fonts


%description
Enterprise scalable realtime graphing


%prep
# create build directory
if [ -d %{buildroot}%{__prefix}/%{name} ];
then
    echo "Cleaning out stale build directory" 1>&2
    %{__rm} -rf %{buildroot}%{__prefix}/%{name}
fi


%build
# define python libs path (hardcoded, but working fine)
%define python_libs %{buildroot}%{__prefix}/%{name}/lib/python2.7/site-packages

# creating virtual environment
virtualenv --distribute %{buildroot}%{__prefix}/%{name}

# install all requirements
%{buildroot}%{__prefix}/%{name}/bin/pip install \
    Django==1.4.1 django-tagging==0.3.1 \
	pycairo==1.8.8 zope.interface==4.0.1 \
	python-memcached==1.48 python-ldap==2.4.10 \
	Twisted==12.1.0 txAMQP==0.6.1 psycopg2==2.4.5

# fix pycairo (WTF?!)
echo "from _cairo import *" > %{python_libs}/cairo/__init__.py

# install whisper (db lib)
%{buildroot}%{__prefix}/%{name}/bin/pip install \
    whisper==%{version}

# install carbon (data aggregator)
%{buildroot}%{__prefix}/%{name}/bin/pip install \
    carbon==%{version} \
    --install-option="--install-scripts=%{buildroot}%{__prefix}/%{name}/bin/" \
    --install-option="--install-lib=%{python_libs}" \
    --install-option="--install-data=%{buildroot}%{__prefix}/%{name}/%{name}"

# install graphite
%{buildroot}%{__prefix}/%{name}/bin/pip install \
    graphite-web \
    --install-option="--install-scripts=%{buildroot}%{__prefix}/%{name}/bin/" \
    --install-option="--install-lib=%{buildroot}%{__prefix}/%{name}" \
    --install-option="--install-data=%{buildroot}%{__prefix}/%{name}"

# install config files
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}%{__prefix}/%{name}/conf/uwsgi.ini
%{__install} -p -D -m 0755 %{SOURCE3} %{buildroot}%{__prefix}/%{name}/conf/graphite.wsgi
%{__install} -p -D -m 0755 %{SOURCE4} %{buildroot}%{__prefix}/%{name}/conf/nginx.conf
%{__install} -p -D -m 0755 %{SOURCE5} %{buildroot}%{__prefix}/%{name}/%{name}/local_settings.py-dist

# do not include *.pyc in rpm
find %{buildroot}%{__prefix}/%{name}/ -type f -name "*.py[co]" -delete

# fix python path
find %{buildroot}%{__prefix}/%{name}/ -type f \
    -exec sed -i 's:'%{buildroot}'::' {} \;


%install
# install init.d files
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}%{_initrddir}/carbon-cache
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_initrddir}/graphite

# compile py files
%{buildroot}%{__prefix}/%{name}/bin/python -m compileall -qf %{buildroot}%{__prefix}/%{name}/


%post
# create default graphite settings files if not exists
if [ ! -f %{__prefix}/%{name}/%{name}/local_settings.py ];
then
    cp %{__prefix}/%{name}/%{name}/local_settings.py-dist %{__prefix}/%{name}/%{name}/local_settings.py
fi

# create default carbon settings files if not exists
if [ ! -f %{__prefix}/%{name}/conf/carbon.conf ];
then
    cp %{__prefix}/%{name}/%{name}/conf/carbon.conf.example %{__prefix}/%{name}/conf/carbon.conf
fi

# create default storage settings files if not exists
if [ ! -f %{__prefix}/%{name}/conf/storage-schemas.conf ];
then
    cp %{__prefix}/%{name}/%{name}/conf/storage-schemas.conf.example %{__prefix}/%{name}/conf/storage-schemas.conf
fi

# create symlink to django admin static files if not exists
if [ ! -d %{__prefix}/%{name}/webapp/content/admin ];
then
    ln -s %{__prefix}/%{name}/lib/python2.7/site-packages/django/contrib/admin/static/admin %{__prefix}/%{name}/webapp/content/admin
fi

ldconfig


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_initrddir}/carbon-cache
%{_initrddir}/graphite
%defattr(-,mail,mail,-)
%{__prefix}/%{name}/
