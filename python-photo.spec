%bcond_with tests
%global distname photo

Name:		python3-%{distname}
Version:	$version
Release:	0
Summary:	$description
Url:		$url
License:	Apache-2.0
Group:		Productivity/Graphics/Viewers
Source:		%{distname}-%{version}.tar.gz
BuildRequires:	fdupes
BuildRequires:	python3-PyYAML
BuildRequires:	python3-devel >= 3.6
BuildRequires:	python3-exif >= 0.8.3
%if %{with tests}
BuildRequires:	python3-distutils-pytest
BuildRequires:	python3-pytest
BuildRequires:	python3-pytest-dependency
%endif
Requires:	python3-PyYAML
Requires:	python3-exif >= 0.8.3
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package provides a Python library and a command line tool for
maintaining tags in a collection of photos.


%package qt
Summary:	Tools for managing photo collections
Requires:	python3-%{distname} = %{version}
Requires:	python3-pyside
Recommends:	python3-vignette >= 4.3.0

%description qt
This package provides an image viewer for collection of photos.


%prep
%setup -q -n %{distname}-%{version}


%build
python3 setup.py build


%install
python3 setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}
%__mv %{buildroot}%{_bindir}/photoidx.py %{buildroot}%{_bindir}/photoidx
%__mv %{buildroot}%{_bindir}/imageview.py %{buildroot}%{_bindir}/imageview
%fdupes %{buildroot}


%if %{with tests}
%check
python3 setup.py test
%endif


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
