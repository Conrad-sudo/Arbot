from tkinter import *
import main
import func_arb
from pandastable import Table

root= Tk()
root.title('ARBOT')

# make app width,height resizable
root.resizable(True,True)
root.grid_columnconfigure(index=0,weight=1)
root.grid_columnconfigure(index=1,weight=1)
root.grid_columnconfigure(index=2,weight=1)
root.grid_columnconfigure(index=3,weight=1)

root.grid_rowconfigure(index=0,weight=1)
root.grid_rowconfigure(index=1,weight=1)
root.grid_rowconfigure(index=2,weight=1)
root.grid_rowconfigure(index=3,weight=1)
root.grid_rowconfigure(index=4,weight=1)
root.grid_rowconfigure(index=5,weight=1)
root.grid_rowconfigure(index=6,weight=1)
root.grid_rowconfigure(index=7,weight=1)
root.grid_rowconfigure(index=8,weight=1)
root.grid_rowconfigure(index=9,weight=1)
root.grid_rowconfigure(index=10,weight=1)
root.grid_rowconfigure(index=12,weight=1)
root.grid_rowconfigure(index=13,weight=1)

alpharates_url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=TRY&apikey=AE966LKHL236KP1K'

table_list=[]

def show_livesrates():

       alpharates_market = func_arb.get_ticker(alpharates_url)

       # Only retieves
       liverate_tickers = func_arb.get_alpha_rate(alpharates_market)
       liverate_bid = liverate_tickers['bid']
       liverate_ask = liverate_tickers['ask']

       rates_label_1.configure(text=f'LIVERATES  USD/TRY: ask {liverate_ask}  bid {liverate_bid}')

       root.after(10000,show_livesrates)




def update():

    rates = main.find_arb( pair=choices, ask_exchange=ask_scenario_pick.get(), bid_exchange=bid_scenario_pick.get() )

    global table_list
    position=0
    try:
        for el in table_list:
            el.model.df = rates[table_list.index(el)]
            el.redraw()
    except IndexError:
        table_list[position].model.df={
            f'Ask': ['', '', '', '', '','', ],
            f' Bid': ['', '', '', '', '','', ],
            'Vol': ['', '', '', '', '','', ],
            'Min Prof': ['1%', '0.75%', '0.5%', '0.25%', '0.1%', '0.01 %',],
            'Weighted': ['', '', '', '', '', '',]
        }



    root.after(6000, update)



#Build a list of pairs that can be passed to the main function to find arbitrages
def get_list():

    global choices
    choices = []

    # Create the reordered pair list by taking the ones that are not empty and combining them with the quote string
    for p in pairs:
        if p.get() != '':
            choices.append(p.get() + quote_pick.get())

    #Check if the exchanges are the same
    if ask_scenario_pick.get()==bid_scenario_pick.get():
        error_label.configure(text='Same exchanges')

    # If the user didn't choose a currency
    elif len(choices) == 0:
        error_label.configure(text='Choose base pair')

    elif quote_pick.get()=='':
        error_label.configure(text='Choose quote pair')

    elif ask_scenario_pick.get()=='':
        error_label.configure(text='Choose ask exchange')

    elif bid_scenario_pick.get()=='':
        error_label.configure(text='Choose bid exchange')


    else:

        #if len(choices) > 4:
            #error_label.configure(text='')
            #error_label.configure(text='Please choose a maximum of 4 pairs')


        # Get the arbitrage rate list

        arb_window = Tk()
        arb_window.title('Arbitrage ')
        el = main.find_arb(pair=choices, ask_exchange=ask_scenario_pick.get(), bid_exchange=bid_scenario_pick.get())
        counter = 0

        # If there is an arbitrage opportunity// Initialise the tables
        if isinstance(el, list) == True and len(el) > 0:

            error_label.configure(text='')

            grid_plan = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (1, 2)]


            # loop through the pairs and find the rates
            while counter < len(el):
                # Create a frame for the table
                frame_counter = Frame(arb_window)
                frame_counter.grid(row=grid_plan[counter][0], column=grid_plan[counter][1])
                # fill = 'both', expand = True

                # Create a table from the dataframe and append it to the frame
                table_counter = Table(frame_counter, dataframe=el[counter], height=135)
                table_list.append(table_counter)
                table_counter.show()

                counter += 1
            update()


        elif isinstance(el, str) == True:
            error_label.configure(text=el)

