"""
Streamlit Dashboard for Crypto Sentiment Monitor
Real-time visualization of sentiment analysis across multiple sources
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta
import pandas as pd
from analysis.trend_detector import get_trending_cryptos, get_sentiment_by_source
from utils.database import get_data_by_timerange, get_all_data
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import re
from collections import Counter
import time


# Page configuration
st.set_page_config(
    page_title="Crypto Sentiment Monitor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === CUSTOM CSS & ASSETS ===
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: #0e1117;
    }
    
    /* Custom Card Style */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Typography */
    .metric-label {
        color: #8b949e;
        font-size: 0.9rem;
        margin-bottom: 5px;
        font-weight: 500;
    }
    .metric-value {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .metric-delta {
        font-size: 0.9rem;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 600;
    }
    .delta-positive { background: rgba(0, 255, 136, 0.15); color: #00ff88; }
    .delta-negative { background: rgba(255, 76, 76, 0.15); color: #ff4c4c; }
    .delta-neutral { background: rgba(139, 148, 158, 0.15); color: #8b949e; }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }

    /* News Ticker */
    .ticker-wrap {
        width: 100%;
        overflow: hidden;
        background: rgba(0, 255, 136, 0.05);
        border-top: 1px solid rgba(0, 255, 136, 0.2);
        border-bottom: 1px solid rgba(0, 255, 136, 0.2);
        padding: 10px 0;
        margin-bottom: 20px;
        white-space: nowrap;
    }
    .ticker {
        display: inline-block;
        animation: marquee 30s linear infinite;
    }
    .ticker-item {
        display: inline-block;
        padding: 0 2rem;
        font-size: 0.9rem;
        color: #00ff88;
    }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* Tag Cloud */
    .tag-cloud {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        padding: 10px;
    }
    .tag {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 5px 15px;
        color: #e6e6e6;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }
    .tag:hover {
        background: rgba(0, 255, 136, 0.1);
        border-color: #00ff88;
        transform: scale(1.05);
        cursor: default;
    }
    .tag-lg { font-size: 1.1rem; font-weight: 600; color: #fff; border-color: rgba(255, 255, 255, 0.3); }
    .tag-md { font-size: 0.9rem; color: #ccc; }
    .tag-sm { font-size: 0.8rem; color: #999; }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* header {visibility: hidden;}  <-- Commented out to show sidebar toggle */
    
    /* Prevent graying out during refresh */
    .stApp {
        transition: none !important;
    }
    [data-testid="stOverlay"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# === SVG ICONS ===
ICONS = {
    "trending_up": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>""",
    "trending_down": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline></svg>""",
    "activity": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>""",
    "message": """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>""",
    "live": """<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="#ff4c4c" stroke="none"><circle cx="12" cy="12" r="12"></circle></svg>"""
}

