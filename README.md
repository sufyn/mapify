
# Mapify Web App

Welcome to **Mapify**!

Mapify is a web application that allows users to securely log in, register, and manage their profiles while leveraging OpenCV for image processing. It integrates MySQL for user authentication and features functionalities like uploading images and applying computer vision techniques.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL (MySQLdb)
- **Image Processing**: OpenCV
- **Authentication**: User login system with secure password hashing

## Features

- **User Authentication**: Register and login with username, password, and email.
- **Image Upload**: Upload images for processing.
- **Image Processing**: Apply computer vision techniques like contour detection, Hough transform, and line segment detection.
- **User Profile**: View and edit user profile information.
- **Security**: Secure user login with hashed passwords.

## Planned Enhancements

- **AI for Image Processing**: Future improvements could include AI-based image analysis techniques to automate detection and recognition.
- **Personalized User Experience**: We aim to offer machine learning-based recommendations to improve user interactions and image processing results.

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- OpenCV
- MySQL server

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/mapify.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the database:
    - Create a MySQL database and configure your `MySQL` connection in the `app.config` section.
    - Use the provided SQL schema or create your own tables for users and images.

4. Run the application:
    ```bash
    python app.py
    ```

5. Visit the app in your browser at:
    ```
    http://localhost:5000
    ```

### Configuration

- **Database Configuration**: Edit the `app.config['MYSQL_*']` values with your MySQL credentials in the `app.py` file.
- **Image Upload Directory**: Set your preferred location for saving images in the `upload()` function.

## Routes

- `/mapify/`: Login page
- `/mapify/logout`: Logout page
- `/mapify/register`: User registration page
- `/mapify/home`: Home page for logged-in users
- `/mapify/profile`: Profile page for logged-in users
- `/upload`: Page for uploading images
- `/output/<filename>`: Page to display processed images

## Contributing

We welcome contributions to Mapify! If you have any suggestions or improvements, feel free to fork the repository and create a pull request.

## License

Mapify is licensed under the MIT License.
