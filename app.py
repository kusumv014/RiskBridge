import os, io, math, textwrap







from datetime import datetime







import numpy as np







import pandas as pd







import streamlit as st







import plotly.express as px







import plotly.graph_objects as go







import numpy_financial as npf















from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor







from sklearn.model_selection import train_test_split, cross_val_score







from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error















from reportlab.lib import colors







from reportlab.lib.enums import TA_CENTER, TA_LEFT







from reportlab.lib.pagesizes import A4, landscape







from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle







from reportlab.lib.units import mm







from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether







from reportlab.graphics.shapes import Drawing







from reportlab.graphics.charts.barcharts import VerticalBarChart, HorizontalBarChart







from reportlab.graphics.charts.linecharts import HorizontalLineChart















# ============================================================







# PAGE + CONSTANTS







# ============================================================







st.set_page_config(







    page_title="RiskBridge | Zero Trust Business Value Intelligence",







    page_icon="🛡️",







    layout="wide",







    initial_sidebar_state="expanded"







)







BASE_DIR = os.path.dirname(os.path.abspath(__file__))







DATA_CANDIDATES = [







    os.path.join(BASE_DIR, "zero_trust_business_value_dataset_10000.csv"),







    os.path.join(BASE_DIR, "zero_trust_business_value_dataset_10000(1).csv"),







]







DATA_FILE = next((p for p in DATA_CANDIDATES if os.path.exists(p)), DATA_CANDIDATES[0])







RANDOM_SEED = 42







HORIZON = 5







N_MC = 10000















PILLARS = {







    "Identity": ["Multi-Factor Authentication", "Identity Lifecycle Management", "Conditional Access", "Privileged Access Management"],







    "Devices": ["Device Inventory", "Device Compliance", "Endpoint Protection", "Device Health Monitoring"],







    "Networks": ["Network Segmentation", "Encrypted Communications", "Network Monitoring", "Software-Defined Access"],







    "Applications": ["Application Access Control", "Workload Identity", "Application Security Monitoring", "Secure Application Integration"],







    "Data": ["Data Classification", "Data Encryption", "Data Loss Prevention", "Data Access Governance"],







}







MATURITY_LEVELS = {1:"Traditional", 2:"Initial", 3:"Advanced", 4:"Optimal"}







ML_FEATURES = ["Employees","Current_Maturity","Target_Maturity","Maturity_Improvement","SLE_USD","LEF",







               "Breach_Likelihood_Reduction","Breach_Impact_Reduction","MTTR_Improvement","Implementation_Cost_USD",







               "Annual_OpEx_USD","Discount_Rate"]















# ============================================================







# VISUAL SYSTEM







# ============================================================







BG="#06101F"; BG2="#091827"; CARD="#0B1A2A"; BORDER="#1A344C"; TEXT="#F8FAFC"; MUTED="#91A8BF"







CYAN="#18C7D4"; BLUE="#2684FF"; GREEN="#22C55E"; AMBER="#F59E0B"; RED="#EF4444"; VIOLET="#8B5CF6"







PLOT_COLORS=[CYAN,BLUE,VIOLET,GREEN,AMBER,RED,"#38BDF8","#A78BFA"]















st.markdown(f"""







<style>







.stApp{{background:{BG};color:{TEXT}}}







.block-container{{max-width:1540px;padding-top:1.25rem;padding-bottom:4rem}}







h1,h2,h3,h4{{color:{TEXT};letter-spacing:-.02em}} p{{color:#C7D3E3}}







[data-testid="stSidebar"]{{background:#081725;border-right:1px solid #183047;min-width:365px;max-width:365px}}







[data-testid="stSidebar"] .block-container{{padding-left:0!important;padding-right:0!important}}







.brand{{padding:20px 22px;border-bottom:1px solid #183047;margin-bottom:12px}}







.brand-title{{font-size:22px;font-weight:850;color:#F8FAFC}} .brand-sub{{font-size:10px;color:#6F89A4;letter-spacing:.15em;text-transform:uppercase;margin-top:4px}}







.nav-group{{font-size:10px;color:#6F89A4;letter-spacing:.14em;text-transform:uppercase;font-weight:800;padding:12px 22px 8px}}







[data-testid="stSidebar"] div[role="radiogroup"]{{gap:2px;padding:0 12px}}



[data-testid="stSidebar"] div[role="radiogroup"]>label{{min-height:38px;padding:7px 12px!important;border-radius:9px;border:0!important;display:flex;align-items:center}}



[data-testid="stSidebar"] div[role="radiogroup"]>label:hover{{background:#102437}}



[data-testid="stSidebar"] div[role="radiogroup"]>label:has(input:checked){{background:#162A3C!important;box-shadow:none!important}}



[data-testid="stSidebar"] div[role="radiogroup"] input{{display:none!important}}

[data-testid="stSidebar"] div[role="radiogroup"]>label>div:first-child{{display:none!important}}

[data-testid="stSidebar"] div[role="radiogroup"]>label{{gap:0!important}}



[data-testid="stSidebar"] div[role="radiogroup"] [data-testid="stMarkdownContainer"]{{margin:0!important}}



[data-testid="stSidebar"] div[role="radiogroup"] p{{color:#C5D4E3!important;font-size:13px!important;margin:0!important}}



[data-testid="stSidebar"] div[role="radiogroup"]>label:has(input:checked) p{{color:#FFFFFF!important;font-weight:650!important}}



.hero{{padding:30px 32px;border:1px solid {BORDER};border-radius:16px;background:linear-gradient(135deg,#0A1B2D,#0B1B30 70%,#101B36);margin-bottom:20px}}







.eyebrow{{font-size:10px;font-weight:850;color:{CYAN};letter-spacing:.15em;text-transform:uppercase}}







.hero-title{{font-size:34px;font-weight:850;color:{TEXT};line-height:1.1;margin-top:8px}}







.hero-sub{{font-size:13px;color:#AFC1D5;line-height:1.65;max-width:1080px;margin-top:10px}}







.page-title{{font-size:30px;font-weight:850;color:{TEXT};margin:4px 0}} .page-desc{{font-size:13px;color:{MUTED};line-height:1.6;margin-bottom:18px}}







.kicker{{font-size:9px;font-weight:850;color:{CYAN};letter-spacing:.15em;text-transform:uppercase}}







.panel{{background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:18px;margin:8px 0 16px}}







.insight{{background:#071E2C;border-left:3px solid {CYAN};padding:13px 16px;border-radius:3px 8px 8px 3px;color:#C8E7EB;font-size:12px;line-height:1.6;margin:12px 0}}







.warn{{background:#211A0C;border-left:3px solid {AMBER};padding:13px 16px;border-radius:3px 8px 8px 3px;color:#F7DFAB;font-size:12px;line-height:1.6;margin:12px 0}}







.good{{background:#092417;border-left:3px solid {GREEN};padding:13px 16px;border-radius:3px 8px 8px 3px;color:#CFF7DE;font-size:12px;line-height:1.6;margin:12px 0}}







div[data-testid="stMetric"]{{background:{CARD};border:1px solid {BORDER};padding:14px;border-radius:10px}}







div[data-testid="stMetricValue"]{{color:{TEXT};font-size:27px}} div[data-testid="stMetricLabel"]{{color:#9FB3C8}}







.stButton>button,.stDownloadButton>button{{border-radius:8px;min-height:40px;font-weight:750;border:1px solid #24506A}}







[data-testid="stDataFrame"]{{border:1px solid {BORDER};border-radius:9px;overflow:hidden}}







.small{{font-size:11px;color:{MUTED}}}







</style>







""", unsafe_allow_html=True)















# ============================================================







# HELPERS







# ============================================================







def currency(v):







    if v is None or not np.isfinite(v): return "N/A"







    sign="-" if v<0 else ""







    return f"{sign}${abs(v):,.0f}"







def pct(v):







    if v is None or not np.isfinite(v): return "N/A"







    return f"{v*100:,.1f}%"







def page_header(kicker,title,desc):







    st.markdown(f'<div class="kicker">{kicker}</div><div class="page-title">{title}</div><div class="page-desc">{desc}</div>',unsafe_allow_html=True)