def display_metric_card(label, value, delta=None, delta_type="neutral", icon=None):
    delta_html = ""
    if delta:
        delta_html = f'<span class="metric-delta delta-{delta_type}">{delta}</span>'
    
    icon_html = f'<span style="opacity: 0.7;">{icon}</span>' if icon else ""
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">
            {icon_html}
            {value}
            {delta_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def generate_word_cloud_html(texts):
    """Generate a simple HTML tag cloud from text"""
    # Basic stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'this', 'that', 'it', 'as', 'from', 'crypto', 'cryptocurrency', 'market', 'price', 'today', 'now', 'news', 'analysis', 'trading', 'bitcoin', 'ethereum'}
    
    # Tokenize and count
    words = []
    for text in texts:
        # Simple cleaning
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words.extend([w for w in clean_text.split() if w not in stop_words and len(w) > 3])
    
    counter = Counter(words)
    top_words = counter.most_common(20)
    
    if not top_words:
        return "<div class='tag-cloud'>No topics found</div>"
    
    html = "<div class='tag-cloud'>"
    max_count = top_words[0][1]
    
    for word, count in top_words:
        size_class = "tag-lg" if count > max_count * 0.6 else "tag-md" if count > max_count * 0.3 else "tag-sm"
        html += f"<span class='tag {size_class}'>{word} ({count})</span>"
    
    html += "</div>"
    return html

# Header
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("Crypto Sentiment Monitor")
    st.markdown(f"**LIVE** {ICONS['live']} | Real-time AI Analysis", unsafe_allow_html=True)
with col_h2:
    st.markdown(f"<div style='text-align: right; color: #8b949e; padding-top: 20px;'>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    demo_mode = st.toggle("Demo Mode (Simulation)", value=False)
    if demo_mode:
        st.info("⚡ Simulation Active: Injecting live data...")
        refresh_rate = st.slider("Refresh Rate (s)", 1, 10, 3)

# ... (Helper function for simulation) ...
def inject_fake_live_data(current_df):
    """Injects a fake live data point for demo purposes"""
    import random
    sources = ['twitter', 'cryptonews', 'cointelegraph']
    cryptos = ['BTC', 'ETH', 'SOL', 'DOGE', 'XRP']
    
    # Generate fake entry
    new_entry = {
        'source': random.choice(sources),
        'content': f"LIVE: {random.choice(cryptos)} is showing strong momentum! #{random.choice(cryptos)}",
        'timestamp': datetime.now(),
        'sentiment_score': random.uniform(-0.8, 0.9),
        'sentiment_label': 'positive', # Simplified
        'crypto_mentioned': random.choice(cryptos),
        'engagement_score': random.randint(10, 500)
    }
    
    # Adjust label based on score
    if new_entry['sentiment_score'] > 0.05:
        new_entry['sentiment_label'] = 'positive'
    elif new_entry['sentiment_score'] < -0.05:
        new_entry['sentiment_label'] = 'negative'
    else:
        new_entry['sentiment_label'] = 'neutral'
        
    # Create DataFrame and concat
    new_df = pd.DataFrame([new_entry])
    return pd.concat([new_df, current_df], ignore_index=True)

# Get data
try:
    all_data = get_all_data()
    
    # If no data and not in demo mode, warn user
    if (not all_data or len(all_data) == 0) and not demo_mode:
        st.warning("Waiting for data collection...")
        st.stop()

    # Filter for analyzed data only
    analyzed_data = [row for row in all_data if row.get('sentiment_score') is not None]

    # Convert to DataFrame
    df = pd.DataFrame(analyzed_data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # === DEMO MODE LOGIC ===
    if demo_mode:
        # Initialize session state for fake data if needed
        if 'fake_data' not in st.session_state:
            st.session_state.fake_data = pd.DataFrame()
        
        # Add new fake point on every rerun
        st.session_state.fake_data = inject_fake_live_data(st.session_state.fake_data)
        
        # Merge real and fake data
        if not df.empty:
            df = pd.concat([st.session_state.fake_data, df], ignore_index=True)
        else:
            df = st.session_state.fake_data
            
        # Keep only recent to avoid memory issues
        df = df.head(500)
        
        # Auto-rerun
        time.sleep(refresh_rate)
        st.rerun()

    if df.empty:
        st.warning("Data collected but not analyzed. Run analysis module.")
        st.stop()

    # === NEWS TICKER ===
    latest_news = df.sort_values('timestamp', ascending=False).head(10)
    ticker_items = ""
    for _, row in latest_news.iterrows():
        sentiment_icon = "🟢" if row['sentiment_label'] == 'positive' else "🔴" if row['sentiment_label'] == 'negative' else "⚪"
        ticker_items += f"<div class='ticker-item'>{sentiment_icon} {row['content'][:80]}...</div>"
    
    st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            {ticker_items}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # === AI INSIGHTS ===
    st.subheader("🤖 AI Market Analysis")
    
    # Generate smart summary
    summary_text = ""
    if not df.empty:
        # Calculate key metrics
        avg_s = df['sentiment_score'].mean()
        dominant_sentiment = "Bullish" if avg_s > 0.1 else "Bearish" if avg_s < -0.1 else "Neutral"
        
        # Find top crypto
        if 'crypto_mentioned' in df.columns:
            top_cryptos = df['crypto_mentioned'].value_counts()
            if not top_cryptos.empty:
                top_coin = top_cryptos.index[0]
                top_coin_count = top_cryptos.iloc[0]
                
                # Get sentiment for top coin
                coin_df = df[df['crypto_mentioned'] == top_coin]
                coin_sent = coin_df['sentiment_score'].mean()
                coin_mood = "surging" if coin_sent > 0.2 else "struggling" if coin_sent < -0.2 else "stable"
                
                summary_text = f"**Market Status:** The overall market sentiment is **{dominant_sentiment}** ({avg_s:.2f}). "
                summary_text += f"**{top_coin}** is dominating the conversation with {top_coin_count} mentions and appears to be **{coin_mood}**. "
                
                # Add source insight
                top_source = df['source'].value_counts().index[0]
                summary_text += f"Most activity is currently observed on **{top_source.title()}**."
    
    if summary_text:
        st.info(summary_text, icon="🤖")
    else:
        st.info("Insufficient data for AI analysis.", icon="⚠️")

    # === METRICS ROW ===
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_sentiment = df['sentiment_score'].mean()
        delta_type = "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral"
        icon = ICONS["trending_up"] if avg_sentiment > 0 else ICONS["trending_down"]
        
        display_metric_card(
            "Market Sentiment",
            f"{avg_sentiment:.2f}",
            delta="Bullish" if avg_sentiment > 0.1 else "Bearish" if avg_sentiment < -0.1 else "Neutral",
            delta_type=delta_type,
            icon=icon
        )

    with col2:
        total_posts = len(df)
        display_metric_card(
            "Analyzed Signals",
            f"{total_posts:,}",
            icon=ICONS["activity"]
        )

    with col3:
        # Recalculate trending for demo mode
        if demo_mode:
            # Simple count for demo
            counts = df['crypto_mentioned'].value_counts()
            if not counts.empty:
                top_crypto = counts.index[0]
                top_mentions = counts.iloc[0]
            else:
                top_crypto = "BTC"
                top_mentions = 0
        else:
            trending = get_trending_cryptos(24)
            if trending:
                top_crypto = trending[0]['crypto']
                top_mentions = trending[0]['mentions']
            else:
                top_crypto = "N/A"
                top_mentions = 0
                
        display_metric_card(
            "Top Trending",
            top_crypto,
            delta=f"{top_mentions} mentions",
            delta_type="neutral",
            icon=ICONS["message"]
        )

    st.markdown("---")

    # === MAIN DASHBOARD ===
    
    # Row 1: Charts
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.subheader("Sentiment Trend (48h)")
        
        # For demo mode, we need to handle the timestamp filtering carefully
        if demo_mode:
            df_48h = df # Use all data in demo
        else:
            df_48h = df[df['timestamp'] >= (datetime.now() - timedelta(hours=48))]
            
        if len(df_48h) > 0:
            df_48h['hour'] = df_48h['timestamp'].dt.floor('H')
            hourly_sentiment = df_48h.groupby('hour')['sentiment_score'].mean().reset_index()

            fig_timeline = go.Figure()
            
            # Add glow effect (multiple traces with different opacity/width)
            fig_timeline.add_trace(go.Scatter(
                x=hourly_sentiment['hour'],
                y=hourly_sentiment['sentiment_score'],
                mode='lines',
                line=dict(color='rgba(0, 255, 136, 0.3)', width=10),
                hoverinfo='skip'
            ))
            
            fig_timeline.add_trace(go.Scatter(
                x=hourly_sentiment['hour'],
                y=hourly_sentiment['sentiment_score'],
                mode='lines',
                line=dict(color='#00ff88', width=3, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(0, 255, 136, 0.1)'
            ))

            fig_timeline.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, color='#8b949e'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color='#8b949e'),
                margin=dict(l=0, r=0, t=0, b=0),
                height=350
            )
            st.plotly_chart(fig_timeline, use_container_width=True)

    with col_chart2:
        st.subheader("Topic Radar")
        # Generate Topic Cloud instead of Pie Chart
        recent_texts = df.sort_values('timestamp', ascending=False).head(50)['content'].tolist()
        st.markdown(generate_word_cloud_html(recent_texts), unsafe_allow_html=True)

    # Row 2: Tables
    col_table1, col_table2 = st.columns(2)
    
    with col_table1:
        st.subheader("Trending Assets")
        
        if demo_mode:
            # Generate simple trending df from current df
            trending_counts = df['crypto_mentioned'].value_counts().head(5)
            trending_data = []
            for crypto, count in trending_counts.items():
                crypto_df = df[df['crypto_mentioned'] == crypto]
                avg_sent = crypto_df['sentiment_score'].mean()
                pos = len(crypto_df[crypto_df['sentiment_label'] == 'positive'])
                neg = len(crypto_df[crypto_df['sentiment_label'] == 'negative'])
                trending_data.append({
                    'crypto': crypto,
                    'mentions': count,
                    'avg_sentiment': avg_sent,
                    'positive_count': pos,
                    'negative_count': neg
                })
            trending_df = pd.DataFrame(trending_data)
        else:
            trending_list = get_trending_cryptos(24)
            trending_df = pd.DataFrame(trending_list) if trending_list else pd.DataFrame()
            
        if not trending_df.empty:
            st.dataframe(
                trending_df[['crypto', 'mentions', 'avg_sentiment', 'positive_count', 'negative_count']],
                column_config={
                    "crypto": "Asset",
                    "mentions": st.column_config.NumberColumn("Volume", format="%d"),
                    "avg_sentiment": st.column_config.ProgressColumn(
                        "Sentiment Score",
                        help="Sentiment score from -1 to 1",
                        min_value=-1,
                        max_value=1,
                        format="%.2f",
                    ),
                    "positive_count": st.column_config.NumberColumn("Pos", format="%d"),
                    "negative_count": st.column_config.NumberColumn("Neg", format="%d"),
                },
                use_container_width=True,
                hide_index=True
            )

    with col_table2:
        st.subheader("Latest Signals")
        recent_posts = df.sort_values('timestamp', ascending=False).head(10)
        
        st.dataframe(
            recent_posts[['source', 'content', 'sentiment_score', 'timestamp']],
            column_config={
                "source": st.column_config.TextColumn("Source", width="small"),
                "content": st.column_config.TextColumn("Signal", width="large"),
                "sentiment_score": st.column_config.NumberColumn(
                    "Score",
                    format="%.2f"
                ),
                "timestamp": st.column_config.DatetimeColumn(
                    "Time",
                    format="HH:mm:ss"
                ),
            },
            use_container_width=True,
            hide_index=True
        )

    # Refresh
    if not demo_mode:
        if st.button("Refresh Analysis"):
            st.rerun()

except Exception as e:
    st.error(f"Dashboard Error: {str(e)}")