def test():
    # Create the reordered pair list by taking the ones that are not empty and combining them with the quote string
    choices=[]
    for p in pairs:
        if p.get() != '':
            choices.append(p.get())
    print(choices)


#Rates label
rates_label_1=Label(root, text='',height=2, background='black', foreground='white')
rates_label_1.grid(row=0,column=0,sticky='nsew')
rates_label_2=Label(root, text='',height=2, background='black',foreground='white')
rates_label_2.grid(row=0,column=1,sticky='nsew')
rates_label_3=Label(root, text='',height=2, background='black',foreground='white')
rates_label_3.grid(row=0,column=2,sticky='nsew')
rates_label_4=Label(root, text='',height=2, background='black',foreground='white')
rates_label_4.grid(row=0,column=3,sticky='nsew')



#Declare panel buttons
#home=Button(root, text='Home', padx=55, pady=15, ).grid(row=1,column=0, )
#arbitrage=Button(root, text='Arbitrage', padx=45, pady=15).grid(row=1,column=1, )
#deep_watch=Button(root, text='Deep Watches', padx=45, pady=15).grid(row=1,column=2, )
#all_pairs=Button(root, text='All pairs', padx=45, pady=15).grid(row=1,column=3,)




#Configure frames for each panel button
frame_1=Frame(root)
frame_1.grid(row=8, column=0, sticky='nsew' )

frame_2=Frame(root)
frame_2.grid(row=8, column=1, sticky='nsew')

frame_3=Frame(root)
frame_3.grid(row=8, column=2, sticky='nsew')

frame_4=Frame(root)
frame_4.grid(row=8, column=3, sticky='nsew')



#Settings lable
title= Label(root, text='Settings', font=('Arial',25,'italic'), fg='red', ).grid(row=3,column=0,sticky='w', pady=(40,0), padx=10)

#Subheading
subheading_1= Label(root, text='Choose base pair', font=('Arial',15,'bold'), fg='#7A796E' ,pady=20, padx=10).grid(row=4,column=0, sticky='w')


#Declare variables
btc=StringVar()
eth=StringVar()
xrp=StringVar()
ltc=StringVar()
usdt=StringVar()
link=StringVar()
atom=StringVar()
trx=StringVar()
dot=StringVar()
uni=StringVar()
mkr=StringVar()
enj=StringVar()
omg=StringVar()
comp=StringVar()
grt=StringVar()
mana=StringVar()
matic=StringVar()
snx=StringVar()
bat=StringVar()
avax=StringVar()
doge=StringVar()
chz=StringVar()
sol=StringVar()
axs=StringVar()
shib=StringVar()
ftm=StringVar()
lrc=StringVar()
storj=StringVar()
aave=StringVar()
gala=StringVar()
sand=StringVar()
audio=StringVar()
spell=StringVar()
luna=StringVar()
algo= StringVar()
ape=StringVar()
bnt=StringVar()
crv=StringVar()
skl=StringVar()
usdc=StringVar()
xlm=StringVar()
eos=StringVar()
xtz=StringVar()
dash=StringVar()
ada=StringVar()
ankr=StringVar()
uma=StringVar()
nu= StringVar()
poly=StringVar()
amp=StringVar()
qnt=StringVar()
bch=StringVar()
inch=StringVar()
ksm=StringVar()
xmr=StringVar()
sushi=StringVar()
mir=StringVar()
yfi=StringVar()
near=StringVar()
qtum=StringVar()
rune=StringVar()
badger=StringVar()
etc=StringVar()
cro=StringVar()

