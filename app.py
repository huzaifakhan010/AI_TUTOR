
import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List

# Import custom modules
from modules.data_processing import (
    load_data, preprocess_data, validate_student_input,
    create_student_profile
)
from modules.recommendation_engine import RecommendationEngine
from modules.explainability import generate_explanation, format_explanation_for_display
from modules.visualization import (
    create_performance_radar_chart,
    create_subject_comparison_bar_chart,
    create_learning_path_timeline,
    create_priority_subjects_table,
    create_comparison_chart,
    create_study_time_distribution,
    create_performance_improvement_projection
)
from modules.evaluation import (
    evaluate_recommendation,
    compare_approaches,
    generate_evaluation_report
)


# Page configuration
st.set_page_config(
    page_title="AI Tutor - Personalized Learning",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'student_db' not in st.session_state:
        st.session_state.student_db = None
    if 'student_profile' not in st.session_state:
        st.session_state.student_profile = None
    if 'recommendation_result' not in st.session_state:
        st.session_state.recommendation_result = None
    if 'comparison_results' not in st.session_state:
        st.session_state.comparison_results = None
    if 'profile_just_created' not in st.session_state:
        st.session_state.profile_just_created = False
    if 'nav_radio' not in st.session_state:
        st.session_state.nav_radio = "👤 Your Profile"
    if 'pending_nav' not in st.session_state:
        st.session_state.pending_nav = None


def main():
    """Main application function."""
    initialize_session_state()

    if st.session_state.pending_nav:
        st.session_state.nav_radio = st.session_state.pending_nav
        st.session_state.pending_nav = None


    st.markdown('<div class="main-header">🎓 AI Tutor</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Personalized Student Learning Recommendations</div>', unsafe_allow_html=True)

    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["👤 Your Profile", "🎯 Get Recommendations", "📊 View Results", "🔍 Explainability", "⚖️ Compare Approaches"],
        key="nav_radio"
    )


    if st.session_state.student_db is None:
        try:
            with st.spinner("Loading student database..."):
                df = load_data()
                df_processed, metadata = preprocess_data(df)
                st.session_state.student_db = df_processed
                st.session_state.db_metadata = metadata
        except Exception as e:
            st.error(f"Error loading student database: {str(e)}")
            st.info("Please ensure 'data/student_profiles.csv' exists.")
            return

    
    if page == "👤 Your Profile":
        problem_setup_page()
    elif page == "🎯 Get Recommendations":
        recommendation_page()
    elif page == "📊 View Results":
        results_page()
    elif page == "🔍 Explainability":
        explainability_page()
    elif page == "⚖️ Compare Approaches":
        comparison_page()


def problem_setup_page():
    """Problem setup and data input page."""
    st.header("👤 Your Profile")

    st.markdown("""
    
    This AI Tutor delivers personalized learning recommendations tailored specifically to you, taking into account:

     Your current academic performance across different subjects.
     Your preferred learning style.
     Your strengths and areas that need improvement.
     Your available study time and academic goals.

    """)
    st.markdown("### 📋 Input Options")


    input_method = st.radio(
        "Select input method:",
        ["📝 Manual Input Form", "📂 Upload CSV", "👥 Use Sample Student"]
    )

    if input_method == "📝 Manual Input Form":
        manual_input_form()
    elif input_method == "📂 Upload CSV":
        csv_upload_form()
    elif input_method == "👥 Use Sample Student":
        sample_student_selector()


