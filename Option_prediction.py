#Imports and set up
from datetime import datetime, timedelta
import pandas as pd
from openbb import obb
obb.user.preferences.output_type = "dataframe"
obb.user.credentials.nasdaq_api_key = "PLACE_HOLDER"

earnings_calendar = obb.equity.calendar.earnings(
    start_date=(datetime.now()+timedelta(days=1)).date(),
    end_date = (datetime.now()+timedelta(days=14)).date(),
    provider="nasdaq"
)
# Select the underlying
symbol = "COST"
last_price = (
    obb
    .equity
    .price
    .quote(symbol, provider="yfinance")
    .T
    .loc["last_price", 0]
)
#Select the underlying
options = obb.derivatives.options.chains(symbol, provider="cboe")
expiration = datetime(2024, 3, 8).date()
chain = options.query("`expiration` == @expiration")
# Construct the straddle
strikes = chain.strike.to_frame()
call_strike = (
    strikes
    .loc[strikes.query("`strike` > @last_price").idxmin()]["strike"]
    .iloc[0]
)
atm_call = chain.query("`strike` == @call_strike and `option_type` == 'call'")
atm_put = chain.query("`strike` == @call_strike and `option_type` == 'put'")
atm = pd.concat([atm_call, atm_put])
straddle_price = round(atm.ask.sum(), 2)

# Calculate the implied move
days = (atm.expiration.iloc[0] - datetime.now().date()).days
implied_move = ((1 + straddle_price/last_price)**(1/days) - 1)







\
















\