#Put variables into a list for selection
pairs=[btc,eth,xrp,ltc,usdt,link,atom,trx,dot,uni,mkr,enj,omg,comp,grt,mana,matic,snx,bat,avax,doge,chz,sol,axs,shib,ftm,lrc,
       storj,aave,gala,sand,audio,spell,luna,algo,ape,bnt,crv,skl,usdc,xlm,eos,xtz,dash,ada,ankr,uma,nu,poly,amp,qnt,bch,inch,ksm,xmr,sushi,mir,yfi,near,qtum,rune,badger,etc,cro]


#Declare Checkbuttons

# 1st column
btc_check=Checkbutton(frame_1,variable=btc,onvalue='BTC',offvalue='',width=5, text= 'BTC', font=('Arial',10,'normal')).grid(row=0,column=0,sticky='w',padx=(1,0))
usdt_check=Checkbutton(frame_1,variable=usdt,onvalue='USDT',offvalue='',width=5, text= 'USDT', font=('Arial',10,'normal')).grid(row=1,column=0,sticky='w',padx=(1,0),)
aave_check=Checkbutton(frame_1,variable=aave,onvalue='AAVE',offvalue='',width=5, text= 'AAVE', font=('Arial',10,'normal')).grid(row=2,column=0,sticky='w',padx=(1,0))
usdc_check=Checkbutton(frame_1,variable=usdc,onvalue='USDC',offvalue='',width=5, text= 'USDC', font=('Arial',10,'normal')).grid(row=3,column=0,sticky='w',padx=1)
xlm_check=Checkbutton(frame_1,variable=xlm,onvalue='XLM',offvalue='',width=5, text= 'XLM', font=('Arial',10,'normal')).grid(row=4,column=0,sticky='w',padx=1)

#2nd column
eth_chek=Checkbutton(frame_1,variable=eth,onvalue='ETH',offvalue='',width=5, text= 'ETH', font=('Arial',10,'normal')).grid(row=0,column=1,sticky='w',padx=(0,1))
link_check=Checkbutton(frame_1,variable=link,onvalue='LINK',offvalue='',width=5, text= 'LINK', font=('Arial',10,'normal')).grid(row=1,column=1,sticky='w',padx=(0,1))
luna_check=Checkbutton(frame_1,variable=luna,onvalue='LUNA',offvalue='',width=5, text= 'LUNA', font=('Arial',10,'normal')).grid(row=2,column=1,sticky='w',padx=(0,1))
eos_check=Checkbutton(frame_1,variable=eos,onvalue='EOS',offvalue='',width=5, text= 'EOS', font=('Arial',10,'normal')).grid(row=3,column=1,sticky='w',padx=1)
xlm_check=Checkbutton(frame_1,variable=xlm,onvalue='XLM',offvalue='',width=5, text= 'XLM', font=('Arial',10,'normal')).grid(row=4,column=1,sticky='w',padx=1)

#3rd column
xrp_check=Checkbutton(frame_1,variable=xrp,onvalue='XRP',offvalue='',width=5, text= 'XRP', font=('Arial',10,'normal')).grid(row=0,column=2,sticky='w',padx=1)
atom_check=Checkbutton(frame_1,variable=atom,onvalue='ATOM',offvalue='',width=5, text= 'ATOM', font=('Arial',10,'normal')).grid(row=1,column=2,sticky='w',padx=1)
storj_check=Checkbutton(frame_1,variable=storj,onvalue='STORJ',offvalue='',width=5, text= 'STORJ', font=('Arial',10,'normal')).grid(row=2,column=2,sticky='w',padx=1)
xtz_check=Checkbutton(frame_1,variable=xtz,onvalue='XTZ',offvalue='',width=5, text= 'XTZ', font=('Arial',10,'normal')).grid(row=3,column=2,sticky='w',padx=1)
dash_check=Checkbutton(frame_1,variable=dash,onvalue='DASH',offvalue='',width=5, text= 'DASH', font=('Arial',10,'normal')).grid(row=4,column=2,sticky='w',padx=1)