def manual_input_form():
    """Manual input form for student data."""
    st.subheader("Enter Student Information")

    with st.form("student_input_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name*", placeholder="e.g., John Doe")
            age = st.number_input("Age*", min_value=10, max_value=100, value=20)
            education_level = st.selectbox(
                "Education Level*",
                ["High School", "Undergraduate", "Graduate", "Postgraduate"]
            )
            semester = st.number_input("Current Semester*", min_value=1, max_value=12, value=3)

        with col2:
            learning_style = st.selectbox(
                "Preferred Learning Style*",
                ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"]
            )
            study_hours = st.number_input(
                "Study Hours Per Day*",
                min_value=0.5, max_value=24.0, value=4.0, step=0.5
            )
            goal = st.text_input("Target Goal*", placeholder="e.g., Improve grades, Prepare for exams")
            interests = st.text_input("Interests", placeholder="e.g., AI, Web Development, Data Science")

        st.subheader("Subject Scores (0-100)")
        col3, col4, col5 = st.columns(3)

        with col3:
            math_score = st.slider("Math Score", 0, 100, 75)
            physics_score = st.slider("Physics Score", 0, 100, 75)

        with col4:
            chemistry_score = st.slider("Chemistry Score", 0, 100, 75)
            programming_score = st.slider("Programming Score", 0, 100, 75)

        with col5:
            english_score = st.slider("English Score", 0, 100, 75)

        weak_subjects = st.text_input(
            "Weak Subjects (comma-separated)",
            placeholder="e.g., Math, Physics"
        )
        strong_subjects = st.text_input(
            "Strong Subjects (comma-separated)",
            placeholder="e.g., Programming, English"
        )

        submitted = st.form_submit_button("✅ Submit Profile")

        if submitted:
            input_data = {
                'name': name,
                'age': age,
                'education_level': education_level,
                'semester': semester,
                'learning_style': learning_style,
                'study_hours_per_day': study_hours,
                'goal': goal,
                'interests': interests,
                'math_score': math_score,
                'physics_score': physics_score,
                'chemistry_score': chemistry_score,
                'programming_score': programming_score,
                'english_score': english_score,
                'weak_subjects': weak_subjects,
                'strong_subjects': strong_subjects
            }

            is_valid, errors = validate_student_input(input_data)

            if is_valid:
                profile = create_student_profile(input_data)
                st.session_state.student_profile = profile
                st.session_state.profile_just_created = True

                st.success("✅ Profile created successfully!")
                st.balloons()

                with st.expander("📄 View Profile Summary"):
                    st.json(profile)

            else:
                st.session_state.profile_just_created = False
                st.error("❌ Validation errors:")
                for error in errors:
                    st.warning(f"• {error}")

    if st.session_state.get('profile_just_created'):
        if st.button("👉 Continue to Get Recommendations",
                     type="primary",
                     use_container_width=True,
                     key="go_to_recommendation"):

            st.session_state.pending_nav = "🎯 Get Recommendations"
            st.session_state.profile_just_created = False
            st.rerun()


def csv_upload_form():
    """CSV upload form."""
    st.subheader("Upload Student Profile CSV")

    st.markdown("""
    Upload a CSV file with the following columns:
    - name, age, education_level, semester, math_score, physics_score, chemistry_score,
      programming_score, english_score, learning_style, study_hours_per_day, goal,
      weak_subjects, strong_subjects, interests
    """)

    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Loaded {len(df)} student(s) from CSV")

            st.dataframe(df.head())

            if len(df) > 1:
                selected_idx = st.selectbox("Select student:", range(len(df)), format_func=lambda i: df.iloc[i]['name'])
            else:
                selected_idx = 0

            if st.button("Use Selected Student"):
                row = df.iloc[selected_idx]

                input_data = {
                    'name': row['name'],
                    'age': row['age'],
                    'education_level': row['education_level'],
                    'semester': row['semester'],
                    'learning_style': row['learning_style'],
                    'study_hours_per_day': row['study_hours_per_day'],
                    'goal': row['goal'],
                    'interests': row.get('interests', ''),
                    'math_score': row['math_score'],
                    'physics_score': row['physics_score'],
                    'chemistry_score': row['chemistry_score'],
                    'programming_score': row['programming_score'],
                    'english_score': row['english_score'],
                    'weak_subjects': row['weak_subjects'],
                    'strong_subjects': row['strong_subjects']
                }

                profile = create_student_profile(input_data)
                st.session_state.student_profile = profile
                st.session_state.profile_just_created = True
                st.success("✅ Student profile loaded!")

        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")

    if st.session_state.get('profile_just_created'):
        if st.button("👉 Continue to Get Recommendations",
                     type="primary",
                     use_container_width=True,
                     key="go_to_recommendation_csv"):

            st.session_state.pending_nav = "🎯 Get Recommendations"
            st.session_state.profile_just_created = False
            st.rerun()


