# DataOps Project: Dashboard with Flask and Plotly

This project was created as part of the DataOps course at EDIT School. The main goal of the project was to explore Docker and the process of building APIs, with a secondary focus on data analytics. While I intended to perform more in-depth data exploration, my primary focus was on learning how to set up Docker containers and build interactive APIs. As a result, the data analytics portion is not as developed as originally planned.

## Features:
- **Landing Page**: Provides an introduction to the dashboard and options to explore the data.
- **Plot of Companies per Sector**: Displays a bar plot showing the number of companies per sector.
- **Data Table**: Displays the data in a tabular format.
- **Multiple Histograms**: Displays histograms for all numerical columns in the dataset.

## Requirements
Make sure you have the following dependencies installed:
- Python 3.10+
- Docker (for containerization)

You can install the required Python packages using the provided `requirements.txt` file:


## Running the Project using Docker:

1. **Clone the repository**:
```bash
git clone <repository_url> cd <repository_name>
```
2. **Build the Docker image**:
Ensure you have Docker installed. Open a terminal in the project directory and build the Docker image:
```bash
docker build -t flask-dashboard .
```
3. **Run the Docker container**:
Once the image is built, you can run the application inside a Docker container:
```bash
docker run -p 5000:5000 flask-dashboard
```

4. **Access the application**:
Open your web browser and go to `http://localhost:5000`. You will be greeted by the landing page with navigation options to explore the data.

## Project Structure:
- `app.py`: The main Flask application file.
- `Dockerfile`: Defines the Docker container setup and installation of dependencies.
- `requirements.txt`: Lists the required Python dependencies.
- `data/`: Directory containing the `dados_sensores_5000.parquet` file for the application.

## Acknowledgments:
This project was created as part of the **DataOps** course at **EDIT School**. A special thanks to the instructors Thiago Turini, Rodrigo moutinho and peers for their support throughout the course.