#4th column
ltc_check=Checkbutton(frame_1,variable=ltc,onvalue='LTC',offvalue='',width=5, text= 'LTC', font=('Arial',10,'normal')).grid(row=0,column=3,sticky='w',padx=1)
trx_check=Checkbutton(frame_1,variable=trx,onvalue='TRX',offvalue='',width=5, text= 'TRX', font=('Arial',10,'normal')).grid(row=1,column=3,sticky='w',padx=1)
spell_check=Checkbutton(frame_1,variable=spell,onvalue='SPELL',offvalue='',width=5, text= 'SPELL', font=('Arial',10,'normal')).grid(row=2,column=3,sticky='w',padx=1)
ada_check=Checkbutton(frame_1,variable=ada,onvalue='ADA',offvalue='',width=5, text= 'ADA', font=('Arial',10,'normal')).grid(row=3,column=3,sticky='w',padx=1)
ankr_check=Checkbutton(frame_1,variable=ankr,onvalue='ANKR',offvalue='',width=5, text= 'ANKR', font=('Arial',10,'normal')).grid(row=4,column=3,sticky='w',padx=1)

#5th column
dot_check=Checkbutton(frame_2,variable=dot,onvalue='DOT',offvalue='',width=10, text= 'DOT', font=('Arial',10,'normal')).grid(row=0,column=0,sticky='w',padx=10)
omg_check=Checkbutton(frame_2,variable=omg,onvalue='OMG',offvalue='',width=10, text= 'OMG', font=('Arial',10,'normal')).grid(row=1,column=0,sticky='w',padx=10)
enj_check=Checkbutton(frame_2,variable=enj,onvalue='ENJ',offvalue='',width=10, text= 'ENJ', font=('Arial',10,'normal')).grid(row=2,column=0,sticky='w',padx=10)
uma_check=Checkbutton(frame_2,variable=uma,onvalue='UMA',offvalue='',width=10, text= 'UMA', font=('Arial',10,'normal')).grid(row=3,column=0,sticky='w',padx=10)
nu_check=Checkbutton(frame_2,variable=nu,onvalue='NU',offvalue='',width=10, text= 'NU', font=('Arial',10,'normal')).grid(row=4,column=0,sticky='w',padx=10)

#6th column
uni_check=Checkbutton(frame_2,variable=uni,onvalue='UNI',offvalue='',width=10, text= 'UNI', font=('Arial',10,'normal')).grid(row=0,column=1,sticky='w',padx=10)
comp_check=Checkbutton(frame_2,variable=comp,onvalue='COMP',offvalue='',width=10, text= 'COMP', font=('Arial',10,'normal')).grid(row=1,column=1,sticky='w',padx=10)
mana_check=Checkbutton(frame_2,variable=mana,onvalue='MANA',offvalue='',width=10, text= 'MANA', font=('Arial',10,'normal')).grid(row=2,column=1,sticky='w',padx=10)
poly_check=Checkbutton(frame_2,variable=poly,onvalue='POLY',offvalue='',width=10, text= 'POLY', font=('Arial',10,'normal')).grid(row=3,column=1,sticky='w',padx=10)
amp_check=Checkbutton(frame_2,variable=amp,onvalue='AMP',offvalue='',width=10, text= 'AMP', font=('Arial',10,'normal')).grid(row=4,column=1,sticky='w',padx=10)

#7th column
mkr_check=Checkbutton(frame_2,variable=mkr,onvalue='MKR',offvalue='',width=10, text= 'MKR', font=('Arial',10,'normal')).grid(row=0,column=2,sticky='w',padx=10)
grt_check=Checkbutton(frame_2,variable=grt,onvalue='GRT',offvalue='',width=10, text= 'GRT', font=('Arial',10,'normal')).grid(row=1,column=2,sticky='w',padx=10)
lrc_check=Checkbutton(frame_2,variable=lrc,onvalue='LRC',offvalue='',width=10, text= 'LRC', font=('Arial',10,'normal')).grid(row=2,column=2,sticky='w',padx=10)
qnt_check=Checkbutton(frame_2,variable=qnt,onvalue='QNT',offvalue='',width=10, text= 'QNT', font=('Arial',10,'normal')).grid(row=3,column=2,sticky='w',padx=10)
bch_check=Checkbutton(frame_2,variable=bch,onvalue='BCH',offvalue='',width=10, text= 'BCH', font=('Arial',10,'normal')).grid(row=4,column=2,sticky='w',padx=10)

