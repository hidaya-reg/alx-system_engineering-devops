#!/usr/bin/env ruby
# regular expression

puts ARGV[0].scan(/^[0-9]{10}$/).join
