

import os
import frontmatter
import markdown
from flask import Flask, render_template, abort

app = Flask(__name__)

# --- Data Loading and Processing ---

def get_posts():
    """
    Scans the 'posts' directory, loads all markdown files,
    parses their metadata and content, and returns a sorted list of posts.
    """
    posts_path = 'posts'
    posts = []
    
    for filename in os.listdir(posts_path):
        if filename.endswith('.md'):
            filepath = os.path.join(posts_path, filename)
            
            # Use python-frontmatter to load metadata and content
            post_data = frontmatter.load(filepath)
            
            # Store metadata and the slug (filename without .md)
            post = post_data.metadata
            post['slug'] = filename[:-3] # Remove .md extension
            
            # Convert Markdown content to HTML
            post['content_html'] = markdown.markdown(post_data.content)
            
            posts.append(post)

    # Sort posts by date, newest first
    posts.sort(key=lambda p: p.get('date'), reverse=True)
    return posts

# Make posts and labels globally available to all templates
@app.context_processor
def inject_global_data():
    """
    Injects global data into the context of all templates.
    This avoids having to pass 'all_posts' and 'all_labels' to every render_template call.
    """
    all_posts = get_posts()
    
    # Get a unique, sorted list of all labels from all posts
    all_labels = sorted(list(set(label for post in all_posts for label in post.get('labels', []))))
    
    return dict(
        all_posts=all_posts,
        all_labels=all_labels
    )

# --- Routes ---

@app.route('/')
def index():
    """
    The homepage. It will display the author and latest posts in the middle.
    The sidebars are handled by the base template and context processor.
    """
    # The 'all_posts' variable is already available thanks to inject_global_data
    return render_template('index.html')

@app.route('/post/<slug>')
def post_page(slug):
    """
    Displays a single post.
    """
    all_posts = get_posts()
    # Find the post with the matching slug
    post = next((p for p in all_posts if p['slug'] == slug), None)
    
    if post is None:
        abort(404) # Not found
        
    return render_template('post.html', post=post)

@app.route('/label/<label_name>')
def posts_by_label(label_name):
    """
    Filters and displays all posts that have a specific label.
    """
    all_posts = get_posts()
    # Filter posts to include only those with the given label
    filtered_posts = [p for p in all_posts if label_name in p.get('labels', [])]
    
    return render_template('index.html', posts=filtered_posts, current_label=label_name)


if __name__ == '__main__':
    app.run(debug=True)