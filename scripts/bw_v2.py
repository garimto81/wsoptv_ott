import sys
sys.stdout.reconfigure(encoding="utf-8")
E = {
  "Bahamas": [("Day 1C",176012,75319,42900),("Day 1D",164870,76606,42900),
    ("Day 2B",332194,193796,42901),("Day 3",378738,239185,42900),
    ("Day 4",280872,163734,22620),("Final Table",485636,309287,37070)],
  "SC Cyprus": [("Day 1A",45261,19369,29476),("Day 1C",44279,18003,26459),
    ("Day 2",66999,29511,34856),("Day 3",63430,29254,26589),
    ("Day 4",66061,31017,24195),("Final Day",75940,40215,21790)],
  "WSOPE": [("Day 1A",27409,10474,38248),("Day 1B",28687,10216,36144),
    ("Day 2",43007,15527,42897),("Day 3",44384,20470,42897),
    ("Day 4",93021,41895,42899),("Final Table",65661,27471,29615)],
}
GB1080=5.0*3600/8/1024; GB720=2.5*3600/8/1024; GB4K=15.0*3600/8/1024
P=print; pct=chr(37)
OTT_CONV={"con":0.05,"base":0.10,"opt":0.15}
SM={"con":1.15,"base":1.15,"opt":1.15}  # ABR overhead only (Multi-Stream multiplier removed v2.3)
P("=" * 90)
P("WSOPTV OTT STREAMING BANDWIDTH ESTIMATION (v2.3 - Multi-Stream removed, ABR 1.15x)")
P("NOTE: YouTube WH = 1-year cumulative (live + replay + organic). No VOD/off-season addition.")
P("=" * 90)
P("OTT conv: Con=5" + pct + " Base=10" + pct + " Opt=15" + pct)
P("Bitrate 1080p=" + str(round(GB1080,3)) + " GB/hr")
P(chr(10) + "=" * 90)
P("SECTION 1: YouTube RAW DATA")
P("=" * 90)
S = {}
for name, streams in E.items():
    P(chr(10) + "### WSOP " + name)
    P("%-15s %10s %10s %7s %8s %10s" % ("Day","Views","WatchHrs","Dur(h)","AvgCCV","Pk1.75x"))
    P("-" * 63)
    tv=twh=tdur=peak=0; dets=[]
    for day,views,wh,dur in streams:
        dh=dur/3600.0; avg=wh/dh; pk=avg*1.75
        tv+=views; twh+=wh; tdur+=dur
        if pk>peak: peak=pk
        dets.append((day,wh,dh,avg,pk))
        P("%-15s %10s %10s %7.2f %8s %10s" % (day,"{:,}".format(views),"{:,}".format(wh),dh,"{:,.0f}".format(avg),"{:,.0f}".format(pk)))
    P("-" * 63)
    P("%-15s %10s %10s %7.1f %8s %10s" % ("TOTAL","{:,}".format(tv),"{:,}".format(twh),tdur/3600,"","{:,.0f}".format(peak)))
    S[name]={"tv":tv,"twh":twh,"tdur":tdur,"peak":peak,"det":dets}
P(chr(10)+"="*90)
P("SECTION 2: OTT BW PER MEASURED EVENT")
P("="*90)
P("%-22s %10s | %10s %10s %10s"%("Event","YT_WH","Con(TB)","Base(TB)","Opt(TB)"))
P("-"*68)
evt_bw={}
for n,s in S.items():
    wh=s["twh"]; bw={}
    for sc in ["con","base","opt"]: bw[sc]=wh*OTT_CONV[sc]*GB1080/1024*SM[sc]
    evt_bw[n]=bw
    P("%-22s %10s | %10.2f %10.2f %10.2f"%("WSOP "+n,"{:,}".format(wh),bw["con"],bw["base"],bw["opt"]))
P(chr(10)+"="*90)
P("SECTION 3: UNMEASURED EVENTS")
P("="*90)
bd=S["Bahamas"]["twh"]/6; cd=S["SC Cyprus"]["twh"]/6; ed=S["WSOPE"]["twh"]/6
P("Daily YT WH: Bah="+"{:,.0f}".format(bd)+" Cyp="+"{:,.0f}".format(cd)+" Eur="+"{:,.0f}".format(ed))
P(chr(10)+"WSOP VEGAS (14 ME + 46 Side):")
veg={}
for sc,mm,sv in [("con",1.5,0.3),("base",1.75,0.4),("opt",2.0,0.5)]:
    wh=bd*mm*14+ed*sv*46; bw=wh*OTT_CONV[sc]*GB1080/1024*SM[sc]
    veg[sc]={"wh":wh,"bw":bw}
    P("  "+sc+": "+"{:,.0f}".format(wh)+" wh -> "+"%.2f TB"%bw)
P(chr(10)+"WSOP SC CANADA (5d):")
can={}
for sc,m in [("con",0.7),("base",0.85),("opt",1.0)]:
    wh=cd*m*5; bw=wh*OTT_CONV[sc]*GB1080/1024*SM[sc]
    can[sc]={"wh":wh,"bw":bw}
    P("  "+sc+": "+"%.2f TB"%bw)
P(chr(10)+"WSOP ASIA (5d):")
asia={}
for sc,m in [("con",0.5),("base",0.65),("opt",0.8)]:
    wh=cd*m*5; bw=wh*OTT_CONV[sc]*GB1080/1024*SM[sc]
    asia[sc]={"wh":wh,"bw":bw}
    P("  "+sc+": "+"%.2f TB"%bw)
