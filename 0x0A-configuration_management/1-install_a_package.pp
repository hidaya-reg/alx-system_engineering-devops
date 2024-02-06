# 1-install_a_package.pp

# Define package resource for flask
package { 'flask':
  ensure   => '2.1.0',
  provider => 'pip3',
  require  => Package['python3-pip'],
}

# Ensure python3-pip is installed
package { 'python3-pip':
  ensure => installed,
}

# Define package resource for Werkzeug
package { 'werkzeug':
  ensure   => '2.1.1',  # Update the version according to Flask's requirements
  provider => 'pip3',
  require  => Package['python3-pip'],
}
