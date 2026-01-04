"""
Streamlit Dashboard for Crypto Sentiment Monitor
Real-time visualization of sentiment analysis across multiple sources
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.database import get_data_by_timerange, get_all_data
from analysis.trend_detector import get_trending_cryptos, get_sentiment_by_source
import pandas as pd
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Crypto Sentiment Monitor", 
    page_icon="📊", 
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Crypto Sentiment Monitor")
st.markdown("Real-time sentiment analysis across Twitter, News, and Professional sources")

# Get data
try:
    all_data = get_all_data()
    recent_data = get_data_by_timerange(48)
    
    if not all_data or len(all_data) == 0:
        st.warning("⚠️ No data available yet. Waiting for data collection...")
        st.info("The scraper team's data collection process needs to run first.")
        st.stop()
    
    # Filter for analyzed data only
    analyzed_data = [row for row in all_data if row.get('sentiment_score') is not None]
    
    if not analyzed_data or len(analyzed_data) == 0:
        st.warning("⚠️ Data has been collected but not yet analyzed.")
        st.info("Run the sentiment analyzer: `python -c \"from analysis.sentiment_analyzer import process_unanalyzed_data; process_unanalyzed_data()\"`")
        st.stop()
    
    # Convert to DataFrame for easier processing
    df = pd.DataFrame(analyzed_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # === METRICS ROW ===
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_sentiment = df['sentiment_score'].mean()
        sentiment_emoji = "😊" if avg_sentiment > 0.1 else "😐" if avg_sentiment > -0.1 else "😟"
        st.metric(
            "Overall Sentiment",
            f"{avg_sentiment:.2f} {sentiment_emoji}",
            delta=f"{'Positive' if avg_sentiment > 0 else 'Negative' if avg_sentiment < 0 else 'Neutral'}"
        )
    
    with col2:
        total_posts = len(df)
        st.metric("Total Posts Analyzed", f"{total_posts:,}")
    
    with col3:
        trending = get_trending_cryptos(24)
        if trending:
            top_crypto = trending[0]['crypto']
            top_mentions = trending[0]['mentions']
            st.metric("Most Mentioned", f"{top_crypto}", f"{top_mentions} mentions")
        else:
            st.metric("Most Mentioned", "N/A")
    
    st.divider()
    
    # === SENTIMENT OVER TIME ===
    st.subheader("📈 Sentiment Trend (Last 48 Hours)")
    
    # Filter for last 48 hours
    df_48h = df[df['timestamp'] >= (datetime.now() - timedelta(hours=48))]
    
    if len(df_48h) > 0:
        # Group by hour
        df_48h['hour'] = df_48h['timestamp'].dt.floor('H')
        hourly_sentiment = df_48h.groupby('hour')['sentiment_score'].mean().reset_index()
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=hourly_sentiment['hour'],
            y=hourly_sentiment['sentiment_score'],
            mode='lines+markers',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        fig_timeline.update_layout(
            xaxis_title="Time",
            yaxis_title="Average Sentiment",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No data in the last 48 hours")
    
    # === SENTIMENT BY SOURCE ===
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("📱 Sentiment by Source")
        sentiment_by_source = get_sentiment_by_source(24)
        
        if sentiment_by_source:
            sources = list(sentiment_by_source.keys())
            sentiments = list(sentiment_by_source.values())
            colors = ['#00FF00' if s > 0 else '#FF0000' if s < 0 else '#808080' for s in sentiments]
            
            fig_source = go.Figure(data=[
                go.Bar(
                    x=sources,
                    y=sentiments,
                    marker_color=colors,
                    text=[f"{s:.2f}" for s in sentiments],
                    textposition='auto',
                )
            ])
            
            fig_source.update_layout(
                yaxis_title="Average Sentiment",
                xaxis_title="Source",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig_source, use_container_width=True)
    
    with col_right:
        st.subheader("🥧 Sentiment Distribution")
        
        # Count sentiment labels
        sentiment_counts = df['sentiment_label'].value_counts()
        
        colors_pie = {
            'positive': '#00FF00',
            'negative': '#FF0000',
            'neutral': '#808080'
        }
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=sentiment_counts.index,
            values=sentiment_counts.values,
            marker=dict(colors=[colors_pie.get(label, '#808080') for label in sentiment_counts.index]),
            hole=0.3
        )])
        
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.divider()
    
    # === TRENDING CRYPTOCURRENCIES ===
    st.subheader("🔥 Trending Cryptocurrencies (24h)")
    
    trending_cryptos = get_trending_cryptos(24)
    
    if trending_cryptos:
        # Create DataFrame for display
        trending_df = pd.DataFrame(trending_cryptos)
        trending_df.insert(0, 'Rank', range(1, len(trending_df) + 1))
        
        # Format the display
        display_df = trending_df.copy()
        display_df['avg_sentiment'] = display_df['avg_sentiment'].apply(lambda x: f"{x:.2f}")
        display_df['Sentiment Breakdown'] = display_df.apply(
            lambda row: f"✅ {row['positive_count']} | ❌ {row['negative_count']} | ⚪ {row['neutral_count']}", 
            axis=1
        )
        
        # Select columns for display
        display_df = display_df[['Rank', 'crypto', 'mentions', 'avg_sentiment', 'Sentiment Breakdown']]
        display_df.columns = ['Rank', 'Crypto', 'Mentions', 'Avg Sentiment', 'Sentiment Breakdown']
        
        # Style the dataframe
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
    else:
        st.info("No trending cryptocurrencies found in the last 24 hours")
    
    st.divider()
    
    # === RECENT POSTS ===
    st.subheader("📝 Recent Posts")
    
    # Get last 20 entries
    recent_posts = df.sort_values('timestamp', ascending=False).head(20)
    
    # Prepare display DataFrame
    display_posts = recent_posts[['source', 'content', 'sentiment_label', 'sentiment_score', 'crypto_mentioned', 'timestamp']].copy()
    
    # Truncate content
    display_posts['content'] = display_posts['content'].apply(
        lambda x: x[:100] + '...' if len(x) > 100 else x
    )
    
    # Format sentiment
    def format_sentiment(row):
        score = row['sentiment_score']
        label = row['sentiment_label']
        if label == 'positive':
            return f"😊 {score:.2f}"
        elif label == 'negative':
            return f"😟 {score:.2f}"
        else:
            return f"😐 {score:.2f}"
    
    display_posts['Sentiment'] = display_posts.apply(format_sentiment, axis=1)
    
    # Format timestamp
    display_posts['timestamp'] = display_posts['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    
    # Select and rename columns
    display_posts = display_posts[['source', 'content', 'Sentiment', 'crypto_mentioned', 'timestamp']]
    display_posts.columns = ['Source', 'Content', 'Sentiment', 'Cryptos', 'Time']
    
    st.dataframe(
        display_posts,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # === REFRESH BUTTON ===
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    # Footer
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
except Exception as e:
    st.error(f"❌ Error loading dashboard: {str(e)}")
    st.info("Make sure the database exists and contains data.")
    st.code(f"Error details: {e}")