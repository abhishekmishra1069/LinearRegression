# MLR (Multilinear Regression) - Setup and Deployment Guide

## Prerequisites
- Docker or Podman installed on your system
- Python 3.10 or higher (for local testing)
- Git (optional, for version control)

**Note:** All Docker commands can be replaced with Podman by substituting `docker` with `podman`. Podman works identically to Docker for this project.

---

## Step 1: Train the Model

Before containerizing the application, train the model using the Jupyter Notebook.

### Steps:
1. Open `Train_and_save.ipynb` in Jupyter Notebook or VS Code
2. Run all cells in sequence:
   - Cell 1: Import required libraries
   - Cell 2: Load California housing dataset
   - Cell 3: Separate features and target
   - Cell 4: Split data into train/test sets
   - Cell 5: Train the Linear Regression model
   - Cell 6: Make predictions on test set
   - Cell 7: Evaluate model accuracy
   - Cell 8: Save the trained model as `linear_regression_model.pkl`

3. Verify that `linear_regression_model.pkl` is created in the MLR directory

### Command to run:
```bash
jupyter notebook Train_and_save.ipynb
```

---

## Step 2: Prepare Local Environment (Optional - for local testing)

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the Flask app locally:
```bash
python app.py
```

The server will start at `http://127.0.0.1:5000`

### Test the API:
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
         "data": [{
             "MedInc": 8.3252,
             "HouseAge": 41.0,
             "AveRooms": 6.984127,
             "AveBedrms": 1.0238095,
             "Population": 322.0,
             "AveOccup": 2.555556,
             "Latitude": 37.88,
             "Longitude": -122.23
         }]
     }'
```

Expected response:
```json
{
  "features": [8.3252, 41.0, 6.984127, 1.0238095, 322.0, 2.555556, 37.88, -122.23],
  "PredictedPrice": 4.5362
}
```

---

## Step 3: Build Docker Container

### Update ContainerFile if needed:
Ensure `ContainerFile` contains:
```dockerfile
FROM python:3.10-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY linear_regression_model.pkl .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Build the Docker image:
```bash
docker build -f ContainerFile -t mlr-model:latest .
```

### Build with Podman (alternative):
```bash
podman build -f ContainerFile -t mlr-model:latest .
```

### Verify the image was created:

**Docker:**
```bash
docker images | grep mlr-model
```

**Podman:**
```bash
podman images | grep mlr-model
```

---

## Step 4: Run Docker Container

### Run the container:

**Docker:**
```bash
docker run -p 5000:5000 mlr-model:latest
```

**Podman:**
```bash
podman run -p 5000:5000 mlr-model:latest
```

The application will be accessible at `http://localhost:5000`

### Run container in background:

**Docker:**
```bash
docker run -d -p 5000:5000 --name mlr-app mlr-model:latest
```

**Podman:**
```bash
podman run -d -p 5000:5000 --name mlr-app mlr-model:latest
```

### Stop the container:

**Docker:**
```bash
docker stop mlr-app
```

**Podman:**
```bash
podman stop mlr-app
```

### View container logs:

**Docker:**
```bash
docker logs mlr-app
```

**Podman:**
```bash
podman logs mlr-app
```

---

## Step 5: Test the Containerized Application

### Test with curl:
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
         "features": [8.3252, 41.0, 6.984127, 1.0238095, 322.0, 2.555556, 37.88, -122.23]
     }'
```

### Alternative format (nested data):
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
         "data": [{
             "MedInc": 8.3252,
             "HouseAge": 41.0,
             "AveRooms": 6.984127,
             "AveBedrms": 1.0238095,
             "Population": 322.0,
             "AveOccup": 2.555556,
             "Latitude": 37.88,
             "Longitude": -122.23
         }]
     }'
```

---

## Accepted API Input Formats

The `/predict` endpoint accepts three input formats:

### Format 1: Array Format
```json
{
  "features": [8.3252, 41.0, 6.984127, 1.0238095, 322.0, 2.555556, 37.88, -122.23]
}
```