#8th column
matic_check=Checkbutton(frame_3,variable=matic,onvalue='MATIC',offvalue='',width=10, text= 'MATIC', font=('Arial',10,'normal')).grid(row=0,column=0,sticky='w',padx=10)
doge_check=Checkbutton(frame_3,variable=doge,onvalue='DOGE',offvalue='',width=10, text= 'DOGE', font=('Arial',10,'normal')).grid(row=1,column=0,sticky='w',padx=10)
audio_check=Checkbutton(frame_3,variable=audio,onvalue='AUDIO',offvalue='',width=10, text= 'AUDIO', font=('Arial',10,'normal')).grid(row=2,column=0,sticky='w',padx=10)
inch_check=Checkbutton(frame_3,variable=inch,onvalue='1INCH',offvalue='',width=10, text= '1INCH', font=('Arial',10,'normal')).grid(row=3,column=0,sticky='w',padx=10)
ksm_check=Checkbutton(frame_3,variable=ksm,onvalue='KSM',offvalue='',width=10, text= 'KSM', font=('Arial',10,'normal')).grid(row=4,column=0,sticky='w',padx=10)

#9th column
snx_check=Checkbutton(frame_3,variable=snx,onvalue='SNX',offvalue='',width=10, text= 'SNX', font=('Arial',10,'normal')).grid(row=0,column=1,sticky='w',padx=10)
chz_check=Checkbutton(frame_3,variable=chz,onvalue='CHZ',offvalue='',width=10, text= 'CHZ', font=('Arial',10,'normal')).grid(row=1,column=1,sticky='w',padx=10)
algo_check=Checkbutton(frame_3,variable=algo,onvalue='ALGO',offvalue='',width=10, text= 'ALGO', font=('Arial',10,'normal')).grid(row=2,column=1,sticky='w',padx=10)
xmr_check=Checkbutton(frame_3,variable=xmr,onvalue='XMR',offvalue='',width=10, text= 'XMR', font=('Arial',10,'normal')).grid(row=3,column=1,sticky='w',padx=10)
sushi_check=Checkbutton(frame_3,variable=sushi,onvalue='SUSHI',offvalue='',width=10, text= 'SUSHI', font=('Arial',10,'normal')).grid(row=4,column=1,sticky='w',padx=10)

#10th column
bat_check=Checkbutton(frame_3,variable=bat,onvalue='BAT',offvalue='',width=10, text= 'BAT', font=('Arial',10,'normal')).grid(row=0,column=2,sticky='w',padx=10)
sol_check=Checkbutton(frame_3,variable=sol,onvalue='SOL',offvalue='',width=10, text= 'SOL', font=('Arial',10,'normal')).grid(row=1,column=2,sticky='w',padx=10)
ape_check=Checkbutton(frame_3,variable=ape,onvalue='APE',offvalue='',width=10, text= 'APE', font=('Arial',10,'normal')).grid(row=2,column=2,sticky='w',padx=10)
mir_check=Checkbutton(frame_3,variable=mir,onvalue='MIR',offvalue='',width=10, text= 'MIR', font=('Arial',10,'normal')).grid(row=3,column=2,sticky='w',padx=10)
yfi_check=Checkbutton(frame_3,variable=yfi,onvalue='YFI',offvalue='',width=10, text= 'YFI', font=('Arial',10,'normal')).grid(row=4,column=2,sticky='w',padx=10)

