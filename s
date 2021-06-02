[1mdiff --git a/TTimes/__pycache__/__init__.cpython-39.pyc b/TTimes/__pycache__/__init__.cpython-39.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..c5bc032[m
Binary files /dev/null and b/TTimes/__pycache__/__init__.cpython-39.pyc differ
[1mdiff --git a/TTimes/__pycache__/apps.cpython-39.pyc b/TTimes/__pycache__/apps.cpython-39.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..a44ccf3[m
Binary files /dev/null and b/TTimes/__pycache__/apps.cpython-39.pyc differ
[1mdiff --git a/static/css/style.css b/static/css/style.css[m
[1mnew file mode 100644[m
[1mindex 0000000..0f6a796[m
[1m--- /dev/null[m
[1m+++ b/static/css/style.css[m
[36m@@ -0,0 +1,39 @@[m
[32m+[m[32m.name{[m
[32m+[m[32m  color: rgb(136, 133, 133);[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.container{[m
[32m+[m[32m  color: rgb(136, 133, 133);[m
[32m+[m[32m}[m
[32m+[m[32m.staff_name{[m
[32m+[m[32m  color: rgb(136, 133, 133);[m
[32m+[m[32m  text-align: center;[m
[32m+[m[41m [m
[32m+[m[32m}[m
[32m+[m[32mbr {[m
[32m+[m[32m  display: block;[m
[32m+[m[32m  content: "";[m
[32m+[m[32m  margin: 0 10px;[m
[32m+[m[32m  }[m
[32m+[m
[32m+[m[32m.button{[m
[32m+[m[32m  background: rgb(148, 146, 146);[m
[32m+[m[32m  border-radius:5%;[m
[32m+[m[32m  padding: 15px 60px;[m
[32m+[m[32m  color         : #ffffff;[m
[32m+[m[32m  font-size     : 19pt;[m
[32m+[m[32m  margin: 30px 30px 4px 10px;[m
[32m+[m[32m}[m
[32m+[m[32m.form{[m
[32m+[m[32m  background: rgb(148, 146, 146);[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.form_control{[m
[32m+[m[32m  display: block;[m
[32m+[m[32m  background: rgb(255, 255, 255);[m
[32m+[m[32m  color         : #8a8787;[m
[32m+[m[32m  font-size: 30px;[m
[32m+[m[32m  padding: 10px 130px;[m
[32m+[m[32m  margin: 0 0 0 0;[m
[32m+[m[41m  [m
[32m+[m[32m}[m
[1mdiff --git a/templates/attendance.html b/templates/attendance.html[m
[1mindex 8b745a5..f080be9 100644[m
[1m--- a/templates/attendance.html[m
[1m+++ b/templates/attendance.html[m
[36m@@ -1,5 +1,5 @@[m
 {% extends 'base.html' %}[m
[31m-[m
[32m+[m[32m{% load widget_tweaks %}[m
 {% block head %}[m
 <script>[m
     function updateClock() {[m
[36m@@ -31,15 +31,18 @@[m
 {% block content %}[m
 [m
 <body onload="start();">[m
[31m-    <div id="myClock" align="center" style="font:bold 20pt Times New Roman;"></div>[m
[31m-    <div id="company_name" align="left" style="font:bold 12pt Times New Roman;">{{ company }}</div>[m
[32m+[m[32m    <div class="name" id="myClock" align="center" style="font:bold 20pt Times New Roman;"></div>[m
[32m+[m[32m    <div class="name" id="company_name" align="left" style="font:bold 12pt Times New Roman;">{{ company }}</div>[m
     <hr>[m
 [m
     <div class="container" align="center">[m
[32m+[m[32m        <p class="staff_name">従業員名</p>[m
         <form action="{% url 'attendance' %}" method="POST">{% csrf_token %}[m
[31m-            {{ form.as_p }}[m
[31m-            <input type="submit" value="出勤" id="arrive" name="arrive">[m
[31m-            <input type="submit" value="退勤" id="leave" name="leave">[m
[32m+[m[32m            <br>[m
[32m+[m[32m            {{ form.staff|add_class:'form_control'}}[m
[32m+[m[32m            <br>[m
[32m+[m[32m            <input class="button" type="submit" value="出勤" id="arrive" name="arrive">[m
[32m+[m[32m            <input class="button" type="submit" value="退勤" id="leave" name="leave">[m
         </form>[m
     </div>[m
 </body>[m
[1mdiff --git a/templates/base.html b/templates/base.html[m
[1mindex 04ca38a..ac37e81 100644[m
[1m--- a/templates/base.html[m
[1m+++ b/templates/base.html[m
[36m@@ -5,7 +5,9 @@[m
     <!-- Required meta tags -->[m
     <meta charset="utf-8">[m
     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">[m
[31m-[m
[32m+[m[32m    <!--CSS-->[m
[32m+[m[32m    {% load static %}[m
[32m+[m[32m    <link rel='stylesheet' type="text/css" href="{% static 'css/style.css'%}">[m
     <!-- Bootstrap CSS -->[m
     <link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">[m
     <title>TTimes</title>[m
[1mdiff --git a/timecardproject/__pycache__/__init__.cpython-39.pyc b/timecardproject/__pycache__/__init__.cpython-39.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..b1878a5[m
Binary files /dev/null and b/timecardproject/__pycache__/__init__.cpython-39.pyc differ
[1mdiff --git a/timecardproject/__pycache__/settings.cpython-39.pyc b/timecardproject/__pycache__/settings.cpython-39.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..dcdc706[m
Binary files /dev/null and b/timecardproject/__pycache__/settings.cpython-39.pyc differ
[1mdiff --git a/timecardproject/__pycache__/urls.cpython-39.pyc b/timecardproject/__pycache__/urls.cpython-39.pyc[m
[1mnew file mode 100644[m
[1mindex 0000000..853bb01[m
Binary files /dev/null and b/timecardproject/__pycache__/urls.cpython-39.pyc differ
[1mdiff --git a/timecardproject/settings.py b/timecardproject/settings.py[m
[1mindex bc52961..35f5307 100644[m
[1m--- a/timecardproject/settings.py[m
[1m+++ b/timecardproject/settings.py[m
[36m@@ -39,6 +39,7 @@[m [mINSTALLED_APPS = [[m
     'django.contrib.staticfiles',[m
     'TTimes.apps.TtimesConfig',[m
     'bootstrap4',[m
[32m+[m[32m    'widget_tweaks',[m
 ][m
 [m
 MIDDLEWARE = [[m
