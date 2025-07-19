from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from uvicorn import run as app_run
from typing import Optional

from Telecom_churn_prediction.constants import APP_HOST, APP_PORT
from Telecom_churn_prediction.pipeline.prediction_pipeline import TelcoChurnData, TelcoChurnClassifier
from Telecom_churn_prediction.pipeline.training_pipeline import TrainPipeline

app = FastAPI()

# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory='templates')

# Allow CORS from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper class to extract form data
class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.gender: Optional[str] = None
        self.SeniorCitizen: Optional[int] = None
        self.Partner: Optional[str] = None
        self.Dependents: Optional[str] = None
        self.Tenure: Optional[int] = None
        self.PhoneService: Optional[str] = None
        self.MultipleLines: Optional[str] = None
        self.InternetService: Optional[str] = None
        self.OnlineSecurity: Optional[str] = None
        self.OnlineBackup: Optional[str] = None
        self.DeviceProtection: Optional[str] = None
        self.TechSupport: Optional[str] = None
        self.StreamingTV: Optional[str] = None
        self.StreamingMovies: Optional[str] = None
        self.Contract: Optional[str] = None
        self.PaperlessBilling: Optional[str] = None
        self.PaymentMethod: Optional[str] = None
        self.MonthlyCharges: Optional[float] = None
        self.TotalCharges: Optional[float] = None

    async def get_telco_data(self):
        form = await self.request.form()
        self.gender = form.get("gender")
        self.SeniorCitizen = form.get("SeniorCitizen")
        self.Partner = form.get("Partner")
        self.Dependents = form.get("Dependents")
        self.Tenure = form.get("Tenure")
        self.PhoneService = form.get("PhoneService")
        self.MultipleLines = form.get("MultipleLines")
        self.InternetService = form.get("InternetService")
        self.OnlineSecurity = form.get("OnlineSecurity")
        self.OnlineBackup = form.get("OnlineBackup")
        self.DeviceProtection = form.get("DeviceProtection")
        self.TechSupport = form.get("TechSupport")
        self.StreamingTV = form.get("StreamingTV")
        self.StreamingMovies = form.get("StreamingMovies")
        self.Contract = form.get("Contract")
        self.PaperlessBilling = form.get("PaperlessBilling")
        self.PaymentMethod = form.get("PaymentMethod")
        self.MonthlyCharges = form.get("MonthlyCharges")
        self.TotalCharges = form.get("TotalCharges")

# Homepage route - show form
@app.get("/", tags=["Home"])
async def index(request: Request):
    return templates.TemplateResponse(
        "telco_churn.html", {"request": request, "context": "Rendering"}
    )

# Trigger training pipeline
@app.get("/train", tags=["Train"])
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

# Handle form submission and return prediction
@app.post("/", tags=["Predict"])
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_telco_data()

        telco_data = TelcoChurnData(
            gender=form.gender,
            SeniorCitizen=form.SeniorCitizen,
            Partner=form.Partner,
            Dependents=form.Dependents,
            tenure=form.Tenure,
            PhoneService=form.PhoneService,
            MultipleLines=form.MultipleLines,
            InternetService=form.InternetService,
            OnlineSecurity=form.OnlineSecurity,
            OnlineBackup=form.OnlineBackup,
            DeviceProtection=form.DeviceProtection,
            TechSupport=form.TechSupport,
            StreamingTV=form.StreamingTV,
            StreamingMovies=form.StreamingMovies,
            Contract=form.Contract,
            PaperlessBilling=form.PaperlessBilling,
            PaymentMethod=form.PaymentMethod,
            MonthlyCharges=form.MonthlyCharges,
            TotalCharges=form.TotalCharges
        )

        telco_df = telco_data.get_telco_churn_input_data_frame()

        model_predictor = TelcoChurnClassifier()
        prediction = model_predictor.predict(dataframe=telco_df)[0]

        status = "Customer will Churn" if prediction == 1 else "Customer will Stay"

        return templates.TemplateResponse(
            "telco_churn.html",
            {"request": request, "context": status},
        )

    except Exception as e:
        return templates.TemplateResponse(
            "telco_churn.html",
            {"request": request, "context": f"Error: {e}"},
        )

# Run with: python main.py
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
