%{?!python3_pkgversion:%global python3_pkgversion 3}

%global srcname termcolor_dg

Name:           python-%{srcname}
Version:        1.0.2
Release:        0%{?dist}
Summary:        ANSI Color formatting for terminal output and log coloring.
License:        MIT
URL:            https://github.com/gunchev/termcolor_dg/%{srcname}
Source0:        https://github.com/gunchev/%{srcname}/archive/refs/tags/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
# BuildRequires:  python%%{python3_pkgversion}-check-manifest >= 0.42
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-flake8
BuildRequires:  python%{python3_pkgversion}-pylint


%{?python_enable_dependency_generator}

%description
ANSI Color formatting for terminal output and log coloring.
Supports 16 color, 256 color and 24-bit color modes.

Python 2 support is present for legacy projects and because
it is not too much work and I have to use it for now.



%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}


%description -n python%{python3_pkgversion}-%{srcname}
ANSI Color formatting for terminal output and log coloring.
Supports 16 color, 256 color and 24-bit color modes.

Python 2 support is present for legacy projects and because
it is not too much work and I have to use it for now.


%package -n python%{python3_pkgversion}-%{srcname}-bin
Summary:  %{summary}
Requires: python%{python3_pkgversion}-%{srcname}

%description -n python%{python3_pkgversion}-%{srcname}-bin
binary files for %{srcname}, you can simply:

    python -m termcolor_dg

or

    python -m termcolor_dg logs


%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%py3_build


%install
rm -rf "$RPM_BUILD_ROOT"
%py3_install


%check
PYLINT=pylint-3 COVERAGE=coverage-3 make test


%files -n  python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc CHANGES.md README.md INSTALL.md TODO.md
%{python3_sitelib}/%{srcname}.py
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/__pycache__/%{srcname}*


%files -n  python%{python3_pkgversion}-%{srcname}-bin
# binaries
%{_bindir}/termcolor_dg_demo
%{_bindir}/termcolor_dg_demo_log


%changelog
* Thu May 25 2023 Doncho N. Gunchev <dgunchev@gmail.com> - 1.0.0-0
- Fix logging.basicConfig has no disable_existing_loggers argument.
- fix DISABLED detection

* Wed Jan 11 2023 Doncho N. Gunchev <dgunchev@gmail.com> - 0.9.3.2-1
- Move the executables to -bin subpackage. Not too useful.

* Wed Jan 11 2023 Doncho N. Gunchev <dgunchev@gmail.com> - 0.9.3.2-0
- Initial package
