import dbus

def disable_desktop_notifications():
    bus = dbus.SessionBus()
    proxy = bus.get_object('org.freedesktop.Notifications', '/org/freedesktop/Notifications')
    interface = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
    
    # Set the property to disable notifications
    interface.Set('org.freedesktop.Notifications', 'Notify', False)

# Example usage
disable_desktop_notifications()  # Disable desktop notifications

