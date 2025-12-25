import os
from datetime import datetime
from flask import Flask, render_template, abort
import markdown

app = Flask(__name__)

# Configuration
BLOG_DIR = os.path.join(os.path.dirname(__file__), 'blog_posts')

# Sample data - customize these!
PROFILE = {
    'name': 'Shayne King',
    'title': 'Network DevOps Engineer',
    'bio': 'Welcome to my corner of the internet. I build things, break things, and write about both.',
    'email': 'sek3b@sek.run',
}

PROJECTS = [
    {
        'name': 'nuke-slack',
        'description': 'Delete all of your own messages from Slack workspaces with rate limiting and resume support',
        'tech': ['Python', 'Slack API'],
        'url': 'https://github.com/sek3b/nuke-slack',
        'status': 'active'
    },
    {
        'name': 'sek.run',
        'description': 'This personal website - a Flask app with a terminal aesthetic',
        'tech': ['Python', 'Flask', 'Jinja2'],
        'url': 'https://github.com/sek3b/sek.run',
        'status': 'active'
    },
    {
        'name': 'mac-kickstart',
        'description': 'macOS bootstrap script to automate setting up a new Mac with dev tools and apps',
        'tech': ['Bash', 'Homebrew'],
        'url': 'https://github.com/sek3b/mac-kickstart',
        'status': 'active'
    },
]

LINKS = [
    {'name': 'GitHub', 'url': 'https://github.com/sek3b', 'icon': 'github'},
    {'name': 'Twitter', 'url': 'https://twitter.com/sek3b', 'icon': 'twitter'},
    {'name': 'Email', 'url': 'mailto:sek3b@sek.run', 'icon': 'email'},
]

GAMES = [
    {
        'name': 'Pokémon Legends: Z-A',
        'platform': 'Nintendo Switch',
        'rating': '6/10',
        'completion': 100,
        'review': 'No voice acting, very easy difficulty, and can get very repetitive.',
        'status': 'completed'
    },
    {
        'name': 'Pokémon Legends: Z-A – Mega Dimension DLC',
        'platform': 'Nintendo Switch',
        'rating': '?/10',
        'completion': 50,
        'review': 'Still working on it.',
        'status': 'playing'
    },
]


def get_blog_posts():
    """Load blog posts from markdown files."""
    posts = []
    if not os.path.exists(BLOG_DIR):
        return posts

    for filename in os.listdir(BLOG_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(BLOG_DIR, filename)
            with open(filepath, 'r') as f:
                content = f.read()

            # Parse frontmatter (simple format: first lines starting with key: value)
            lines = content.split('\n')
            metadata = {}
            body_start = 0

            for i, line in enumerate(lines):
                if ':' in line and i < 10:  # Check first 10 lines for metadata
                    key, value = line.split(':', 1)
                    metadata[key.strip().lower()] = value.strip()
                    body_start = i + 1
                elif line.strip() == '---':
                    body_start = i + 1
                    break
                elif line.strip() and ':' not in line:
                    break

            body = '\n'.join(lines[body_start:])
            slug = filename.replace('.md', '')

            posts.append({
                'slug': slug,
                'title': metadata.get('title', slug.replace('-', ' ').title()),
                'date': metadata.get('date', 'Unknown'),
                'tags': [t.strip() for t in metadata.get('tags', '').split(',') if t.strip()],
                'body': body,
                'html': markdown.markdown(body, extensions=['fenced_code', 'codehilite', 'tables'])
            })

    # Sort by date, newest first
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts


@app.route('/')
def index():
    return render_template('index.html', profile=PROFILE, posts=get_blog_posts()[:3])


@app.route('/about')
def about():
    return render_template('about.html', profile=PROFILE)


@app.route('/projects')
def projects():
    return render_template('projects.html', projects=PROJECTS)


@app.route('/games')
def games():
    return render_template('games.html', games=GAMES)


@app.route('/blog')
def blog():
    return render_template('blog.html', posts=get_blog_posts())


@app.route('/blog/<slug>')
def blog_post(slug):
    posts = get_blog_posts()
    post = next((p for p in posts if p['slug'] == slug), None)
    if not post:
        abort(404)
    return render_template('post.html', post=post)


@app.route('/links')
def links():
    return render_template('links.html', links=LINKS, profile=PROFILE)


@app.context_processor
def inject_now():
    return {'now': datetime.now()}


if __name__ == '__main__':
    app.run(debug=True)
