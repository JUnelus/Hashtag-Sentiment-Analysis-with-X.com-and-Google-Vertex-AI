import praw
import pandas as pd
from textblob import TextBlob

# Set up Reddit API credentials
reddit = praw.Reddit(client_id='c6511yYdarp1V2LI_9NHSg',
                     client_secret='16KolA3s9x9AnxuQd2FVc03-bNJGPw',
                     user_agent='my_reddit_app/0.1 by u/JUnelus3')

# Function to perform sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    # Polarity > 0 = Positive, < 0 = Negative, 0 = Neutral
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

# Define the subreddit and keyword to search for
subreddit = reddit.subreddit('all')
search_query = 'Wolverine and Deadpool'

# Search Reddit posts based on the query
posts = []
for submission in subreddit.search(search_query, limit=100):
    title = submission.title
    body = submission.selftext
    full_text = title + " " + body
    sentiment = analyze_sentiment(full_text)
    posts.append([title, body, full_text, sentiment])

# Create a DataFrame and store results in a CSV file
df = pd.DataFrame(posts, columns=['title', 'body', 'full_text', 'sentiment'])

# Drop rows where 'body' or 'full_text' is NaN
df = df.dropna(subset=['full_text'])

# Remove special characters or emojis (optional)
df['full_text'] = df['full_text'].str.replace(r'[^\x00-\x7F]+', '', regex=True)

# Ensure valid sentiment values
valid_sentiments = ['positive', 'negative', 'neutral']
df = df[df['sentiment'].isin(valid_sentiments)]

# Truncate long text fields (title and full_text) to 128 characters
df['title'] = df['title'].apply(lambda x: x[:128] if isinstance(x, str) else x)
df['full_text'] = df['full_text'].apply(lambda x: x[:128] if isinstance(x, str) else x)

# Drop the 'body' column
df = df.drop(columns=['body'])

# Remove any remaining duplicate rows based on 'full_text' and 'sentiment'
df = df.drop_duplicates(subset=['full_text', 'sentiment'])

# Save the corrected dataset
file_path = 'data/cleaned_reddit_wolverine_deadpool_sentiment.csv'
df.to_csv(file_path, index=False)

print("Data saved to CSV successfully.")

# # Pull comments from the search query results
# comments = []
# for submission in subreddit.search(search_query, limit=100):
#     submission.comments.replace_more(limit=0)
#     for comment in submission.comments.list():
#         text = comment.body
#         sentiment = analyze_sentiment(text)
#         comments.append([text, sentiment])
#
# # Save comments to a CSV file
# df_comments = pd.DataFrame(comments, columns=['comment', 'sentiment'])
# df_comments.to_csv('data/reddit_wolverine_deadpool_comments_sentiment.csv', index=False)

# print("Comments data saved to CSV successfully.")