#11th column
avax_check=Checkbutton(frame_3,variable=avax,onvalue='AVAX',offvalue='',width=10, text= 'AVAX', font=('Arial',10,'normal')).grid(row=0,column=3,sticky='w',padx=10)
axs_check=Checkbutton(frame_3,variable=axs,onvalue='AXS',offvalue='',width=10, text= 'AXS', font=('Arial',10,'normal')).grid(row=1,column=3,sticky='w',padx=10)
bnt_check=Checkbutton(frame_3,variable=bnt,onvalue='BNT',offvalue='',width=10, text= 'BNT', font=('Arial',10,'normal')).grid(row=2,column=3,sticky='w',padx=10)
near_check=Checkbutton(frame_3,variable=near,onvalue='NEAR',offvalue='',width=10, text= 'NEAR', font=('Arial',10,'normal')).grid(row=3,column=3,sticky='w',padx=10)
qtum_check=Checkbutton(frame_3,variable=qtum,onvalue='QTUM',offvalue='',width=10, text= 'QTUM', font=('Arial',10,'normal')).grid(row=4,column=3,sticky='w',padx=10)

#12th column
shib_check=Checkbutton(frame_4,variable=shib,onvalue='SHIB',offvalue='',width=10, text= 'SHIB', font=('Arial',10,'normal')).grid(row=0,column=0,sticky='w',padx=10)
gala_check=Checkbutton(frame_4,variable=gala,onvalue='GALA',offvalue='',width=10, text= 'GALA', font=('Arial',10,'normal')).grid(row=1,column=0,sticky='w',padx=10)
crv_check=Checkbutton(frame_4,variable=crv,onvalue='CRV',offvalue='',width=10, text= 'CRV', font=('Arial',10,'normal')).grid(row=2,column=0,sticky='w',padx=10)
rune_check=Checkbutton(frame_4,variable=rune,onvalue='RUNE',offvalue='',width=10, text= 'RUNE', font=('Arial',10,'normal')).grid(row=3,column=0,sticky='w',padx=10)
badger_check=Checkbutton(frame_4,variable=badger,onvalue='BADGER',offvalue='',width=10, text= 'BADGER', font=('Arial',10,'normal')).grid(row=4,column=0,sticky='w',padx=10)

#13th column
ftm_check=Checkbutton(frame_4,variable=ftm,onvalue='FTM',offvalue='',width=10, text= 'FTM', font=('Arial',10,'normal')).grid(row=0,column=1,sticky='w',padx=10)
sand_check=Checkbutton(frame_4,variable=sand,onvalue='SAND',offvalue='',width=10, text= 'SAND', font=('Arial',10,'normal')).grid(row=1,column=1,sticky='w',padx=10)
skl_check=Checkbutton(frame_4,variable=skl,onvalue='SKL',offvalue='',width=10, text= 'SKL', font=('Arial',10,'normal')).grid(row=2,column=1,sticky='w',padx=10)
etc_check=Checkbutton(frame_4,variable=etc,onvalue='ETC',offvalue='',width=10, text= 'ETC', font=('Arial',10,'normal')).grid(row=3,column=1,sticky='w',padx=10)
cro_check=Checkbutton(frame_4,variable=cro,onvalue='CRO',offvalue='',width=10, text= 'CRO', font=('Arial',10,'normal')).grid(row=4,column=1,sticky='w',padx=10)



#Quote label
quote_label= Label(frame_1,text='Quote pair',font=('Arial',15,'bold'), fg='#7A796E').grid(row=7, column=0,pady=(30,20), padx=(10,0) , sticky='w')
quote_pick=StringVar()

#Quote button
quote_usd=Checkbutton(frame_1,variable=quote_pick, onvalue='/USD', offvalue='', text='USD', width=12,font=('Arial',13,'bold')).grid(row=8,column=0)
quote_usdt=Checkbutton(frame_1,variable=quote_pick, onvalue='/USDT', offvalue='', text='USDT', width=12,font=('Arial',13,'bold')).grid(row=8,column=1)
quote_euro=Checkbutton(frame_1,variable=quote_pick, onvalue='/USDC', offvalue='', text='USDC', width=12,font=('Arial',13,'bold')).grid(row=8,column=2)


#Scenario Label for Ask exchange
ask_scenario_label= Label(frame_1,text='Ask exchange',font=('Arial',15,'bold'), fg='#7A796E').grid(row=9, column=0,pady=(30,20),padx=10, sticky='w')
ask_scenario_pick =StringVar()

