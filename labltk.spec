%ifarch %{ocaml_native_compiler}
%global native_compiler 1
%else
%global native_compiler 0
%endif
Name:                ocaml-labltk
Version:             8.06.4
Release:             1
Summary:             Tcl/Tk interface for OCaml
License:             LGPLv2+ with exceptions
URL:                 https://github.com/garrigue/labltk 
Source0:             https://github.com/garrigue/labltk/archive/labltk-%{version}/labltk-%{version}.tar.gz
# This adds debugging (-g) everywhere.
Patch1:              labltk-8.06.0-enable-debugging.patch
Patch2:              labltk-8.06.4-enable-more-debugging.patch
BuildRequires:       ocaml tcl-devel tk-devel
%description
labltk or mlTk is a library for interfacing OCaml with the scripting
language Tcl/Tk (all versions since 8.0.3, but no betas).

%package devel
Summary:             Tcl/Tk interface for OCaml
Requires:            %{name}%{?_isa} = %{version}-%{release}
%description devel
labltk or mlTk is a library for interfacing OCaml with the scripting
language Tcl/Tk (all versions since 8.0.3, but no betas).
This package contains the development files.

%prep
%setup -q -n labltk-labltk-%{version}
%patch1 -p1
%patch2 -p1
find -name .gitignore -delete
find -type f | xargs sed -i -e 's/-warn-error/-w/g'

%build
./configure
unset MAKEFLAGS
%if !%{native_compiler}
make byte
%else
make all
make opt
%endif

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk
mkdir -p $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
make install \
    BINDIR=$RPM_BUILD_ROOT%{_bindir} \
    INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/labltk \
    STUBLIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
%if %{native_compiler}
install -m 0644 camltk/*.o $RPM_BUILD_ROOT%{_libdir}/ocaml/labltk
%endif

%files
%doc Changes README.mlTk
%dir %{_libdir}/ocaml/labltk
%{_libdir}/ocaml/labltk/*.cmi
%{_libdir}/ocaml/labltk/*.cma
%{_libdir}/ocaml/labltk/*.cmo
%{_libdir}/ocaml/stublibs/dlllabltk.so

%files devel
%doc README.mlTk
%doc examples_camltk
%doc examples_labltk
%{_bindir}/labltk
%{_bindir}/ocamlbrowser
%{_libdir}/ocaml/labltk/labltktop
%{_libdir}/ocaml/labltk/pp
%{_libdir}/ocaml/labltk/tkcompiler
%{_libdir}/ocaml/labltk/*.a
%if %{native_compiler}
%{_libdir}/ocaml/labltk/*.cmxa
%{_libdir}/ocaml/labltk/*.cmx
%{_libdir}/ocaml/labltk/*.o
%endif
%{_libdir}/ocaml/labltk/*.mli

%changelog
* Fri Oct 9 2020 maminjie <maminjie1@huawei.com> - 8.06.4-1
- package init
