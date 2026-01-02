import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Load the trained model
MODEL_PATH = 'models/bank.pkl'
with open(MODEL_PATH, 'rb') as file:
    model = pickle.load(file)

# Feature names and categories
FEATURES_INFO = {
    'categorical': {
        'job': ['admin.', 'blue-collar', 'entrepreneur', 'housemaid', 
                'management', 'retired', 'self-employed', 'services', 
                'student', 'technician', 'unemployed', 'unknown'],
        'marital': ['married', 'single', 'divorced'],
        'education': ['primary', 'secondary', 'tertiary', 'unknown'],
        'default': ['no', 'yes'],
        'housing': ['no', 'yes'],
        'loan': ['no', 'yes'],
        'contact': ['cellular', 'telephone', 'unknown'],
        'month': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                  'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
        'poutcome': ['failure', 'success', 'unknown', 'other']
    },
    'numerical': {
        'age': {'min': 18, 'max': 95, 'default': 30},
        'balance': {'min': -10000, 'max': 150000, 'default': 0},
        'day': {'min': 1, 'max': 31, 'default': 15},
        'duration': {'min': 0, 'max': 5000, 'default': 300},
        'campaign': {'min': 1, 'max': 50, 'default': 3},
        'pdays': {'min': -1, 'max': 900, 'default': -1},
        'previous': {'min': 0, 'max': 50, 'default': 0}
    }
}

def create_prediction_plots(prediction_proba):
    """Create visualization plots for predictions"""
    
    # Probability gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction_proba[1] * 100,
        title={'text': "Conversion Probability"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': prediction_proba[1] * 100
            }
        }
    ))
    
    fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    
    # Probability bar chart
    fig_bar = go.Figure(data=[
        go.Bar(
            x=['Will Not Subscribe', 'Will Subscribe'],
            y=[prediction_proba[0] * 100, prediction_proba[1] * 100],
            marker_color=['#FF6B6B', '#4ECDC4'],
            text=[f'{prediction_proba[0]*100:.1f}%', f'{prediction_proba[1]*100:.1f}%'],
            textposition='auto',
        )
    ])
    
    fig_bar.update_layout(
        title="Prediction Confidence",
        xaxis_title="Outcome",
        yaxis_title="Probability (%)",
        height=300,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig_gauge, fig_bar

@app.route('/')
def index():
    """Home page with interactive dashboard"""
    # Pass the features information to the template
    return render_template('index.html', features=FEATURES_INFO)

@app.route('/predict', methods=['GET'])
def predict_form():
    """Display prediction form"""
    return render_template('predict.html', features=FEATURES_INFO)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        # Get form data
        input_data = {}
        for feature in FEATURES_INFO['categorical']:
            input_data[feature] = request.form.get(feature, '')
        
        for feature in FEATURES_INFO['numerical']:
            try:
                input_data[feature] = float(request.form.get(feature, 0))
            except:
                input_data[feature] = FEATURES_INFO['numerical'][feature]['default']
        
        # Create DataFrame
        df_input = pd.DataFrame([input_data])
        
        # Make prediction
        prediction = model.predict(df_input)[0]
        prediction_proba = model.predict_proba(df_input)[0]
        
        # Create visualizations
        fig_gauge, fig_bar = create_prediction_plots(prediction_proba)
        
        # Store in session for results page
        session['prediction'] = int(prediction)
        session['probability'] = float(prediction_proba[1])
        session['confidence'] = max(prediction_proba) * 100
        session['input_data'] = input_data
        
        # Convert plots to JSON
        graphJSON_gauge = json.dumps(fig_gauge, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON_bar = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
        
        return render_template('results.html',
                             prediction=prediction,
                             probability=prediction_proba[1] * 100,
                             confidence=max(prediction_proba) * 100,
                             graphJSON_gauge=graphJSON_gauge,
                             graphJSON_bar=graphJSON_bar)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    # Sample analytics data (replace with actual data)
    analytics_data = {
        'total_predictions': 1500,
        'positive_rate': 32.5,
        'avg_confidence': 78.3,
        'top_job': 'management',
        'most_contacted_month': 'may'
    }
    
    # Create sample charts
    monthly_data = {
        'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'predictions': [120, 145, 210, 180, 250, 195],
        'conversions': [35, 42, 68, 54, 85, 62]
    }
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly_data['months'],
        y=monthly_data['predictions'],
        mode='lines+markers',
        name='Total Predictions',
        line=dict(color='#4ECDC4', width=3)
    ))
    fig_trend.add_trace(go.Bar(
        x=monthly_data['months'],
        y=monthly_data['conversions'],
        name='Conversions',
        marker_color='#FF6B6B'
    ))
    
    fig_trend.update_layout(
        title='Monthly Prediction Trends',
        xaxis_title='Month',
        yaxis_title='Count',
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    graphJSON_trend = json.dumps(fig_trend, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('dashboard.html',
                         analytics=analytics_data,
                         graphJSON_trend=graphJSON_trend)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        df_input = pd.DataFrame([data])
        prediction = model.predict(df_input)[0]
        prediction_proba = model.predict_proba(df_input)[0]
        
        return jsonify({
            'prediction': int(prediction),
            'probability': float(prediction_proba[1]),
            'confidence': float(max(prediction_proba)),
            'message': 'Will subscribe' if prediction == 1 else 'Will not subscribe'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)