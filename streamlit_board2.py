import streamlit as st
import json
import os
import datetime
import time
import pandas as pd
import numpy as np


# --- Configuration ---
POSTS_FILE = 'posts.json'
UPLOAD_DIR = 'uploads'

# --- Setup ---
# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Data Handling Functions ---
def load_posts():
    """Loads posts from the JSON file."""
    if not os.path.exists(POSTS_FILE):
        return []
    with open(POSTS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_posts(posts):
    """Saves posts to the JSON file."""
    with open(POSTS_FILE, 'w') as f:
        json.dump(posts, f, indent=4)

# --- UI Components ---
st.set_page_config(page_title="Image Bulletin Board", layout="centered")
st.title("📸 Image Bulletin Board")

data = pd.DataFrame(np.random.randn(10, 2), columns=['a', 'b']).plot.line()



# --- Create New Post (in sidebar) ---
st.sidebar.header("Create a New Post")
with st.sidebar.form("new_post_form", clear_on_submit=True):
    author = st.text_input("Your Name")
    title = st.text_input("Post Title")
    content = st.text_area("Content")
    uploaded_file = st.file_uploader("Upload an Image", type=['png', 'jpg', 'jpeg', 'gif'])
    submitted = st.form_submit_button("Submit")

    if submitted:
        if author and title and content:
            posts = load_posts()
            image_path = None

            # Handle file upload
            if uploaded_file is not None:
                # Create a unique filename and save the file
                unique_filename = f"{int(time.time())}_{uploaded_file.name}"
                image_path = os.path.join(UPLOAD_DIR, unique_filename)
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

            new_post = {
                "id": len(posts) + 1, # Simple ID generation
                "author": author,
                "title": title,
                "content": content,
                "timestamp": datetime.datetime.now().isoformat(),
                "image_path": image_path
            }
            posts.append(new_post)
            save_posts(posts)
            st.sidebar.success("Post created successfully!")
            st.rerun()
        else:
            st.sidebar.error("Please fill out all fields.")

# --- Display Posts (Main Area) ---
posts = load_posts()

if not posts:
    st.info("No posts yet. Create one using the form on the left!")
else:
    sorted_posts = sorted(posts, key=lambda x: x['timestamp'], reverse=True)

    for post in sorted_posts:
        with st.container(border=True):
            st.subheader(post['title'])
            st.caption(f"Posted by {post['author']} on {datetime.datetime.fromisoformat(post['timestamp']).strftime('%Y-%m-%d %H:%M')}")
            
            # Display image if it exists
            if post.get("image_path") and os.path.exists(post["image_path"]):
                st.image(post["image_path"])
            
            st.write(post['content'])

            # --- Update and Delete Buttons ---
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                if st.button("Edit", key=f"edit_{post['id']}"):
                    st.session_state.edit_post_id = post['id']
            with col2:
                if st.button("Delete", key=f"delete_{post['id']}"):
                    # Delete associated image file if it exists
                    if post.get("image_path") and os.path.exists(post["image_path"]):
                        os.remove(post["image_path"])
                    posts_after_deletion = [p for p in posts if p['id'] != post['id']]
                    save_posts(posts_after_deletion)
                    st.rerun()

            # --- Update Form (appears when 'Edit' is clicked) ---
            if 'edit_post_id' in st.session_state and st.session_state.edit_post_id == post['id']:
                with st.form(f"edit_form_{post['id']}"):
                    st.write("### Edit Post")
                    new_title = st.text_input("Title", value=post['title'])
                    new_content = st.text_area("Content", value=post['content'])
                    new_uploaded_file = st.file_uploader("Replace Image (optional)", type=['png', 'jpg', 'jpeg', 'gif'])

                    save_button, cancel_button = st.columns(2)
                    with save_button:
                        if st.form_submit_button("Save Changes"):
                            updated_post_ref = next((p for p in posts if p['id'] == post['id']), None)
                            if updated_post_ref:
                                updated_post_ref['title'] = new_title
                                updated_post_ref['content'] = new_content

                                # Handle image replacement
                                if new_uploaded_file is not None:
                                    # Delete old image if it exists
                                    if updated_post_ref.get("image_path") and os.path.exists(updated_post_ref["image_path"]):
                                        os.remove(updated_post_ref["image_path"])
                                    
                                    # Save new image
                                    unique_filename = f"{int(time.time())}_{new_uploaded_file.name}"
                                    new_image_path = os.path.join(UPLOAD_DIR, unique_filename)
                                    with open(new_image_path, "wb") as f:
                                        f.write(new_uploaded_file.getbuffer())
                                    updated_post_ref["image_path"] = new_image_path

                                save_posts(posts)
                                del st.session_state.edit_post_id
                                st.rerun()
                    with cancel_button:
                        if st.form_submit_button("Cancel"):
                            del st.session_state.edit_post_id
                            st.rerun()
        st.write("") # Add some space