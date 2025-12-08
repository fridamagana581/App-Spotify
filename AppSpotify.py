import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
file_path = '/content/drive/MyDrive/Colab Notebooks/Práctica limpieza/Most Streamed Spotify Songs 2024.csv'
df = pd.read_csv(file_path, encoding='latin1')

# 2. Define and drop columns
# This list is consolidated from all previous drop operations, ensuring 'TikTok Posts' is retained for later analysis.
all_columns_to_drop = [
    'TIDAL Popularity',
    'Explicit Track',
    'Pandora Streams',
    'Deezer Playlist Count',
    'Deezer Playlist Reach',
    'SiriusXM Spins',
    'Spotify Playlist Count',
    'ISRC',
    'Track Score',
    'AirPlay Spins',
    'Amazon Playlist Count',
    'Pandora Track Stations',
    'Soundcloud Streams',
    'TikTok Views',
    'TikTok Likes',
    'YouTube Views',
    'YouTube Playlist Reach',
    'Apple Music Playlist Count',
    'All Time Rank',
    'Spotify Popularity'
]
df = df.drop(columns=all_columns_to_drop, errors='ignore')

# 3. Handle missing values (after column drops)
df = df.dropna()

# 4. Convert 'Release Date' to datetime
df['Release Date'] = pd.to_datetime(df['Release Date'])

# 5. Filter by year 2024
df = df[df['Release Date'].dt.year == 2024]

# 6. Clean and convert 'Spotify Streams'
df['Spotify Streams'] = df['Spotify Streams'].astype(str).str.replace(',', '', regex=False)
df['Spotify Streams'] = pd.to_numeric(df['Spotify Streams'], errors='coerce')
df.dropna(subset=['Spotify Streams'], inplace=True)

# 7. Calculate top 5 artists by Spotify Streams
top_5_artists_2024 = df.groupby('Artist')['Spotify Streams'].sum().nlargest(5)
display(top_5_artists_2024)

# 8. Plot top 5 artists by Spotify Streams
plt.figure(figsize=(10, 6))
sns.barplot(x=top_5_artists_2024.index, y=top_5_artists_2024.values / 1_000_000_000, palette='viridis')
plt.title('Top 5 Most Streamed Artists in 2024')
plt.xlabel('Artist')
plt.ylabel('Spotify Streams (Billions)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 9. Clean and convert 'TikTok Posts' and calculate top 5 songs by TikTok Posts
# This block is conditionally executed as 'TikTok Posts' might have been dropped by other means if not specifically excluded.
if 'TikTok Posts' in df.columns:
    df['TikTok Posts'] = df['TikTok Posts'].astype(str).str.replace(',', '', regex=False)
    df['TikTok Posts'] = pd.to_numeric(df['TikTok Posts'], errors='coerce')
    df.dropna(subset=['TikTok Posts'], inplace=True)

    top_5_tiktok_songs = df.groupby('Track')['TikTok Posts'].sum().nlargest(5)
    display(top_5_tiktok_songs)
else:
    print("The 'TikTok Posts' column is not available in the DataFrame. Cannot calculate top TikTok songs.")

# 10. Plot top 5 songs by TikTok Posts
# Only attempt to plot if top_5_tiktok_songs was successfully calculated and is not empty
if 'TikTok Posts' in df.columns and 'top_5_tiktok_songs' in locals() and not top_5_tiktok_songs.empty:
    plt.figure(figsize=(12, 7))
    sns.barplot(x=top_5_tiktok_songs.index, y=top_5_tiktok_songs.values / 1_000_000, palette='magma')
    plt.title('Top 5 Songs by TikTok Posts')
    plt.xlabel('Track')
    plt.ylabel('Number of TikTok Posts (Millions)')
    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()
    plt.show()