def dark(fig, height=None):







    fig.update_layout(template="plotly_dark",paper_bgcolor=BG,plot_bgcolor=BG,font=dict(color=TEXT),







                      colorway=PLOT_COLORS,margin=dict(l=25,r=25,t=55,b=25),legend_title_text="")







    if height: fig.update_layout(height=height)







    fig.update_xaxes(gridcolor="#183047",zerolinecolor="#34506A")







    fig.update_yaxes(gridcolor="#183047",zerolinecolor="#34506A")







    return fig







def section(title, subtitle=None):







    st.markdown(f"### {title}")







    if subtitle: st.caption(subtitle)







def insight_box(html, kind="insight"):







    st.markdown(f'<div class="{kind}">{html}</div>',unsafe_allow_html=True)















@st.cache_data(show_spinner=False)







def load_dataset():







    if os.path.exists(DATA_FILE): return pd.read_csv(DATA_FILE)







    return None















def calc_risk(sle, lef, lr, ir):







    baseline=sle*lef; rlef=lef*(1-lr); rsle=sle*(1-ir); residual=rlef*rsle; avoided=baseline-residual







    return dict(baseline_ale=baseline,residual_lef=rlef,residual_sle=rsle,residual_ale=residual,







                avoided_loss=avoided,risk_reduction=(avoided/baseline if baseline>0 else 0))















def calc_financial(gross_benefit, impl, opex, dr, horizon=HORIZON):







    annual_net=gross_benefit-opex; cfs=[-impl]+[annual_net]*horizon







    npv=float(npf.npv(dr,cfs)); irr=float(npf.irr(cfs)) if annual_net>0 else np.nan







    roi=((annual_net*horizon)-impl)/impl if impl>0 else np.nan







    payback=impl/annual_net if annual_net>0 else np.inf







    cumulative=np.cumsum(cfs)







    return dict(annual_net_benefit=annual_net,cash_flows=cfs,npv=npv,irr=irr,roi_5y=roi,payback=payback,cumulative=cumulative)















def benefit_components():
    # Derive avoided loss from the latest session-state inputs on every rerun.
    current_risk = calc_risk(
        st.session_state.sle,
        st.session_state.lef,
        st.session_state.lr,
        st.session_state.ir,
    )
    return {
        "Avoided cyber loss": current_risk["avoided_loss"],
        "Tool consolidation": st.session_state.tool_savings,
        "Incident response": st.session_state.ir_savings,
        "Compliance": st.session_state.compliance_savings,
        "Productivity": st.session_state.productivity_savings,
    }















def maturity_detail():







    rows=[]







    for p,caps in PILLARS.items():







        for cap in caps:







            c=st.session_state[f"cur_{p}_{cap}"]; t=st.session_state[f"tar_{p}_{cap}"]







            rows.append({"Pillar":p,"Capability":cap,"Current":c,"Target":t,"Gap":t-c})







    detail=pd.DataFrame(rows)







    pillars=detail.groupby("Pillar",as_index=False)[["Current","Target","Gap"]].mean()







    return detail,pillars,float(detail.Current.mean()),float(detail.Target.mean())















def current_ml_row(cur_m, tar_m):







    return pd.DataFrame([{







        "Employees":st.session_state.employees,"Current_Maturity":cur_m,"Target_Maturity":tar_m,







        "Maturity_Improvement":tar_m-cur_m,"SLE_USD":st.session_state.sle,"LEF":st.session_state.lef,







        "Breach_Likelihood_Reduction":st.session_state.lr,"Breach_Impact_Reduction":st.session_state.ir,







        "MTTR_Improvement":st.session_state.mttr,"Implementation_Cost_USD":st.session_state.impl,







        "Annual_OpEx_USD":st.session_state.opex,"Discount_Rate":st.session_state.dr







    }])[ML_FEATURES]















@st.cache_resource(show_spinner=False)







def train_models():







    df=load_dataset()







    if df is None: return None







    missing=[c for c in ML_FEATURES+["NPV_5Y_USD"] if c not in df.columns]







    if missing: return {"error":", ".join(missing)}







    X=df[ML_FEATURES]; y=df["NPV_5Y_USD"]







    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.30,random_state=RANDOM_SEED)







    rf=RandomForestRegressor(n_estimators=300,max_depth=10,min_samples_split=10,min_samples_leaf=5,max_features=.8,random_state=42,n_jobs=-1)







    gb=GradientBoostingRegressor(n_estimators=200,learning_rate=.05,max_depth=3,min_samples_split=10,min_samples_leaf=5,subsample=.8,random_state=42)







    rf.fit(Xtr,ytr); gb.fit(Xtr,ytr)







    def m(model):







        pred=model.predict(Xte)







        return {"R2":r2_score(yte,pred),"MAE":mean_absolute_error(yte,pred),"RMSE":np.sqrt(mean_squared_error(yte,pred)),"pred":pred}







    return {"rf":rf,"gb":gb,"Xtr":Xtr,"Xte":Xte,"ytr":ytr,"yte":yte,"rfm":m(rf),"gbm":m(gb)}















# ============================================================







# REPORT ENGINE







# ============================================================







def pdf_styles():







    s=getSampleStyleSheet()







    s.add(ParagraphStyle(name="ZTTitle",parent=s["Title"],fontSize=21,leading=25,textColor=colors.HexColor("#071B3A"),alignment=TA_CENTER,spaceAfter=8))







    s.add(ParagraphStyle(name="ZTH1",parent=s["Heading1"],fontSize=15,leading=19,textColor=colors.HexColor("#0B4F6C"),spaceBefore=8,spaceAfter=7))







    s.add(ParagraphStyle(name="ZTBody",parent=s["BodyText"],fontSize=9.5,leading=14,textColor=colors.HexColor("#1F2937")))







    s.add(ParagraphStyle(name="ZTNote",parent=s["BodyText"],fontSize=8,leading=11,textColor=colors.HexColor("#64748B")))







    return s















def pdf_table(rows, widths=None, font=8):







    t=Table(rows,colWidths=widths,repeatRows=1,hAlign="LEFT")







    t.setStyle(TableStyle([







        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#0B4F6C")),("TEXTCOLOR",(0,0),(-1,0),colors.white),







        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("FONTSIZE",(0,0),(-1,-1),font),







        ("GRID",(0,0),(-1,-1),.35,colors.HexColor("#CBD5E1")),("VALIGN",(0,0),(-1,-1),"TOP"),







        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F8FAFC")]),("PADDING",(0,0),(-1,-1),5)







    ])); return t















def pdf_bar_chart(labels, values, title, width=460, height=180):







    d=Drawing(width,height); c=VerticalBarChart(); c.x=45;c.y=35;c.height=105;c.width=380







    c.data=[values]; c.categoryAxis.categoryNames=labels; c.valueAxis.valueMin=min(0,min(values)*1.1); c.valueAxis.valueMax=max(values)*1.2 if max(values)>0 else 1







    c.bars[0].fillColor=colors.HexColor("#0B7285"); c.categoryAxis.labels.fontSize=6; c.valueAxis.labels.fontSize=6







    d.add(c); return d















