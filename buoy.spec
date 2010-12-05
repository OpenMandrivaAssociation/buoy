%define name    buoy
%define version 1.9
%define release %mkrel 2

Name:           %{name}
Version:        %{version}
Release:        %{release}

Summary:        A toolkit for creating user interfaces in Java programs
URL:            http://buoy.sourceforge.net/
Group:          Development/Java

Source0:        Buoy%{version}.zip
Source1:        Buoyx%{version}.zip
# Fix rpmlint fail
Patch0:         fix-indexed-jars.patch
# The original ant build doesnt make buoyx's javadoc
Patch1:         fix-javadoc.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:        Public Domain

BuildArch:      noarch

BuildRequires:  java-rpmbuild
BuildRequires:  ant
BuildRequires:  ant-nodeps

Requires:       java >= 1.4

%description
Buoy is a library for creating user interfaces in Java programs. 
It is built on top of Swing, but provides a completely new set
of classes to represent graphical components.

The current version of Buoy is 1.9, released May 1, 2008.
It is stable, extensively tested, and ready for production use. 


%files
%defattr(-,root,root,-)
%doc AboutBuoy.html
%_javadir/*.jar

#--------------------------------------------------------------------

%package javadoc
Summary:        Javadoc for buoy
Group:          Development/Java

%description javadoc
Javadoc for buoy.


%files javadoc
%defattr(-,root,root,-)
%_javadocdir/*

#--------------------------------------------------------------------

%prep
# %setup -q -n Buoy\ Folder  Doesnt work
# because of the space in the dirname 
%setup -qc -a1
cp -r Buoy\ Folder/* .
# renaming the folder
mv Buoyx\ Folder src
mv buoy src/
rm src/Buoyx.jar
%patch0 -p0
%patch1 -p0

%build
export CLASSPATH="."
%ant -buildfile buoy.xml dist docs

%install
rm -rf $RPM_BUILD_ROOT

%__install -dm 755 $RPM_BUILD_ROOT%_javadir
%__install -m 644 Buoy.jar $RPM_BUILD_ROOT%_javadir/%{name}-%{version}.jar
%__install -m 644 Buoyx.jar $RPM_BUILD_ROOT%_javadir/%{name}x-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%_javadir/%{name}.jar
ln -s %{name}x-%{version}.jar $RPM_BUILD_ROOT%_javadir/%{name}x.jar

# javadoc
%__install -dm 755 $RPM_BUILD_ROOT%_javadocdir/%{name}-%{version}
cd docs
cp -pr * $RPM_BUILD_ROOT%_javadocdir/%{name}-%{version}
cd ..
ln -s %{name}-%{version} $RPM_BUILD_ROOT%_javadocdir/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

