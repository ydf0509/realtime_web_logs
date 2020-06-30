# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2019/6/14 17:33
import os
from pathlib import Path
from flask import Flask, send_from_directory, url_for, jsonify, request, render_template, current_app, abort, g, \
    send_file, redirect
from flask_httpauth import HTTPBasicAuth
from flask_bootstrap import Bootstrap
from function_scheduling_distributed_framework.utils import LogManager, nb_print, time_util

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

print(str((Path(__file__).parent / Path('ydf_dir')).absolute()))
app = Flask(__name__, template_folder=str((Path(__file__).parent / Path('ydf_dir')).absolute()))
app.config['JSON_AS_ASCII'] = False
app.config['REFRESH_MSEC'] = 1000
auth = HTTPBasicAuth()
LogManager(app.logger.name).get_logger_and_add_handlers()
bootstrap = Bootstrap(app)


@app.route('/favicon.ico')
def favicon():
    print(Path(__file__).parent / Path('ydf_dir/').absolute())
    return send_from_directory(str(Path(__file__).parent / Path('ydf_dir/').absolute()),
                               'log_favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/ajax0/<path:fullname>/")
def info0(fullname):
    fullname = f'/{fullname}'
    position = int(request.args.get('position'))
    current_app.logger.debug(position)
    # if os.path.isfile(full_name):
    #     fo = open(full_name,encoding='utf8')
    #     content  = fo.read()
    #     return content
    # else :
    #     return "There is no log file"

    with open(fullname, 'rb') as f:
        try:
            if position == 0:
                f.seek(-50000, 2)
            else:
                f.seek(position, 0)
        except Exception:
            current_app.logger.exception('读取错误')
            f.seek(0, 0)
        content_text = f.read().decode()
        # nb_print([content_text])
        content_text = content_text.replace('\n', '<br>')
        # nb_print(content_text)
        position_new = f.tell()
        current_app.logger.debug(position_new)
        # nb_print(len(content_text))

        return jsonify(content_text=content_text, position=position_new)


@app.route("/ajax/<path:fullname>/")
def info(fullname):
    fullname = f'/{fullname}'
    position = int(request.args.get('position'))
    current_app.logger.debug(position)
    # if os.path.isfile(full_name):
    #     fo = open(full_name,encoding='utf8')
    #     content  = fo.read()
    #     return content
    # else :
    #     return "There is no log file"

    with open(fullname, 'rb') as f:
        try:
            if position == 0:
                f.seek(-50000, 2)
            else:
                f.seek(position, 0)
        except Exception:
            current_app.logger.exception('读取错误')
            f.seek(0, 0)
        lines = f.readlines()
        content_text = ''
        for line in lines:
            line = line.strip().decode()
            if '- DEBUG -' in line:
                color = '#00FF00'
            elif '- INFO -' in line:
                color = '#00FFFF'
            elif '- WARNING -' in line:
                color = 'yellow'
            elif '- ERROR -' in line:
                color = '#FF00FF'
            elif '- CRITICAL -' in line:
                color = '#FF0033'
            else:
                color = ''
            content_text += f'<p style="color:{color}"> {line} </p>'

        # content_text = f.read().decode()
        # # nb_print([content_text])
        # content_text = content_text.replace('\n', '<br>')
        # # nb_print(content_text)
        position_new = f.tell()
        current_app.logger.debug(position_new)
        # nb_print(content_text)

        return jsonify(content_text=content_text, position=position_new)


@app.route("/view/<path:fullname>")
def view(fullname):
    view_html = '''
    <html>
    <head>
    <title>查看 %s </title>
    <script type="text/javascript" src="http://libs.baidu.com/jquery/2.1.1/jquery.min.js">
    </script>
    </head>
    <body>
    <div id="result"></div>
    <hr>
    <button onclick="toggle_scroll()"> 自动滚动浏览器滚动条 </button>
    &nbsp;
    <div style="display: inline" id="auto_scroll_stat">ON</div>
    <button id= "runButton"  style="margin-left:300px" onclick="startOrStop()"> 运行中 </button>
    <button id= "runButton"  style="margin-left:300px" > <a href="/%s/d" download="%s">下载 %s</a></button>
    </body>
    <script>
    var autoscroll = "ON";
    toggle_scroll = function(){
        if(autoscroll == "ON") autoscroll = "OFF";
        else autoscroll = "ON";
    }
    var position = 0;
    function downloadFile(){

    }
    get_log = function(){
     $.ajax({url: "/%s/a", data: {"position":position} ,success: function(result){
        console.debug(4444);
        var resultObj = result;
        console.debug(6666);
        //var html = document.getElementById("div_id").innerHTML;
        var html = $("#result").html();
        var  htmlShort = html.substr(-40000);
        console.debug(htmlShort);
        document.getElementById("result").innerHTML = htmlShort || "";
        console.debug($("#result").html());
        $("#result").append( resultObj.content_text);
        console.debug(resultObj.position);
        position = resultObj.position;
        if(autoscroll == "ON")
            window.scrollTo(0,document.body.scrollHeight);
        $("#auto_scroll_stat").text(autoscroll);
     }});
    }
    iid = setInterval(get_log,%s);
    status = 1;
    function startRun(){
            $("#runButton").text("运行中");
            iid = setInterval(get_log,%s);
            status = 1;
        }

    function stopRun(){
        $("#runButton").text("停止了");
        clearInterval(iid);
        status = 0;
    }
    function startOrStop(){
        if(status == 1){
            stopRun();}
        else
            {startRun();}
    }
    </script>
    </html>
    '''
    # return view_html % (logfilename,logfilename,logfilename,logfilename,logfilename, REFRESH_MSEC, REFRESH_MSEC)
    return render_template('/log_view_html.html', fullname=fullname)


@app.route('/download/<path:fullname>', )
def download_file(fullname):
    current_app.logger.debug(fullname)
    return send_file(f'/{fullname}')
    # return send_from_directory(f'/{logs_dir}',
    #                            filename, as_attachment=True, )


@app.route('/scan/', )
@app.route('/scan/<path:logs_dir>', )
def index(logs_dir=''):
    current_app.logger.debug(logs_dir)
    file_ele_list = list()
    dir_ele_list = list()
    for f in (Path('/') / Path(logs_dir)).iterdir():
        fullname = str(f).replace('\\', '/')
        if f.is_file():
            # current_app.logger.debug(str(f).replace('\\', '/')[1:])
            # current_app.logger.debug((logs_dir, str(f).replace('\\','/')[1:]))
            current_app.logger.debug(str(f))
            current_app.logger.debug(url_for('download_file', fullname=fullname[0:]))
            # current_app.logger.debug(url_for('download_file', logs_dir='', filename='windows_to_linux_syn_config.json'))
            file_ele_list.append({'is_dir': 0, 'filesize': os.path.getsize(f) / 1000000,
                                  'last_modify_time': time_util.DatetimeConverter(
                                      os.stat(str(fullname)).st_mtime).datetime_str,
                                  'url': url_for('view', fullname=fullname[1:]),
                                  'download_url': url_for('download_file', fullname=fullname[1:]),
                                  'fullname': fullname})
        if f.is_dir():
            fullname = str(f).replace('\\', '/')
            dir_ele_list.append({'is_dir': 1, 'filesize': 0,
                                 'last_modify_time': time_util.DatetimeConverter(os.stat(str(f)).st_mtime).datetime_str,
                                 'url': url_for('index', logs_dir=fullname[1:]),
                                 'download_url': url_for('index', logs_dir=fullname[1:]), 'fullname': fullname})

    return render_template('dir_view.html', ele_list=dir_ele_list + file_ele_list, logs_dir=logs_dir)


@app.route('/', )
def root():
    return redirect(url_for('index', logs_dir=''))


@app.template_filter()
def file_filter(filefullname, file_name_part):
    if file_name_part == 1:
        return str(Path(filefullname).parent)
    if file_name_part == 2:
        return str(Path(filefullname).name)


@app.context_processor
def dir_processor():
    def format_logs_dir_to_multi(logs_dir):
        parent_dir_list = list()
        pa = Path(f'/{logs_dir}')
        while True:
            nb_print(pa.as_posix())
            parent_dir_list.append({'url': url_for('index', logs_dir=pa.as_posix()[1:]), 'dir_name': pa.name[:]})
            pa = pa.parent
            if pa == Path('/'):
                parent_dir_list.append({'url': url_for('index', logs_dir=''), 'dir_name': '根目录'})
                break
        nb_print(parent_dir_list)
        return parent_dir_list

    return dict(format_logs_dir_to_multi=format_logs_dir_to_multi)


@auth.verify_password
def verify_password(username, password):
    if (username == 'user' and password == 'mtfy123') or (username == 'admin' and password == 'pass123'):
        return True
    return False


@app.before_request
@auth.login_required
def before_request():
    pass


def main():
    print(app.url_map)
    # app.run(host="0.0.0.0", port=9999,  )
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(9999)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()
