# THU_balance_check
Implemented based on Project[TsinghuaBills](https://github.com/ZenithalHourlyRate/thuservices/blob/master/aux/TsinghuaBills.py)
## Step One
- install packages requirements
## Step Two
input username,password,token
- You need to register for an account of [pushplus](http://www.pushplus.plus/) to access argument 'token'
- copy and paste your token
## Step Three
set up a scheduled task
This is an example:
```python
import schedule
import time

def my_function():
    do what u want

schedule.every().day.at("22:00").do(my_function)

while True:
    schedule.run_pending()
    time.sleep(1)
```python
