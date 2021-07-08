import sys
sys.path.append(".")

import logging
# logging.basicConfig(level=logging.DEBUG)

from flask import Flask, jsonify, request, render_template, redirect
from form import SearchForm
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter
from search import elasticSearch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DontTellAnyone'
bootstrap = Bootstrap(app)


@app.route('/')
@app.route('/index/')
def index():
    searchForm = SearchForm()
    return render_template('index.html', searchForm=searchForm)


@app.route('/search/', methods=['GET','POST'])
def search():
    search_key = request.args.get("search_key", default=None)
    print(search_key)
    if search_key:
        searchForm = SearchForm()
        match_data = es.search(search_key,count=30)
        print(match_data['hits']['hits'][3])
        print(match_data['hits']['hits'][5])

        # 翻页
        PER_PAGE = 10
        page = request.args.get(get_page_parameter(), type=int, default=1)
        start = (page - 1) * PER_PAGE
        end = start + PER_PAGE
        total = 30
        pagination = Pagination(page=page, start=start, end=end, total=total)
        context = {
            'match_data': match_data["hits"]["hits"][start:end],
            'pagination': pagination,
            'uid_link': "/wiki/"
        }
        return render_template('data.html', q=search_key, searchForm=searchForm, **context)
    return redirect('/')



if __name__ == "__main__":
    es = elasticSearch(index_type='logs', index_name='zhwiki-*')
    app.run(host='0.0.0.0', port=5000, debug=True)



