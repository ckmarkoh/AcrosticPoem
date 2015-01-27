#-*- coding:utf-8 -*
#!/usr/bin/python
from bottle import route, get, post, request, run 
from AcrosticPoem import PoemGen
import json

m = PoemGen()

@get('/poem') # or @route('/login')
def poem():
    return ''' 
        <h1>藏頭詩產生器</h1>
        <hr>
        <form action="/poem" method="post">
            請輸入要藏的句子: <input name="input_str" type="text" value=""><br/>
            每句字數：<select name="length">
              <option value="5" selected="selected">五言</option>
              <option value="7">七言</option>
            </select><br/>
            藏字位置<select name="position">
              <option value="1" selected="selected">第一個字</option>
              <option value="2">第二個字</option>
              <option value="3">第三個字</option>
              <option value="4">第四個字</option>
            </select><br/>
            回傳格式<select name="type">
              <option value="html" selected="true">html</option>
              <option value="json">json</option>
            </select><br/>
            <input value="Go" type="submit" />
        </form>
    '''

@post('/poem') # or @route('/login', method='POST')
def do_poem():
    input_str= request.forms.get('input_str')
    length= request.forms.get('length')
    position= request.forms.get('position')
    rtype= request.forms.get('type')

    input_str_arg = "%s -l %s -p %s"%(input_str,length, position)
    result = m.main(input_str_arg.split(),print_out=False)
    if rtype == 'html':
      return ''' 
      <p>
      原文: %s <br/>
      </p><p>
      詩: <br/> %s
      </p>
      <a href="./poem" >back</a>
      '''%(input_str,result.encode('utf-8').replace('\n','<br/>'))
    elif rtype == 'json':
      return ''' 
        %s
      '''%(json.dumps({'input':input_str,'output':result.encode('utf-8').replace('\n',' ')}))
    #if check_login(username, password):

run( host='localhost', port=3000, debug=True)

