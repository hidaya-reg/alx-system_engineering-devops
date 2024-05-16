# Enable the user to login and open files without error

# Adjust hard file limit for user holberton
exec { 'increase-hard-file-limit-for-holberton':
  command => 'sed -i "/holberton hard/s/5/50000/" /etc/security/limits.conf',
  path    => ['/usr/local/bin/', '/bin/'],
}

# Adjust soft file limit for user holberton
exec { 'increase-soft-file-limit-for-holberton':
  command => 'sed -i "/holberton soft/s/4/50000/" /etc/security/limits.conf',
  path    => ['/usr/local/bin/', '/bin/'],
}
