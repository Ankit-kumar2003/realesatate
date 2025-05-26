# Real Estate Website

A modern real estate website built with Flask, Tailwind CSS, and Bootstrap. This application allows users to browse, search, and list properties for sale or rent.

## Features

- User authentication (register, login, logout)
- Property listings with detailed information
- Property search and filtering
- Responsive design using Tailwind CSS and Bootstrap
- Property management (add, view properties)
- User dashboard

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd realestate
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

2. Run the development server:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
realestate/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── property_detail.html
│   └── add_property.html
└── static/           # Static files (CSS, JS, images)
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 