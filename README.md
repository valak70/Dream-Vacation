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

3. **Create Dream Vacation**
   - Users can add new vacations by providing details such as title, description, category, and an image.

4. **Vacation Details**
   - View detailed information about a vacation, including its description, image, and comments.
   - Add comments to interact with vacations.

5. **Category Pages**
   - Explore vacations within a specific category, sorted by user interactions.

6. **Authentication**
   - Users are redirected to the home page upon successful login.

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
4. Railway CLI (for deployment)

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

### Deployment

1. Login to Railway and create a new project:
   ```bash
   railway login
   railway init
   ```

2. Add environment variables in Railway:
   - `DEBUG=False`
   - `SECRET_KEY=<your-secret-key>`
   - `ALLOWED_HOSTS=dream-vacation-production.up.railway.app`

3. Configure the database:
   ```bash
   railway run python manage.py migrate
   ```

4. Deploy the application:
   ```bash
   railway up
   ```

5. Access the live application at:
   ```
   https://dream-vacation-production.up.railway.app
   ```

---

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

---

## Future Enhancements

1. Add user profiles with saved vacations.
2. Enhance search with advanced filters.
3. Add email notifications for vacation updates.
4. Use a cloud storage service for image uploads.

---

## Contributors
- **Aryan Agrahari**: Developer

---

## Screenshots
![image](https://github.com/user-attachments/assets/dd6d154d-96b0-4f3b-88ee-ddf7346232fd)
![image](https://github.com/user-attachments/assets/9e1db226-8d53-4d3e-82b0-ff99748fcb17)
![image](https://github.com/user-attachments/assets/38f4a326-d720-4f37-91e7-bb9c66436f9d)
![image](https://github.com/user-attachments/assets/ae0429ff-87f0-46fd-b1fc-04ec80ce75c1)




