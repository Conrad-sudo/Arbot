import main
import time
import logging
import telegram
from telegram import ParseMode, Bot
from telegram.utils.request import Request
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
from telegram.update import Update


# Configure logging so errors are visible
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Proxy config — only needed for free PythonAnywhere accounts
PROXY_URL = "http://proxy.server:3128"

# Bot credentials and access control — set these before running
TELEGRAM_TOKEN = ''
GROUP_CHAT_ID = ""
USER_WHITELIST = []


# Set up bot with proxy
request = Request(proxy_url=PROXY_URL, con_pool_size=8)
bot = Bot(token=TELEGRAM_TOKEN, request=request)
updater = Updater(bot=bot, use_context=True)
job_queue = updater.job_queue

# Module-level state
job_handler = None
on = False


# ── Command handlers ──────────────────────────────────────────────────────────

def start(update: Update, context: CallbackContext):
    update.message.reply_text('To start bot enter /run\nTo stop bot enter /stop')


def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text('You can only add one pair at a time')


def init(update: Update, context: CallbackContext):
    global job_handler, on

    user_id = update.message.chat_id

    if user_id not in USER_WHITELIST:
        update.message.reply_text('Restricted access!')
        return

    if on:
        update.message.reply_text('Arbot has already been started')
        return

    on = True
    job_handler = job_queue.run_repeating(scan_job, interval=1200, first=2)
    update.message.reply_text('Arbot started')


def stop(update: Update, context: CallbackContext):
    global job_handler, on

    user_id = update.message.chat_id

    if user_id not in USER_WHITELIST:
        update.message.reply_text('Restricted access!')
        return

    if not on:
        update.message.reply_text("Arbot hasn't been started")
        return

    if job_handler is not None:
        job_handler.schedule_removal()
        job_handler = None

    on = False
    update.message.reply_text(text="Arbot stopped")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you, you said '%s'" % update.message.text)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


# ── Scanning logic ────────────────────────────────────────────────────────────

def send_rates(rates):
    """Send each arbitrage result as a separate Telegram message."""
    for message in rates:
        try:
            bot.send_message(
                text=f'```\n{message}```',
                chat_id=GROUP_CHAT_ID,
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        except telegram.error.TelegramError as e:
            logger.error("Failed to send message: %s", e)


def launcher(pair):
    exchanges = ["huobi", "kucoin", "okx", "bitget", "binance", "bittrex", "coinbase", "okcoin", "kraken"]
    ask_exchanges = exchanges[:]
    bid_exchanges = exchanges[:]

    for ask in ask_exchanges:
        for bid in bid_exchanges:
            time.sleep(0.1)

            if not on:
                return

            if ask == bid:
                continue

            rates = main.find_arb(pair=[pair], ask_exchange=ask, bid_exchange=bid)

            if rates not in ('No common pairs', 'No arbitrage found', []):
                send_rates(rates)


def scan_job(context: CallbackContext):
    """Job queue callback: scan all pairs across all exchange combos."""
    if not on:
        return

    all_pairs = main.get_all_pairs()

    for pair in all_pairs:
        if not on:
            break
        launcher(pair)


# ── Handler registration ──────────────────────────────────────────────────────

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('stop', stop))
updater.dispatcher.add_handler(CommandHandler('help', help_cmd))
updater.dispatcher.add_handler(CommandHandler('run', init))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


# ── Start the bot ─────────────────────────────────────────────────────────────

updater.start_polling()
updater.idle()
