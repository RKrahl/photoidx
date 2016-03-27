%define pkgname		 photo

Name:		python-%{pkgname}
Version:	0.3
Release:	1
Summary:	Tools for managing photo collections
License:	Apache-2.0
Group:		Development/Languages/Python
Source:		%{pkgname}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	python-devel >= 2.7
Requires:	python-PyYAML
Requires:	python-gexiv2
%if 0%{?suse_version}
BuildRequires:	fdupes
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package provides a Python library and a command line tool for
maintaining tags in a collection of photos.


%package qt
Summary:	Tools for managing photo collections
Requires:	python-%{pkgname} = %{version}
Requires:	python-pyside

%description qt
This package provides an image viewer for collection of photos.


%prep
%setup -q -n %{pkgname}-%{version}


%build
python setup.py build


%install
python setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}
%__mv %{buildroot}%{_bindir}/photoidx.py %{buildroot}%{_bindir}/photoidx
%__mv %{buildroot}%{_bindir}/imageview.py %{buildroot}%{_bindir}/imageview
%if 0%{?suse_version}
%fdupes %{buildroot}
%endif


%check
python setup.py test


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc README.rst
%{python_sitelib}/*
%exclude %{python_sitelib}/photo/qt
%{_bindir}/photoidx

%files qt
%defattr(-,root,root)
%{python_sitelib}/photo/qt
%{_bindir}/imageview


%changelog
