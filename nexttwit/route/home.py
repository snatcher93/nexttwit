# -*- encoding: utf-8 -*-
from flask import render_template
from server import app

# 여기에 원하는 주소를 입력하세요
@app.route('/') 
def home():
    # 여기에 html 페이지 이름을 입력하세요
    return render_template('')
