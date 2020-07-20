import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash, 
    render_template, 
    redirect,
    request,
    url_for,
)

import pyparticle as pp

load_dotenv()
app = Flask(__name__)
app.secret_key = "ssssh don't tell anyone"

AUTH_TOKEN = os.getenv('AUTH_TOKEN')
DEVICE_ID = os.getenv('DEVICE_ID')


particle = pp.Particle(access_token=AUTH_TOKEN)
devices = particle.list_devices()
device = devices[0]

def get_sent_messages():
    # TODO: Make this return a collection of messages that were sent from the number
    messages = []
    return messages

def send_message(to, body):
    # TODO: Send the text message
    pass

@app.route("/", methods=["GET"])
def index():
    try:
      messages = get_sent_messages()
      status = particle.get_variable(device['id'], 'test')
      if status['result']:
        flash(f"A lâmpada está ligada, meu cachorrão")
      else:
          flash(f"A lâmpada está desligada, meu cachorrinho")
      return render_template("index.html", messages=messages)
    except:
      flash(f"Achamos um erro... Provavelmente a lâmpada está desconectada.")
      return render_template("index.html", messages=messages)

@app.route("/on", methods=["POST"])
def on():
  try:
    particle.call_function(device['id'], 'pisca', 1)
    flash('PISCOU :)')
    return redirect(url_for('index'))
  except:
      flash(f"Um erro foi encontrado. O aparelho está desconectado.")
      return redirect(url_for('index'))
    

  
@app.route("/off", methods=["POST"])
def off():
  try:
    particle.call_function(device['id'], 'pisca', 0)
    flash('DESLIGOU :(')
    return redirect(url_for('index'))
  except:
    flash(f"Um erro foi detectado. O aparelho está desconectado.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
