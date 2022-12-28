%bcond_without tests
%global distname photoidx

Name:		python3-%{distname}
Version:	$version
Release:	0
Url:		$url
Summary:	$description
License:	Apache-2.0
Group:		Productivity/Graphics/Viewers
Source:		%{distname}-%{version}.tar.gz
BuildRequires:	fdupes
BuildRequires:	python3-base >= 3.6
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-pytest
BuildRequires:	python3-distutils-pytest
BuildRequires:	python3-pytest-dependency
BuildRequires:	python3-PyYAML
BuildRequires:	python3-ExifRead >= 2.2.0
%endif
Provides:	python3-photo = %{version}-%{release}
Obsoletes:	python3-photo < %{version}-%{release}
Requires:	python3-PyYAML
Requires:	python3-ExifRead >= 2.2.0
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This package maintains indices for photo collections.  The index is
stored as a YAML file and contains metadata and tags describing the
photos.  The photos are accessed read only.

This package provides a Python library and a command line tool for
creating and managing the index.


%package qt
Summary:	Tools for managing photo collections
Provides:	python3-photo-qt = %{version}-%{release}
Obsoletes:	python3-photo-qt < %{version}-%{release}
Requires:	python3-%{distname} = %{version}
Requires:	python3-pyside
Recommends:	python3-vignette >= 4.3.0

%description qt
This package maintains indices for photo collections.  The index is
stored as a YAML file and contains metadata and tags describing the
photos.  The photos are accessed read only.

This package provides an image viewer.


%prep
%setup -q -n %{distname}-%{version}


%build
python3 setup.py build


%install
python3 setup.py install --optimize=1 --prefix=%{_prefix} --root=%{buildroot}
%__mv %{buildroot}%{_bindir}/photo-idx.py %{buildroot}%{_bindir}/photo-idx
%__mv %{buildroot}%{_bindir}/imageview.py %{buildroot}%{_bindir}/imageview
%fdupes %{buildroot}


%if %{with tests}
%check
python3 setup.py test
%endif


%files
%defattr(-,root,root)
%doc README.rst CHANGES.rst
%license LICENSE.txt
%{python3_sitelib}/*
%exclude %{python3_sitelib}/photoidx/qt
%{_bindir}/photo-idx

%files qt
%defattr(-,root,root)
%{python3_sitelib}/photoidx/qt
%{_bindir}/imageview


%changelog