def build_pdf(report_type, detail, pillars, cur_m, tar_m, risk, fin, dataset):







    buf=io.BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=15*mm,bottomMargin=15*mm)







    s=pdf_styles(); story=[Paragraph("RiskBridge — Zero Trust Business Value Decision Support",s["ZTTitle"]),Paragraph(report_type,s["ZTH1"]),







        Paragraph(f"Organisation: <b>{st.session_state.org_name}</b> &nbsp;&nbsp; Industry: {st.session_state.industry} &nbsp;&nbsp; Employees: {st.session_state.employees:,}",s["ZTBody"]),







        Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}",s["ZTNote"]),Spacer(1,8)]







    summary=[ ["Metric","Result"], ["Current maturity",f"{cur_m:.2f}/4"],["Target maturity",f"{tar_m:.2f}/4"],







              ["Baseline ALE",currency(risk['baseline_ale'])],["Residual ALE",currency(risk['residual_ale'])],["Risk reduction",pct(risk['risk_reduction'])],







              ["5-year NPV",currency(fin['npv'])],["5-year ROI",pct(fin['roi_5y'])],["IRR",pct(fin['irr']) if np.isfinite(fin['irr']) else 'N/A'],







              ["Payback",f"{fin['payback']:.2f} years" if np.isfinite(fin['payback']) else 'Not achieved'] ]







    story += [pdf_table(summary,[75*mm,90*mm]),Spacer(1,10)]







    if report_type in ("Full Assessment Report","Zero Trust Assessment Report"):







        story += [Paragraph("Maturity Assessment",s["ZTH1"]), pdf_table([["Pillar","Current","Target","Gap"]]+[[r.Pillar,f"{r.Current:.2f}",f"{r.Target:.2f}",f"{r.Gap:.2f}"] for r in pillars.itertuples()],[55*mm,30*mm,30*mm,30*mm]),Spacer(1,8),







                  pdf_bar_chart(pillars.Pillar.tolist(),pillars.Gap.tolist(),"Maturity gaps"),Spacer(1,8)]







    if report_type in ("Full Assessment Report","Cyber Risk Report"):







        story += [Paragraph("Cyber Risk Quantification",s["ZTH1"]),Paragraph("The model converts SLE and LEF into baseline annual loss exposure and applies scenario-specific likelihood and impact reductions to estimate residual exposure.",s["ZTBody"]),Spacer(1,6),







                  pdf_table([["Risk measure","Value"],["SLE",currency(st.session_state.sle)],["LEF",f"{st.session_state.lef:.3f}"],["Baseline ALE",currency(risk['baseline_ale'])],["Residual ALE",currency(risk['residual_ale'])],["Avoided annual loss",currency(risk['avoided_loss'])],["Risk reduction",pct(risk['risk_reduction'])]],[80*mm,80*mm]),Spacer(1,8)]







    if report_type in ("Full Assessment Report","Financial Business Case"):







        story += [Paragraph("Financial Business Case",s["ZTH1"]),pdf_table([["Financial measure","Value"],["Implementation cost",currency(st.session_state.impl)],["Annual OpEx",currency(st.session_state.opex)],["Gross annual benefit",currency(sum(benefit_components().values()))],["Annual net benefit",currency(fin['annual_net_benefit'])],["5-year NPV",currency(fin['npv'])],["5-year ROI",pct(fin['roi_5y'])],["IRR",pct(fin['irr']) if np.isfinite(fin['irr']) else 'N/A'],["Payback",f"{fin['payback']:.2f} years" if np.isfinite(fin['payback']) else 'Not achieved']],[80*mm,80*mm]),Spacer(1,8),







                  pdf_bar_chart([f"Y{i}" for i in range(6)],fin['cash_flows'],"Cash flow"),Spacer(1,8)]







    if report_type in ("Full Assessment Report","Monte Carlo Report") and dataset is not None:







        n=dataset.NPV_5Y_USD







        story += [Paragraph("Simulation Evidence",s["ZTH1"]),pdf_table([["Statistic","Result"],["Scenarios",f"{len(dataset):,}"],["P5 NPV",currency(n.quantile(.05))],["Median NPV",currency(n.median())],["P95 NPV",currency(n.quantile(.95))],["Positive NPV proportion",pct((n>0).mean())]],[80*mm,80*mm]),Spacer(1,8)]







    if report_type in ("Full Assessment Report","Implementation Roadmap"):







        pr=pillars.sort_values("Gap",ascending=False).reset_index(drop=True)







        roadmap=[["Phase","Priority pillar","Gap","Indicative focus"]]







        windows=["0–3 months","3–6 months","6–9 months","9–12 months","12+ months"]







        for i,r in pr.iterrows(): roadmap.append([windows[i],r.Pillar,f"{r.Gap:.2f}","Close highest assessed capability gaps first"])







        story += [Paragraph("Prioritised Implementation Roadmap",s["ZTH1"]),pdf_table(roadmap,[30*mm,42*mm,20*mm,75*mm]),Spacer(1,8)]







    story += [Paragraph("Interpretation & Limitations",s["ZTH1"]),Paragraph("This output is generated from user-selected assumptions and a synthetic research dataset. It supports structured comparison and scenario analysis; it is not an audit, external validation, or guaranteed forecast of realised organisational outcomes.",s["ZTBody"])]







    doc.build(story); buf.seek(0); return buf.getvalue()















def build_excel(detail,pillars,risk,fin,dataset):







    out=io.BytesIO()







    with pd.ExcelWriter(out,engine="openpyxl") as w:







        pd.DataFrame({"Metric":["Organisation","Industry","Employees","Current Maturity","Target Maturity","Baseline ALE","Residual ALE","Avoided Loss","5Y NPV","5Y ROI","IRR","Payback"],







                      "Value":[st.session_state.org_name,st.session_state.industry,st.session_state.employees,cur_m,tar_m,risk['baseline_ale'],risk['residual_ale'],risk['avoided_loss'],fin['npv'],fin['roi_5y'],fin['irr'],fin['payback']]}).to_excel(w,sheet_name="Executive Summary",index=False)







        detail.to_excel(w,sheet_name="Maturity Detail",index=False); pillars.to_excel(w,sheet_name="Pillar Summary",index=False)







        pd.DataFrame({"Year":range(6),"Cash Flow":fin['cash_flows'],"Cumulative":fin['cumulative']}).to_excel(w,sheet_name="Cash Flow",index=False)







        if dataset is not None: dataset.describe(include="all").T.to_excel(w,sheet_name="Dataset Profile")







    out.seek(0); return out.getvalue()















# ============================================================







# SESSION DEFAULTS







# ============================================================







defaults={"org_name":"Sample Organisation","industry":"Financial Services","employees":500,"sle":4_440_000.0,"lef":.10,







          "lr":.20,"ir":.20,"mttr":.15,"impl":185_000.0,"opex":30_000.0,"dr":.10,







          "tool_savings":10_000.0,"ir_savings":5_000.0,"compliance_savings":10_000.0,"productivity_savings":15_000.0}







for k,v in defaults.items():







    if k not in st.session_state: st.session_state[k]=v







for p,caps in PILLARS.items():







    for cap in caps:







        st.session_state.setdefault(f"cur_{p}_{cap}",2); st.session_state.setdefault(f"tar_{p}_{cap}",3)















dataset=load_dataset(); detail,pillars,cur_m,tar_m=maturity_detail()







risk=calc_risk(st.session_state.sle,st.session_state.lef,st.session_state.lr,st.session_state.ir)







gross_benefit=sum(benefit_components().values())







financial=calc_financial(gross_benefit,st.session_state.impl,st.session_state.opex,st.session_state.dr)













st.markdown(f"""

<style>



/* ============================================================

   RISKBRIDGE SIDEBAR

   ============================================================ */



[data-testid="stSidebar"] {{

    background: #081725;

    border-right: 1px solid #183047;

    min-width: 380px !important;

    max-width: 380px !important;

}}



/* Sidebar inner area */

[data-testid="stSidebar"] > div:first-child {{

    overflow-y: auto !important;

    overflow-x: hidden !important;

    height: 100vh !important;

}}



/* Better scrollbar */

[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {{

    width: 7px;

}}



[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-track {{

    background: transparent;

}}



[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {{

    background: #29445B;

    border-radius: 10px;

}}



[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb:hover {{

    background: #3C607B;

}}





/* ============================================================

   BRAND

   ============================================================ */



.brand {{

    padding: 26px 28px 22px 28px;

    border-bottom: 1px solid #183047;

    margin-bottom: 14px;

}}



.brand-title {{

    font-size: 25px !important;

    font-weight: 850 !important;

    color: #F8FAFC !important;

    letter-spacing: -0.02em;

}}



.brand-sub {{

    font-size: 10px !important;

    color: #7895B0 !important;

    letter-spacing: .16em;

    text-transform: uppercase;

    margin-top: 7px;

}}





/* ============================================================

   DECISION PLATFORM HEADING

   ============================================================ */



.nav-group {{

    font-size: 11px !important;

    color: #7895B0 !important;

    letter-spacing: .15em;

    text-transform: uppercase;

    font-weight: 800;

    padding: 16px 28px 10px 28px;

}}





/* ============================================================

   NAVIGATION

   ============================================================ */



[data-testid="stSidebar"] div[role="radiogroup"] {{

    gap: 5px !important;

    padding: 0 18px !important;

}}





/* Each navigation row */

[data-testid="stSidebar"] div[role="radiogroup"] > label {{

    min-height: 47px !important;

    padding: 0 15px !important;

    margin: 0 !important;



    display: flex !important;

    align-items: center !important;



    border-radius: 10px !important;

    border: none !important;



    cursor: pointer !important;

    transition: background .15s ease !important;

}}





/* REMOVE STREAMLIT RADIO CIRCLES */

[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {{

    display: none !important;

}}



[data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {{

    display: none !important;

}}





/* Navigation text */

[data-testid="stSidebar"] div[role="radiogroup"] label p {{

    font-size: 15px !important;

    font-weight: 500 !important;

    color: #D5E2EF !important;

    line-height: 1.25 !important;

    margin: 0 !important;

}}





/* Hover */

[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{

    background: #10283A !important;

}}





/* Selected navigation item */

/* :has() is not supported consistently in all CSS parsers/runtime contexts, so the

   selected-state styling is intentionally left to the default Streamlit radio markup. */





/* ============================================================

   SIDEBAR GENERAL TEXT

   ============================================================ */



[data-testid="stSidebar"] p {{

    font-size: 14px;

}}



</style>

""", unsafe_allow_html=True)














