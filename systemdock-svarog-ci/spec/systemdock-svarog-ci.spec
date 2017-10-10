%define         _module systemdock-svarog-ci

# SVAROG-related variables
%{!?svn_revision:%define svn_revision 1}
# COMPATIBILITY FIX: Jenkins job name is neccessary to make build root unique (for CentOS5 and earlier)
%{!?JOB_NAME:%define JOB_NAME standalone}


Name:		systemdock-svarog-ci
Version:	0.1
Release:	%{svn_revision}%{?dist}
Summary:	SystemDock profile to run svarog-ci container as systemd service

Group:		Development/Tools
License:	GPLv3
URL:		https://github.com/SoftServeInc/svarog
Packager:       Roman Pavlyuk <roman.pavlyuk@gmail.com>
Source:         %{_module}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)-%{JOB_NAME}
BuildArch:      noarch

Requires:	systemdock
Requires:	systemd

%description
SystemDock profile to run svarog-ci container as systemd service

%prep
%setup -n %{_module}

%build
# Nothing

%install
%make_install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
ln -s %{_sysconfdir}/systemdock/containers.d/svarog-ci/systemdock-svarog-ci.service $RPM_BUILD_ROOT%{_unitdir}/systemdock-svarog-ci.service

%files
%doc README.md

%config(noreplace) %{_sysconfdir}/systemdock/containers.d/svarog-ci/config.yml
%{_sysconfdir}/systemdock/containers.d/svarog-ci/systemdock-svarog-ci.service

%{_unitdir}/systemdock-svarog-ci.service

%dir %{_sharedstatedir}/jenkins

%changelog

