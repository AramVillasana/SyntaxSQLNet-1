"""
Start Flask app by running ./run_flask.py
"""

from flaskexample import app
from flask import request
from flask import render_template
from inference import infer_script
from train_feedback import train_feedback
from utils import get_table_names, get_tables_html, load_word_emb

# @app.route('/')
# @app.route('/index')
# def index():
#    return "Hello, World!"

N_word=300
B_word=42
LOAD_USED_W2I = False
USE_SMALL=True
print("Creating word embedding dictionary...")
word_emb = load_word_emb('glove/glove.%dB.%dd.txt'%(B_word,N_word), \
      load_used=LOAD_USED_W2I, 
      use_small=USE_SMALL)

@app.route('/')
@app.route('/index')
@app.route('/input')
def cesareans_input():

   return render_template("input.html")


@app.route('/output')
# @app.route('/')
# @app.route('/index')
def cesareans_output():

   # pull english question and tokenize it
   # eng_q = "What are the maximum and minimum budget of the departments?"
   eng_q = request.args.get('english_question')
   print("Question: {}".format(eng_q))

   # pull the database name for the question
   # db_name_q = 'department_management'
   db_name_q = request.args.get('database_name')
   print("Database Name: {}".format(db_name_q))

   # generate the sql query
   gen_sql = infer_script(nlq = eng_q,
                           db_name = db_name_q,
                           toy = True,
                           word_emb = word_emb)
   print("Generated SQL: {}".format(gen_sql))

   # get tables from database
   tables_html, titles = get_tables_html(db_name = db_name_q)
   print("Number of Tables in DB: {}".format(len(tables_html)))


   return render_template("output.html", 
                         question = eng_q,
                         database_name = db_name_q,
                          generated_sql = gen_sql,
                          tables = tables_html,
                          titles = titles)

@app.route('/retrain')
def retrain_flask():

   # pull english question and tokenize it
   # eng_q = "What are the maximum and minimum budget of the departments?"
   eng_q = request.args.get('english_question')
   print("Question: {}".format(eng_q))

   # pull the database name for the question
   # db_name_q = 'department_management'
   db_name_q = request.args.get('database_name')
   print("Database Name: {}".format(db_name_q))

   # pull the correct query from the website of output
   correct_query = request.args.get('correct_query')
   print("Correct Query: {}".format(correct_query))

   # get tables from database
   tables_html, titles = get_tables_html(db_name = db_name_q)
   print("Number of Tables in DB: {}".format(len(tables_html)))

   # retrain the model with the correct sql query
   train_feedback(nlq = eng_q,
                  db_name = db_name_q,
                  correct_query = correct_query,
                  toy = True,
                  word_emb = word_emb)

   return render_template("retrain.html", 
                         question = eng_q,
                         database_name = db_name_q,
                          correct_query = correct_query,
                          tables = tables_html,
                          titles = titles)