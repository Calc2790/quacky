avascript
// Get the post container element
const postContainer = document.getElementById('post-container');

// Function to create a new post element
function createPost(post) {
const postElement = document.createElement('div');
postElement.innerHTML = 
<h3>${post.username}</h3>
<p>${post.content}</p>
<button>Like</button>
<button>Comment</button>
;
postContainer.appendChild(postElement);
}

// Function to update the feed section
function updateFeed() {
// Get the current user's posts from the API
fetch('/api/posts')
.then(response => response.json())
.then(posts => {
// Clear the post container
postContainer.innerHTML = '';

// Create a new post element for each post
posts.forEach(post => createPost(post));
});
}

// Add an event listener to the like button
document.addEventListener('DOMContentLoaded', () => {
updateFeed();

// Add an event listener to the like button
document.querySelector('#post-container button').addEventListener('click', () => {
// Send a request to the API to like the post
fetch('/api/posts/like', {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify({
post_id: post.id
})
})
.then(response => response.json())
.then(data => console.log(data));
});
});
