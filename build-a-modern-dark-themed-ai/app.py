import math
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import scipy.stats as stats
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler

st.set_page_config(page_title="InsightPilot", page_icon="IP", layout="wide", initial_sidebar_state="expanded")

GREEN = "#39ff88"
CYAN = "#19d7ff"
TEXT = "#edf7ff"
MUTED = "#8ea5b8"


def css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    .stApp {{ background: radial-gradient(circle at 15% 12%, rgba(25,215,255,.15), transparent 28%), radial-gradient(circle at 88% 3%, rgba(57,255,136,.12), transparent 24%), linear-gradient(135deg,#05070d 0%,#07111d 44%,#020409 100%); color:{TEXT}; }}
    [data-testid="stSidebar"] {{ background:rgba(6,10,18,.96); border-right:1px solid rgba(25,215,255,.16); }}
    [data-testid="stSidebar"] * {{ color:{TEXT}; }}
    .block-container {{ padding-top:1.5rem; padding-bottom:2rem; }}
    h1,h2,h3 {{ color:{TEXT}; letter-spacing:0; }}
    .dv-hero {{ border:1px solid rgba(25,215,255,.18); background:linear-gradient(135deg,rgba(12,17,29,.93),rgba(6,14,24,.88)); border-radius:8px; padding:24px; box-shadow:0 20px 70px rgba(0,0,0,.34); position:relative; overflow:hidden; }}
    .dv-hero:after {{ content:""; position:absolute; inset:0; background:linear-gradient(90deg,rgba(25,215,255,.08) 1px,transparent 1px),linear-gradient(rgba(57,255,136,.06) 1px,transparent 1px); background-size:46px 46px; mask-image:linear-gradient(90deg,transparent,black 18%,black 82%,transparent); pointer-events:none; }}
    .dv-title {{ font-size:clamp(2.3rem,5vw,4.7rem); line-height:.95; margin:0; font-weight:800; }}
    .dv-subtitle {{ color:{MUTED}; max-width:780px; margin-top:12px; font-size:1.03rem; }}
    .dv-chip {{ display:inline-flex; border:1px solid rgba(57,255,136,.32); background:rgba(57,255,136,.08); color:{GREEN}; padding:7px 11px; border-radius:999px; font-weight:800; font-size:.82rem; margin-bottom:14px; }}
    .metric-card {{ border:1px solid rgba(255,255,255,.08); background:linear-gradient(145deg,rgba(17,24,39,.93),rgba(5,9,16,.88)); border-radius:8px; padding:18px; min-height:128px; box-shadow:inset 0 1px 0 rgba(255,255,255,.05),0 18px 42px rgba(0,0,0,.22); }}
    .metric-card .label {{ color:{MUTED}; font-size:.82rem; font-weight:800; text-transform:uppercase; }}
    .metric-card .value {{ color:{TEXT}; font-size:2rem; font-weight:800; margin-top:8px; }}
    .metric-card .hint {{ color:{CYAN}; font-size:.86rem; margin-top:7px; }}
    .insight-card {{ border-left:3px solid {GREEN}; background:rgba(12,17,29,.82); border-radius:8px; padding:14px 16px; margin-bottom:10px; color:{TEXT}; box-shadow:0 8px 28px rgba(0,0,0,.2); }}
    .module-header {{ display:flex; align-items:center; justify-content:space-between; gap:16px; border-bottom:1px solid rgba(255,255,255,.08); padding-bottom:10px; margin:16px 0 18px; }}
    .module-header p {{ color:{MUTED}; margin:4px 0 0; }}
    .stButton>button,.stDownloadButton>button {{ border-radius:8px; border:1px solid rgba(25,215,255,.36); background:linear-gradient(135deg,rgba(25,215,255,.16),rgba(57,255,136,.12)); color:{TEXT}; font-weight:800; min-height:42px; }}
    .stDataFrame,[data-testid="stDataFrame"] {{ border:1px solid rgba(255,255,255,.08); border-radius:8px; overflow:hidden; }}
    div[data-testid="stTabs"] button {{ color:{TEXT}; }}
    @media(max-width:760px) {{ .dv-hero{{padding:18px}} .metric-card{{min-height:auto}} .module-header{{display:block}} }}
    </style>
    """, unsafe_allow_html=True)


def sample(rows=420):
    rng = np.random.default_rng(42)
    seg = rng.choice(["Retail", "Enterprise", "Startup"], rows, p=[.48, .27, .25])
    age = rng.normal(37, 11, rows).round().clip(18, 72)
    income = rng.lognormal(10.6, .43, rows).round(0)
    ad = rng.gamma(3.2, 260, rows).round(2)
    visits = rng.poisson(9, rows) + rng.integers(0, 7, rows)
    purchase = (income*.018 + ad*.42 + visits*18 + np.where(seg == "Enterprise", 580, 0) + rng.normal(0,260,rows)).clip(40,None).round(2)
    retention = (.38 + visits*.018 + np.where(seg == "Enterprise", .13, 0) + rng.normal(0,.09,rows)).clip(.05,.97)
    df = pd.DataFrame({"Customer_ID":[f"IP-{10000+i}" for i in range(rows)], "Segment":seg, "Age":age.astype(float), "Annual_Income":income, "Ad_Spend":ad, "Site_Visits":visits, "Purchase_Value":purchase, "Retention_Rate":retention.round(3), "Churn_Risk":(1-retention+rng.normal(0,.09,rows)).clip(.02,.98).round(3), "Region":rng.choice(["North","South","East","West"], rows)})
    for col, count in {"Age":12, "Annual_Income":9, "Retention_Rate":16}.items():
        df.loc[rng.choice(df.index, count, replace=False), col] = np.nan
    return pd.concat([df, df.sample(8, random_state=7)], ignore_index=True)


@st.cache_data(show_spinner=False)
def read_file(file):
    ext = file.name.split(".")[-1].lower()
    return pd.read_csv(file) if ext == "csv" else pd.read_excel(file)


def nums(df): return df.select_dtypes(include=np.number).columns.tolist()
def cats(df): return df.select_dtypes(exclude=np.number).columns.tolist()


def quality(df):
    cells = max(df.shape[0] * df.shape[1], 1)
    miss = df.isna().sum().sum() / cells
    dup = df.duplicated().sum() / max(len(df), 1)
    obj = len(cats(df)) / max(df.shape[1], 1) * .08
    return round(max(100 * (1 - min(.82, miss*1.45 + dup*.9 + obj)), 0), 1)


def card(label, value, hint):
    st.markdown(f'<div class="metric-card"><div class="label">{label}</div><div class="value">{value}</div><div class="hint">{hint}</div></div>', unsafe_allow_html=True)


def header(title, subtitle, tag):
    st.markdown(f'<div class="module-header"><div><h2>{title}</h2><p>{subtitle}</p></div><span class="dv-chip">{tag}</span></div>', unsafe_allow_html=True)


def insights(items):
    for item in items:
        st.markdown(f'<div class="insight-card">{item}</div>', unsafe_allow_html=True)


def theme(fig, height=420):
    fig.update_layout(height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT, family="Inter"), margin=dict(l=20,r=20,t=48,b=24), legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom"))
    fig.update_xaxes(gridcolor="rgba(255,255,255,.08)", zerolinecolor="rgba(255,255,255,.14)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,.08)", zerolinecolor="rgba(255,255,255,.14)")
    return fig


def clean(df, scale=False):
    out = df.copy(); notes = []; before = out.isna().sum()
    for col in out.columns:
        if out[col].isna().sum() == 0: continue
        if pd.api.types.is_numeric_dtype(out[col]):
            skew = out[col].skew(skipna=True); strategy = "median" if abs(skew) > .75 else "mean"
            out[col] = out[col].fillna(out[col].median() if strategy == "median" else out[col].mean())
            notes.append(f"{int(before[col])} missing values detected in {col}. {strategy.title()} imputation applied because distribution skew is {skew:.2f}.")
        else:
            mode = out[col].mode(dropna=True); fill = mode.iloc[0] if not mode.empty else "Unknown"
            out[col] = out[col].fillna(fill); notes.append(f"{int(before[col])} missing values detected in {col}. Mode imputation applied using '{fill}'.")
    dups = int(out.duplicated().sum())
    if dups:
        out = out.drop_duplicates(); notes.append(f"{dups} duplicate rows removed to prevent repeated records from biasing analysis.")
    converted = []
    for col in out.select_dtypes(include="object").columns:
        parsed = pd.to_datetime(out[col], errors="coerce")
        if parsed.notna().mean() > .86:
            out[col] = parsed; converted.append(col)
    if converted: notes.append(f"Datatype correction converted {', '.join(converted)} into datetime fields.")
    if scale and nums(out):
        out[nums(out)] = StandardScaler().fit_transform(out[nums(out)]); notes.append(f"Normalization applied to {len(nums(out))} numeric columns with StandardScaler.")
    return out, notes or ["No critical cleaning actions were required. The dataset is already in strong analytical condition."], dups


def null_heatmap(df):
    if df.isna().sum().sum() == 0:
        z, x, y = np.zeros((1, len(df.columns))), df.columns, ["No missing values"]
    else:
        z, x, y = df.isna().astype(int).T.values, df.index.astype(str), df.columns
    fig = go.Figure(data=go.Heatmap(z=z, x=x, y=y, colorscale=[[0,"#0d1523"],[1,CYAN]], showscale=True))
    fig.update_layout(title="Null Heatmap")
    return theme(fig, 360)


def gauge(p):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=min(float(p), 1.0), number={"valueformat":".4f","font":{"color":TEXT}}, title={"text":"p-value","font":{"color":TEXT}}, gauge={"axis":{"range":[0,1],"tickcolor":TEXT},"bar":{"color":GREEN if p < .05 else "#f5c542"},"bgcolor":"#111827","borderwidth":1,"bordercolor":"rgba(255,255,255,.12)","steps":[{"range":[0,.05],"color":"rgba(57,255,136,.25)"},{"range":[.05,1],"color":"rgba(245,197,66,.16)"}],"threshold":{"line":{"color":CYAN,"width":4},"value":.05}}))
    fig.update_layout(height=310, paper_bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT))
    return fig


def explain(test, p, alpha=.05):
    sign = "<" if p < alpha else ">="; verdict = "rejected" if p < alpha else "not rejected"; strength = "statistically significant" if p < alpha else "not statistically significant"
    return f"{test} returned p-value {p:.4f}. Since p-value {sign} {alpha}, the null hypothesis is {verdict}, indicating the relationship is {strength}."


def ai_notes(df):
    out = []; n = nums(df); c = cats(df)
    if len(n) >= 2:
        pairs = df[n].corr(numeric_only=True).abs().where(np.triu(np.ones((len(n), len(n))), k=1).astype(bool)).stack()
        if not pairs.empty:
            a, b = pairs.sort_values(ascending=False).index[0]; out.append(f"{a} and {b} move {'strongly' if pairs.max() >= .7 else 'moderately'} together with correlation {pairs.max():.2f}.")
    if n:
        miss = df[n].isna().sum().sort_values(ascending=False)
        if miss.iloc[0] > 0: out.append(f"{miss.index[0]} has the highest numeric data gap with {int(miss.iloc[0])} missing values.")
        out.append(f"{df[n].var(numeric_only=True).sort_values(ascending=False).index[0]} shows the widest spread, making it a strong candidate for segmentation analysis.")
    if n and c:
        means = df.groupby(c[0])[n[0]].mean(numeric_only=True).dropna().sort_values(ascending=False)
        if len(means) >= 2: out.append(f"{means.index[0]} leads {c[0]} groups for average {n[0]}, outperforming {means.index[-1]}.")
    q = quality(df); out.append("The dataset is BI-ready with high structural quality and limited cleaning risk." if q >= 88 else "The dataset is usable for analysis after targeted cleaning of missing or repeated records." if q >= 70 else "The dataset needs cleaning before strategic decisions should rely on its outputs.")
    return out[:5]


def sidebar():
    st.sidebar.markdown("## InsightPilot"); st.sidebar.caption("AI-powered analytics command center")
    up = st.sidebar.file_uploader("Upload CSV or Excel", type=["csv","xlsx","xls"])
    use_sample = st.sidebar.toggle("Use sample customer dataset", value=up is None)
    if up and not use_sample:
        try: df, source = read_file(up), up.name
        except Exception as e: st.sidebar.error(str(e)); df, source = sample(), "Sample Data"
    else: df, source = sample(), "Sample Data"
    module = st.sidebar.radio("Modules", ["Home Dashboard", "DataCleaner AI", "Hypothesis Lab", "ClusterVibe", "InsightPilot", "AI Insight Panel"])
    st.sidebar.divider(); st.sidebar.metric("Rows", f"{df.shape[0]:,}"); st.sidebar.metric("Columns", f"{df.shape[1]:,}"); st.sidebar.metric("Quality", f"{quality(df)}%"); st.sidebar.caption(f"Active source: {source}")
    return df, module, source


def home(df, source):
    st.markdown('<div class="dv-hero"><span class="dv-chip">LIVE ANALYTICS OS</span><h1 class="dv-title">InsightPilot</h1><p class="dv-subtitle">Upload CSV or Excel data and explore cleaning, hypothesis testing, clustering, and AI-style business insights inside one interactive analytics platform.</p></div>', unsafe_allow_html=True)
    st.write(""); cols = st.columns(4)
    data = [("Rows", f"{df.shape[0]:,}", "Active observations"), ("Columns", f"{df.shape[1]:,}", "Detected fields"), ("Missing Values", f"{int(df.isna().sum().sum()):,}", "Cells needing attention"), ("Data Quality", f"{quality(df)}%", "Readiness score")]
    for col, item in zip(cols, data):
        with col: card(*item)
    left, right = st.columns([1.25, 1])
    with left: st.subheader("Dataset Summary"); st.caption(f"Source: {source}"); st.dataframe(df.head(12), use_container_width=True, hide_index=True)
    with right: st.subheader("Field Profile"); st.dataframe(pd.DataFrame({"Type":df.dtypes.astype(str), "Missing":df.isna().sum(), "Unique":df.nunique(dropna=True)}), use_container_width=True)
    n = nums(df); c = cats(df)
    if len(n) >= 2:
        st.subheader("Signal Map"); fig = px.imshow(df[n].corr(numeric_only=True), color_continuous_scale=["#111827", CYAN, GREEN], aspect="auto"); fig.update_layout(title="Numeric Correlation Matrix"); st.plotly_chart(theme(fig, 430), use_container_width=True)
    elif c:
        counts = df[c[0]].value_counts().reset_index(); counts.columns = [c[0], "count"]; st.plotly_chart(theme(px.bar(counts, x=c[0], y="count", color="count", color_continuous_scale=[CYAN, GREEN]), 390), use_container_width=True)


def cleaner(df):
    header("DataCleaner AI", "Detect nulls, remove duplicates, correct datatypes, normalize values, and explain every cleaning move.", "CLEANING ENGINE")
    cleaned, notes, dups = clean(df, st.toggle("Normalize numeric columns with StandardScaler", value=False))
    for col, item in zip(st.columns(4), [("Before Missing", f"{int(df.isna().sum().sum()):,}", "Raw null cells"), ("After Missing", f"{int(cleaned.isna().sum().sum()):,}", "Post-clean null cells"), ("Duplicates Removed", f"{dups:,}", "Repeated records"), ("Clean Quality", f"{quality(cleaned)}%", "After cleaning")]):
        with col: card(*item)
    st.subheader("Auto-Generated Cleaning Insights"); insights(notes)
    t1, t2, t3 = st.tabs(["Null Heatmap", "Before vs After", "Clean Dataset"])
    with t1: st.plotly_chart(null_heatmap(df), use_container_width=True)
    with t2:
        comp = pd.DataFrame({"Stage":["Before","After"], "Missing Values":[df.isna().sum().sum(), cleaned.isna().sum().sum()], "Duplicate Rows":[df.duplicated().sum(), cleaned.duplicated().sum()], "Quality Score":[quality(df), quality(cleaned)]})
        st.plotly_chart(theme(px.bar(comp.melt(id_vars="Stage", var_name="Metric", value_name="Value"), x="Metric", y="Value", color="Stage", barmode="group", color_discrete_sequence=[CYAN,GREEN]), 420), use_container_width=True)
    with t3: st.dataframe(cleaned.head(40), use_container_width=True, hide_index=True); st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode("utf-8"), "insightpilot_cleaned.csv", "text/csv")


def lab(df):
    header("Hypothesis Lab", "Run statistical tests and translate results into plain-English decision guidance.", "STATS COPILOT")
    n, c = nums(df), cats(df); test = st.selectbox("Select statistical test", ["Correlation", "t-test", "Chi-square", "ANOVA"])
    if test == "Correlation":
        if len(n) < 2: st.warning("Correlation requires at least two numeric columns."); return
        x = st.selectbox("Numeric field A", n, index=0); y = st.selectbox("Numeric field B", n, index=min(1, len(n)-1)); d = df[[x,y]].dropna(); r, p = stats.pearsonr(d[x], d[y])
        st.plotly_chart(gauge(p), use_container_width=True); insights([explain("Pearson correlation", p), f"Correlation coefficient is {r:.3f}."]); st.plotly_chart(theme(px.scatter(d, x=x, y=y, trendline="ols", color_discrete_sequence=[CYAN]), 460), use_container_width=True)
    elif test == "t-test":
        if not n or not c: st.warning("t-test requires one numeric column and one categorical column."); return
        val = st.selectbox("Numeric outcome", n); grp = st.selectbox("Two-group category", c); choices = st.multiselect("Compare groups", df[grp].dropna().unique().tolist(), default=df[grp].dropna().unique().tolist()[:2], max_selections=2)
        if len(choices) == 2:
            a = df.loc[df[grp] == choices[0], val].dropna(); b = df.loc[df[grp] == choices[1], val].dropna(); _, p = stats.ttest_ind(a, b, equal_var=False)
            ci = stats.t.interval(.95, max(len(a)+len(b)-2, 1), loc=a.mean()-b.mean(), scale=math.sqrt(a.var(ddof=1)/len(a) + b.var(ddof=1)/len(b)))
            g1, g2 = st.columns([.9, 1.1])
            with g1: st.plotly_chart(gauge(p), use_container_width=True)
            with g2: card("95% Confidence Interval", f"{ci[0]:.2f} to {ci[1]:.2f}", "Difference in means"); insights([explain("Welch t-test", p)])
            st.plotly_chart(theme(px.box(df[df[grp].isin(choices)], x=grp, y=val, color=grp, color_discrete_sequence=[CYAN,GREEN]), 430), use_container_width=True)
    elif test == "Chi-square":
        if len(c) < 2: st.warning("Chi-square requires two categorical columns."); return
        a = st.selectbox("Category A", c); b = st.selectbox("Category B", c, index=min(1, len(c)-1)); table = pd.crosstab(df[a], df[b]); chi2, p, dof, _ = stats.chi2_contingency(table)
        g1, g2 = st.columns([.85, 1.15])
        with g1: st.plotly_chart(gauge(p), use_container_width=True)
        with g2: card("Chi-square", f"{chi2:.2f}", f"Degrees of freedom: {dof}"); insights([explain("Chi-square test", p)])
        st.plotly_chart(theme(px.imshow(table, text_auto=True, color_continuous_scale=["#111827", CYAN, GREEN]), 430), use_container_width=True)
    else:
        if not n or not c: st.warning("ANOVA requires one numeric column and one categorical column."); return
        val = st.selectbox("Numeric outcome", n); grp = st.selectbox("Group category", c); groups = [g[val].dropna() for _, g in df.groupby(grp) if len(g[val].dropna()) > 1]
        if len(groups) < 2: st.warning("ANOVA needs at least two groups with more than one numeric value."); return
        f, p = stats.f_oneway(*groups); g1, g2 = st.columns([.85, 1.15])
        with g1: st.plotly_chart(gauge(p), use_container_width=True)
        with g2: card("F-statistic", f"{f:.2f}", "Between-group variance ratio"); insights([explain("ANOVA", p)])
        st.plotly_chart(theme(px.violin(df, x=grp, y=val, color=grp, box=True, points="all"), 460), use_container_width=True)


def persona_names(cluster_df, selected):
    centers = cluster_df.groupby("Cluster")[selected].mean(); overall = cluster_df[selected].mean(); names = {}
    for cid, row in centers.iterrows():
        lift = row - overall; top = lift.sort_values(ascending=False).index[0]; low = lift.sort_values().index[0]
        names[cid] = "High Spenders" if any(t in top.lower() for t in ["spend","sales","purchase","revenue","income"]) else "Budget Buyers" if any(t in low.lower() for t in ["spend","sales","purchase","revenue","income"]) else "Premium Customers" if any(t in top.lower() for t in ["retention","loyal","score"]) else f"{top.replace('_',' ')} Leaders"
    return names


def cluster(df):
    header("ClusterVibe", "Segment records with KMeans, reduce dimensions with PCA, and turn clusters into business personas.", "SEGMENTATION AI")
    n = nums(df)
    if len(n) < 2: st.warning("Clustering requires at least two numeric columns."); return
    selected = st.multiselect("Features", n, default=n[:min(5, len(n))]); k = st.slider("Number of clusters", 2, min(8, max(2, len(df)//8)), 3)
    if len(selected) < 2: st.info("Select at least two numeric features to activate ClusterVibe."); return
    scaled = MinMaxScaler().fit_transform(SimpleImputer(strategy="median").fit_transform(df[selected].replace([np.inf, -np.inf], np.nan)))
    max_k = min(9, len(df)-1); inertias = [KMeans(n_clusters=i, random_state=42, n_init=10).fit(scaled).inertia_ for i in range(1, max_k+1)]
    labels = KMeans(n_clusters=k, random_state=42, n_init=10).fit_predict(scaled); sil = silhouette_score(scaled, labels) if len(set(labels)) > 1 else 0
    pca = PCA(n_components=2, random_state=42); coords = pca.fit_transform(scaled); out = df.copy(); out["Cluster"] = labels; names = persona_names(out, selected); out["Cluster Persona"] = out["Cluster"].map(names); out["PCA 1"] = coords[:,0]; out["PCA 2"] = coords[:,1]
    for col, item in zip(st.columns(3), [("Clusters", k, "KMeans personas"), ("Silhouette", f"{sil:.2f}", "Separation quality"), ("PCA Variance", f"{pca.explained_variance_ratio_.sum()*100:.1f}%", "2D projection signal")]):
        with col: card(*item)
    t1, t2, t3 = st.tabs(["Cluster Map", "Elbow Method", "Persona Dashboard"])
    with t1:
        fig = px.scatter(out, x="PCA 1", y="PCA 2", color="Cluster Persona", hover_data=selected[:4], color_discrete_sequence=[GREEN,CYAN,"#f5c542","#ff5da2","#9b8cff","#ffffff"], title="PCA Cluster Projection"); fig.update_traces(marker=dict(size=10, line=dict(width=1, color="rgba(255,255,255,.45)"))); st.plotly_chart(theme(fig, 500), use_container_width=True)
    with t2:
        fig = px.line(pd.DataFrame({"k":list(range(1,max_k+1)), "Inertia":inertias}), x="k", y="Inertia", markers=True, color_discrete_sequence=[GREEN]); fig.add_vline(x=k, line_color=CYAN, line_dash="dash"); st.plotly_chart(theme(fig, 420), use_container_width=True)
    with t3:
        summary = out.groupby(["Cluster", "Cluster Persona"])[selected].mean().round(2); st.dataframe(summary, use_container_width=True); insights([f"{name} contains {int((labels == cid).sum())} records and is distinguished by elevated {summary.loc[(cid, name)].idxmax()}." for cid, name in names.items()])


def insight_panel(df):
    header("AI Insight Panel", "Automatic observations synthesized from correlations, missingness, variance, group behavior, and quality signals.", "OBSERVATION STREAM")
    insights(ai_notes(df)); n = nums(df); c = cats(df)
    if n:
        st.subheader("Business Intelligence View"); primary = st.selectbox("Primary metric", n)
        if c:
            dim = st.selectbox("Dimension", c); agg = df.groupby(dim)[primary].mean(numeric_only=True).reset_index().sort_values(primary, ascending=False); st.plotly_chart(theme(px.bar(agg, x=dim, y=primary, color=primary, color_continuous_scale=[CYAN,GREEN]), 430), use_container_width=True)
        if len(n) >= 2:
            other = st.selectbox("Compare against", [x for x in n if x != primary]); st.plotly_chart(theme(px.scatter(df, x=other, y=primary, trendline="ols", color_discrete_sequence=[GREEN]), 430), use_container_width=True)
    with st.expander("Column Intelligence", expanded=True):
        st.dataframe(pd.DataFrame({"dtype":df.dtypes.astype(str), "missing":df.isna().sum(), "missing_pct":(df.isna().mean()*100).round(2), "unique":df.nunique(dropna=True)}), use_container_width=True)


def chat_answer(df, question):
    q = question.lower()
    n, c = nums(df), cats(df)
    if not question.strip():
        return "Ask me about rows, columns, missing values, averages, correlations, outliers, or top categories."
    if "summary" in q or "summarize" in q:
        return f"This dataset has {df.shape[0]:,} rows, {df.shape[1]:,} columns, {int(df.isna().sum().sum()):,} missing values, and a {quality(df)}% quality score."
    if "missing" in q or "null" in q:
        miss = df.isna().sum().sort_values(ascending=False)
        top = miss[miss > 0].head(3)
        return "No missing values were detected." if top.empty else "Highest missing-value columns: " + ", ".join([f"{k} ({int(v)})" for k, v in top.items()]) + "."
    if "correlation" in q or "relationship" in q:
        if len(n) < 2:
            return "Correlation needs at least two numeric columns."
        pairs = df[n].corr(numeric_only=True).abs().where(np.triu(np.ones((len(n), len(n))), k=1).astype(bool)).stack()
        if pairs.empty:
            return "I could not find a reliable numeric correlation pair."
        a, b = pairs.sort_values(ascending=False).index[0]
        return f"The strongest numeric relationship is between {a} and {b}, with correlation {pairs.max():.2f}."
    if "outlier" in q or "anomaly" in q:
        if not n:
            return "Outlier detection needs numeric columns."
        col = n[0]
        s = df[col].dropna()
        q1, q3 = s.quantile(.25), s.quantile(.75)
        count = int(((s < q1 - 1.5 * (q3 - q1)) | (s > q3 + 1.5 * (q3 - q1))).sum())
        return f"Using IQR on {col}, I found {count} possible outliers."
    for col in n:
        if col.lower() in q:
            s = df[col].dropna()
            return f"{col} averages {s.mean():.2f}, ranges from {s.min():.2f} to {s.max():.2f}, and has standard deviation {s.std():.2f}."
    for col in c:
        if col.lower() in q:
            top = df[col].value_counts(dropna=True).head(3)
            return f"Top {col} values are " + ", ".join([f"{k} ({int(v)})" for k, v in top.items()]) + "."
    return "I can answer dataset questions about summary, missing values, correlations, outliers, numeric columns, and category distributions."


def insightpilot_chat(df):
    st.subheader("AI Chat With Dataset")
    examples = ["Summarize this dataset", "Which columns have missing values?", "Show strongest correlation", "Detect outliers"]
    question = st.text_input("Ask InsightPilot", value=examples[0], placeholder="Example: Which region has highest purchase value?")
    cols = st.columns(len(examples))
    for col, example in zip(cols, examples):
        with col:
            if st.button(example, key=f"chat_{example}"):
                question = example
    insights([chat_answer(df, question)])
    st.dataframe(df.head(8), use_container_width=True, hide_index=True)


def insightpilot_outliers(df):
    st.subheader("Outlier Detection AI")
    n = nums(df)
    if not n:
        st.warning("Outlier detection needs at least one numeric column.")
        return
    selected = st.multiselect("Numeric columns", n, default=n[:min(4, len(n))])
    method = st.selectbox("Detection method", ["IQR", "Z-score", "Isolation Forest"])
    if not selected:
        st.info("Select at least one numeric column.")
        return
    data = df[selected].replace([np.inf, -np.inf], np.nan)
    flags = pd.Series(False, index=df.index)
    if method == "IQR":
        for col in selected:
            s = data[col]
            q1, q3 = s.quantile(.25), s.quantile(.75)
            iqr = q3 - q1
            flags = flags | (s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)
    elif method == "Z-score":
        z = np.abs(stats.zscore(data.fillna(data.median()), nan_policy="omit"))
        flags = pd.Series((z > 3).any(axis=1), index=df.index)
    else:
        clean_data = SimpleImputer(strategy="median").fit_transform(data)
        labels = IsolationForest(contamination="auto", random_state=42).fit_predict(clean_data)
        flags = pd.Series(labels == -1, index=df.index)
    out = df.copy()
    out["Outlier_Flag"] = np.where(flags, "Outlier", "Normal")
    c1, c2, c3 = st.columns(3)
    with c1: card("Outliers", f"{int(flags.sum()):,}", f"{method} detected")
    with c2: card("Normal Rows", f"{int((~flags).sum()):,}", "Within expected range")
    with c3: card("Outlier Rate", f"{flags.mean()*100:.1f}%", "Dataset anomaly share")
    if len(selected) >= 2:
        fig = px.scatter(out, x=selected[0], y=selected[1], color="Outlier_Flag", color_discrete_map={"Outlier":"#ff5da2", "Normal":CYAN}, title="Outlier Map")
        st.plotly_chart(theme(fig, 440), use_container_width=True)
    else:
        fig = px.box(out, y=selected[0], color="Outlier_Flag", color_discrete_map={"Outlier":"#ff5da2", "Normal":CYAN})
        st.plotly_chart(theme(fig, 420), use_container_width=True)
    insights([f"{method} identified {int(flags.sum())} unusual records. Review these rows before modeling or business reporting."])
    st.dataframe(out[out["Outlier_Flag"] == "Outlier"].head(40), use_container_width=True, hide_index=True)


def insightpilot_timeseries(df):
    st.subheader("Time Series Analyzer")
    date_candidates = []
    for col in df.columns:
        parsed = pd.to_datetime(df[col], errors="coerce")
        if parsed.notna().mean() > .65:
            date_candidates.append(col)
    n = nums(df)
    if not date_candidates or not n:
        st.warning("Time series analysis needs one date-like column and one numeric metric.")
        return
    date_col = st.selectbox("Date column", date_candidates)
    metric = st.selectbox("Metric", n)
    freq = st.selectbox("Aggregation", ["D", "W", "M", "Q"], format_func=lambda x: {"D":"Daily", "W":"Weekly", "M":"Monthly", "Q":"Quarterly"}[x])
    d = df[[date_col, metric]].copy()
    d[date_col] = pd.to_datetime(d[date_col], errors="coerce")
    d = d.dropna().sort_values(date_col).set_index(date_col).resample(freq)[metric].mean().dropna().reset_index()
    if d.empty:
        st.warning("Not enough valid time-series rows after parsing dates.")
        return
    d["Moving Average"] = d[metric].rolling(min(3, len(d)), min_periods=1).mean()
    growth = 0 if len(d) < 2 or d[metric].iloc[0] == 0 else ((d[metric].iloc[-1] / d[metric].iloc[0]) - 1) * 100
    c1, c2, c3 = st.columns(3)
    with c1: card("Periods", f"{len(d):,}", "Aggregated points")
    with c2: card("Latest Value", f"{d[metric].iloc[-1]:.2f}", metric)
    with c3: card("Growth", f"{growth:.1f}%", "First to latest")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=d[date_col], y=d[metric], mode="lines+markers", name=metric, line=dict(color=CYAN, width=3)))
    fig.add_trace(go.Scatter(x=d[date_col], y=d["Moving Average"], mode="lines", name="Moving Average", line=dict(color=GREEN, width=3)))
    fig.update_layout(title=f"{metric} Trend")
    st.plotly_chart(theme(fig, 460), use_container_width=True)
    direction = "increased" if growth >= 0 else "decreased"
    insights([f"{metric} {direction} by {abs(growth):.1f}% across the selected timeline.", "Moving average smooths short-term noise so the broader trend is easier to read."])


def insight_pilot(df):
    header("InsightPilot", "Chat with your data, detect anomalies, and analyze time trends from one AI workflow.", "AI ANALYST")
    t1, t2, t3 = st.tabs(["Dataset Chat", "Outlier Detection AI", "Time Series Analyzer"])
    with t1:
        insightpilot_chat(df)
    with t2:
        insightpilot_outliers(df)
    with t3:
        insightpilot_timeseries(df)


def main():
    css(); df, module, source = sidebar()
    if module == "Home Dashboard":
        home(df, source)
    else:
        {"DataCleaner AI": cleaner, "Hypothesis Lab": lab, "ClusterVibe": cluster, "InsightPilot": insight_pilot, "AI Insight Panel": insight_panel}[module](df)


if __name__ == "__main__":
    main()

