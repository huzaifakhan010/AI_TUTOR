
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from typing import Dict, List


def create_performance_radar_chart(subject_scores: Dict) -> go.Figure:
    
    subjects = list(subject_scores.keys())
    scores = list(subject_scores.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=subjects,
        fill='toself',
        name='Current Performance',
        line=dict(color='rgb(99, 110, 250)', width=2),
        fillcolor='rgba(99, 110, 250, 0.3)'
    ))

    
    fig.add_trace(go.Scatterpolar(
        r=[70] * len(subjects),
        theta=subjects,
        name='Passing Grade (70%)',
        line=dict(color='rgb(255, 165, 0)', width=2, dash='dash'),
        fill=None
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[0, 25, 50, 75, 100],
                ticktext=['0', '25', '50', '75', '100']
            )
        ),
        showlegend=True,
        title="Performance Across Subjects",
        height=500
    )

    return fig


def create_subject_comparison_bar_chart(subject_scores: Dict, avg_score: float) -> go.Figure:
    
    subjects = list(subject_scores.keys())
    scores = list(subject_scores.values())


    colors = []
    for score in scores:
        if score >= 85:
            colors.append('rgb(72, 187, 120)')  # Green - Strong
        elif score >= 70:
            colors.append('rgb(66, 153, 225)')  # Blue - Good
        elif score >= 60:
            colors.append('rgb(237, 137, 54)')  # Orange - Needs improvement
        else:
            colors.append('rgb(245, 101, 101)')  # Red - Weak

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=subjects,
        y=scores,
        marker=dict(color=colors),
        text=scores,
        textposition='outside',
        texttemplate='%{text:.1f}%',
        name='Score'
    ))

    
    fig.add_hline(
        y=avg_score,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Average: {avg_score:.1f}%",
        annotation_position="right"
    )

    fig.update_layout(
        title="Subject Performance Comparison",
        xaxis_title="Subject",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 105]),
        showlegend=False,
        height=400
    )

    return fig


def create_learning_path_timeline(learning_path: List[Dict], student_profile: Dict) -> go.Figure:
    
    if not learning_path:
        
        fig = go.Figure()
        fig.add_annotation(text="No learning path generated", showarrow=False)
        return fig

    
    cumulative_hours = 0
    timeline_data = []

    for i, module in enumerate(learning_path):
        start_hours = cumulative_hours
        end_hours = cumulative_hours + module['estimated_hours']

        timeline_data.append({
            'Module': f"{module['module']}",
            'Subject': module['subject'],
            'Start': start_hours,
            'Finish': end_hours,
            'Duration': module['estimated_hours'],
            'Difficulty': module['difficulty']
        })

        cumulative_hours = end_hours

    df = pd.DataFrame(timeline_data)

    
    difficulty_colors = {
        'beginner': 'rgb(72, 187, 120)',
        'intermediate': 'rgb(66, 153, 225)',
        'advanced': 'rgb(159, 122, 234)'
    }

    fig = go.Figure()

    for i, row in df.iterrows():
        color = difficulty_colors.get(row['Difficulty'], 'rgb(160, 174, 192)')

        fig.add_trace(go.Bar(
            x=[row['Duration']],
            y=[row['Module']],
            orientation='h',
            name=row['Subject'],
            marker=dict(color=color),
            text=f"{row['Subject']}<br>{row['Duration']}hrs",
            textposition='inside',
            hovertemplate=(
                f"<b>{row['Module']}</b><br>"
                f"Subject: {row['Subject']}<br>"
                f"Duration: {row['Duration']} hours<br>"
                f"Difficulty: {row['Difficulty']}<br>"
                "<extra></extra>"
            ),
            showlegend=False
        ))

    fig.update_layout(
        title="Learning Path Timeline",
        xaxis_title="Cumulative Hours",
        yaxis_title="",
        barmode='stack',
        height=max(400, len(learning_path) * 50),
        yaxis=dict(autorange="reversed")
    )

    return fig


def create_priority_subjects_table(priority_subjects: List[Dict], subject_scores: Dict) -> pd.DataFrame:
    
    data = []

    for item in priority_subjects[:5]:  # Top 5
        subject = item['subject']
        priority = item['priority_score']
        current_score = subject_scores.get(subject, 0)

        # Determine status
        if current_score >= 85:
            status = "Strong ⭐"
        elif current_score >= 70:
            status = "Good ✓"
        elif current_score >= 60:
            status = "Needs Work ⚠️"
        else:
            status = "Weak ❌"

        data.append({
            'Subject': subject,
            'Current Score': f"{current_score:.1f}%",
            'Priority Score': f"{priority:.2f}",
            'Status': status
        })

    return pd.DataFrame(data)


