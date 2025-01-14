document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('click', function (event) {
        if (event.target.matches('.upvote-btn')) {
            const button = event.target;
            const commentId = button.getAttribute('data-id');
            const upvoteCountElem = document.getElementById(`upvote-count-${commentId}`);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Send the upvote request to the server
            fetch(`/comment/upvote/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update the upvote count
                        upvoteCountElem.textContent = data.upvotes;

                        // Toggle the upvoted class and update button text
                        if (data.status === 'added') {
                            button.classList.add('upvoted');
                            
                        } else {
                            button.classList.remove('upvoted');
                            
                        }
                    } else {
                        alert(data.message || 'Error toggling upvote.');
                    }
                })
                .catch(error => console.error('Error:', error));

            // Prevent default button action
            event.preventDefault();
        }
    });
});


document.getElementById('comment-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting the traditional way
    const form = e.target;
    const text = document.getElementById('comment-text').value;
    const vacationId = form.dataset.vacationId; // Get the vacation ID from the form's data attribute
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/comment/add/${vacationId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ text: text }), // Send the comment text
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const commentSection = document.getElementById('comments-section');
            const comment = data.comment;
            commentSection.innerHTML += `
                <div class="comment" id="comment-${comment.id}">
                    <p class="comment-username">${comment.username}</p>
                    <p class="comment-text">${comment.text}</p>
                    <div class="comment-actions">
                        <button class="upvote-btn" data-id="${comment.id}">↑</button>
                        <span class="upvote-count" id="upvote-count-${comment.id}">${comment.upvotes}</span>
                    </div>
                </div>`;
            document.getElementById('comment-text').value = ''; // Clear the comment input field
        } else {
            alert(data.message || 'Error adding comment.');
        }
    });
});


function scrollToLeft() {
    const container = document.querySelector('.category-container');
    container.scrollLeft -= 300; // Adjust the scroll amount as needed
}

function scrollToRight() {
    const container = document.querySelector('.category-container');
    container.scrollLeft += 300; // Adjust the scroll amount as needed
}

document.addEventListener('DOMContentLoaded', () => {
    const favoriteIcon = document.querySelector('.favorite-icon');
    const popup = document.getElementById('favorite-popup');
    const confirmBtn = document.getElementById('confirm-btn');
    const cancelBtn = document.getElementById('cancel-btn');

    // Show popup on clicking the favorite icon
    favoriteIcon.addEventListener('click', () => {
        popup.classList.remove('hidden');
    });

    // Handle confirm button
    confirmBtn.addEventListener('click', () => {
        const vacationId = favoriteIcon.dataset.id;

        // Send AJAX request to add to favorites
        fetch(`/toggle-favorite/${vacationId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'added') {
                favoriteIcon.querySelector('img').src = '/favorited.png';
                alert('Added to favorites!');
            } else if (data.status === 'removed') {
                favoriteIcon.querySelector('img').src = '/favorite.png';
                alert('Removed from favorites!');
            }
        })
        .catch(error => console.error('Error:', error));

        // Close the popup
        popup.classList.add('hidden');
    });

    // Handle cancel button
    cancelBtn.addEventListener('click', () => {
        popup.classList.add('hidden');
    });
});


