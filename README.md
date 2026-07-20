# AI Tutor for Personalized Student Learning Recommendations

An intelligent web application that provides personalized learning path recommendations for students based on their performance, learning style, strengths/weaknesses, and goals.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎯 Project Overview

This AI-powered educational tool helps students optimize their learning journey by:
- Analyzing current academic performance across multiple subjects
- Identifying weak areas that need focused attention
- Recommending a personalized sequence of learning modules
- Creating realistic study schedules based on available time
- Providing explainable AI reasoning for all recommendations

## 🤖 AI Methodology

### Hybrid Recommendation System

The application implements a **hybrid AI approach** combining:

1. **Content-Based Filtering**
   - Analyzes individual student's performance data
   - Identifies patterns in weak vs. strong subjects
   - Prioritizes modules based on current skill level
   - Matches difficulty to student capabilities

2. **Collaborative Filtering**
   - Uses K-Nearest Neighbors (KNN) algorithm from scikit-learn
   - Finds similar students based on performance profiles
   - Learns from successful learning paths of peers
   - Recommends subjects where similar students improved

3. **Rule-Based Scoring**
   - Ensures prerequisite coherence
   - Balances difficulty progression
   - Aligns with stated learning goals
   - Optimizes for available study time

## ✨ Features

### 1️⃣ Problem Setup Module
- **Multiple Input Methods**: Manual form, CSV upload, or sample data selection
- **Comprehensive Profile**: Captures performance, learning style, goals, and constraints
- **Input Validation**: Real-time validation with clear error messages

### 2️⃣ Core Logic Module
- **Hybrid AI Engine**: Combines content-based and collaborative filtering
- **Personalized Learning Paths**: Generates ordered sequence of modules
- **Adaptive Difficulty**: Matches module difficulty to student level
- **Time-Based Planning**: Creates realistic schedules based on availability

### 3️⃣ Visual UI Module
- **Interactive Dashboard**: Built with Streamlit for intuitive navigation
- **Performance Visualizations**:
  - Radar charts showing subject performance
  - Bar charts comparing scores to average
  - Timeline view of learning path
  - Pie charts for time distribution
  - Projection charts for expected improvement
- **Color-Coded Tables**: Priority subjects with status indicators
- **Responsive Design**: Clean, professional, and user-friendly

### 4️⃣ Explainability Module
- **Natural Language Explanations**: Why each subject/module was recommended
- **Key Factors Display**: Shows importance of each decision factor
- **Learning Style Alignment**: Explains how recommendations match learning preferences
- **Time Allocation Reasoning**: Justifies time distribution strategy

### 5️⃣ Evaluation Module
- **Multiple Performance Metrics**:
  - Relevance Score: How well recommendations match student needs
  - Weak Area Coverage: Comprehensiveness of weak subject addressing
  - Estimated Learning Time: Total hours required
  - Difficulty Balance: Distribution across beginner/intermediate/advanced
  - Prerequisite Coherence: Logical progression of modules
  - Overall Score: Weighted combination of all metrics
- **Approach Comparison**: Compare content-focused vs collaborative-focused strategies
- **Visual Comparisons**: Side-by-side metric charts

## 📁 Project Structure

```
ai_tutor_app/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── REPORT.md                       # Detailed project report
│
├── data/
│   └── student_profiles.csv        # Sample student dataset (20 profiles)
│
├── modules/
│   ├── data_processing.py          # Data loading and preprocessing
│   ├── recommendation_engine.py    # Core AI recommendation logic
│   ├── explainability.py           # Natural language explanations
│   ├── visualization.py            # Interactive charts and graphs
│   └── evaluation.py               # Performance metrics and comparison
│
└── screenshots/
    └── (placeholder for app screenshots)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd ai_tutor_app
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import streamlit; import pandas; import plotly; print('All dependencies installed successfully!')"
```

## 🎮 Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

The application will automatically open in your default web browser at `http://localhost:8501`

### Alternative: Specify Port
```bash
streamlit run app.py --server.port 8080
```

## 📖 How to Use

### 1. Problem Setup
1. Navigate to the **"Problem Setup"** page
2. Choose your input method:
   - **Manual Input**: Fill out the form with student information
   - **CSV Upload**: Upload a CSV file with student data
   - **Sample Student**: Select from 20 pre-loaded sample profiles
3. Click **Submit Profile**

### 2. Generate Recommendations
1. Go to **"Get Recommendations"** page
2. Adjust AI parameters (optional):
   - **Content-Based Weight**: Focus on own performance (0.0 - 1.0)
   - **Weak Subject Focus**: How much to prioritize weak areas (0.0 - 1.0)
   - **Goal Alignment Weight**: Importance of stated goals (0.0 - 1.0)
3. Click **Generate Recommendations**

