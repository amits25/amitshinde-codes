#####################################################################
'''
    # Author  :: Amit Shinde
    # Date    :: 20 June 2020
    # Platform:: Linux 16.04/18.04 LTS
    # DESC    :: Docker Functions code with python flask module
       	      -  We Can Docker From UI
       	      -  This Code Will Perform Following Operations:
       	                          1. Install Git
                                  2. Install Docker
                                  3. Docker Server Login
                                  4. Docker Functions
                                  #  Docker Images:
                                    i.   List Of All Docker IMG's
                                    ii.  IMG Del
                                    iii. IMG Run
                                    iv.  IMG Pull
                                    v.   IMG Build with Dockerfile & Requirement.txt
                                  #  Docker Containers:
                                    i.   List Of All Docker Containers
                                    ii.  Del Containers
                                    iii. Start Container
                                    iv.  Stop Container
                                    v.   Exec Command On Start Container

             - Note: You Can See Current Running Docker command Process Output On Browser.
                    (Ubuntu Terminal On web-Browser)
    # Prerequisite Packages:(linux 16.04 LTS)
        - Install Python flask Module
        - Install Python http Module
        - Install Python werkzeug Module
        - Install Gotty Linux package
    # Application Will Used Following Ports:
        - tcp::8085 port - Mani App Server
        - tcp::9000 port - Gotty server
    # Process To Run App:
        - command   : python docker-url.py
        - App url   : http://localhost:8085/
        - gotty url : http://127.0.0.1:9000/
    # Port Issues:
        - If You Face Port Busy Error While Run Appl Then Please execute Following Comm.
            - sudo lsof -i tcp:8085
            - This Command Shows PID
            - sudo kill -9 PID
        - Then Try To Run Appl Again
        $ gotty port Issues
            - sudo lsof -i tcp:9000
            - This Command Shows PID
            - sudo kill -9 PID
'''

#####################################################################

from flask import Flask, render_template, redirect, url_for, request
import os
import subprocess
from http import cookies
import sqlite3
import base64
from werkzeug import secure_filename

app = Flask(__name__, template_folder='template')
PEOPLE_FOLDER = os.path.join('static', 'files')
app.config['Images'] = PEOPLE_FOLDER
C = cookies.SimpleCookie()


def DB():
    global conn, cursor
    conn = sqlite3.connect("Database.db")
    cursor = conn.cursor()


def tcp_port():
    count = 0
    query = "sudo lsof -i tcp:9000 > /home/kpit/PycharmProjects/Docker_UI/venv/static/files/tcp_port.txt"
    # print(query)
    res = os.system(query)
    adj_res = os.system("awk '{$2=$2};1' /home/kpit/PycharmProjects/Docker_UI/venv/static/files/tcp_port.txt > "
                        "/home/kpit/PycharmProjects/Docker_UI/venv/static/files/adj_tcp_port.txt")
    print(adj_res)
    if adj_res == 0:
        rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/adj_tcp_port.txt', 'r')
        Lines = rows.readlines()
        for line in Lines:
            if count == 0:
                print("Head-Line")
                count = 1
            else:
                print(line)
                word = line.split(" ")
                pid = word[1]
                # print(pid + "************************")
                pidQuery = "sudo kill -9 {}".format(pid)
                print(pidQuery)
                pidres = os.system(pidQuery)
                if pidres == 0:
                    print("tcp-port 90000 are not engaged")
                else:
                    print("tcp-port 90000 are engaged")


@app.route('/')
def homepage():
    return render_template('user/home.html')


@app.route('/git_Installation')
def git_installation():
    count = 0
    FileLines = []
    rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/git_installation.txt', 'r')
    Lines = rows.readlines()
    for line in Lines:
        # print(line)
        FileLines.append(line)
        count = count + 1

    return render_template('user/Installer.html', comm=FileLines, count=count)


@app.route('/Docker_Installation')
def docker_Installation():
    count = 0
    FileLines = []
    rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/Docker_installation.txt', 'r')
    Lines = rows.readlines()
    for line in Lines:
        # print(line)
        FileLines.append(line)
        count = count + 1
    return render_template('user/docker_Installer.html', comm=FileLines, count=count)


@app.route('/user_logout')
def user_logout():
    C.clear()
    return render_template('user/home.html')


@app.route('/main-menu')
def back_to_menu():
    return render_template('user/docker_login_success.html')


@app.route('/Docker_Login', methods=['GET', 'POST'])
def docker_login():
    error = None
    username = None
    if request.method == 'GET':
        return render_template('user/docker_login.html')
    else:
        if request.form['username'] == "amit" and request.form['password'] == "amit":
            # C["username"] = request.form['username']
            return render_template('user/docker_login_success.html', admin="AMIT")
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('user/docker_login.html', error=error)