def sample_student_selector():
    """Select from sample students in database."""
    st.subheader("Use Sample Student from Database")

    db = st.session_state.student_db

    st.dataframe(db[['name', 'education_level', 'semester', 'average_score', 'learning_style']].head(10))

    selected_name = st.selectbox(
        "Select a student:",
        db['name'].tolist()
    )

    if st.button("Load Selected Student"):
        row = db[db['name'] == selected_name].iloc[0]

        input_data = {
            'name': row['name'],
            'age': row['age'],
            'education_level': row['education_level'],
            'semester': row['semester'],
            'learning_style': row['learning_style'],
            'study_hours_per_day': row['study_hours_per_day'],
            'goal': row['goal'],
            'interests': row.get('interests', ''),
            'math_score': row['math_score'],
            'physics_score': row['physics_score'],
            'chemistry_score': row['chemistry_score'],
            'programming_score': row['programming_score'],
            'english_score': row['english_score'],
            'weak_subjects': row['weak_subjects'],
            'strong_subjects': row['strong_subjects']
        }

        profile = create_student_profile(input_data)
        st.session_state.student_profile = profile
        st.session_state.profile_just_created = True
        st.success(f"✅ Loaded profile for {selected_name}!")

    if st.session_state.get('profile_just_created'):
        if st.button("👉 Continue to Get Recommendations",
                     type="primary",
                     use_container_width=True,
                     key="go_to_recommendation_sample"):

            st.session_state.pending_nav = "🎯 Get Recommendations"
            st.session_state.profile_just_created = False
            st.rerun()


