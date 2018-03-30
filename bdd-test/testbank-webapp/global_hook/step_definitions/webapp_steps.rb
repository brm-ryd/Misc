Given /^i have \$(\d+) in my account$/ do | balance |
  @browser.navigate to 'http://127.0.0.1/account'
end