@app.route('/Docker_Image_creator')
def docker_image_creator():
    REPOSITORY_list = []
    TAG_list = []
    IMAGE_ID_list = []
    CREATED_list = []
    SIZE_list = []
    query = "sudo docker images > /home/kpit/PycharmProjects/Docker_UI/venv/static/files/images.txt "
    os.system(query)
    os.system("awk '{$2=$2};1' /home/kpit/PycharmProjects/Docker_UI/venv/static/files/images.txt > "
              "/home/kpit/PycharmProjects/Docker_UI/venv/static/files/adj_images.txt")

    rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/adj_images.txt', 'r')
    Lines = rows.readlines()
    count = 0
    # Strips the newline character
    for line in Lines:
        if count == 0:
            # print("Title")
            count = count + 1
        else:
            # print("inside else")
            word = line.split(" ")
            REPOSITORY_list.append(word[0])
            TAG_list.append(word[1])
            # print(word[1])
            IMAGE_ID_list.append(word[2])
            CREATED_list.append(word[3])
            SIZE_list.append(word[6])
            count = count + 1

    count = count - 1

    return render_template('user/docker_images_list.html', repo=REPOSITORY_list, tag=TAG_list, Iid=IMAGE_ID_list,
                           create=CREATED_list, size=SIZE_list, count=count)


@app.route('/delete_IMG', methods=['GET', 'POST'])
def delete_IMG():
    error = None
    if request.method == 'POST':
        data = request.form['img_id']
        # print(data)
        query = "sudo docker rmi {}".format(data)
        # print(query)
        res = os.system(query)
        if res == 0:
            error = "Image with ID {} are deleted".format(data)
        else:
            error = "Image with ID {} are not deleted: may be there are some dependencies".format(data)

    return render_template('user/docker_images_del_status.html', error=error)


@app.route('/run_IMG', methods=['GET', 'POST'])
def Docker_Run_IMG():
    error = None
    tcp_port()
    if request.method == 'POST':
        data = request.form['img_run_id']
        C["return_ID"] = data
        # print(data)
        query = "gotty sudo docker run {} > /home/kpit/PycharmProjects/Docker_UI/venv/static/files/run_images.txt &".format(
            data)
        print(query)
        res = os.system(query)
        if res == 0:
            error = "Image with ID {} are Run_able".format(data)
            rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/run_images.txt', 'r')
            Lines = rows.readlines()
        else:
            error = "Image with ID {} are not Run_able: may be there are some dependencies".format(data)
            Lines = "NO run result Data"

    return render_template('user/docker_images_run_status.html', error=error, res=Lines, Iid=data)


@app.route('/docker_Ing_pull', methods=['GET', 'POST'])
def Docker_Pull_IMG():
    error = None
    if request.method == 'POST':
        data = request.form['img_pull_cmd']
        # print(data+"********************")
        query = "gotty sudo docker pull {} & > /home/kpit/PycharmProjects/Docker_UI/venv/static/files/pull_images.txt ".format(
            data)
        print(query)
        res = os.system(query)
        if res == 0:
            rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/pull_images.txt', 'r')
            Lines = rows.readlines()
            error = " docker image {} are pulled successfully..check Inmage list".format(data)
        else:
            Lines = "No pull status data..please check docker Images list.. "
            error = " docker image {} are not pulled successfully..".format(data)

        return render_template('user/docker_images_pull_status.html', error=error, res=Lines)
    else:
        Lines = " "
        return render_template('user/docker_images_pull_page.html', error=error, res=Lines)


@app.route('/docker_Img_build', methods=['GET', 'POST'])
def Docker_build_IMG():
    error = None
    tcp_port()
    if request.method == 'POST':
        name = request.form['name']
        pri_path = request.form['path1']
        docfile = request.form['Dockerfile']
        docname = pri_path + "Dockerfile"
        doc = open(docname, "w+")
        doc.write(docfile)
        doc.close()
        reqfile = request.form['Requirement_txt']
        reqname = pri_path + "Requirement.txt"
        req = open(reqname, "w+")
        req.write(reqfile)
        req.close()
        # build_path = request.form['path']
        tag = request.form['arg_tag']
        print(docfile)
        print(reqfile)
        query = "gotty sudo docker build {} {} {} &".format(tag, name, pri_path)
        print(query)
        res = os.system(query)
        if res == 0:
            error = "Img Build Successfully"
            return render_template('user/docker_images_build_status.html', err=error)
        else:
            error = "Img Build Failed"
            return render_template('user/docker_images_build_status.html', err=error)

    else:
        return render_template('user/docker_image_build_page.html')