### Format 2: Object Format (Named Keys)
```json
{
  "MedInc": 8.3252,
  "HouseAge": 41.0,
  "AveRooms": 6.984127,
  "AveBedrms": 1.0238095,
  "Population": 322.0,
  "AveOccup": 2.555556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

### Format 3: Nested Data Format
```json
{
  "data": [{
    "MedInc": 8.3252,
    "HouseAge": 41.0,
    "AveRooms": 6.984127,
    "AveBedrms": 1.0238095,
    "Population": 322.0,
    "AveOccup": 2.555556,
    "Latitude": 37.88,
    "Longitude": -122.23
  }]
}
```

---

## Feature Order for California Housing Dataset

The 8 features must be provided in this exact order:
1. **MedInc** - Median income in block group (in units of $100,000)
2. **HouseAge** - Median house age in block group
3. **AveRooms** - Average number of rooms per household
4. **AveBedrms** - Average number of bedrooms per household
5. **Population** - Block group population
6. **AveOccup** - Average occupancy (persons per household)
7. **Latitude** - Geographic latitude of block group
8. **Longitude** - Geographic longitude of block group

---

## Common Failures and Solutions

### Failure 1: ModuleNotFoundError: No module named 'sklearn'

**Error:**
```
ModuleNotFoundError: No module named 'sklearn.datasets'
```

**Solutions:**
1. **For pip users:**
   ```bash
   pip install scikit-learn
   ```

2. **For conda users:**
   ```bash
   conda install -c conda-forge scikit-learn
   ```

3. **For Docker:** Ensure `requirements.txt` includes `scikit-learn` and rebuild the image:
   ```bash
   docker build -f ContainerFile -t mlr-model:latest .
   ```

---

### Failure 2: FileNotFoundError: linear_regression_model.pkl not found

**Error:**
```
Error: linear_regression_model.pkl not found. Ensure Train_and_save.ipynb was run to generate the model.
```

**Solutions:**
1. **Ensure model is trained:**
   - Run all cells in `Train_and_save.ipynb`
   - Verify `linear_regression_model.pkl` exists in the MLR directory

2. **Fix file path in app.py:**
   - If running from different directory, use absolute path
   - Current path expects the script to run from MLR directory

3. **For Docker:** Ensure model file is copied:
   ```dockerfile
   COPY linear_regression_model.pkl .
   ```

---

### Failure 3: Missing required feature: 'MedInc'

**Error:**
```json
{
  "error": "Missing required feature: 'MedInc'"
}
```

**Solutions:**
1. **Check JSON format:** Ensure all 8 features are provided
2. **Verify feature names:** Use exact names (case-sensitive):
   - MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude
3. **Use array format if unsure:**
   ```json
   {
     "features": [8.3252, 41.0, 6.984127, 1.0238095, 322.0, 2.555556, 37.88, -122.23]
   }
   ```

---

### Failure 4: Port 5000 already in use

**Error:**
```
Address already in use
```

**Solutions:**
1. **Find process using port 5000:**
   ```bash
   lsof -i :5000
   ```

2. **Kill the process:**
   ```bash
   kill -9 <PID>
   ```

3. **Use a different port:**

   **Docker:**
   ```bash
   docker run -p 5001:5000 mlr-model:latest
   ```

   **Podman:**
   ```bash
   podman run -p 5001:5000 mlr-model:latest
   ```

   Then access at `http://localhost:5001`

---

### Failure 5: Docker build fails with "No such file or directory"

**Error:**
```
COPY requirements.txt: no such file or directory
```

**Solutions:**
1. **Ensure you're in the correct directory:**
   ```bash
   cd /Users/abhishekmishra/Development/ML/LinearRegression/MLR
   ```

2. **Verify all required files exist:**
   ```bash
   ls -la
   # Should show: app.py, ContainerFile, requirements.txt, linear_regression_model.pkl
   ```

3. **Check ContainerFile name:** Docker/Podman expects `Dockerfile` or specify with `-f`:

   **Docker:**
   ```bash
   docker build -f ContainerFile -t mlr-model:latest .
   ```

   **Podman:**
   ```bash
   podman build -f ContainerFile -t mlr-model:latest .
   ```

---

### Failure 6: Invalid input format or prediction error

**Error:**
```json
{
  "error": "Invalid input format or prediction error: ..."
}
```

**Solutions:**
1. **Verify JSON is valid:** Use JSON validator
2. **Check all 8 features are numeric**
3. **Ensure no extra fields** beyond the 8 features
4. **Check request format matches one of the three accepted formats**

---

### Failure 7: Connection refused

**Error:**
```
curl: (7) Failed to connect to localhost port 5000: Connection refused
```

**Solutions:**
1. **Verify Flask app is running:**
   ```bash
   python app.py
   ```

2. **Verify container is running:**

   **Docker:**
   ```bash
   docker ps
   ```

   **Podman:**
   ```bash
   podman ps
   ```

3. **Check if mapped port is correct:**
   - If started with `-p 5001:5000`, use `localhost:5001` not `localhost:5000`

4. **Allow container to start:**
   - Wait 2-3 seconds after running container before testing

---

### Failure 8: Conda install fails with conflicting dependencies

**Error:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed with conda
```

**Solutions:**
1. **Use pip with compatible versions:**
   ```bash
   pip install numpy==1.24.3 pandas==2.0.3 scikit-learn==1.3.0 Flask==2.3.2
   ```

2. **Create fresh conda environment:**
   ```bash
   conda create -n mlr-env python=3.10
   conda activate mlr-env
   pip install -r requirements.txt
   ```

3. **For Docker/Podman:** The image installation handles this automatically

---

## Quick Reference Commands

### Training Model
```bash
jupyter notebook Train_and_save.ipynb
```

### Local Testing
```bash
python app.py
```

### Docker Build
```bash
docker build -f ContainerFile -t mlr-model:latest .
```

### Docker Run
```bash
docker run -p 5000:5000 mlr-model:latest
```

### Podman Build
```bash
podman build -f ContainerFile -t mlr-model:latest .
```

### Podman Run
```bash
podman run -p 5000:5000 mlr-model:latest
```

### Test API
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [8.3252, 41.0, 6.984127, 1.0238095, 322.0, 2.555556, 37.88, -122.23]}'
```

### Check Docker Logs
```bash
docker logs <container-id>
```

### Check Podman Logs
```bash
podman logs <container-id>
```

### Remove Old Docker Images
```bash
docker rmi mlr-model:latest
```

### Remove Old Podman Images
```bash
podman rmi mlr-model:latest
```

### List Running Containers (Docker)
```bash
docker ps
```

### List Running Containers (Podman)
```bash
podman ps
```

### Stop Container (Docker)
```bash
docker stop mlr-app
```

### Stop Container (Podman)
```bash
podman stop mlr-app
```

---

## File Structure

```
MLR/
├── app.py                          # Flask application
├── Train_and_save.ipynb            # Model training notebook
├── linear_regression_model.pkl     # Trained model (generated after training)
├── ContainerFile                   # Docker configuration
├── requirements.txt                # Python dependencies
└── steps.md                        # This file
```

---

## Support

For issues, check the **Common Failures and Solutions** section above or review:
- `app.py` for API logic
- `ContainerFile` for Docker configuration
- `requirements.txt` for dependency versions