def create_comparison_chart(results_1: Dict, results_2: Dict, labels: List[str]) -> go.Figure:
   
    metrics = ['Weak Area Coverage', 'Learning Efficiency', 'Goal Alignment']

    # Extract or calculate metrics for both approaches
    scores_1 = [
        _calculate_weak_area_coverage(results_1),
        _calculate_learning_efficiency(results_1),
        _calculate_goal_alignment(results_1)
    ]

    scores_2 = [
        _calculate_weak_area_coverage(results_2),
        _calculate_learning_efficiency(results_2),
        _calculate_goal_alignment(results_2)
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=metrics,
        y=scores_1,
        name=labels[0],
        marker=dict(color='rgb(99, 110, 250)'),
        text=[f"{s:.2f}" for s in scores_1],
        textposition='outside'
    ))

    fig.add_trace(go.Bar(
        x=metrics,
        y=scores_2,
        name=labels[1],
        marker=dict(color='rgb(239, 68, 68)'),
        text=[f"{s:.2f}" for s in scores_2],
        textposition='outside'
    ))

    fig.update_layout(
        title="Recommendation Approach Comparison",
        xaxis_title="Metric",
        yaxis_title="Score (0-1)",
        yaxis=dict(range=[0, 1.1]),
        barmode='group',
        height=400
    )

    return fig


def create_study_time_distribution(learning_path: List[Dict]) -> go.Figure:
    """
    Create pie chart showing time distribution across subjects.

    Args:
        learning_path: Learning path modules

    Returns:
        Plotly figure object
    """
    # Aggregate hours by subject
    subject_hours = {}
    for module in learning_path:
        subject = module['subject']
        hours = module['estimated_hours']
        subject_hours[subject] = subject_hours.get(subject, 0) + hours

    subjects = list(subject_hours.keys())
    hours = list(subject_hours.values())

    fig = go.Figure(data=[go.Pie(
        labels=subjects,
        values=hours,
        hole=0.3,
        textinfo='label+percent',
        textposition='outside',
        marker=dict(
            colors=px.colors.qualitative.Set3[:len(subjects)]
        )
    )])

    fig.update_layout(
        title="Study Time Distribution by Subject",
        height=400
    )

    return fig


def create_performance_improvement_projection(current_scores: Dict, learning_path: List[Dict]) -> go.Figure:
    """
    Create line chart projecting performance improvement.

    Args:
        current_scores: Current subject scores
        learning_path: Learning path modules

    Returns:
        Plotly figure object
    """
    subjects = list(current_scores.keys())

    # Project improvement based on learning path focus
    subject_focus_hours = {subject: 0 for subject in subjects}
    for module in learning_path:
        subject = module['subject']
        if subject in subject_focus_hours:
            subject_focus_hours[subject] += module['estimated_hours']

    fig = go.Figure()

    for subject in subjects:
        current = current_scores[subject]
        focus_hours = subject_focus_hours[subject]

        # Simple improvement model: more focus hours = more improvement
        # Cap at 95% to be realistic
        improvement_rate = min(focus_hours / 30.0, 1.0)  # Normalize by 30 hours
        projected = min(current + (95 - current) * improvement_rate * 0.6, 95)

        fig.add_trace(go.Scatter(
            x=['Current', 'Projected'],
            y=[current, projected],
            mode='lines+markers',
            name=subject,
            line=dict(width=3),
            marker=dict(size=10)
        ))

    fig.update_layout(
        title="Projected Performance Improvement",
        xaxis_title="Status",
        yaxis_title="Score (%)",
        yaxis=dict(range=[0, 100]),
        height=400,
        hovermode='x unified'
    )

    return fig


def _calculate_weak_area_coverage(result: Dict) -> float:
    """
    Calculate how well the recommendation covers weak areas.

    Args:
        result: Recommendation result

    Returns:
        Coverage score (0-1)
    """
    # Look at priority subjects in learning path
    learning_path = result.get('learning_path', [])
    priority_subjects = result.get('priority_subjects', [])

    if not priority_subjects:
        return 0.5

    # Count how many of top 3 priority subjects are in learning path
    top_priorities = set(s['subject'] for s in priority_subjects[:3])
    path_subjects = set(m['subject'] for m in learning_path)

    coverage = len(top_priorities & path_subjects) / len(top_priorities)
    return coverage


def _calculate_learning_efficiency(result: Dict) -> float:
    """
    Calculate learning efficiency (coverage vs time).

    Args:
        result: Recommendation result

    Returns:
        Efficiency score (0-1)
    """
    learning_path = result.get('learning_path', [])
    total_hours = result['metadata'].get('total_estimated_hours', 100)

    if not learning_path:
        return 0.0

    # Efficiency: number of modules covered per 10 hours
    modules_per_10h = len(learning_path) / (total_hours / 10.0)

    # Normalize to 0-1 (assume 1 module per 10h is baseline efficiency)
    efficiency = min(modules_per_10h / 1.0, 1.0)

    return efficiency


def _calculate_goal_alignment(result: Dict) -> float:
    """
    Calculate alignment with student goals.

    Args:
        result: Recommendation result

    Returns:
        Alignment score (0-1)
    """
    # This is a simplified metric
    # In reality, would need NLP to match goal text with modules

    learning_path = result.get('learning_path', [])

    if not learning_path:
        return 0.0

    # Check for balanced difficulty distribution (aligns with comprehensive learning goal)
    difficulties = [m['difficulty'] for m in learning_path]
    unique_difficulties = len(set(difficulties))

    # More variety in difficulty = better goal alignment (comprehensive learning)
    alignment = unique_difficulties / 3.0  # 3 difficulty levels

    return min(alignment, 1.0)


def style_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply styling to DataFrame for better display.

    Args:
        df: Input DataFrame

    Returns:
        Styled DataFrame
    """
    # This returns the dataframe as-is for now
    # Streamlit will handle display styling
    return df
