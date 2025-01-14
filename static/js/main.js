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

document.addEventListener("DOMContentLoaded", function () {
    const favoriteIcons = document.querySelectorAll(".favorite-icon");

    favoriteIcons.forEach((icon) => {
        icon.addEventListener("click", function () {
            const isFavorited = icon.dataset.favorited === "true"; // Check current state
            const vacationId = icon.dataset.id; // Vacation ID
            const action = isFavorited ? "Remove from Favorites" : "Add to Favorites";

            // Create and show the confirmation popup
            const popup = document.createElement("div");
            popup.className = "confirmation-popup";
            popup.innerHTML = `
                <div class="popup-content">
                    <p>Are you sure you want to ${action}?</p>
                    <button class="confirm-btn">Confirm</button>
                    <button class="cancel-btn">Cancel</button>
                </div>
            `;

            document.body.appendChild(popup);

            // Handle confirmation
            popup.querySelector(".confirm-btn").addEventListener("click", function () {
                toggleFavorite(vacationId, !isFavorited, icon);
                document.body.removeChild(popup); // Close popup
            });

            // Handle cancellation
            popup.querySelector(".cancel-btn").addEventListener("click", function () {
                document.body.removeChild(popup); // Close popup
            });
        });
    });
});

// Function to toggle favorite status
function toggleFavorite(vacationId, isFavorited, icon) {
    fetch(`/toggle-favorite/${vacationId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(), // Include CSRF token
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ favorited: isFavorited }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                // Update the icon state
                icon.dataset.favorited = isFavorited ? "true" : "false";
                icon.querySelector("img").src = isFavorited
                    ? "/static/favourited.png"
                    : "/static/favourite.png";
            } else {
                alert("Failed to update favorite status. Please try again.");
            }
        });
}

// Function to get CSRF token (helper)
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

