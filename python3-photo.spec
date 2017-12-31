%define pkgname		 photo

Name:		python3-%{pkgname}
Version:	0.6
Release:	1
Summary:	Tools for managing photo collections
License:	Apache-2.0
Group:		Development/Languages/Python
Url:		https://github.com/RKrahl/photo-tools
Source:		%{pkgname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python3-devel
BuildRequires:	python3-PyYAML
BuildRequires:	python3-gexiv2
BuildRequires:	python3-pytest
%if 0%{?sle_version} >= 150000 || 0%{?sle_version} == 120300
BuildRequires:	python3-pytest-dependency
%endif
BuildRequires:	python3-distutils-pytest
Requires:	python3-PyYAML
Requires:	python3-gexiv2
%if 0%{?suse_version}
BuildRequires:	fdupes
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package provides a Python library and a command line tool for
maintaining tags in a collection of photos.


%package qt
Summary:	Tools for managing photo collections
Requires:	python3-%{pkgname} = %{version}
Requires:	python3-pyside
Recommends:	python3-vignette

%description qt
This package provides an image viewer for collection of photos.


%prep
%setup -q -n %{pkgname}-%{version}


%build
python3 setup.py build


%install
python3 setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}
%__mv %{buildroot}%{_bindir}/photoidx.py %{buildroot}%{_bindir}/photoidx
%__mv %{buildroot}%{_bindir}/imageview.py %{buildroot}%{_bindir}/imageview
%if 0%{?suse_version}
%fdupes %{buildroot}
%endif


%check
python3 setup.py test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README.rst CHANGES
%{python3_sitelib}/*
%exclude %{python3_sitelib}/photo/qt
%{_bindir}/photoidx

%files qt
%defattr(-,root,root)
%{python3_sitelib}/photo/qt
%{_bindir}/imageview


%changelog
