Summary:	A program to view structured fax files (sff)
Name:		sffview
Version:	0.4
Release:	%mkrel 2
License:	MIT
Group:		Communications
URL:		http://sfftools.sourceforge.net/sffview.html
Source0:	sffview_0_4_src.zip
Source1:	sffview-16x16.png
Source2:	sffview-32x32.png
Source3:	sffview-48x48.png
Patch0:		sffview-cflags.diff
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:	wxGTK2.6-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The CAPI interface for programming ISDN hardware expects and gives you faxes in
the "Structured Fax File" (SFF) format.

SffView is a viewer for SFF-files. SffView is written in C++ using the
wxWindows/wxGTK toolkit and is therefore available for Linux and Windows
(wxWindows is a platform independent toolkit and wxGTK is a unix implementation
based on GTK+, see wxWindows homepage).

Authors:
--------
    Peter Schäfer

%prep

%setup -q -n %{name}
%patch0 -p0

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build

%make \
    WXCONFIG_CPP="\`wx-config-ansi --cflags\`" \
    WXCONFIG_LD="\`wx-config-ansi --libs\`" \
    CFLAGS="%{optflags} -Wall"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -m0755 %{name} %{buildroot}%{_bindir}

# menu

# icon
install -d %{buildroot}%{_liconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}

install -m0644 sffview-48x48.png %{buildroot}%{_liconsdir}/%{name}.png
install -m0644 sffview-32x32.png %{buildroot}%{_iconsdir}/%{name}.png
install -m0644 sffview-16x16.png %{buildroot}%{_miconsdir}/%{name}.png

# XDG menu
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=SffView
Comment=%{summary}
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Graphics;X-MandrivaLinux-Multimedia-Graphics;
EOF

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc doc/* testfax.sff
%{_bindir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/*.desktop


