Graphite SPECS for CentOS
=========================

All that you need to build CentOS RPMs for:

* [Graphite][graphite] 0.9.10
* [StatsD][statsd] 0.6.0


Set Up an RPM Build Environment under CentOS
--------------------------------------------

More info: [Set Up an RPM Build Environment][prepare-rpm].

    yum install rpm-build make gcc
    mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
    echo '%_topdir %(echo $HOME)/rpmbuild' > ~/.rpmmacros


Prepare
-------

    mkdir ~/temp
    cd ~/temp/
    git clone https://github.com/dreadatour/graphite-specs.git


Build Graphite RPM
------------------

	yum install openldap-devel cairo cairo-devel

    cp -vr ~/temp/graphite-specs/graphite/* ~/rpmbuild/
    cd ~/rpmbuild/
    rpmbuild -v -bb SPECS/graphite.spec

Result RPM:

    ls ~/rpmbuild/RPMS/x86_64/graphite-0.9.10-1.el6.x86_64.rpm


Build StatsD RPM
----------------

    cp -vr ~/temp/graphite-specs/statsd/* ~/rpmbuild/
    cd ~/rpmbuild/
    rpmbuild -v -bb SPECS/statsd.spec

Result RPM:

    ls ~/rpmbuild/RPMS/noarch/statsd-0.6.0-1.el6.noarch.rpm

[graphite]: https://launchpad.net/graphite
[statsd]: https://github.com/etsy/statsd
[prepare-rpm]: http://wiki.centos.org/HowTos/SetupRpmBuildEnvironment
