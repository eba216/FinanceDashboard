from flask import render_template

from . import simulate
from .forms import StockSimulatorForm

import numpy as np
import numpy.random as npr
import yfinance as yf
import matplotlib.pyplot as plt

# this block is needed to import mpld3, looking to fix soon
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from distutils.version import LooseVersion
    import mpld3

from matplotlib import style

style.use("seaborn-deep")


@simulate.route("/",methods=["GET", "POST"])
def simulate():
    figure = ""
    stock_sim_form = StockSimulatorForm()
    stock = stock_sim_form.stock_name.data

    if stock_sim_form.validate_on_submit():

        fig = plt.figure(figsize=(10,5),clear=True)
        
        stock_sim_form.stock_name.data = stock_sim_form.stock_name.data.upper()
        
        stock = stock_sim_form.stock_name.data
        simulations= stock_sim_form.num_sims.data
        sim_time = stock_sim_form.sim_time.data #time in years

        steps = 100

        #time step
        dt = sim_time/steps

        df = yf.download(stock)

        # normalize returns
        returns = df["Adj Close"]

        mu, sigma = 0.08, 0.25 # avg market return, avg volatility
        initial = df["Adj Close"].iloc[-1]

        St = np.exp(
            (mu - sigma ** 2 / 2) * dt
            + sigma * npr.normal(0, np.sqrt(dt), size=(simulations, steps)).T
        )
        # include array of 1's
        St = np.vstack([np.ones(simulations), St])
        # multiply through by S0 and return the cumulative product of elements along a given simulation path (axis=0).
        St = initial * St.cumprod(axis=0)

        # Define time interval correctly
        time = np.linspace(0, sim_time, steps + 1)

        # Require numpy array that is the same shape as St
        tt = np.full(shape=(simulations, steps + 1), fill_value=time).T

        plt.plot(tt, St,linewidth= 0.5)

        plt.plot(time, initial*np.ones(steps + 1), linewidth=2, linestyle="--", color ="black",label ="Starting Price")
        plt.plot(time, [0] + St.sum(axis=1)//simulations , linewidth=2 ,  color="black", label ="Simulation Average")

        title = f"{simulations} Realization{'s' if simulations >1 else ''} of Geometric Brownian Motion to Estimate {stock} Price"
        plt.title(title, size=24)

        plt.xlabel("Years")
        plt.ylabel(f"Stock Price (USD)")
        plt.legend()
        figure = mpld3.fig_to_html(fig)
        
        df = None
        return render_template("simulate.html", form=stock_sim_form, figure=figure)

    return render_template("simulate.html", form=stock_sim_form, figure=figure)