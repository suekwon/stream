
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Simple Bulletin Board", layout="wide")

# Initialize session state for posts and post ID counter
if 'posts' not in st.session_state:
    st.session_state.posts = []
if 'post_id_counter' not in st.session_state:
    st.session_state.post_id_counter = 0

# --- Functions for CRUD Operations ---
def create_post(title, content):
    """Adds a new post to the session state."""
    st.session_state.post_id_counter += 1
    new_post = {"id": st.session_state.post_id_counter, "title": title, "content": content}
    st.session_state.posts.append(new_post)
    st.success("Post created successfully!")

def read_posts():
    """Displays all posts."""
    if not st.session_state.posts:
        st.info("No posts yet. Create one!")
        return

    # Sort posts by ID in descending order to show newest first
    sorted_posts = sorted(st.session_state.posts, key=lambda x: x['id'], reverse=True)

    for post in sorted_posts:
        with st.expander(f"#{post['id']} - {post['title']}"):
            st.write(post['content'])

def update_post(post_id, new_title, new_content):
    """Updates an existing post."""
    for post in st.session_state.posts:
        if post['id'] == post_id:
            post['title'] = new_title
            post['content'] = new_content
            st.success("Post updated successfully!")
            return
    st.error("Post not found.")

def delete_post(post_id):
    """Deletes a post."""
    post_to_delete = None
    for post in st.session_state.posts:
        if post['id'] == post_id:
            post_to_delete = post
            break
    if post_to_delete:
        st.session_state.posts.remove(post_to_delete)
        st.success("Post deleted successfully!")
    else:
        st.error("Post not found.")

# --- Streamlit UI ---
st.title("📝 Simple Bulletin Board")

# Sidebar for other actions
st.sidebar.title("Actions")
choice = st.sidebar.selectbox("Menu", ["Update", "Delete"])

# Main layout with two columns
col1, col2 = st.columns(2)

# Column 1: Create Post
with col1:
    st.header("✍️ Create a New Post")
    with st.form("create_form", clear_on_submit=True):
        post_title = st.text_input("Title")
        post_content = st.text_area("Content")
        submit_button = st.form_submit_button(label="Submit Post")

        if submit_button:
            if post_title and post_content:
                create_post(post_title, post_content)
            else:
                st.warning("Please fill in both title and content.")

# Column 2: Read Posts
with col2:
    st.header("📚 View All Posts")
    read_posts()

# --- Handlers for Update and Delete from Sidebar ---
if choice == "Update":
    st.header("🔄 Update a Post")
    if not st.session_state.posts:
        st.info("No posts to update.")
    else:
        post_ids = [post['id'] for post in st.session_state.posts]
        selected_id = st.selectbox("Select Post to Update by ID", post_ids)

        if selected_id:
            selected_post = next((post for post in st.session_state.posts if post['id'] == selected_id), None)
            if selected_post:
                with st.form("update_form"):
                    new_title = st.text_input("New Title", value=selected_post['title'])
                    new_content = st.text_area("New Content", value=selected_post['content'])
                    update_button = st.form_submit_button(label="Update Post")

                    if update_button:
                        if new_title and new_content:
                            update_post(selected_id, new_title, new_content)
                        else:
                            st.warning("Please fill in both title and content.")

elif choice == "Delete":
    st.header("🗑️ Delete a Post")
    if not st.session_state.posts:
        st.info("No posts to delete.")
    else:
        post_ids = [post['id'] for post in st.session_state.posts]
        selected_id_to_delete = st.selectbox("Select Post to Delete by ID", post_ids)

        if selected_id_to_delete:
            # Confirmation button to prevent accidental deletion
            if st.button(f"Confirm Delete Post #{selected_id_to_delete}"):
                delete_post(selected_id_to_delete)