### 3. View Results
1. Navigate to **"View Results"** page
2. Explore:
   - Performance analysis charts
   - Priority subjects table
   - Learning path timeline
   - Time distribution
   - Projected improvement
   - Detailed module breakdown
   - Daily and weekly schedules

### 4. Understand Reasoning
1. Go to **"Explainability"** page
2. Read explanations for:
   - Why specific subjects were prioritized
   - How learning style influenced recommendations
   - Key factors in decision-making
   - Time allocation strategy

### 5. Compare Approaches
1. Visit **"Compare Approaches"** page
2. Click **Generate Comparison**
3. Review:
   - Side-by-side metric comparison
   - Detailed evaluation reports
   - Winner recommendation

## 📊 Sample Data

The application includes 20 sample student profiles with diverse characteristics:
- **Education Levels**: High School, Undergraduate, Graduate
- **Learning Styles**: Visual, Auditory, Reading/Writing, Kinesthetic, Mixed
- **Performance Ranges**: Struggling (50-70%), Average (70-85%), Excellent (85-100%)
- **Varied Goals**: High GPA, skill improvement, exam preparation, research

### CSV Format for Custom Data

```csv
student_id,name,education_level,semester,age,math_score,physics_score,chemistry_score,programming_score,english_score,learning_style,study_hours_per_day,goal,weak_subjects,strong_subjects,interests
1,John Doe,Undergraduate,3,20,75,80,70,85,78,Visual,4.5,Improve programming skills,Math;Chemistry,Programming,Web Development
```

## 🔧 Customization

### Adding New Learning Modules
Edit `modules/recommendation_engine.py` and modify the `_define_learning_modules()` method to add subjects or modules.

### Adjusting Evaluation Metrics
Modify `modules/evaluation.py` to change metric calculations or add new evaluation criteria.

### Changing UI Theme
Edit the CSS in `app.py` under the `st.markdown()` custom styles section.

## 📈 Performance Metrics Explained

| Metric | Description | Range |
|--------|-------------|-------|
| **Relevance Score** | How well recommendations match student's current level and needs | 0.0 - 1.0 |
| **Weak Area Coverage** | Comprehensiveness in addressing weak subjects | 0.0 - 1.0 |
| **Estimated Time** | Total learning hours required | Hours |
| **Difficulty Balance** | Distribution across beginner/intermediate/advanced | 0.0 - 1.0 |
| **Prerequisite Coherence** | Logical progression respecting prerequisites | 0.0 - 1.0 |
| **Overall Score** | Weighted combination of all metrics | 0.0 - 1.0 |

## 🧪 Testing

### Test with Sample Data
1. Run the application
2. Go to Problem Setup → Use Sample Student
3. Select "Alice Johnson" or any other sample student
4. Generate recommendations with default parameters
5. Verify all visualizations display correctly

### Test Manual Input
1. Enter custom student data via manual form
2. Try edge cases (very low scores, very high scores)
3. Test validation (empty fields, invalid ranges)

### Test Comparison
1. Generate recommendations for a student
2. Go to Compare Approaches
3. Verify both approaches generate different results
4. Check that evaluation metrics are calculated

## 🐛 Troubleshooting

### Issue: Module not found error
**Solution**: Ensure you're in the correct directory and have activated the virtual environment.

### Issue: Port already in use
**Solution**: Specify a different port: `streamlit run app.py --server.port 8502`

### Issue: Data file not found
**Solution**: Verify `data/student_profiles.csv` exists in the correct location.

### Issue: Visualizations not displaying
**Solution**: Clear Streamlit cache: `streamlit cache clear`

## 🔮 Future Improvements

- **Export to PDF**: Download learning plans as PDF documents
- **Progress Tracking**: Log student progress over time and adjust recommendations
- **Resource Integration**: Link to actual learning resources (videos, books, courses)
- **Multi-Language Support**: Translate interface to multiple languages
- **Mobile Optimization**: Enhanced mobile-responsive design
- **Calendar Integration**: Sync study schedule with Google Calendar
- **Gamification**: Add badges, achievements, and progress tracking
- **Teacher Dashboard**: Interface for teachers to manage multiple students
- **Advanced ML Models**: Deep learning for more sophisticated patterns
- **A/B Testing**: Built-in experimentation framework for comparing strategies

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- **Project Lead**: [Your Name]
- **AI Lab Course**: [University Name]
- **Instructor**: [Instructor Name]

## 🙏 Acknowledgments

- Streamlit for the excellent web framework
- Plotly for interactive visualizations
- scikit-learn for machine learning algorithms
- Sample student data generated for educational purposes

## 📧 Contact

For questions or feedback, please contact:
- Email: [your-email@example.com]
- GitHub: [your-github-profile]

---

**Note**: This is an educational project developed for AI Lab coursework. It demonstrates AI integration, modular design, and user-centric development principles rather than production deployment.
