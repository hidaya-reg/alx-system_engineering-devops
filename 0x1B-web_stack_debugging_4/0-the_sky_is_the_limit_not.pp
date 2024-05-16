# Increase the amount of traffic an Nginx server can handle

# Adjust ULIMIT for Nginx server
exec { 'increase-nginx-ulimit':
  command => 'sed -i "s/15/4096/" /etc/default/nginx',
  path    => '/usr/local/bin/:/bin/'
}

# Restart Nginx
-> exec { 'restart-nginx':
  command => 'nginx restart',
  path    => '/etc/init.d/'
}