P(chr(10)+"="*90)
P("SECTION 4: ANNUAL TOTAL")
P("="*90)
ann={}
for sc,label in [("con","CONSERVATIVE"),("base","BASELINE"),("opt","OPTIMISTIC")]:
    total=sum(evt_bw[n][sc] for n in S)+veg[sc]["bw"]+can[sc]["bw"]+asia[sc]["bw"]
    pb=total/1024
    ann[sc]={"total":total,"pb":pb}
    P(chr(10)+"### "+label)
    for n in S: P("  %-22s %8.2f TB"%("WSOP "+n,evt_bw[n][sc]))
    P("  %-22s %8.2f TB"%("WSOP VEGAS",veg[sc]["bw"]))
    P("  %-22s %8.2f TB"%("WSOP SC Canada",can[sc]["bw"]))
    P("  %-22s %8.2f TB"%("WSOP Asia",asia[sc]["bw"]))
    P("  "+"="*40)
    P("  %-22s %8.2f TB = %.4f PB"%("ANNUAL TOTAL",total,pb))
P(chr(10)+"="*90)
P("SCENARIO COMPARISON")
P("="*90)
h="%-28s %14s %14s %14s"
P(h%("Metric","Conservative","Baseline","Optimistic"))
P("-"*72)
P(h%("OTT Conversion","5 pct","10 pct","15 pct"))
P(h%("Stream Multiplier","2.0x","2.5x","3.0x"))
nf="%-28s %14.2f %14.2f %14.2f"
P(nf%("Annual Total (TB)",ann["con"]["total"],ann["base"]["total"],ann["opt"]["total"]))
P("%-28s %14.4f %14.4f %14.4f"%("Annual Total (PB)",ann["con"]["pb"],ann["base"]["pb"],ann["opt"]["pb"]))
P(chr(10)+"="*90)
P("SECTION 5: VIMEO TIER MAPPING")
P("="*90)
tiers=[("S",326000,5,70),("M",356000,7.5,150),("L",386000,10,300),("XL",426000,15,500),("XXL",486000,20,1024)]
P("%-5s %10s %7s %5s %5s %5s %5s %8s"%("Tier","Cost/yr","BW(PB)","Stor","Con","Base","Opt","BaseUse"))
P("-"*52)
rt="S"; rc=326000
for n,co,bw,st in tiers:
    fc="OK" if bw>=ann["con"]["pb"] else "--"
    fb="OK" if bw>=ann["base"]["pb"] else "--"
    fo="OK" if bw>=ann["opt"]["pb"] else "--"
    ut=ann["base"]["pb"]/bw*100
    P("%-5s $%9s %7.1f %3dTB %5s %5s %5s %7.1f"%(n,"{:,}".format(co),bw,st,fc,fb,fo,ut))
    if bw>=ann["opt"]["pb"] and rt=="S": rt=n; rc=co
P(chr(10)+"RECOMMENDATION: Tier "+rt+" ($"+"{:,}".format(rc)+"/yr)")
P("  Base: %.4f PB = %.1f pct of Tier S"%(ann["base"]["pb"],ann["base"]["pb"]/5*100))
P(chr(10)+"="*90)
P("APPENDIX A: CONCURRENT VIEWERS")
P("="*90)
for n,s in S.items():
    P(chr(10)+"WSOP "+n+":")
    for day,wh,dh,avg,pk in s["det"]:
        P("  %-15s YT_Avg=%8s  OTT_10pct=%6s  OTT_Peak=%6s"%(day,"{:,.0f}".format(avg),"{:,.0f}".format(avg*0.1),"{:,.0f}".format(pk*0.1)))
P(chr(10)+"="*90)
P("APPENDIX B: BW BY QUALITY (Baseline)")
P("="*90)
for n,s in S.items():
    wh=s["twh"]*0.10
    P("WSOP "+n+": OTT_WH="+"{:,.0f}".format(wh)+" -> 720p="+"%.2f"%(wh*GB720/1024*2.5)+"TB 1080p="+"%.2f"%(wh*GB1080/1024*2.5)+"TB 4K="+"%.2f"%(wh*GB4K/1024*2.5)+"TB")
P(chr(10)+"="*90)
P("APPENDIX C: TBD ITEMS")
P("="*90)
for i,t in enumerate(["VEGAS ME: Bah x1.5-2.0","VEGAS Side: WSOPE x0.3-0.5","VEGAS days: 60 assumed","Canada: Cyp x0.7-1.0","Asia: Cyp x0.5-0.8","OTT conv: 5-15 pct (key)","Multi-stream: 2-3x","4K: not in baseline","YT data = 1yr cumulative (no VOD/off-season addition)"],1):
    P("  "+str(i)+". "+t)
P(chr(10)+"="*90)
P("APPENDIX D: STORAGE")
P("="*90)
th=sum(s["tdur"]/3600 for s in S.values())
est=th+14*12+46*8+10*8
rc2=est*4; st2=rc2*GB1080/1024
P("  Stream hrs: %.0f + %.0f = %.0f"%(th,est-th,est))
P("  x4 streams: %.0f hrs -> %.1f TB"%(rc2,st2))
P("  +Archive: ~%.0f TB | Total ~%.0f TB"%(st2*5,st2*6))
P(chr(10)+"="*90)
P("END OF REPORT")
P("="*90)