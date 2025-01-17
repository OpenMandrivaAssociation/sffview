Summary:	A program to view structured fax files (sff)
Name:		sffview
Version:	0.4
Release:	%mkrel 3
License:	MIT
Group:		Communications
URL:		https://sfftools.sourceforge.net/sffview.html
Source0:	sffview_0_4_src.zip
Source1:	sffview-16x16.png
Source2:	sffview-32x32.png
Source3:	sffview-48x48.png
Patch0:		sffview-cflags.diff
# Fix build with GCC 4.3 - AdamW 2008/12
Patch1:		sffview-0.4-gcc43.patch
# From upstream CVS: fix code to work with unicode wx - AdamW 2008/12
Patch2:		sffview-0.4-wx_unicode.patch
# From upstream CVS: don't apply a workaround with newer wx versions
# where it's not needed (like ours) - AdamW 2008/12
Patch3:		sffview-0.4-restrict_fix.patch
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
BuildRequires:	wxgtku-devel
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
    Peter Sch�fer

%prep

%setup -q -n %{name}
%patch0 -p0
%patch1 -p1 -b .gcc43
%patch2 -p0 -b .unicode
%patch3 -p0 -b .restrict

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build

%make \
    WXCONFIG_CPP="\`wx-config-unicode --cflags\`" \
    WXCONFIG_LD="\`wx-config-unicode --libs\`" \
    CFLAGS="%{optflags} -Wall"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -m0755 %{name} %{buildroot}%{_bindir}

# icon
install -d %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

install -m0644 sffview-48x48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m0644 sffview-32x32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m0644 sffview-16x16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

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
Categories=Graphics;2DGraphics;Viewer;
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
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/*.desktop

