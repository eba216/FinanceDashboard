from flask import render_template, jsonify, request
from datetime import datetime

from . import main
from .forms import StockForm

import yfinance as yf
import matplotlib.pyplot as plt
import mpld3
from matplotlib import style
style.use("seaborn-deep")



@main.route("/get_live_data", methods= ['GET', 'POST'])
def get_live_data():
    
    now = datetime.now()
    now = now.strftime('%d/%m/%Y %I:%M:%S')

    stock = request.args.get('stock', 'FB')
    stock = stock.upper()

    tickers = "^GSPC ^IXIC ^DJI" + " " + stock
    fig, [(ax1, ax2), (ax3 , ax4)] = plt.subplots(2, 2, figsize=(14,12))
    df = yf.download(tickers=tickers, period='1d', interval='1m')
    df.index = df.index.tz_localize(None) 


    ax1.plot(df["Adj Close"]["^GSPC"])
    ax1.set_ylabel("Share Price")
    ax1.set_title(f"S&P 500")
    ax1.grid(color = 'grey', linestyle = '--', linewidth = 0.5)

    ax2.plot(df["Adj Close"]["^IXIC"])
    ax2.set_ylabel("Share Price")
    ax2.set_title(f"NASDAQ")
    ax2.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    
    ax3.plot(df["Adj Close"]["^DJI"])
    ax3.set_ylabel("Share Price")
    ax3.set_title(f"DOW JONES")
    ax3.grid(color = 'grey', linestyle = '--', linewidth = 0.5)

    ax4.plot(df["Adj Close"][stock])
    ax4.set_ylabel("Share Price")
    ax4.set_title(f"{stock}")
    ax4.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
    
    fig.get_axes()[0].annotate(f"Data on {now[:10]} as of {now[10:]} (updates every minute)", (0.5, 0.93), 
                            xycoords='figure fraction', ha='center', 
                            fontsize=65
                            )
    figure = mpld3.fig_to_html(fig)   

    plt.clf()
    plt.close(fig)
    df = None
    
    return jsonify(result=figure)


@main.route("/index",methods=["GET", "POST"])
@main.route("/",methods=["GET", "POST"])
def index():
    stock_form = StockForm()

    if stock_form.validate_on_submit():
        stock_form.stock_name.data = stock_form.stock_name.data.upper()
        stock_info = yf.Ticker(stock_form.stock_name.data).info
        return render_template("index.html", form=stock_form, stock_info=stock_info)

    stock_form.stock_name.data = "AAPL"
    stock_info = yf.Ticker(stock_form.stock_name.data)
    stock_info = stock_info.info

    return render_template("index.html", form=stock_form,stock_info=stock_info)

