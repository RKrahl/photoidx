%define pkgname		 photo

Name:		python-%{pkgname}
Version:	0.1
Release:	1
Summary:	Tools for tagging photo collections
License:	Apache-2.0
Group:		Development/Languages/Python
Source:		%{pkgname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-devel >= 2.6
Requires:	python-PyYAML
Requires:	python-pyexiv2
%if 0%{?suse_version}
BuildRequires:	fdupes
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package provides a Python library and a command line tool for
maintaining tags in a collection of photos.


%prep
%setup -q -n %{pkgname}-%{version}


%build
python setup.py build


%install
python setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}
%__mv %{buildroot}%{_bindir}/photoidx.py %{buildroot}%{_bindir}/photoidx
%if 0%{?suse_version}
%fdupes %{buildroot}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/*


%changelog