# ============================================================
# SIDEBAR NAVIGATION + COMMAND CENTRE
# ============================================================

# Final sidebar patch: larger text, scrollable navigation, no radio dots.
st.markdown("""
<style>
[data-testid="stSidebar"] {
    min-width: 390px !important;
    max-width: 390px !important;
}
[data-testid="stSidebar"] > div:first-child {
    height: 100vh !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
}
[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
    width: 7px;
}
[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar-thumb {
    background: #29445B;
    border-radius: 10px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
    gap: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    min-height: 46px !important;
    padding: 0 14px !important;
    margin: 0 12px !important;
    border-radius: 10px !important;
    display: flex !important;
    align-items: center !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #10283A !important;
}
/* Hide every native radio indicator while retaining clickable labels */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadio"] label [data-baseweb="radio"] > div:first-child,
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"],
[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
    display: none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    font-size: 15px !important;
    line-height: 1.25 !important;
    font-weight: 500 !important;
    color: #D5E2EF !important;
    margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #183147 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        '<div class="brand"><div class="brand-title">◇ RISKBRIDGE</div>'
        '<div class="brand-sub">ZERO TRUST BUSINESS VALUE INTELLIGENCE</div></div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="nav-group">Decision Platform</div>', unsafe_allow_html=True)

    pages = [
        "01  Command Centre",
        "02  Organisation & Assumptions",
        "03  Maturity Assessment",
        "04  Risk Intelligence",
        "05  Financial Intelligence",
        "06  Scenario Studio",
        "07  Monte Carlo Lab",
        "08  ML & XAI Lab",
        "09  Sensitivity & Thresholds",
        "10  Decision Studio",
        "11  Implementation Roadmap",
        "12  Validation",
        "13  Report Centre",
    ]
    page = st.radio("Navigation", pages, label_visibility="collapsed")

    st.markdown(
        '<div style="margin:22px 20px 28px;padding:16px;border:1px solid #17354B;'
        'border-radius:12px;background:#0B1E2F;font-size:13px;color:#9DB2C7;line-height:1.8;">'
        '<b style="color:#E5EEF7;">Research configuration</b><br>'
        f'{len(dataset) if dataset is not None else 0:,} simulated scenarios<br>'
        '12 predictive features<br>70 / 30 train-test split<br>5-year horizon</div>',
        unsafe_allow_html=True
    )

# ============================================================
# 01 COMMAND CENTRE
# ============================================================

if page.startswith("01"):
    st.markdown(
        '<div class="hero">'
        '<div class="eyebrow">MSc Data Science &amp; Artificial Intelligence • Research Artefact</div>'
        '<div class="hero-title">RiskBridge</div>'
        '<div class="hero-sub">Zero Trust Business Value Intelligence</div>'
        '<div class="hero-sub">A unified decision-support platform connecting Zero Trust maturity, '
        'quantitative cyber risk, financial value, uncertainty, machine learning, explainability '
        'and implementation priorities.</div></div>',
        unsafe_allow_html=True
    )

    c = st.columns(6)
    c[0].metric("Current Maturity", f"{cur_m:.2f}/4", f"Target {tar_m:.2f}")
    c[1].metric("Baseline ALE", currency(risk["baseline_ale"]))
    c[2].metric("Residual ALE", currency(risk["residual_ale"]), f"-{risk['risk_reduction']:.1%}")
    c[3].metric("5Y NPV", currency(financial["npv"]))
    c[4].metric("5Y ROI", pct(financial["roi_5y"]))
    c[5].metric("Payback", f"{financial['payback']:.2f} yrs" if np.isfinite(financial["payback"]) else "N/A")

    c1, c2 = st.columns(2)
    with c1:
        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(
            r=pillars["Current"], theta=pillars["Pillar"], fill="toself", name="Current"
        ))
        radar.add_trace(go.Scatterpolar(
            r=pillars["Target"], theta=pillars["Pillar"], fill="toself", name="Target"
        ))
        radar.update_layout(
            polar=dict(radialaxis=dict(range=[0, 4])),
            title="Zero Trust Maturity Profile"
        )
        st.plotly_chart(dark(radar, 440), use_container_width=True)

    with c2:
        cash = pd.DataFrame({
            "Year": range(6),
            "Annual Cash Flow": financial["cash_flows"],
            "Cumulative": financial["cumulative"],
        })
        trajectory = go.Figure()
        trajectory.add_bar(x=cash["Year"], y=cash["Annual Cash Flow"], name="Annual Cash Flow")
        trajectory.add_scatter(
            x=cash["Year"], y=cash["Cumulative"], mode="lines+markers", name="Cumulative"
        )
        trajectory.add_hline(y=0, line_dash="dash")
        trajectory.update_layout(title="Five-Year Financial Trajectory")
        st.plotly_chart(dark(trajectory, 440), use_container_width=True)

    st.markdown("## Decision Signals")
    top_pillar = pillars.sort_values("Gap", ascending=False).iloc[0]
    a, b, c3 = st.columns(3)
    with a:
        insight_box(
            f"<b>Largest maturity gap:</b> {top_pillar.Pillar} "
            f"({top_pillar.Gap:.2f} points). This pillar should receive early assessment attention."
        )
    with b:
        insight_box(
            f"<b>Modelled risk change:</b> annual loss exposure falls from "
            f"{currency(risk['baseline_ale'])} to {currency(risk['residual_ale'])} "
            f"under the selected assumptions."
        )
    with c3:
        if dataset is not None and "NPV_5Y_USD" in dataset.columns:
            positive = (dataset["NPV_5Y_USD"] > 0).mean()
            insight_box(
                f"<b>Simulation context:</b> {positive:.1%} of synthetic scenarios have positive "
                "five-year NPV. This describes the simulated dataset, not an empirical probability."
            )
        else:
            insight_box("<b>Simulation context:</b> Dataset unavailable for scenario comparison.", "warn")



# ============================================================







# 02 INPUTS







# ============================================================







elif page.startswith("02"):







    page_header("INPUT LAYER","Organisation & Assumptions","Define the organisational, cyber-risk, benefit and financial assumptions used throughout the platform.")







    c1,c2,c3=st.columns(3)







    with c1: st.text_input("Organisation name",key="org_name")







    with c2: st.selectbox("Industry",["Financial Services","Healthcare","Technology","Retail","Manufacturing","Professional Services","Government","Education","Other"],key="industry")







    with c3: st.number_input("Employees",min_value=1,step=50,key="employees")







    section("Cyber-risk assumptions")







    c1,c2,c3,c4=st.columns(4)







    with c1: st.number_input("Single Loss Expectancy — SLE ($)",min_value=0.0,step=10000.0,key="sle")







    with c2: st.number_input("Loss Event Frequency — LEF",min_value=0.0,max_value=1.0,step=.01,key="lef")







    with c3:
        lr_pct = st.slider("Likelihood reduction", 0, 80, value=int(round(float(st.session_state.lr) * 100)), step=1, format="%d%%", key="lr_pct")
        st.session_state.lr = lr_pct / 100.0







    with c4:
        ir_pct = st.slider("Impact reduction", 0, 80, value=int(round(float(st.session_state.ir) * 100)), step=1, format="%d%%", key="ir_pct")
        st.session_state.ir = ir_pct / 100.0







    mttr_pct = st.slider("MTTR improvement", 0, 80, value=int(round(float(st.session_state.mttr) * 100)), step=1, format="%d%%", key="mttr_pct")
    st.session_state.mttr = mttr_pct / 100.0







    section("Operational benefit assumptions","These benefits are kept separate so the business case is not based on avoided cyber loss alone.")







    c1,c2,c3,c4=st.columns(4)







    with c1: st.number_input("Tool consolidation savings ($/yr)",min_value=0.0,step=1000.0,key="tool_savings")







    with c2: st.number_input("Incident response savings ($/yr)",min_value=0.0,step=1000.0,key="ir_savings")







    with c3: st.number_input("Compliance savings ($/yr)",min_value=0.0,step=1000.0,key="compliance_savings")







    with c4: st.number_input("Productivity savings ($/yr)",min_value=0.0,step=1000.0,key="productivity_savings")







    section("Financial assumptions")







    c1,c2,c3=st.columns(3)







    with c1: st.number_input("Implementation cost ($)",min_value=0.0,step=5000.0,key="impl")







    with c2: st.number_input("Annual OpEx ($)",min_value=0.0,step=1000.0,key="opex")







    with c3:
        dr_pct = st.slider("Discount rate", 0, 30, value=int(round(float(st.session_state.dr) * 100)), step=1, format="%d%%", key="dr_pct")
        st.session_state.dr = dr_pct / 100.0







    insight_box("Inputs are scenario assumptions. Control-effect assumptions are intentionally separated from ordinal maturity scores to avoid treating maturity points as fixed breach-probability reductions.","warn")















# ============================================================







# 03 MATURITY







# ============================================================







elif page.startswith("03"):







    page_header("ASSESSMENT CENTRE","Zero Trust Maturity Assessment","Assess 20 capabilities across Identity, Devices, Networks, Applications and Data, then identify the largest implementation gaps.")







    c1,c2,c3,c4=st.columns(4); c1.metric("Current",f"{cur_m:.2f}/4");c2.metric("Target",f"{tar_m:.2f}/4");c3.metric("Gap",f"{tar_m-cur_m:.2f}");c4.metric("Capabilities","20")







    tabs=st.tabs(["Assessment","Radar & Pillars","Gap Heatmap","Priority Register"])







    with tabs[0]:







        for p,caps in PILLARS.items():







            with st.expander(f"🛡️ {p}",expanded=(p=="Identity")):







                for cap in caps:







                    a,b,c=st.columns([2.2,1,1]); a.markdown(f"**{cap}**")







                    with b: st.select_slider("Current",[1,2,3,4],format_func=lambda x:f"{x} — {MATURITY_LEVELS[x]}",key=f"cur_{p}_{cap}")







                    with c: st.select_slider("Target",[1,2,3,4],format_func=lambda x:f"{x} — {MATURITY_LEVELS[x]}",key=f"tar_{p}_{cap}")







    detail,pillars,cur_m,tar_m=maturity_detail()







    with tabs[1]:







        c1,c2=st.columns(2)







        with c1:







            rd=go.Figure(); rd.add_trace(go.Scatterpolar(r=pillars.Current,theta=pillars.Pillar,fill='toself',name='Current'));rd.add_trace(go.Scatterpolar(r=pillars.Target,theta=pillars.Pillar,fill='toself',name='Target'));rd.update_layout(polar=dict(radialaxis=dict(range=[0,4])),title="Current vs Target Maturity");st.plotly_chart(dark(rd,430),use_container_width=True)







        with c2:







            md=pillars.melt(id_vars="Pillar",value_vars=["Current","Target"],var_name="Assessment",value_name="Score");fig=px.bar(md,x="Pillar",y="Score",color="Assessment",barmode="group",range_y=[0,4],title="Pillar Scores");st.plotly_chart(dark(fig,430),use_container_width=True)







    with tabs[2]:







        hm=detail.pivot(index="Capability",columns="Pillar",values="Gap")







        fig=px.imshow(hm,aspect="auto",text_auto=".0f",color_continuous_scale="YlOrRd",title="Capability Gap Heatmap");st.plotly_chart(dark(fig,650),use_container_width=True)







    with tabs[3]:







        pr=detail.sort_values(["Gap","Pillar"],ascending=[False,True]).copy(); pr["Priority"]=np.where(pr.Gap>=2,"Critical",np.where(pr.Gap>=1,"High","Maintain"));st.dataframe(pr,use_container_width=True,hide_index=True)







        top=pr.iloc[0]; insight_box(f"<b>Highest assessed capability gap:</b> {top.Capability} in {top.Pillar} (gap {top.Gap:.0f}).")















# ============================================================







# 04 RISK







# ============================================================







elif page.startswith("04"):







    page_header("RISK INTELLIGENCE","Cyber Risk Quantification","Translate SLE and LEF into baseline exposure, residual exposure and avoided annual loss, then explore the risk surface.")







    c=st.columns(5); c[0].metric("SLE",currency(st.session_state.sle));c[1].metric("LEF",f"{st.session_state.lef:.3f}");c[2].metric("Baseline ALE",currency(risk['baseline_ale']));c[3].metric("Residual ALE",currency(risk['residual_ale']));c[4].metric("Risk Reduction",pct(risk['risk_reduction']))







    c1,c2=st.columns(2)







    with c1:







        wf=go.Figure(go.Waterfall(x=["Baseline ALE","Likelihood effect","Impact effect","Residual ALE"],measure=["absolute","relative","relative","total"],y=[risk['baseline_ale'],-(risk['baseline_ale']-st.session_state.sle*risk['residual_lef']),-(st.session_state.sle*risk['residual_lef']-risk['residual_ale']),0]));wf.update_layout(title="Baseline-to-Residual Risk Waterfall");st.plotly_chart(dark(wf,430),use_container_width=True)







    with c2:







        lefs=np.linspace(max(.005,st.session_state.lef*.2),min(1,st.session_state.lef*2.2),25); sles=np.linspace(max(1000,st.session_state.sle*.2),st.session_state.sle*2,25);z=np.outer(sles,lefs)







        hm=go.Figure(go.Heatmap(x=lefs,y=sles,z=z,colorscale="YlOrRd",colorbar=dict(title="ALE $")));hm.add_trace(go.Scatter(x=[st.session_state.lef],y=[st.session_state.sle],mode="markers",marker=dict(size=13,symbol="x"),name="Current"));hm.update_layout(title="Loss Exposure Heatmap",xaxis_title="LEF",yaxis_title="SLE ($)");st.plotly_chart(dark(hm,430),use_container_width=True)







    c1,c2=st.columns(2)







    with c1:







        df=pd.DataFrame({"Measure":["Baseline SLE","Residual SLE"],"USD":[st.session_state.sle,risk['residual_sle']]});st.plotly_chart(dark(px.bar(df,x="Measure",y="USD",color="Measure",title="Impact Exposure"),360),use_container_width=True)







    with c2:







        df=pd.DataFrame({"Measure":["Baseline LEF","Residual LEF"],"Frequency":[st.session_state.lef,risk['residual_lef']]});st.plotly_chart(dark(px.bar(df,x="Measure",y="Frequency",color="Measure",title="Likelihood Exposure"),360),use_container_width=True)















# ============================================================







# 05 FINANCIAL







# ============================================================







elif page.startswith("05"):







    page_header("FINANCIAL INTELLIGENCE","Five-Year Business Value","Combine avoided cyber loss and operational benefits with implementation cost, OpEx and discounting.")







    # Refresh the risk engine at page render time so financial outputs always
    # use the same current assumptions shown in Risk Intelligence.
    risk = calc_risk(st.session_state.sle, st.session_state.lef, st.session_state.lr, st.session_state.ir)
    comps = benefit_components()
    gross = sum(comps.values())
    financial = calc_financial(gross, st.session_state.impl, st.session_state.opex, st.session_state.dr)







    c=st.columns(6); c[0].metric("Gross Benefit / yr",currency(gross));c[1].metric("Net Benefit / yr",currency(financial['annual_net_benefit']));c[2].metric("5Y NPV",currency(financial['npv']));c[3].metric("5Y ROI",pct(financial['roi_5y']));c[4].metric("IRR",pct(financial['irr']) if np.isfinite(financial['irr']) else "N/A");c[5].metric("Payback",f"{financial['payback']:.2f} yrs" if np.isfinite(financial['payback']) else "N/A")







    c1,c2=st.columns(2)







    with c1:







        bd=pd.DataFrame({"Benefit":list(comps.keys()),"USD":list(comps.values())});fig=px.pie(bd,names="Benefit",values="USD",hole=.55,title="Annual Benefit Composition");st.plotly_chart(dark(fig,430),use_container_width=True)







    with c2:







        cf=pd.DataFrame({"Year":range(6),"Cash Flow":financial['cash_flows'],"Cumulative":financial['cumulative']});fig=go.Figure();fig.add_bar(x=cf.Year,y=cf['Cash Flow'],name="Cash Flow");fig.add_scatter(x=cf.Year,y=cf.Cumulative,name="Cumulative",mode="lines+markers");fig.add_hline(y=0,line_dash="dash");fig.update_layout(title="Cash Flow & Break-Even Path");st.plotly_chart(dark(fig,430),use_container_width=True)







    wf=go.Figure(go.Waterfall(x=["Implementation","5Y Avoided Loss","5Y Operational Benefits","5Y OpEx","Net undiscounted value"],measure=["relative","relative","relative","relative","total"],y=[-st.session_state.impl,risk['avoided_loss']*5,(gross-risk['avoided_loss'])*5,-st.session_state.opex*5,0]));wf.update_layout(title="Five-Year Value Bridge");st.plotly_chart(dark(wf,400),use_container_width=True)















# ============================================================







# 06 SCENARIO STUDIO







# ============================================================







elif page.startswith("06"):







    page_header("WHAT-IF LAB","Scenario Studio","Create and compare alternative Zero Trust investment assumptions using the same risk and financial equations.")







    defs=[("Conservative",.10,.10,.85,1.10),("Base",st.session_state.lr,st.session_state.ir,1,1),("Enhanced",min(.8,st.session_state.lr+.15),min(.8,st.session_state.ir+.10),1.20,1.20)]







    rows=[]; cols=st.columns(3)







    for i,(name,lr0,ir0,cost_mult,benefit_mult) in enumerate(defs):







        with cols[i]:







            st.markdown(f"### {name}")







            lr_pct = st.slider("Likelihood reduction", 0, 80, int(round(float(lr0) * 100)), 1, format="%d%%", key=f"sc_lr_pct{i}")
            ir_pct = st.slider("Impact reduction", 0, 80, int(round(float(ir0) * 100)), 1, format="%d%%", key=f"sc_ir_pct{i}")
            lr = lr_pct / 100.0
            ir = ir_pct / 100.0







            impl=st.number_input("Implementation cost",min_value=0.0,value=float(st.session_state.impl*cost_mult),step=5000.0,key=f"sc_imp{i}")







            op=st.number_input("Annual OpEx",min_value=0.0,value=float(st.session_state.opex*cost_mult),step=1000.0,key=f"sc_op{i}")







            rr=calc_risk(st.session_state.sle,st.session_state.lef,lr,ir); g=rr['avoided_loss']+(gross_benefit-risk['avoided_loss'])*benefit_mult; ff=calc_financial(g,impl,op,st.session_state.dr)







            rows.append({"Scenario":name,"Risk Reduction":rr['risk_reduction'],"NPV":ff['npv'],"ROI":ff['roi_5y'],"IRR":ff['irr'],"Payback":ff['payback']})







    sdf=pd.DataFrame(rows); st.dataframe(sdf.style.format({"Risk Reduction":"{:.1%}","NPV":"${:,.0f}","ROI":"{:.1%}","IRR":"{:.1%}","Payback":"{:.2f}"}),use_container_width=True,hide_index=True)







    c1,c2=st.columns(2)







    with c1: st.plotly_chart(dark(px.bar(sdf,x="Scenario",y="NPV",color="Scenario",title="Scenario NPV Comparison"),400),use_container_width=True)







    with c2: st.plotly_chart(dark(px.scatter(sdf,x="Risk Reduction",y="NPV",size=np.maximum(np.abs(sdf.NPV),1),text="Scenario",title="Risk Reduction vs NPV"),400),use_container_width=True)















# ============================================================







# 07 MONTE CARLO







# ============================================================







elif page.startswith("07"):







    page_header("UNCERTAINTY LAB","Monte Carlo & Simulation Analytics","Explore distributions, percentiles, downside exposure and relationships across the 10,000 synthetic enterprise scenarios.")







    if dataset is None: st.error("Dataset not found beside app.py.")







    else:







        n=dataset.NPV_5Y_USD; c=st.columns(6); c[0].metric("Scenarios",f"{len(dataset):,}");c[1].metric("P5 NPV",currency(n.quantile(.05)));c[2].metric("P50 NPV",currency(n.median()));c[3].metric("P95 NPV",currency(n.quantile(.95)));c[4].metric("Positive NPV",pct((n>0).mean()));c[5].metric("Payback ≤5Y",pct((dataset.Payback_Years<=5).mean()))







        tabs=st.tabs(["Distributions","Risk ↔ Return","Correlation Heatmap","Industry View"])







        with tabs[0]:







            c1,c2=st.columns(2)







            with c1:







                f=px.histogram(dataset,x="NPV_5Y_USD",nbins=80,marginal="box",title="Five-Year NPV Distribution");f.add_vline(x=0,line_dash="dash");st.plotly_chart(dark(f,450),use_container_width=True)







            with c2:







                f=px.histogram(dataset,x="ROI_5Y",nbins=80,marginal="box",title="Five-Year ROI Distribution");f.add_vline(x=0,line_dash="dash");st.plotly_chart(dark(f,450),use_container_width=True)







        with tabs[1]:







            sm=dataset.sample(min(2500,len(dataset)),random_state=42); f=px.scatter(sm,x="Risk_Reduction_Pct" if "Risk_Reduction_Pct" in sm.columns else "Avoided_Loss_USD",y="NPV_5Y_USD",color="Industry",size="Implementation_Cost_USD",opacity=.55,title="Risk Reduction / Avoided Loss vs NPV");st.plotly_chart(dark(f,600),use_container_width=True)







        with tabs[2]:







            cols=[c for c in ML_FEATURES+["Avoided_Loss_USD","Gross_Annual_Benefit_USD","Net_Annual_Benefit_USD","NPV_5Y_USD","ROI_5Y","IRR_5Y","Payback_Years"] if c in dataset.columns];corr=dataset[cols].corr();f=px.imshow(corr,color_continuous_scale="RdBu_r",zmin=-1,zmax=1,aspect="auto",title="Financial & Risk Correlation Heatmap");st.plotly_chart(dark(f,720),use_container_width=True)







        with tabs[3]:







            agg=dataset.groupby("Industry").agg(Median_NPV=("NPV_5Y_USD","median"),Positive_NPV=("NPV_5Y_USD",lambda s:(s>0).mean()),Median_ROI=("ROI_5Y","median"),Scenarios=("Scenario_ID","count")).reset_index();st.dataframe(agg.style.format({"Median_NPV":"${:,.0f}","Positive_NPV":"{:.1%}","Median_ROI":"{:.1%}"}),use_container_width=True,hide_index=True);st.plotly_chart(dark(px.bar(agg,x="Industry",y="Median_NPV",color="Positive_NPV",title="Median Simulated NPV by Industry"),430),use_container_width=True)







        insight_box("Simulation percentiles and proportions describe the synthetic scenario model under its assumptions; they are not observed enterprise frequencies.","warn")















# ============================================================







# 08 ML + XAI







# ============================================================







elif page.startswith("08"):







    page_header("PREDICTIVE INTELLIGENCE","Machine Learning & Explainability","Compare Random Forest and Gradient Boosting, inspect prediction error, identify important features and explain the current scenario.")







    bundle=train_models()







    if bundle is None: st.error("Dataset not found.")







    elif "error" in bundle: st.error(bundle["error"])







    else:







        rf=bundle['rfm']; gb=bundle['gbm']; c=st.columns(6);c[0].metric("RF R²",f"{rf['R2']:.3f}");c[1].metric("GB R²",f"{gb['R2']:.3f}");c[2].metric("RF MAE",currency(rf['MAE']));c[3].metric("GB MAE",currency(gb['MAE']));c[4].metric("RF RMSE",currency(rf['RMSE']));c[5].metric("GB RMSE",currency(gb['RMSE']))







        row=current_ml_row(cur_m,tar_m); rfp=float(bundle['rf'].predict(row)[0]); gbp=float(bundle['gb'].predict(row)[0]);st.markdown("### Current Scenario Prediction");a,b=st.columns(2);a.metric("RF Predicted NPV",currency(rfp));b.metric("GB Predicted NPV",currency(gbp))







        tabs=st.tabs(["Actual vs Predicted","Residual Diagnostics","Feature Importance","SHAP Explanation"])







        with tabs[0]:







            d=pd.DataFrame({"Actual":bundle['yte'],"RF":rf['pred'],"GB":gb['pred']}); c1,c2=st.columns(2)







            with c1:







                f=px.scatter(d,x="Actual",y="RF",opacity=.45,title="Random Forest: Actual vs Predicted");lo=min(d.Actual.min(),d.RF.min());hi=max(d.Actual.max(),d.RF.max());f.add_shape(type="line",x0=lo,y0=lo,x1=hi,y1=hi,line=dict(dash="dash"));st.plotly_chart(dark(f,430),use_container_width=True)







            with c2:







                f=px.scatter(d,x="Actual",y="GB",opacity=.45,title="Gradient Boosting: Actual vs Predicted");lo=min(d.Actual.min(),d.GB.min());hi=max(d.Actual.max(),d.GB.max());f.add_shape(type="line",x0=lo,y0=lo,x1=hi,y1=hi,line=dict(dash="dash"));st.plotly_chart(dark(f,430),use_container_width=True)







        with tabs[1]:







            res=pd.DataFrame({"Predicted":gb['pred'],"Residual":bundle['yte'].values-gb['pred']});c1,c2=st.columns(2)







            with c1: st.plotly_chart(dark(px.scatter(res,x="Predicted",y="Residual",opacity=.45,title="GB Residuals vs Predicted"),430),use_container_width=True)







            with c2: st.plotly_chart(dark(px.histogram(res,x="Residual",nbins=60,marginal="box",title="GB Residual Distribution"),430),use_container_width=True)







        with tabs[2]:







            imp=pd.DataFrame({"Feature":ML_FEATURES,"Importance":bundle['gb'].feature_importances_}).sort_values("Importance");st.plotly_chart(dark(px.bar(imp,x="Importance",y="Feature",orientation="h",title="Gradient Boosting Global Feature Importance"),520),use_container_width=True)







        with tabs[3]:







            try:







                import shap







                bg=bundle['Xtr'].sample(min(400,len(bundle['Xtr'])),random_state=42); ex=shap.Explainer(bundle['gb'],bg); sv=ex(row); vals=np.asarray(sv.values)[0]







                loc=pd.DataFrame({"Feature":ML_FEATURES,"Input":row.iloc[0].values,"SHAP Contribution":vals});loc['Abs']=loc['SHAP Contribution'].abs();loc=loc.sort_values('Abs')







                st.plotly_chart(dark(px.bar(loc,x="SHAP Contribution",y="Feature",orientation="h",title="Local SHAP Contributions to Current Predicted NPV"),520),use_container_width=True)







                st.dataframe(loc.sort_values('Abs',ascending=False).drop(columns='Abs'),use_container_width=True,hide_index=True)







            except Exception as e: st.warning(f"SHAP unavailable in this environment: {e}")







        insight_box("R² measures regression goodness-of-fit, not classification accuracy. The models learn the synthetic response surface and do not constitute external real-world predictive validation.")















# ============================================================







# 09 SENSITIVITY + THRESHOLDS







# ============================================================







elif page.startswith("09"):







    page_header("ROBUSTNESS LAB","Sensitivity & Break-Even Thresholds","Identify the assumptions that move NPV most and calculate the conditions required for financial break-even.")







    base={"SLE":st.session_state.sle,"LEF":st.session_state.lef,"Likelihood Reduction":st.session_state.lr,"Impact Reduction":st.session_state.ir,"Implementation Cost":st.session_state.impl,"Annual OpEx":st.session_state.opex,"Discount Rate":st.session_state.dr}







    other_benefits=gross_benefit-risk['avoided_loss']







    def eval_npv(v):







        rr=calc_risk(v['SLE'],v['LEF'],np.clip(v['Likelihood Reduction'],0,.99),np.clip(v['Impact Reduction'],0,.99));ff=calc_financial(rr['avoided_loss']+other_benefits,v['Implementation Cost'],v['Annual OpEx'],np.clip(v['Discount Rate'],0,.99));return ff['npv']







    bn=eval_npv(base); rows=[]







    for var,val in base.items():







        lo=base.copy();hi=base.copy();lo[var]=val*.8;hi[var]=val*1.2;rows.append({"Variable":var,"Low":eval_npv(lo),"Base":bn,"High":eval_npv(hi)})







    sens=pd.DataFrame(rows);sens['Range']=(sens[['Low','High']].max(axis=1)-sens[['Low','High']].min(axis=1));sens=sens.sort_values('Range')







    fig=go.Figure()







    for _,r in sens.iterrows(): fig.add_trace(go.Bar(y=[r.Variable],x=[r.High-r.Low],base=r.Low,orientation='h',name=r.Variable,showlegend=False,hovertemplate=f"Low {currency(r.Low)}<br>High {currency(r.High)}"))







    fig.add_vline(x=bn,line_dash='dash');fig.update_layout(title="NPV Tornado / One-Way Sensitivity Range");st.plotly_chart(dark(fig,520),use_container_width=True)







    section("Break-Even Thresholds")







    annuity=sum(1/(1+st.session_state.dr)**t for t in range(1,6)); required_net=st.session_state.impl/annuity; required_gross=required_net+st.session_state.opex; required_avoided=max(0,required_gross-other_benefits)







    control_factor=1-(1-st.session_state.lr)*(1-st.session_state.ir)







    min_lef=required_avoided/(st.session_state.sle*control_factor) if st.session_state.sle>0 and control_factor>0 else np.nan







    max_impl=(gross_benefit-st.session_state.opex)*annuity







    c=st.columns(4);c[0].metric("Required gross benefit / yr",currency(required_gross));c[1].metric("Required avoided loss / yr",currency(required_avoided));c[2].metric("Break-even LEF",f"{min_lef:.3f}" if np.isfinite(min_lef) else "N/A");c[3].metric("Max initial cost for NPV≥0",currency(max_impl))







    insight_box("Thresholds answer 'what has to be true?' under the selected assumptions. They are algebraic model thresholds, not externally observed cut-offs.")















# ============================================================







# 10 DECISION STUDIO







# ============================================================







elif page.startswith("10"):







    page_header("INTEGRATED DECISION SUPPORT","Decision Studio","Bring maturity, risk, finance, uncertainty and predictive evidence together in one management-facing view.")







    pr=pillars.sort_values('Gap',ascending=False).reset_index(drop=True); top=pr.iloc[0]







    bundle=train_models(); pred=np.nan







    if bundle and 'error' not in bundle: pred=float(bundle['gb'].predict(current_ml_row(cur_m,tar_m))[0])







    c=st.columns(5);c[0].metric("Maturity Gap",f"{tar_m-cur_m:.2f}");c[1].metric("Risk Reduction",pct(risk['risk_reduction']));c[2].metric("Deterministic NPV",currency(financial['npv']));c[3].metric("GB Predicted NPV",currency(pred));c[4].metric("Priority Pillar",top.Pillar)







    section("Evidence Matrix")







    p5=dataset.NPV_5Y_USD.quantile(.05) if dataset is not None else np.nan;p50=dataset.NPV_5Y_USD.median() if dataset is not None else np.nan;p95=dataset.NPV_5Y_USD.quantile(.95) if dataset is not None else np.nan







    ev=pd.DataFrame({"Decision Layer":["Maturity","Cyber Risk","Financial Value","Uncertainty","Machine Learning","Priority"],"Evidence":[f"{cur_m:.2f} → {tar_m:.2f}",f"ALE {currency(risk['baseline_ale'])} → {currency(risk['residual_ale'])}",f"NPV {currency(financial['npv'])} | ROI {pct(financial['roi_5y'])}",f"Synthetic P5 {currency(p5)} | P50 {currency(p50)} | P95 {currency(p95)}",f"GB predicted NPV {currency(pred)}",f"Largest pillar gap: {top.Pillar} ({top.Gap:.2f})"]});st.dataframe(ev,use_container_width=True,hide_index=True)







    section("Management Interpretation")







    if financial['npv']>=0: insight_box(f"Under the selected assumptions, discounted five-year benefits exceed modelled costs by {currency(financial['npv'])}. This is a scenario result rather than an investment instruction.","good")







    else: insight_box(f"Under the selected assumptions, the five-year NPV is {currency(financial['npv'])}. Use the threshold and scenario modules to identify which assumptions would need to change for break-even.","warn")







    insight_box(f"The maturity assessment identifies <b>{top.Pillar}</b> as the largest pillar-level gap. The roadmap therefore places it earlier in the implementation sequence.")







    insight_box("The platform intentionally presents evidence rather than issuing an automatic 'invest / do not invest' command. Risk appetite, regulatory obligations, architecture constraints and input quality remain organisational decision factors.")















# ============================================================







# 11 ROADMAP







# ============================================================







elif page.startswith("11"):







    page_header("ACTION LAYER","Implementation Roadmap","Translate assessed maturity gaps into a phased, explainable Zero Trust improvement sequence.")







    pr=pillars.sort_values('Gap',ascending=False).reset_index(drop=True); windows=[("Phase 1","0–3 months"),("Phase 2","3–6 months"),("Phase 3","6–9 months"),("Phase 4","9–12 months"),("Phase 5","12+ months")]







    rows=[]







    for i,r in pr.iterrows():







        caps=detail[detail.Pillar==r.Pillar].sort_values('Gap',ascending=False).head(2).Capability.tolist();rows.append({"Phase":windows[i][0],"Window":windows[i][1],"Pillar":r.Pillar,"Gap":r.Gap,"Priority capabilities":"; ".join(caps)})







    rdf=pd.DataFrame(rows);st.dataframe(rdf,use_container_width=True,hide_index=True)







    fig=go.Figure()







    for i,r in rdf.iterrows(): fig.add_trace(go.Bar(x=[1],y=[r.Pillar],orientation='h',name=r.Phase,text=f"{r.Phase} • {r.Window}",textposition='inside'))







    fig.update_layout(barmode='stack',title="Prioritised Zero Trust Roadmap",xaxis=dict(showticklabels=False,title="Implementation sequence"));st.plotly_chart(dark(fig,430),use_container_width=True)







    insight_box("Roadmap ordering is driven by assessed pillar gaps. It is a prioritisation aid; dependencies, regulation, technical feasibility and security architecture should be considered before implementation.")















# ============================================================







# 12 VALIDATION







# ============================================================







elif page.startswith("12"):







    page_header("MODEL ASSURANCE","Validation & Robustness","Show transparent internal validation evidence for formulas, holdout performance and dataset consistency.")







    if dataset is not None:







        ale_check=np.isclose(dataset.Baseline_ALE_USD,dataset.SLE_USD*dataset.LEF,rtol=1e-8,atol=.01).mean()







        residual_check=np.isclose(dataset.Residual_ALE_USD,dataset.Residual_LEF*dataset.Residual_SLE_USD,rtol=1e-8,atol=.01).mean()







        avoided_check=np.isclose(dataset.Avoided_Loss_USD,dataset.Baseline_ALE_USD-dataset.Residual_ALE_USD,rtol=1e-8,atol=.01).mean()







        c=st.columns(4);c[0].metric("Baseline ALE consistency",pct(ale_check));c[1].metric("Residual ALE consistency",pct(residual_check));c[2].metric("Avoided loss consistency",pct(avoided_check));c[3].metric("Rows",f"{len(dataset):,}")







        bundle=train_models();







        if bundle and 'error' not in bundle:







            score=pd.DataFrame({"Model":["Random Forest","Gradient Boosting"],"Holdout R²":[bundle['rfm']['R2'],bundle['gbm']['R2']],"MAE":[bundle['rfm']['MAE'],bundle['gbm']['MAE']],"RMSE":[bundle['rfm']['RMSE'],bundle['gbm']['RMSE']]});st.dataframe(score.style.format({"Holdout R²":"{:.4f}","MAE":"${:,.0f}","RMSE":"${:,.0f}"}),use_container_width=True,hide_index=True)







        missing=dataset.isna().sum().sort_values(ascending=False);st.plotly_chart(dark(px.bar(x=missing.index,y=missing.values,title="Missing Values by Variable",labels={'x':'Variable','y':'Missing'}),430),use_container_width=True)







        st.dataframe(dataset.describe().T,use_container_width=True)







    insight_box("Internal consistency and synthetic holdout performance do not substitute for external validation using observed enterprise outcomes.","warn")















# ============================================================







# 13 REPORT CENTRE







# ============================================================







elif page.startswith("13"):







    page_header("REPORTING HUB","Report Centre","Export management-ready reports and analytical data from the current organisation scenario.")







    st.markdown(f"""<div class='hero'><div class='eyebrow'>CURRENT ASSESSMENT</div><div class='hero-title'>{st.session_state.org_name}</div><div class='hero-sub'>{st.session_state.industry} • {st.session_state.employees:,} employees • Current maturity {cur_m:.2f}/4 • Target {tar_m:.2f}/4 • Five-year NPV {currency(financial['npv'])}</div></div>""",unsafe_allow_html=True)







    reports=[("📘 Full Assessment Report","Full Assessment Report"),("🛡️ Zero Trust Assessment","Zero Trust Assessment Report"),("⚠️ Cyber Risk Report","Cyber Risk Report"),("💰 Financial Business Case","Financial Business Case"),("🎲 Monte Carlo Report","Monte Carlo Report"),("🗺️ Implementation Roadmap","Implementation Roadmap")]







    cols=st.columns(3)







    for i,(label,rtype) in enumerate(reports):







        with cols[i%3]:







            data=build_pdf(rtype,detail,pillars,cur_m,tar_m,risk,financial,dataset)







            st.download_button(label,data,file_name=rtype.lower().replace(' ','_')+'.pdf',mime='application/pdf',use_container_width=True,key=f"pdf{i}")







    st.markdown("### Data Exports")







    e1,e2,e3=st.columns(3)







    summary=pd.DataFrame({"Metric":["Current Maturity","Target Maturity","Baseline ALE","Residual ALE","Avoided Loss","5Y NPV","5Y ROI","IRR","Payback"],"Value":[cur_m,tar_m,risk['baseline_ale'],risk['residual_ale'],risk['avoided_loss'],financial['npv'],financial['roi_5y'],financial['irr'],financial['payback']]})







    with e1: st.download_button("📊 Executive Summary CSV",summary.to_csv(index=False).encode(),"executive_summary.csv","text/csv",use_container_width=True)







    with e2: st.download_button("📗 Analysis Workbook XLSX",build_excel(detail,pillars,risk,financial,dataset),"zero_trust_analysis.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)







    with e3:







        if dataset is not None: st.download_button("📁 Synthetic Dataset CSV",dataset.to_csv(index=False).encode(),"zero_trust_dataset.csv","text/csv",use_container_width=True)







    insight_box("All reports are generated from the current assessment state. They explicitly retain the research limitation that the scenario dataset is synthetic and outputs are decision-support evidence rather than guaranteed realised outcomes.","warn")
