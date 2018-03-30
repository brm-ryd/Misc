require 'selenium-webdriver'

Before do
  @browser = selenium::WebDriver.for :firefox
end

After do
  @browser.quit
end