def recommendation_page():
    """Generate recommendations page."""
    st.header("🎯 Generate Personalized Recommendations")

    if st.session_state.student_profile is None:
        st.warning("⚠️ Please complete the Problem Setup first!")
        st.info("👈 Go to **'Problem Setup'** page to enter student information")
        return

    profile = st.session_state.student_profile

    with st.expander("📄 Current Student Profile"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Name", profile['name'])
            st.metric("Age", profile['age'])
        with col2:
            st.metric("Education", profile['education_level'])
            st.metric("Semester", profile['semester'])
        with col3:
            st.metric("Average Score", f"{profile['average_score']:.1f}%")
            st.metric("Study Hours/Day", profile['study_hours_per_day'])

    st.markdown("---")

    st.subheader("⚙️ Recommendation Parameters")

    col1, col2 = st.columns(2)

    with col1:
        content_weight = st.slider(
            "Content-Based Weight",
            0.0, 1.0, 0.6, 0.1,
            help="Weight for content-based filtering (own performance analysis)"
        )

        weak_subject_focus = st.slider(
            "Weak Subject Focus",
            0.0, 1.0, 0.7, 0.1,
            help="How much to prioritize weak subjects"
        )

    with col2:
        collaborative_weight = 1.0 - content_weight
        st.metric("Collaborative Weight", f"{collaborative_weight:.1f}")
        st.caption("(Automatically calculated as 1 - Content Weight)")

        goal_alignment = st.slider(
            "Goal Alignment Weight",
            0.0, 1.0, 0.8, 0.1,
            help="How much to align with stated goals"
        )

    if st.button("🚀 Generate Recommendations", type="primary"):
        with st.spinner("🔄 Analyzing profile and generating recommendations..."):
            try:
                engine = RecommendationEngine(st.session_state.student_db)

                params = {
                    'content_weight': content_weight,
                    'collaborative_weight': collaborative_weight,
                    'weak_subject_focus': weak_subject_focus,
                    'goal_alignment': goal_alignment
                }

                result = engine.run_recommendation_model(profile, params)

                st.session_state.recommendation_result = result

                st.success("✅ Recommendations generated successfully!")
                st.balloons()
                st.info("👉 Go to **'View Results'** to see your personalized learning plan!")

            except Exception as e:
                st.error(f"❌ Error generating recommendations: {str(e)}")
                st.exception(e)

    if st.session_state.recommendation_result is not None:
        st.markdown("---")
        if st.button("👉 View Results", type="primary", use_container_width=True, key="nav_to_results"):
            st.session_state.pending_nav = "📊 View Results"
            st.rerun()


def results_page():
    """Display recommendation results page."""
    st.header("📊 Your Personalized Learning Plan")

    if st.session_state.recommendation_result is None:
        st.warning("⚠️ No recommendations generated yet!")
        st.info("👈 Go to **'Get Recommendations'** to generate your plan")
        return

    result = st.session_state.recommendation_result
    profile = st.session_state.student_profile

    st.subheader("📈 Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Learning Modules", len(result['learning_path']))
    with col2:
        st.metric("Estimated Weeks", result['estimated_completion_weeks'])
    with col3:
        st.metric("Total Hours", result['metadata']['total_estimated_hours'])
    with col4:
        approach = result['metadata'].get('approach', 'hybrid').title()
        st.metric("AI Approach", approach)

    st.markdown("---")

    st.subheader("📊 Current Performance Analysis")

    tab1, tab2 = st.tabs(["Radar Chart", "Bar Chart"])

    with tab1:
        fig_radar = create_performance_radar_chart(profile['subject_scores'])
        st.plotly_chart(fig_radar, use_container_width=True)

    with tab2:
        fig_bar = create_subject_comparison_bar_chart(
            profile['subject_scores'],
            profile['average_score']
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    st.subheader("🎯 Priority Subjects")
    priority_df = create_priority_subjects_table(
        result['priority_subjects'],
        profile['subject_scores']
    )
    st.dataframe(priority_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    st.subheader("🗺️ Learning Path Timeline")
    fig_timeline = create_learning_path_timeline(result['learning_path'], profile)
    st.plotly_chart(fig_timeline, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏱️ Time Distribution")
        fig_time_dist = create_study_time_distribution(result['learning_path'])
        st.plotly_chart(fig_time_dist, use_container_width=True)

    with col2:
        st.subheader("📈 Projected Improvement")
        fig_projection = create_performance_improvement_projection(
            profile['subject_scores'],
            result['learning_path']
        )
        st.plotly_chart(fig_projection, use_container_width=True)

    st.markdown("---")

    st.subheader("📚 Detailed Learning Path")

    for i, module in enumerate(result['learning_path'], 1):
        with st.expander(f"{i}. {module['module']} - {module['subject']} ({module['difficulty']})"):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.write(f"**Reason:** {module.get('reason', 'N/A')}")
                st.write(f"**Difficulty:** {module['difficulty'].title()}")

            with col2:
                st.metric("Estimated Hours", module['estimated_hours'])
                st.metric("Priority Score", f"{module['priority_score']:.2f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📅 Daily Schedule")
        for item in result['daily_schedule']:
            st.info(item)

    with col2:
        st.subheader("📆 Weekly Plan")
        for item in result['weekly_plan']:
            st.success(item)

    st.markdown("---")
    if st.button("👉 Explainability", type="primary", use_container_width=True, key="nav_to_explainability"):
        st.session_state.pending_nav = "🔍 Explainability"
        st.rerun()


def explainability_page():
    """Explainability and reasoning page."""
    st.header("🔍 Why These Recommendations?")

    if st.session_state.recommendation_result is None:
        st.warning("⚠️ No recommendations to explain yet!")
        st.info("👈 Generate recommendations first")
        return

    result = st.session_state.recommendation_result
    profile = st.session_state.student_profile

    with st.spinner("Generating explanations..."):
        explanations = generate_explanation(result, profile)

    st.markdown(explanations['overview'])

    st.markdown("---")

    st.subheader("🔑 Key Factors Influencing Recommendations")

    for factor in explanations['key_factors']:
        with st.container():
            st.markdown(f"**{factor['factor']}** - *{factor['importance']} Importance*")
            st.write(factor['description'])
            st.markdown("")

    st.markdown("---")

    st.subheader("🎯 Subject Priority Explanations")

    for subj_exp in explanations['subject_explanations']:
        with st.expander(f"{subj_exp['subject']} - Priority: {subj_exp['priority_score']:.2f}"):
            st.markdown(subj_exp['explanation'])

    st.markdown("---")

    st.subheader("🎨 Learning Style Alignment")
    st.markdown(explanations['learning_style_match'])

    st.markdown("---")

    st.subheader("⏰ Time Allocation Strategy")
    st.markdown(explanations['time_allocation'])

    st.markdown("---")

    st.subheader("📚 Module-by-Module Reasoning")

    for module_exp in explanations['module_explanations']:
        with st.expander(f"{module_exp['module']} ({module_exp['subject']})"):
            st.markdown(module_exp['explanation'])

    st.markdown("---")
    if st.button("👉 Compare Approaches", type="primary", use_container_width=True, key="nav_to_compare"):
        st.session_state.pending_nav = "⚖️ Compare Approaches"
        st.rerun()


def comparison_page():
    """Compare different recommendation approaches."""
    st.header("⚖️ Compare Recommendation Approaches")

    if st.session_state.student_profile is None:
        st.warning("⚠️ Please complete Problem Setup first!")
        return

    profile = st.session_state.student_profile

    st.markdown("""
    Compare different recommendation strategies to see which one works best for this student profile.
    This helps understand the impact of different AI parameters and approaches.
    """)

    if st.button("🔄 Generate Comparison", type="primary"):
        with st.spinner("Generating recommendations with different approaches..."):
            try:
                engine = RecommendationEngine(st.session_state.student_db)

                params_1 = {
                    'content_weight': 0.8,
                    'collaborative_weight': 0.2,
                    'weak_subject_focus': 0.9,
                    'goal_alignment': 0.7
                }
                result_1 = engine.run_recommendation_model(profile, params_1)

                params_2 = {
                    'content_weight': 0.3,
                    'collaborative_weight': 0.7,
                    'weak_subject_focus': 0.5,
                    'goal_alignment': 0.9
                }
                result_2 = engine.run_recommendation_model(profile, params_2)

                comparison = compare_approaches(
                    [result_1, result_2],
                    profile,
                    ["Content-Focused", "Collaborative-Focused"]
                )

                st.session_state.comparison_results = {
                    'result_1': result_1,
                    'result_2': result_2,
                    'comparison': comparison
                }

                st.success("✅ Comparison generated!")

            except Exception as e:
                st.error(f"Error: {str(e)}")

    if st.session_state.comparison_results is not None:
        comp = st.session_state.comparison_results
        comparison = comp['comparison']

        st.markdown("---")

        st.subheader("🏆 Recommended Approach")
        st.success(f"**{comparison['winner']}** performs best for this student profile")

        st.subheader("📊 Metrics Comparison")

        fig_comparison = create_comparison_chart(
            comp['result_1'],
            comp['result_2'],
            comparison['approaches']
        )
        st.plotly_chart(fig_comparison, use_container_width=True)

        st.subheader("📋 Detailed Metrics")

        metrics_df = pd.DataFrame({
            'Metric': ['Relevance Score', 'Weak Area Coverage', 'Estimated Time (hrs)',
                      'Difficulty Balance', 'Prerequisite Coherence', 'Overall Score'],
            comparison['approaches'][0]: [
                f"{comparison['metrics']['relevance_score'][0]:.3f}",
                f"{comparison['metrics']['weak_area_coverage'][0]:.3f}",
                f"{comparison['metrics']['estimated_learning_time'][0]}",
                f"{comparison['metrics']['difficulty_balance'][0]:.3f}",
                f"{comparison['metrics']['prerequisite_coherence'][0]:.3f}",
                f"{comparison['metrics']['overall_score'][0]:.3f}"
            ],
            comparison['approaches'][1]: [
                f"{comparison['metrics']['relevance_score'][1]:.3f}",
                f"{comparison['metrics']['weak_area_coverage'][1]:.3f}",
                f"{comparison['metrics']['estimated_learning_time'][1]}",
                f"{comparison['metrics']['difficulty_balance'][1]:.3f}",
                f"{comparison['metrics']['prerequisite_coherence'][1]:.3f}",
                f"{comparison['metrics']['overall_score'][1]:.3f}"
            ]
        })

        st.dataframe(metrics_df, use_container_width=True, hide_index=True)

        st.subheader("📝 Approach Summaries")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(comparison['summary'][0])

        with col2:
            st.markdown(comparison['summary'][1])

        st.markdown("---")
        st.subheader("📊 Detailed Evaluation Reports")

        tab1, tab2 = st.tabs(comparison['approaches'])

        with tab1:
            eval_1 = evaluate_recommendation(comp['result_1'], profile)
            report_1 = generate_evaluation_report(eval_1, comparison['approaches'][0])
            st.markdown(report_1)

        with tab2:
            eval_2 = evaluate_recommendation(comp['result_2'], profile)
            report_2 = generate_evaluation_report(eval_2, comparison['approaches'][1])
            st.markdown(report_2)

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅ Back to Your Profile", type="primary", use_container_width=True, key="nav_back_profile"):
                st.session_state.pending_nav = "👤 Your Profile"
                st.rerun()
        with col2:
            if st.button("🔄 Start Over", type="primary", use_container_width=True, key="nav_start_over"):
                st.session_state.student_profile = None
                st.session_state.recommendation_result = None
                st.session_state.comparison_results = None
                st.session_state.profile_just_created = False
                st.session_state.pending_nav = "👤 Your Profile"
                st.rerun()


if __name__ == "__main__":
    main()