# Ask Buttons
ftx_ask_check=Checkbutton(frame_1,variable=ask_scenario_pick, onvalue='ftx_pairs', offvalue='', text='FTX', width=12,font=('Arial',13,'bold')).grid(row=10,column=0)
btcturk_ask_check=Checkbutton(frame_1,variable=ask_scenario_pick, onvalue='btcturk_pairs', offvalue='', text='BtcTurk', width=12,font=('Arial',13,'bold')).grid(row=10,column=1)
coinbase_ask_check=Checkbutton(frame_1,variable=ask_scenario_pick, onvalue='coinbase_pairs', offvalue='', text='Coinbase', width=12,font=('Arial',13,'bold')).grid(row=10,column=2)
kraken_ask_check=Checkbutton(frame_1,variable=ask_scenario_pick, onvalue='kraken_pairs', offvalue='', text='Kraken', width=12,font=('Arial',13,'bold')).grid(row=11,column=0)
okx_ask_check=Checkbutton(frame_1,variable=ask_scenario_pick, onvalue='okx_pairs', offvalue='', text='Okx', width=12,font=('Arial',13,'bold')).grid(row=11,column=1)
okcoin_ask_check=Checkbutton(frame_1,variable=ask_scenario_pick, onvalue='okcoin_pairs', offvalue='', text='Okcoin', width=12,font=('Arial',13,'bold')).grid(row=11,column=2)
huobi_ask_check=Checkbutton(frame_1,variable=ask_scenario_pick, onvalue='huobi_pairs', offvalue='', text='Huobi', width=12,font=('Arial',13,'bold')).grid(row=12,column=0)

#Scenario Label for Bid exchange
bid_scenario_label= Label(frame_1,text='Bid exchange',font=('Arial',15,'bold'), fg='#7A796E').grid(row=13, column=0,pady=(30,20),padx=10, sticky='w')
bid_scenario_pick =StringVar()

#Bid Buttons
ftx_ask_check=Checkbutton(frame_1,variable=bid_scenario_pick, onvalue='ftx_pairs', offvalue='', text='FTX', width=12,font=('Arial',13,'bold')).grid(row=14,column=0)
btcturk_ask_check=Checkbutton(frame_1,variable=bid_scenario_pick, onvalue='btcturk_pairs', offvalue='', text='BtcTurk', width=12,font=('Arial',13,'bold')).grid(row=14,column=1)
coinbase_ask_check=Checkbutton(frame_1,variable=bid_scenario_pick, onvalue='coinbase_pairs', offvalue='', text='Coinbase', width=12,font=('Arial',13,'bold')).grid(row=14,column=2)
kraken_ask_check=Checkbutton(frame_1,variable=bid_scenario_pick, onvalue='kraken_pairs', offvalue='', text='Kraken', width=12,font=('Arial',13,'bold')).grid(row=15,column=0)
okx_ask_check=Checkbutton(frame_1,variable=bid_scenario_pick, onvalue='okx_pairs', offvalue='', text='Okx', width=12,font=('Arial',13,'bold')).grid(row=15,column=1)
okcoin_ask_check=Checkbutton(frame_1,variable=bid_scenario_pick, onvalue='okcoin_pairs', offvalue='', text='Okcoin', width=12,font=('Arial',13,'bold')).grid(row=15,column=2)
huobi_ask_check=Checkbutton(frame_1,variable=bid_scenario_pick, onvalue='huobi_pairs', offvalue='', text='Huobi', width=12,font=('Arial',13,'bold')).grid(row=16,column=0)



#Error label
error_label=Label(frame_1, text='',font=('Arial',15,'bold'), fg='red',padx=10, pady=20 )
error_label.grid(row=17,column=0)




#Button to get the tables
find_arb=Button(frame_1, text='Find arbitrage',width=11,height=2, bg='#23BA86', font=('Arial', 15, 'bold'), command=get_list).grid(row=18, column=0, pady=(35,45),padx=20)

#show_livesrates()

root.mainloop()



