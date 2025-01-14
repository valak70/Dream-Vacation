# Dream Vacation App

The **Dream Vacation App** is a web application where users can create, share, and explore dream vacation ideas. Users can comment on and upvote vacations, search by title, and browse vacations based on categories.

---

## Features

1. **Home Page**
   - Displays top-voted vacations and a categorized list of vacations.
   - Each category shows 3-4 vacations with a "See All" button to explore more.

2. **Search Functionality**
   - Users can search for vacations by title.
   - Results are displayed dynamically, with a message when no results are found.
   - Includes a debounce function to delay search execution and optimize performance.
   - Displays search results dynamically without page reload.

3. **Create Dream Vacation**
   - Users can add new vacations by providing details such as title, description, category, and an image.

4. **Vacation Details**
   - View detailed information about a vacation, including its description, image, and comments.
   - Add comments to interact with vacations.

5. **Category Pages**
   - Explore vacations within a specific category, sorted by user interactions.

6. **Authentication**
   - Users are redirected to the home page upon successful login.

7. **Popup for Adding to Favorites**
   - Users can mark a dream vacation as a favorite through a visually engaging popup.
   - The popup includes a confirmation message and two buttons: "Confirm" and "Cancel."
   - The popup closes dynamically upon user interaction.

8. **Dark and Light Mode**
   - Users can toggle between dark and light themes for better usability.
   - A toggle button is available in the navbar for switching modes.
   - User preferences are saved and persist across sessions.

9. **Dropdown in Navbar**
   - Enhances navigation with an intuitive dropdown menu.
   - A dropdown is available under the "Categories" link in the navbar.
   - Ensures the dropdown is accessible and responsive.

---

## Tech Stack

### Backend
- **Django**: For server-side processing and handling requests.
- **SQLite**: Default database for development.

### Frontend
- **HTML/CSS**: For building responsive and visually appealing pages.
- **Django Templates**: Used for rendering dynamic content.

### Media Handling
- **Django File Storage**: For managing user-uploaded vacation images.

---

## Installation

### Prerequisites
1. Python 3.9+
2. Virtual environment (optional but recommended)
3. Django 5.1.4

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dream-vacation.git
   cd dream-vacation
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

6. Test the application locally:
   ```bash
   python manage.py runserver
   ```

7. Open the application in your browser:
   ```
   http://127.0.0.1:8000
   ```


## Usage

1. **Home Page**:
   - View top vacations and explore categories.

2. **Category Page**:
   - Explore vacations by category.

3. **Search**:
   - Use the search bar to find vacations by title.

4. **Create Vacation**:
   - Log in and navigate to the "Create" page to add a new vacation.

5. **Vacation Details**:
   - Click on a vacation to view more details and add comments.

6. **Favorites**:
   - Mark vacations as favorites using the popup confirmation.

7. **Theme Toggle**:
   - Switch between dark and light modes using the toggle button in the navbar.

8. **Navigation**:
   - Use the dropdown menu under "Categories" for easy navigation.

---

## Future Enhancements

1. Add user profiles with saved vacations.
2. Enhance search with advanced filters.
3. Add email notifications for vacation updates.
4. Use a cloud storage service for image uploads.

---

## Contributors
- **Aryan Agrahari**: Developer





