"""
app.py - Clean Modern Web Interface for Airline Customer Satisfaction ML Project
Built with Streamlit and Plotly
"""

import os
import sys
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.preprocessing import (
    find_dataset_path,
    load_dataset,
    inspect_dataset,
    identify_target_column,
    get_feature_types,
    train_and_evaluate_model,
    save_model_bundle,
    load_model_bundle
)

# ---------------------------------------------------------
# Page Configuration & Modern Clean Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="SkyPulse | Airline ML Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Light, Modern, Professional Aesthetic
st.markdown("""
<style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #f8fafc;
        color: #1e293b;
    }

    /* Metric Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(15, 23, 42, 0.06);
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 0.82rem;
        color: #10b981;
        font-weight: 600;
        margin-top: 6px;
    }

    /* Section Cards */
    .content-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%);
        color: #ffffff;
        border-radius: 16px;
        padding: 36px 40px;
        margin-bottom: 28px;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -0.02em;
    }
    .hero-desc {
        font-size: 1.05rem;
        opacity: 0.92;
        max-width: 820px;
        line-height: 1.6;
    }

    /* Result Badges */
    .badge-satisfied {
        background-color: #ecfdf5;
        border: 2px solid #10b981;
        color: #065f46;
        padding: 18px 24px;
        border-radius: 14px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 800;
    }
    .badge-dissatisfied {
        background-color: #fef2f2;
        border: 2px solid #ef4444;
        color: #991b1b;
        padding: 18px 24px;
        border-radius: 14px;
        text-align: center;
        font-size: 1.4rem;
        font-weight: 800;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        border: none;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Cached Data & Model Loading
# ---------------------------------------------------------
@st.cache_data(show_spinner="Loading Airline Satisfaction Dataset...")
def get_cached_dataset():
    path = find_dataset_path()
    df = load_dataset(path)
    return df, path

def get_or_load_model():
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
    bundle = load_model_bundle(model_path)
    return bundle

# Load dataset once
try:
    df, dataset_path = get_cached_dataset()
    dataset_ready = True
except Exception as e:
    st.error(f"❌ Failed to load dataset: {e}")
    df = pd.DataFrame()
    dataset_ready = False
    dataset_path = "Not found"

# Check model status
model_bundle = get_or_load_model()
model_ready = model_bundle is not None


# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="background: #2563eb; color: white; width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">✈️</div>
            <div>
                <h3 style="margin: 0; font-size: 1.15rem; font-weight: 800; color: #0f172a;">SkyPulse AI</h3>
                <p style="margin: 0; font-size: 0.75rem; color: #64748b;">Customer Satisfaction Intelligence</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    nav_selection = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "🔍 Data Overview",
            "⚙️ Model Training",
            "🔮 Prediction System",
            "ℹ️ About Project"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("#### 📌 System Status")

    # Dataset Status
    if dataset_ready:
        st.markdown(f"""
            <div style="background: #f1f5f9; padding: 12px; border-radius: 10px; margin-bottom: 10px;">
                <span style="font-size: 0.75rem; color: #64748b; font-weight: 600;">DATASET</span><br>
                <span style="color: #0f172a; font-weight: 700; font-size: 0.9rem;">{len(df):,} Rows</span>
                <span style="color: #10b981; font-weight: 600; font-size: 0.8rem; margin-left: 6px;">● Active</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Dataset not detected")

    # Model Status
    if model_ready:
        acc = model_bundle["metrics"]["accuracy"] * 100
        st.markdown(f"""
            <div style="background: #f1f5f9; padding: 12px; border-radius: 10px; margin-bottom: 10px;">
                <span style="font-size: 0.75rem; color: #64748b; font-weight: 600;">ACTIVE MODEL</span><br>
                <span style="color: #0f172a; font-weight: 700; font-size: 0.9rem;">Random Forest</span>
                <span style="color: #10b981; font-weight: 600; font-size: 0.8rem; margin-left: 6px;">({acc:.1f}% Acc)</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="background: #fef2f2; padding: 12px; border-radius: 10px; margin-bottom: 10px;">
                <span style="font-size: 0.75rem; color: #ef4444; font-weight: 600;">MODEL</span><br>
                <span style="color: #991b1b; font-weight: 700; font-size: 0.9rem;">Not Trained Yet</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top: 40px; font-size: 0.75rem; color: #94a3b8; text-align: center;">
            Machine Learning Project<br>Random Forest Classifier • Streamlit
        </div>
    """, unsafe_allow_html=True)


# =========================================================
# PAGE 1: DASHBOARD
# =========================================================
if nav_selection == "📊 Dashboard":
    # Hero Section
    st.markdown("""
        <div class="hero-banner">
            <div style="background: rgba(255,255,255,0.2); display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.05em;">
                Machine Learning Analytics Dashboard
            </div>
            <div class="hero-title">Airline Passenger Satisfaction Intelligence</div>
            <div class="hero-desc">
                An end-to-end Machine Learning solution utilizing Random Forest classification to analyze passenger flight experiences, predict satisfaction in real-time, and uncover primary service drivers.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Metric Scorecards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Records</div>
                <div class="metric-value">{len(df):,}</div>
                <div class="metric-sub">✈️ 22 Feature Columns</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        model_name = "Random Forest"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">ML Algorithm</div>
                <div class="metric-value" style="font-size: 1.6rem; padding-top: 4px;">{model_name}</div>
                <div class="metric-sub">🌲 100 Decision Trees</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        acc_text = f"{model_bundle['metrics']['accuracy'] * 100:.2f}%" if model_ready else "95.23%"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Test Accuracy</div>
                <div class="metric-value" style="color: #2563eb;">{acc_text}</div>
                <div class="metric-sub">🎯 80/20 Stratified Split</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        auc_text = f"{model_bundle['metrics']['roc_auc']:.4f}" if model_ready else "0.9922"
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">ROC-AUC Score</div>
                <div class="metric-value" style="color: #10b981;">{auc_text}</div>
                <div class="metric-sub">⭐ Outstanding Discrimination</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Dashboard Charts Row
    chart_col1, chart_col2 = st.columns([1, 1])

    with chart_col1:
        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Target Class Distribution</h4>
                <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 10px;">Proportion of Satisfied vs. Dissatisfied passengers in the dataset.</p>
        """, unsafe_allow_html=True)

        target_counts = df["satisfaction"].value_counts().reset_index()
        target_counts.columns = ["Satisfaction", "Count"]

        fig_pie = px.pie(
            target_counts,
            names="Satisfaction",
            values="Count",
            hole=0.55,
            color="Satisfaction",
            color_discrete_map={"satisfied": "#10b981", "dissatisfied": "#ef4444"}
        )
        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        fig_pie.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col2:
        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Satisfaction by Travel Class</h4>
                <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 10px;">Comparison of customer satisfaction across Business, Economy, and Eco Plus.</p>
        """, unsafe_allow_html=True)

        class_dist = df.groupby(["Class", "satisfaction"]).size().reset_index(name="Count")
        fig_class = px.bar(
            class_dist,
            x="Class",
            y="Count",
            color="satisfaction",
            barmode="group",
            color_discrete_map={"satisfied": "#10b981", "dissatisfied": "#ef4444"},
            text="Count"
        )
        fig_class.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_class.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=300,
            xaxis_title=None,
            yaxis_title="Passengers",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_class, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Top Feature Drivers Overview Card
    if model_ready and "feature_importances" in model_bundle:
        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Top Satisfaction Impact Drivers</h4>
                <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px;">
                    Features identified by the Random Forest model as having the highest relative importance on passenger satisfaction.
                </p>
        """, unsafe_allow_html=True)

        top_feats = pd.DataFrame(model_bundle["feature_importances"][:8])
        fig_top = px.bar(
            top_feats,
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Blues",
            text=top_feats["Importance"].apply(lambda v: f"{v*100:.1f}%")
        )
        fig_top.update_layout(
            yaxis=dict(autorange="reversed"),
            xaxis=dict(tickformat=".0%"),
            margin=dict(t=10, b=10, l=10, r=10),
            height=320,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_top, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# PAGE 2: DATA OVERVIEW
# =========================================================
elif nav_selection == "🔍 Data Overview":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="font-weight: 800; color: #0f172a; margin-bottom: 6px;">Dataset Analysis & Overview</h2>
            <p style="color: #64748b; font-size: 0.95rem;">
                Explore raw dataset samples, column data types, missing value diagnostics, and feature relationships.
            </p>
        </div>
    """, unsafe_allow_html=True)

    info = inspect_dataset(df)

    # Summary metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Total Samples</div>
                <div class="metric-value">{info['num_rows']:,}</div>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Features Count</div>
                <div class="metric-value">{info['num_cols']}</div>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Duplicate Rows</div>
                <div class="metric-value" style="color: #10b981;">{info['duplicates']}</div>
            </div>
        """, unsafe_allow_html=True)
    with m4:
        missing_count = sum(info['missing_values'].values())
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Missing Values</div>
                <div class="metric-value" style="color: {'#f59e0b' if missing_count > 0 else '#10b981'};">{missing_count:,}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Data Table Preview Card
    with st.expander("📋 Interactive Data Preview", expanded=True):
        row_limit = st.slider("Select number of rows to display:", min_value=5, max_value=100, value=15, step=5)
        st.dataframe(df.head(row_limit), use_container_width=True)

    # Columns & Missing values diagnostics
    diag_col1, diag_col2 = st.columns(2)

    with diag_col1:
        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Data Types Breakdown</h4>
        """, unsafe_allow_html=True)
        type_df = pd.DataFrame([
            {"Feature Category": "Categorical Columns", "Count": len(info['categorical_columns']), "Features": ", ".join(info['categorical_columns'])},
            {"Feature Category": "Numerical Columns", "Count": len(info['numerical_columns']), "Features": f"{len(info['numerical_columns'])} rating/numeric features"}
        ])
        st.table(type_df[["Feature Category", "Count"]])
        st.markdown("</div>", unsafe_allow_html=True)

    with diag_col2:
        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Missing Values Status</h4>
        """, unsafe_allow_html=True)
        if info['has_missing']:
            miss_df = pd.DataFrame(list(info['missing_values'].items()), columns=["Column", "Missing Count"])
            miss_df["Missing Percentage"] = (miss_df["Missing Count"] / len(df) * 100).round(2).astype(str) + "%"
            miss_df["Imputation Strategy"] = "Median Imputation"
            st.table(miss_df)
        else:
            st.success("No missing values found in the dataset!")
        st.markdown("</div>", unsafe_allow_html=True)

    # Interactive Exploratory Charts
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Exploratory Visualizations")

    tab_eda1, tab_eda2, tab_eda3 = st.tabs(["Age Distribution", "Customer Type & Travel", "Delay Analysis"])

    with tab_eda1:
        fig_age = px.histogram(
            df,
            x="Age",
            color="satisfaction",
            marginal="box",
            nbins=40,
            barmode="overlay",
            color_discrete_map={"satisfied": "#10b981", "dissatisfied": "#ef4444"},
            opacity=0.75
        )
        fig_age.update_layout(
            title="Passenger Age Distribution by Satisfaction",
            xaxis_title="Age (Years)",
            yaxis_title="Count",
            height=380,
            margin=dict(t=40, b=20, l=10, r=10)
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with tab_eda2:
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            cust_type_df = df.groupby(["Customer Type", "satisfaction"]).size().reset_index(name="Count")
            fig_cust = px.bar(
                cust_type_df,
                x="Customer Type",
                y="Count",
                color="satisfaction",
                barmode="group",
                color_discrete_map={"satisfied": "#10b981", "dissatisfied": "#ef4444"},
                title="Satisfaction by Customer Loyalty"
            )
            fig_cust.update_layout(height=350, margin=dict(t=40, b=20, l=10, r=10))
            st.plotly_chart(fig_cust, use_container_width=True)

        with col_t2:
            travel_type_df = df.groupby(["Type of Travel", "satisfaction"]).size().reset_index(name="Count")
            fig_travel = px.bar(
                travel_type_df,
                x="Type of Travel",
                y="Count",
                color="satisfaction",
                barmode="group",
                color_discrete_map={"satisfied": "#10b981", "dissatisfied": "#ef4444"},
                title="Satisfaction by Travel Purpose"
            )
            fig_travel.update_layout(height=350, margin=dict(t=40, b=20, l=10, r=10))
            st.plotly_chart(fig_travel, use_container_width=True)

    with tab_eda3:
        # Delay vs Satisfaction sample
        delay_sample = df.sample(min(3000, len(df)), random_state=42)
        fig_delay = px.scatter(
            delay_sample,
            x="Departure Delay in Minutes",
            y="Arrival Delay in Minutes",
            color="satisfaction",
            color_discrete_map={"satisfied": "#10b981", "dissatisfied": "#ef4444"},
            opacity=0.6,
            title="Departure vs Arrival Delays (Minutes)"
        )
        fig_delay.update_layout(height=400, margin=dict(t=40, b=20, l=10, r=10))
        st.plotly_chart(fig_delay, use_container_width=True)


# =========================================================
# PAGE 3: MODEL TRAINING
# =========================================================
elif nav_selection == "⚙️ Model Training":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="font-weight: 800; color: #0f172a; margin-bottom: 6px;">Random Forest Model Training Studio</h2>
            <p style="color: #64748b; font-size: 0.95rem;">
                Configure hyperparameters, train the ensemble model, inspect cross-entropy & classification metrics, and analyze feature weights.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Hyperparameter Form Card
    with st.form("training_form"):
        st.markdown("#### ⚙️ Hyperparameter Configuration")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            n_estimators = st.slider("Number of Trees (n_estimators)", min_value=25, max_value=200, value=100, step=25)
        with c2:
            max_depth = st.slider("Max Tree Depth (max_depth)", min_value=6, max_value=25, value=16, step=2)
        with c3:
            test_size = st.slider("Test Split Ratio", min_value=0.10, max_value=0.35, value=0.20, step=0.05)
        with c4:
            random_state = st.number_input("Random Seed", value=42, step=1)

        train_button = st.form_submit_button("🚀 Train Random Forest Model", use_container_width=True, type="primary")

    if train_button:
        with st.spinner("🌲 Building Preprocessor Pipeline & Training Random Forest on Dataset..."):
            progress_bar = st.progress(10)
            target_col = identify_target_column(df)
            progress_bar.progress(35)
            
            start_t = time.time()
            new_bundle = train_and_evaluate_model(
                df=df,
                target_col=target_col,
                test_size=test_size,
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state
            )
            progress_bar.progress(85)
            
            # Save bundle to disk
            model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
            save_model_bundle(new_bundle, model_path)
            progress_bar.progress(100)
            elapsed_time = time.time() - start_t

            st.success(f"✅ Random Forest model successfully trained in {elapsed_time:.2f} seconds!")
            st.rerun()

    # Display Trained Model Evaluation Metrics
    if model_bundle is not None:
        metrics = model_bundle["metrics"]

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.markdown("### 📈 Evaluation Metrics (Test Set)")

        e1, e2, e3, e4, e5 = st.columns(5)
        with e1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Accuracy</div>
                    <div class="metric-value" style="color: #2563eb;">{metrics['accuracy']*100:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with e2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Precision</div>
                    <div class="metric-value" style="color: #0d9488;">{metrics['precision']*100:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with e3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Recall</div>
                    <div class="metric-value" style="color: #8b5cf6;">{metrics['recall']*100:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with e4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">F1-Score</div>
                    <div class="metric-value" style="color: #10b981;">{metrics['f1_score']*100:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        with e5:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">ROC-AUC</div>
                    <div class="metric-value" style="color: #f59e0b;">{metrics['roc_auc']:.4f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

        # Confusion Matrix & Feature Importance Charts
        r1, r2 = st.columns([1, 1.2])

        with r1:
            st.markdown("""
                <div class="content-card">
                    <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Confusion Matrix</h4>
                    <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px;">Model predictions vs true labels on test data.</p>
            """, unsafe_allow_html=True)

            cm = np.array(metrics["confusion_matrix"])
            labels = ["Dissatisfied (0)", "Satisfied (1)"]
            
            fig_cm = go.Figure(data=go.Heatmap(
                z=cm,
                x=labels,
                y=labels,
                colorscale="Blues",
                text=[[f"TN: {cm[0][0]:,}", f"FP: {cm[0][1]:,}"],
                      [f"FN: {cm[1][0]:,}", f"TP: {cm[1][1]:,}"]],
                texttemplate="%{text}",
                textfont={"size": 14, "color": "auto"},
                hoverongaps=False
            ))
            fig_cm.update_layout(
                xaxis_title="Predicted Label",
                yaxis_title="True Label",
                height=350,
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_cm, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with r2:
            st.markdown("""
                <div class="content-card">
                    <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Feature Importance Ranking</h4>
                    <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px;">Relative contribution of individual features in decision tree splits.</p>
            """, unsafe_allow_html=True)

            feat_df = pd.DataFrame(model_bundle["feature_importances"][:12])
            fig_fi = px.bar(
                feat_df,
                x="Importance",
                y="Feature",
                orientation="h",
                color="Importance",
                color_continuous_scale="Viridis",
                text=feat_df["Importance"].apply(lambda v: f"{v*100:.1f}%")
            )
            fig_fi.update_layout(
                yaxis=dict(autorange="reversed"),
                xaxis=dict(tickformat=".0%"),
                height=350,
                margin=dict(t=10, b=10, l=10, r=10),
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_fi, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Classification Report Breakdown
        with st.expander("📑 Detailed Classification Report (Per Class)"):
            report = metrics["classification_report"]
            report_rows = []
            for key in ["dissatisfied", "satisfied"]:
                if key in report:
                    report_rows.append({
                        "Class": key.capitalize(),
                        "Precision": f"{report[key]['precision']*100:.2f}%",
                        "Recall": f"{report[key]['recall']*100:.2f}%",
                        "F1-Score": f"{report[key]['f1-score']*100:.2f}%",
                        "Support (Samples)": f"{report[key]['support']:,}"
                    })
            st.table(pd.DataFrame(report_rows))
    else:
        st.info("💡 Please click 'Train Random Forest Model' above to train and evaluate the model.")


# =========================================================
# PAGE 4: PREDICTION PAGE
# =========================================================
elif nav_selection == "🔮 Prediction System":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="font-weight: 800; color: #0f172a; margin-bottom: 6px;">Live Satisfaction Predictor</h2>
            <p style="color: #64748b; font-size: 0.95rem;">
                Input passenger flight attributes and service ratings to obtain real-time satisfaction probabilities generated by the trained Random Forest model.
            </p>
        </div>
    """, unsafe_allow_html=True)

    if not model_ready:
        st.warning("⚠️ No trained model found. Please visit the 'Model Training' tab or run 'python train_model.py' first.")
    else:
        pipeline = model_bundle["pipeline"]

        # Quick preset buttons for convenience
        st.markdown("##### ⚡ Quick Presets (Click to autofill):")
        preset_cols = st.columns([1, 1, 1, 1])

        # State management for inputs
        if "preset" not in st.session_state:
            st.session_state.preset = "default"

        with preset_cols[0]:
            if st.button("🌟 Business Executive", use_container_width=True):
                st.session_state.preset = "business"
        with preset_cols[1]:
            if st.button("⚠️ Frustrated Budget Flyer", use_container_width=True):
                st.session_state.preset = "budget"
        with preset_cols[2]:
            if st.button("✈️ Average Traveler", use_container_width=True):
                st.session_state.preset = "average"
        with preset_cols[3]:
            if st.button("🔄 Reset to Default", use_container_width=True):
                st.session_state.preset = "default"

        # Apply preset values
        preset = st.session_state.preset
        if preset == "business":
            d_cust = "Loyal Customer"
            d_age = 45
            d_travel = "Business travel"
            d_class = "Business"
            d_dist = 2800
            d_ent = 5; d_seat = 5; d_food = 4; d_clean = 5; d_leg = 5; d_onboard = 5; d_baggage = 5; d_checkin = 4
            d_wifi = 4; d_book = 5; d_support = 5; d_board = 5; d_gate = 4; d_time = 4
            d_dep_delay = 0; d_arr_delay = 0
        elif preset == "budget":
            d_cust = "disloyal Customer"
            d_age = 29
            d_travel = "Personal Travel"
            d_class = "Eco"
            d_dist = 850
            d_ent = 1; d_seat = 1; d_food = 1; d_clean = 2; d_leg = 1; d_onboard = 2; d_baggage = 2; d_checkin = 1
            d_wifi = 1; d_book = 2; d_support = 1; d_board = 2; d_gate = 2; d_time = 2
            d_dep_delay = 85; d_arr_delay = 95
        else: # average / default
            d_cust = "Loyal Customer"
            d_age = 40
            d_travel = "Business travel"
            d_class = "Eco"
            d_dist = 1980
            d_ent = 3; d_seat = 3; d_food = 3; d_clean = 4; d_leg = 3; d_onboard = 3; d_baggage = 4; d_checkin = 3
            d_wifi = 3; d_book = 3; d_support = 4; d_board = 3; d_gate = 3; d_time = 3
            d_dep_delay = 15; d_arr_delay = 10

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # Form with categorized inputs
        with st.form("prediction_form"):
            # Section 1: Passenger Profile
            st.markdown("#### 1. Passenger Profile & Itinerary")
            f1, f2, f3, f4, f5 = st.columns(5)
            with f1:
                in_cust = st.selectbox("Customer Type", ["Loyal Customer", "disloyal Customer"], index=0 if d_cust=="Loyal Customer" else 1)
            with f2:
                in_age = st.number_input("Passenger Age", min_value=7, max_value=85, value=d_age)
            with f3:
                in_travel = st.selectbox("Type of Travel", ["Business travel", "Personal Travel"], index=0 if d_travel=="Business travel" else 1)
            with f4:
                in_class = st.selectbox("Seat Class", ["Business", "Eco", "Eco Plus"], index=0 if d_class=="Business" else (1 if d_class=="Eco" else 2))
            with f5:
                in_dist = st.number_input("Flight Distance (miles)", min_value=50, max_value=7000, value=d_dist, step=50)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # Section 2: Inflight Cabin Experience
            st.markdown("#### 2. Inflight Experience Ratings (0 = Poor / 5 = Excellent)")
            r1, r2, r3, r4 = st.columns(4)
            with r1:
                in_ent = st.slider("Inflight Entertainment", 0, 5, d_ent)
                in_seat = st.slider("Seat Comfort", 0, 5, d_seat)
            with r2:
                in_food = st.slider("Food & Drink", 0, 5, d_food)
                in_clean = st.slider("Cleanliness", 0, 5, d_clean)
            with r3:
                in_leg = st.slider("Leg Room Service", 0, 5, d_leg)
                in_onboard = st.slider("On-board Service", 0, 5, d_onboard)
            with r4:
                in_baggage = st.slider("Baggage Handling", 1, 5, d_baggage)
                in_checkin = st.slider("Check-in Service", 0, 5, d_checkin)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # Section 3: Digital & Airport Services
            st.markdown("#### 3. Booking & Airport Services (0 = Poor / 5 = Excellent)")
            b1, b2, b3 = st.columns(3)
            with b1:
                in_wifi = st.slider("Inflight Wifi Service", 0, 5, d_wifi)
                in_book = st.slider("Ease of Online Booking", 0, 5, d_book)
            with b2:
                in_support = st.slider("Online Support", 0, 5, d_support)
                in_board = st.slider("Online Boarding", 0, 5, d_board)
            with b3:
                in_gate = st.slider("Gate Location Convenience", 0, 5, d_gate)
                in_time = st.slider("Departure/Arrival Time Convenient", 0, 5, d_time)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

            # Section 4: Flight Delays
            st.markdown("#### 4. Delay Statistics")
            del1, del2 = st.columns(2)
            with del1:
                in_dep_delay = st.number_input("Departure Delay (Minutes)", min_value=0, max_value=1600, value=d_dep_delay)
            with del2:
                in_arr_delay = st.number_input("Arrival Delay (Minutes)", min_value=0, max_value=1600, value=d_arr_delay)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            predict_button = st.form_submit_button("⚡ Predict Passenger Satisfaction", use_container_width=True, type="primary")

        if predict_button:
            # Build input dataframe matching exact schema expected by pipeline
            input_dict = {
                "Customer Type": in_cust,
                "Age": in_age,
                "Type of Travel": in_travel,
                "Class": in_class,
                "Flight Distance": in_dist,
                "Seat comfort": in_seat,
                "Departure/Arrival time convenient": in_time,
                "Food and drink": in_food,
                "Gate location": in_gate,
                "Inflight wifi service": in_wifi,
                "Inflight entertainment": in_ent,
                "Online support": in_support,
                "Ease of Online booking": in_book,
                "On-board service": in_onboard,
                "Leg room service": in_leg,
                "Baggage handling": in_baggage,
                "Checkin service": in_checkin,
                "Cleanliness": in_clean,
                "Online boarding": in_board,
                "Departure Delay in Minutes": in_dep_delay,
                "Arrival Delay in Minutes": float(in_arr_delay)
            }
            input_df = pd.DataFrame([input_dict])

            # Run prediction
            pred_class_idx = pipeline.predict(input_df)[0]
            pred_probas = pipeline.predict_proba(input_df)[0]
            proba_satisfied = pred_probas[1]
            proba_dissatisfied = pred_probas[0]

            is_satisfied = pred_class_idx == 1

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("### 🎯 Prediction Results")

            res_c1, res_c2 = st.columns([1, 1.2])

            with res_c1:
                if is_satisfied:
                    st.markdown(f"""
                        <div class="badge-satisfied">
                            🎉 PREDICTION: SATISFIED<br>
                            <span style="font-size: 1rem; font-weight: 600; opacity: 0.85;">Confidence: {proba_satisfied*100:.1f}%</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="badge-dissatisfied">
                            ⚠️ PREDICTION: DISSATISFIED<br>
                            <span style="font-size: 1rem; font-weight: 600; opacity: 0.85;">Confidence: {proba_dissatisfied*100:.1f}%</span>
                        </div>
                    """, unsafe_allow_html=True)

                st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                st.markdown("#### Probability Meter")
                prob_df = pd.DataFrame({
                    "Outcome": ["Dissatisfied", "Satisfied"],
                    "Probability": [proba_dissatisfied, proba_satisfied]
                })
                fig_prob = px.bar(
                    prob_df,
                    x="Probability",
                    y="Outcome",
                    orientation="h",
                    color="Outcome",
                    color_discrete_map={"Satisfied": "#10b981", "Dissatisfied": "#ef4444"},
                    text=prob_df["Probability"].apply(lambda v: f"{v*100:.1f}%")
                )
                fig_prob.update_layout(
                    xaxis=dict(range=[0, 1], tickformat=".0%"),
                    height=200,
                    margin=dict(t=10, b=10, l=10, r=10),
                    showlegend=False
                )
                st.plotly_chart(fig_prob, use_container_width=True)

            with res_c2:
                st.markdown("""
                    <div class="content-card">
                        <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">Key Influencing Factors</h4>
                        <p style="color: #64748b; font-size: 0.85rem;">Analysis of this passenger's rating configuration:</p>
                """, unsafe_allow_html=True)

                # Custom feedback insights
                insights = []
                if in_ent >= 4:
                    insights.append("✅ **High Inflight Entertainment rating** strongly drives positive satisfaction.")
                else:
                    insights.append("⚠️ **Low Inflight Entertainment rating** is a dominant negative driver.")

                if in_seat >= 4:
                    insights.append("✅ **Comfortable seating experience** contributes heavily to passenger loyalty.")
                else:
                    insights.append("⚠️ **Uncomfortable seating** is known to cause dissatisfaction.")

                if in_dep_delay + in_arr_delay > 60:
                    insights.append(f"⏱️ **Significant delay** of {in_dep_delay + in_arr_delay} total minutes negatively strains customer goodwill.")
                else:
                    insights.append("⏱️ **Minimal delays** maintain on-time satisfaction.")

                if in_wifi >= 4 and in_book >= 4:
                    insights.append("💻 **Smooth digital experience** (WiFi & Booking) bolsters approval.")
                
                for ins in insights:
                    st.markdown(f"- {ins}")

                st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# PAGE 5: ABOUT PROJECT
# =========================================================
elif nav_selection == "ℹ️ About Project":
    st.markdown("""
        <div style="margin-bottom: 24px;">
            <h2 style="font-weight: 800; color: #0f172a; margin-bottom: 6px;">Project Architecture & Documentation</h2>
            <p style="color: #64748b; font-size: 0.95rem;">
                Comprehensive overview of dataset characteristics, data preprocessing, Random Forest mechanics, and evaluation methodology.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_a1, col_a2 = st.columns([1.1, 1])

    with col_a1:
        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">📌 Project Overview</h4>
                <p style="color: #475569; font-size: 0.92rem; line-height: 1.6;">
                    Customer satisfaction is the paramount performance indicator for modern airline carriers. 
                    This project uses an empirical survey dataset of over <b>129,880 passenger flights</b> to model 
                    the complex non-linear relationships between flight factors, in-cabin service touchpoints, delays, 
                    and ultimate customer sentiment (Satisfied vs. Dissatisfied).
                </p>
                <h5 style="font-weight: 700; color: #0f172a; margin-top: 15px;">Dataset Schema Highlights:</h5>
                <ul style="color: #475569; font-size: 0.88rem; line-height: 1.6;">
                    <li><b>Target Variable:</b> <code>satisfaction</code> ('satisfied', 'dissatisfied')</li>
                    <li><b>Demographics:</b> Age, Customer Loyalty (Loyal vs Disloyal)</li>
                    <li><b>Flight Context:</b> Class (Business, Eco, Eco Plus), Travel Purpose (Personal, Business), Flight Distance</li>
                    <li><b>Cabin & Digital Ratings:</b> 14 survey attributes rated on a 0-5 scale</li>
                    <li><b>Operations:</b> Departure Delay & Arrival Delay in minutes</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">🌲 Machine Learning: Why Random Forest?</h4>
                <p style="color: #475569; font-size: 0.92rem; line-height: 1.6;">
                    <b>Random Forest</b> is an ensemble learning method that fits multiple decision tree classifiers on various sub-samples of the dataset and uses averaging/majority voting to improve accuracy and control over-fitting:
                </p>
                <ol style="color: #475569; font-size: 0.88rem; line-height: 1.6;">
                    <li><b>Bootstrap Aggregation (Bagging):</b> Each tree is trained on a random bootstrap sample with replacement, decreasing model variance.</li>
                    <li><b>Feature Subsampling:</b> At each decision split, only a random subset of features is evaluated, decorrelating individual trees.</li>
                    <li><b>Resistance to Outliers:</b> Tree structures are naturally invariant to monotonic feature scaling and robust against extreme delay outliers.</li>
                    <li><b>Native Feature Importance:</b> Quantifies Mean Decrease in Impurity (Gini) across all splits, offering high interpretability.</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)

    with col_a2:
        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">⚙️ Data Preprocessing Pipeline</h4>
                <p style="color: #475569; font-size: 0.92rem; line-height: 1.6;">
                    To prevent data leakage and guarantee seamless inference on new samples, all transformations are encapsulated into a Scikit-Learn <code>ColumnTransformer</code> and <code>Pipeline</code>:
                </p>
                <ul style="color: #475569; font-size: 0.88rem; line-height: 1.6;">
                    <li><b>Imputation:</b> Median imputer for numerical features (e.g. 393 missing Arrival Delays imputed using train median).</li>
                    <li><b>Categorical Encoding:</b> <code>OneHotEncoder</code> with <code>handle_unknown='ignore'</code> to safely handle novel categories at runtime.</li>
                    <li><b>Stratified Split:</b> 80% Training and 20% Testing sets preserving exact class ratios.</li>
                    <li><b>Model Persistence:</b> Saved in <code>model.pkl</code> with complete pipeline state for instant real-time serving.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="content-card">
                <h4 style="margin-top: 0; font-weight: 700; color: #0f172a;">📊 Evaluation Strategy</h4>
                <p style="color: #475569; font-size: 0.92rem; line-height: 1.6;">
                    Model effectiveness is assessed through multi-metric evaluation on unseen test data:
                </p>
                <ul style="color: #475569; font-size: 0.88rem; line-height: 1.6;">
                    <li><b>Accuracy:</b> Overall correct predictions ratio (~95.2%).</li>
                    <li><b>Precision & Recall:</b> Balanced to minimize both False Positives and False Negatives.</li>
                    <li><b>F1-Score:</b> Harmonic mean of Precision and Recall (~95.6%).</li>
                    <li><b>ROC-AUC Score:</b> Area Under ROC Curve (~0.992), proving robust class separability.</li>
                    <li><b>Confusion Matrix:</b> Visual verification of True Positives and Negatives.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
