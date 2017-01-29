from flask import Flask,render_template,request,session
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    return render_template('index.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if not session.has_key('user_id'):
		if request.method == 'POST':
			email = request.form['inputEmail']
			password = request.form['inputPassword']
			conn = mysql.connect()
			curser = conn.cursor()
			Q = "SELECT user_username , user_password FROM tbl_user"
			curser.execute(Q)
			users = curser.fetchall()
			for user in users:
				if str(user[0]) == (email) and str(user[1]) == password:
					conn = mysql.connect()
					curser = conn.cursor()
					Q = "SELECT user_id FROM tbl_user WHERE user_username = '" + email + "' and user_password = '" + password + "'"
					curser.execute(Q)
					session['user_id'] = str(curser.fetchone()).strip("(,)")
					return 'Hello'
			return "failed"
		else:
			return render_template("signin.html")
	else: return session['user_id']


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		name = request.form['inputName']
		email = request.form['inputEmail']
		password = request.form['inputPassword']
		conn = mysql.connect()
		curser = conn.cursor()
		Q = "INSERT INTO tbl_user (user_name,user_username,user_password) VALUES ('" + name + "','" + email + "','" + password + "')"
		curser.execute(Q)
		conn.commit()
		return "done"
	else:
		return render_template("signup.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    	session.pop('user_id', None)
	return "you have been logged out"

@app.route('/remove_post', methods=['GET', 'POST'])
def remove_post():
	if request.method == 'POST':
		post_id = request.form['post_id']
		conn = mysql.connect()
		curser = conn.cursor()
		Q = "delete from posts where post_id = '" + post_id + "'"
		curser.execute(Q)
		conn.commit()
		return "done"
	else: return "there is no page."


@app.route('/post', methods=['GET', 'POST'])
def post():
	if request.method == 'POST':
		post = request.form['post']
		conn = mysql.connect()
		curser = conn.cursor()
		Q = "INSERT INTO posts (author_id,post_content) VALUES ('" + session['user_id'] + "','" + post + "')"
		curser.execute(Q)
		conn.commit()
		return "done"
	else:
		conn = mysql.connect()
		curser = conn.cursor()
		Q = "SELECT post_content,post_id FROM posts WHERE author_id = '" + session['user_id'] + "'"
		curser.execute(Q)
		data = curser.fetchall()
		return render_template("post.html",data=data)

app.secret_key = 'A0Zr98j/3asasdyX R~XHH!jmN]LWX/,?RT'
if __name__ == "__main__":
    app.run()



