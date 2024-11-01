document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('[id^="like-btn-"]'); // Select all like buttons

    likeButtons.forEach(function (likeBtn) {
        likeBtn.addEventListener('click', function () {
            const postId = likeBtn.id.split('-')[2]; // Get post ID from button ID
            const csrfToken = document.querySelector(`#like-form-${postId} input[type="hidden"]`).value; // Get CSRF token
            const url = `/likepost/${postId}/`; // Adjust the URL according to your URL configuration

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                const likeCount = document.getElementById(`like-count-${postId}`);
                likeCount.textContent = data.total_likes; // Update the like count
                likeBtn.setAttribute('data-liked', data.liked ? 'true' : 'false'); // Update the data attribute
                likeBtn.textContent = data.liked ? 'Unlike 🤍' : 'Like 🤍'; // Update the button text
            })
            .catch(error => {
                console.error('Error:', error); // Log any errors for debugging
            });
        });
    });
});
// document.addEventListener('DOMContentLoaded', function() {
//     const likeBtn = document.getElementById('like-btn');

//     likeBtn.addEventListener('click', function() {
//         const postId = "{{ post.id }}";
//         const isLiked = likeBtn.getAttribute('data-liked') === 'true';

//         // Change button text based on current state
//         if (isLiked) {
//             likeBtn.textContent = 'Like'; // Change text to "Like" if it was "Unlike"
//         } else {
//             likeBtn.textContent = 'Unlike'; // Change text to "Unlike" if it was "Like"
//         }

//         // Toggle the data-liked attribute
//         likeBtn.setAttribute('data-liked', !isLiked);
        
//         // Your existing AJAX logic to update the server can go here...
//     });
// });