@app.route('/Docker_container_list', methods=['GET', 'POST'])
def Docker_container_list():
    error = None
    if request.method == 'POST':
        data = C.output("return_ID")
        uname = data.split("=")
        Uname = uname[1]
        Img_ID = Uname
        error = "Recently run-able Image ID= {} Please check into list".format(Img_ID)
    if error == " ":
        error = " "
    con_name_list = []
    con_ID_list = []
    IMAGE_ID_list = []
    command_list = []
    port_list = []
    # CREATED_list = []
    Status_list = []
    query = "sudo docker ps --all > /home/kpit/PycharmProjects/Docker_UI/venv/static/files/containers.txt "
    os.system(query)
    os.system("awk '{$2=$2};1' /home/kpit/PycharmProjects/Docker_UI/venv/static/files/containers.txt > "
              "/home/kpit/PycharmProjects/Docker_UI/venv/static/files/adj_containers.txt")

    rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/adj_containers.txt', 'r')
    Lines = rows.readlines()
    count = 0
    for line in Lines:
        if count == 0:
            # print("Title")
            count = count + 1
        else:
            # print("inside else")
            word = line.split(" ")
            con_name_list.append(word[-1])
            con_ID_list.append(word[0])
            # print(word[1])
            IMAGE_ID_list.append(word[1])
            command_list.append(word[2])
            if word[-2] == "ago":
                port_list.append("Not Specified")
                Status_list.append(word[-6])
            else:
                port_list.append(word[-2])
                Status_list.append(word[-7])

            count = count + 1

    count = count - 1

    return render_template('user/docker_con_list.html', conName=con_name_list, conID=con_ID_list, image=IMAGE_ID_list,
                           status=Status_list, command=command_list, port=port_list, count=count, err=error)


@app.route('/delete_con', methods=['GET', 'POST'])
def Docker_delete_con():
    error = None
    tcp_port()
    if request.method == 'POST':
        data = request.form['img_del_id']
        # print(data)
        query = " gotty sudo docker stop {} &".format(data)
        res1 = os.system(query)
        if res1 == 0:
            query = "sudo docker rm {}".format(data)
            print(query)
            res = os.system(query)
            if res == 0:
                error = "Container with ID {} are deleted".format(data)
            else:
                error = "Container with ID {} are not deleted: may be there are some dependencies".format(data)

    return render_template('user/docker_con_del_status.html', error=error)


@app.route('/start_con', methods=['GET', 'POST'])
def Docker_start_con():
    error = None
    tcp_port()
    if request.method == 'POST':
        C["ID"] = request.form['con_start_id']
        data = C.output("ID")
        uname = data.split("=")
        Uname = uname[1]
        data = Uname
        # print(C.output("ID"))
        query = "gotty sudo docker start {} &".format(data)
        print(query)
        res = os.system(query)
        if res == 0:
            error = "Container with ID {} are Started".format(data)
        else:
            error = "Container with ID {} are not started: may be there are some dependencies".format(data)
            # rows = open('/home/kpit/PycharmProjects/login1/venv/static/files/con_start_log.txt', 'r')
            # Lines = rows.readlines()

    return render_template('user/docker_con_start_status.html', error=error, Id=data)


@app.route('/Docker_container_exec', methods=['GET', 'POST'])
def Docker_exec_con():
    tcp_port()
    if request.method == 'POST':
        error = None
        data = request.form['con_exec_id']
        # print(data + "ID NOt Found")
        command = request.form['con_exec_cmd']
        query = "gotty sudo docker exec {} {} > /home/kpit/PycharmProjects/Docker_UI/venv/static/files/exec.txt &".format(
            data,
            command)
        print(query)
        res1 = os.system(query)
        if res1 == 0:
            error = "Container with ID {} are executed".format(data)
            rows = open('/home/kpit/PycharmProjects/Docker_UI/venv/static/files/exec.txt', 'r')
            Lines = rows.readlines()
        else:
            error = "Container with ID {} are not executed: may be there are some dependencies".format(data)
            Lines = ""

        return render_template('user/docker_con_start_status.html', error=error, res=Lines)


@app.route('/Docker_container_exec_page_back', methods=['GET', 'POST'])
def Docker_exec_con_page_back():
    if request.method == 'POST':
        data = C.output("ID")
        uname = data.split("=")
        Uname = uname[1]
        return render_template('user/docker_con_exec_page.html', ID=Uname)


@app.route('/Docker_container_exec_page', methods=['GET', 'POST'])
def Docker_exec_con_page():
    if request.method == 'POST':
        data = C.output("ID")
        uname = data.split("=")
        Uname = uname[1]
        return render_template('user/docker_con_exec_page.html', ID=Uname)


'''
@app.route('/trial')
def Docker_Trial():
    query = "gotty sudo echo HOOOO & "
    os.system(query)
    # req = open("/home/kpit/PycharmProjects/login1/venv/static/files/trial.sh", "w+")
    # req.write(query)
    # req.close()
    # os.system("sudo /home/kpit/PycharmProjects/login1/venv/static/files/trial.sh")
    return render_template('user/trial.html')
'''


@app.route('/stop_con', methods=['GET', 'POST'])
def Docker_stop_con():
    if request.method == 'POST':
        error = None
        data = request.form['con_stop_id']
        # print(data)
        query = "sudo docker stop {}".format(data)
        res = os.system(query)
        if res == 0:
            error = "Container with ID {} are Stop".format(data)
        else:
            error = "Container with ID {} are not Stop: may be there are some dependencies".format(data)

    return render_template('user/docker_con_stop_status.html', error=error)


if __name__ == "__main__":
    # tcp_port()
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='localhost', port=8085)
