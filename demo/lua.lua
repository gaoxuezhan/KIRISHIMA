function main(splash, args)

  splash:set_user_agent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')

  assert(splash:go(args.url))
  assert(splash:wait(0.5))

  input1 = splash:select("#nav_flight")
  input1:mouse_click()

  assert(splash:wait(5))

  input2 = splash:select("#ArriveCity1TextBox")
  input2:mouse_click()
  input2:send_text('深圳')


  input1 = splash:select("#DepartCity1TextBox")
  input1:mouse_click()
  input1:send_text('北京')



  input3 = splash:select("#DepartDate1TextBox")
  input3:mouse_click()
  assert(splash:wait(1))
  input3:mouse_click()
  input3:send_text('2018-11-03\r')


  splash:select("#mainbody > container"):mouse_click()

  input4 = splash:select("#search_btn")
  input4:mouse_click()
  input4:mouse_click()

  assert(splash:wait(30))

  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end