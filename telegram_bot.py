


import main
import time
import urllib3
import telepot
import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram import ParseMode
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters



# You can leave this bit out if you're using a paid PythonAnywhere account
proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
# end of the stuff that's only needed for free accounts



#Set the telegram token
telegram_token=''
group_chat_id=""
user_whitelist=[]


#Set up the connection with the bot API
updater = Updater(telegram_token,use_context=True)
job = updater.job_queue
bot = telegram.Bot(token=telegram_token)

global job_handler
on=False



#Step 1: defining functions for the bot
def start(update: Update, context: CallbackContext):
	update.message.reply_text('To start bot enter /run\nTo stop bot enter /stop')




def help(update: Update, context: CallbackContext):
	update.message.reply_text(' You can only add one pair at a time')





def launcher(pair):

    ask_exchanges=["huobi","kucoin","okx","bitget","binance","bittrex","coinbase","okcoin","kraken"]
    bid_exchages=["kucoin","huobi","okx","bitget","binance","bittrex","coinbase","okcoin","kraken"]

    for ask in ask_exchanges:
        for bid in bid_exchages:
            time.sleep(0.1)
            if ask != bid and on==True:

                #combo=ask +"/"+bid
                #print("Exchanges: ",combo)
                #print("Pair***: ",pair)
                rates= main.find_arb( pair=[pair], ask_exchange=ask, bid_exchange=bid)

                if rates=='No common pairs':
                     pass
                elif rates=='No arbitrage found':
                     pass
                elif rates==[]:
                     pass
                else:
                    bot.send_message(text=f'```{rates}```', chat_id=group_chat_id,parse_mode=ParseMode.MARKDOWN_V2)

            elif on==False:
                break






def run (context: CallbackContext):


    global on

    if on== False:
        on = True
        all_pairs=main.get_all_pairs()

        for pair in all_pairs:
            launcher(pair)



    elif on==True:
        on=False
        time.sleep(0.5)
        re_run()




def re_run():

    global on

    on=True

    all_pairs = main.get_all_pairs()

    for pair in all_pairs:
        launcher(pair)

    run()





def init(update, context:CallbackContext):


    global job_handler
    global pairs_list
    user_id= update.message.chat_id

    if user_id in user_whitelist and on== False:

        job_handler = job.run_repeating(run , interval=1200, first=2)

        update.message.reply_text('Arbot started ')

    elif user_id in user_whitelist and on == True:
        update.message.reply_text('Arbot has already been started')





def stop(update, context:CallbackContext):
    user_id = update.message.chat_id
    global job_handler
    global on
    if user_id in user_whitelist and on == True:

        job_handler.enabled = False
        update.message.reply_text(text="Arbot stopped")

        on = False

    elif user_id in user_whitelist and on == False:
        update.message.reply_text(text="Arbot hasn't been started")

    else:
        update.message.reply_text('Restricted access! ')




def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s'" % update.message.text)



def unknown(update: Update, context: CallbackContext):
    update.message.reply_text( "Sorry '%s' is not a valid command" % update.message.text)




#Step 2: Adding the Handlers to handle our messages and commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('run', init))

updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


#Step 3: Run the bot

updater.start_polling()
#updater.start_webhook(listen="0.0.0.0",port=int(PORT),url_path=telegram_token,webhook_url='https://Conrad92.pythonanywhere.com' + telegram_token)
updater.idle()
