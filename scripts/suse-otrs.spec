# --
# RPM spec file for SuSE Linux of the OpenTRS package
# Copyright (C) 2002 Martin Edenhofer <bugs+rpm@otrs.org>
# --
# $Id: suse-otrs.spec,v 1.10 2002-05-09 23:50:23 martin Exp $
# --
# This software comes with ABSOLUTELY NO WARRANTY. For details, see 
# the enclosed file COPYING for license information (GPL). If you 
# did not receive this file, see http://www.gnu.org/licenses/gpl.txt.
# --
#
# please send bugfixes or comments to bugs+rpm@otrs.org
#
# --
Summary:      The Open Ticket Request System. 
Name:         otrs
Version:      0.5
Copyright:    GNU GENERAL PUBLIC LICENSE Version 2, June 1991
Group:        Applications/Mail
Provides:     otrs 
Requires:     perl perl-DBI perl-Date-Calc perl-GD perl-MIME-Base64 perl-MailTools perl-MIME-Lite perl-MIME-tools perl-Net-DNS perl-Syslog perl-Digest-MD5 apache mod_perl mysql mysql-client perl-Msql-Mysql-modules mysql-shared
Autoreqprov:  on
Release:      BETA4
Source0:      otrs-%{version}-%{release}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
The Open Ticket Request System (http://otrs.org/) is a web based ticket system.

Feedback: feedback@otrs.org


Authors:
--------
    Carsten Gross <carsten@siski.de>
    Franz Breu <breu.franz@bogen.net>
    Stefan Wintermeyer <stefan@wintermeyer.de>
    Martin Edenhofer <martin+rpm@otrs.org>

  Feature list:
  - Agent web interface for viewing and working on all customer requests.
  - Admin web interface for changing system things.
  - Customer web interface for viewing and sending infos to the agents.
  - Central database which contains all configuration, customer information.
  - Custom queue view.
  - Ticket locking.
  - Ticket autoreplies (standard responses)
  - Ticket history, evolution of ticket status and actions taken on ticket
  - Abaility to add notes (with different note types) to a ticket.
  - Ticket zoom feature
  - Tickets can be bounced or forwarded to other email addresses.
  - Ticket can be moved to a different queue (this is helpful if emails are
     for a specific subject)
  - Fulltext search.
  - Ticket priority.
  - Creation and configuration of user accounts, and groups
  - Creation of standard responses
  - Signature and Salutation configuration
  - Multi language support.
  - Email-notification of administrators.
  - Email-notification sent to problem reporter (by create, locked, deleted,
     moved and closed)
  - Submitting update-info (via email or webinterface).
  - Deadlines for trouble tickets.
  - Different levels of permissions/access-rights.


SuSE series: ap


%prep
%setup -n OpenTRS
# remove CVS dirs
find . -name CVS | xargs rm -rf
# remove old sessions, articles and spool
rm -f var/sessions/*
rm -rf var/article/*
rm -rf var/spool/*


%build
# nothing


%install
# delete old RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
# set DESTROOT
export DESTROOT="/opt/OpenTRS/"
# create RPM_BUILD_ROOT DESTROOT
mkdir -p $RPM_BUILD_ROOT/$DESTROOT/
# copy files
cp -R . $RPM_BUILD_ROOT/$DESTROOT
# Install init-Script and rc.config entry
install -d -m 755 $RPM_BUILD_ROOT/etc/init.d
install -d -m 755 $RPM_BUILD_ROOT/usr/sbin
install -d -m 744 $RPM_BUILD_ROOT/var/adm/fillup-templates

install -m 644 scripts/suse-fillup-template-rc.config.otrs $RPM_BUILD_ROOT/var/adm/fillup-templates/sysconfig.otrs

install -m 755 scripts/suse-rcotrs $RPM_BUILD_ROOT/etc/init.d/otrs
rm -f $RPM_BUILD_ROOT/sbin/otrs
ln -s ../../etc/init.d/otrs $RPM_BUILD_ROOT/usr/sbin/rcotrs


%post
# useradd
export OTRSUSER=otrs
echo -n "Check OpenTRS user (/etc/passwd)... " 
if cat /etc/passwd | grep $OTRSUSER > /dev/null ; then 
    echo "$OTRSUSER exists."
else
    useradd $OTRSUSER -d /opt/OpenTRS/ -s /bin/false && echo "$OTRSUSER added."
fi

# set permission
/opt/OpenTRS/bin/SetPermissions.sh
# set Config.pm permission to be writable for the webserver 
chown wwwrun /opt/OpenTRS/Kernel/Config.pm

# rc.config
%{fillup_and_insserv -s otrs START_OTRS}

# add suse-httpd.include.conf to apache.rc.config
APACHERC=/etc/sysconfig/apache

OTRSINCLUDE=/opt/OpenTRS/scripts/suse-httpd.include.conf
sed 's+^HTTPD_CONF_INCLUDE_FILES=.*$+HTTPD_CONF_INCLUDE_FILES='$OTRSINCLUDE'+' \
$APACHERC > /tmp/apache.rc.config.tmp && mv /tmp/apache.rc.config.tmp $APACHERC 

# note
echo ""
echo "Next steps: "
echo ""
echo "[SuSEconfig]"
echo " Execute SuSEconfig to configure the webserver."
echo ""
echo "[OpenTRS services]"
echo " Start OpenTRS 'rcotrs start' (rcotrs {start|stop|status|restart})."
echo ""
echo "Have fun!"
echo ""
echo " Your OpenTRS Team"
echo ""

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) /opt/OpenTRS/Kernel/Config.pm
%config(noreplace) /opt/OpenTRS/var/log/TicketCounter.log
%config(noreplace) /opt/OpenTRS/.procmailrc
%config(noreplace) /opt/OpenTRS/Kernel/Output/HTML/Standard/Motd.dtl
%config(noreplace) /opt/OpenTRS/Kernel/Output/HTML/Standard/Login.dtl

/etc/init.d/otrs
/usr/sbin/rcotrs

/opt/OpenTRS/Kernel/Language.pm
/opt/OpenTRS/Kernel/Language/*
/opt/OpenTRS/Kernel/Modules/*
/opt/OpenTRS/Kernel/Output/HTML/*.pm
/opt/OpenTRS/Kernel/Output/HTML/Lite/*.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Header.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Footer.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Error.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Test.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Queue*.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Agent*.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Admin*.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/System*.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Ticket*.dtl
/opt/OpenTRS/Kernel/Output/HTML/Standard/Installer*.dtl
/opt/OpenTRS/Kernel/System/*
/opt/OpenTRS/bin/*
/opt/OpenTRS/scripts/*
/opt/OpenTRS/var/article/
/opt/OpenTRS/var/httpd/*
/opt/OpenTRS/var/sessions/
/opt/OpenTRS/var/spool/

/var/adm/fillup-templates/sysconfig.otrs

%doc INSTALL TODO COPYING READM* doc/* install*


%changelog
* Sat May 05 2002 - martin+rpm@otrs.org
- added Kernel/Output/HTML/Standard/Motd.dtl as config file 
* Thu Apr 16 2002 - martin+rpm@otrs.org
- moved to SuSE 8.0 support
* Sun Feb 03 2002 - martin+rpm@otrs.org
- added SuSE-Apache support
* Wed Jan 30 2002 - martin+rpm@otrs.org
- added to useradd bash=/bin/false
* Sat Jan 12 2002 - martin+rpm@otrs.org
- added SuSE like rc scripts
* Tue Jan 10 2002 - martin+rpm@otrs.org 
- new package created

