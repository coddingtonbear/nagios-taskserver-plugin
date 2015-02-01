Nagios Plugin for monitoring Taskwarrior's Taskserver
=====================================================

1. Install this package using pip::

    pip install nagios-taskserver-plugin

   or from a clone of this repository using pip::

    pip install .

   or from a clone of this repository using setup.py::

    python setup.py install

2. Copy ``plugin/taskserver.cfg`` and ``plugin/restart_taskserver.cfg`` into your nagios plugin path.
   On Ubuntu 12.04 this will be ``/etc/nagios-plugins/config``.
3. Add a new service definition to your nagios services configuration (e.g. ``/etc/nagios3/conf.d/services_nagios2.conf``); for example::

    # check that taskserver is running
    define service {
        hostgroup_name                  taskservers
        service_description             Taskserver
        check_command                   check_taskserver!/path/to/taskrc
        use                             generic-service
        notification_interval           0
        event_handler                   restart_taskserver!sudo service taskd restart
    }

4. Add a hostgroup matching the hostgroup name above to your hostgroup configuration (e.g. ``/etc/nagios3/conf.d/hostgroups_nagios2.conf``):
   
   ::
   
       define hostgroup {
            hostgroup_name                  taskservers
            alias                           Taskd Servers
            members                         your_hostname
       }

