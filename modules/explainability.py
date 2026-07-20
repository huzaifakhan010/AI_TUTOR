
from typing import Dict, List


def generate_explanation(recommendation_result: Dict, student_profile: Dict) -> Dict:

    explanations = {
        'overview': _generate_overview_explanation(recommendation_result, student_profile),
        'subject_explanations': _explain_subject_priorities(recommendation_result, student_profile),
        'module_explanations': _explain_module_recommendations(recommendation_result, student_profile),
        'learning_style_match': _explain_learning_style_alignment(student_profile),
        'time_allocation': _explain_time_allocation(recommendation_result, student_profile),
        'key_factors': _identify_key_factors(recommendation_result, student_profile)
    }

    return explanations


def _generate_overview_explanation(result: Dict, profile: Dict) -> str:
    
    name = profile.get('name', 'Student')
    approach = result['metadata'].get('approach', 'hybrid')
    num_modules = len(result['learning_path'])
    weeks = result.get('estimated_completion_weeks', 8)

    explanation = f"Hello {name}! Based on your profile analysis using a {approach} AI approach, "
    explanation += f"we've created a personalized learning path with {num_modules} key modules "
    explanation += f"that can be completed in approximately {weeks} weeks. "

    
    style = profile.get('learning_style', '')
    explanation += f"This plan is tailored to your {style} learning style "

    
    goal = profile.get('goal', '')
    if goal:
        explanation += f"and aligned with your goal: '{goal}'."
    else:
        explanation += "and designed to maximize your learning outcomes."

    return explanation


def _explain_subject_priorities(result: Dict, profile: Dict) -> List[Dict]:
    
    explanations = []
    priority_subjects = result.get('priority_subjects', [])[:3]
    metadata = result.get('metadata', {})

    content_scores = metadata.get('content_scores', {})
    collaborative_scores = metadata.get('collaborative_scores', {})
    subject_scores = profile.get('subject_scores', {})

    for item in priority_subjects:
        subject = item['subject']
        priority_score = item['priority_score']

        # Build explanation factors
        factors = []

        # Current performance factor
        current_score = subject_scores.get(subject, 0)
        if current_score < 70:
            factors.append(f"Current score of {current_score}% indicates need for improvement")
        elif current_score >= 85:
            factors.append(f"Strong foundation ({current_score}%) enables advanced learning")
        else:
            factors.append(f"Moderate performance ({current_score}%) with room for growth")

        # subject designation
        if subject in profile.get('weak_subjects', []):
            factors.append("Identified as a weak subject requiring focused attention")
        if subject in profile.get('strong_subjects', []):
            factors.append("Identified as a strong subject for further development")

        # Content-based score contribution
        content_score = content_scores.get(subject, 0)
        if content_score > 0.5:
            factors.append(f"Content analysis priority: {content_score:.2f}")

        # Collaborative filtering insight
        collab_score = collaborative_scores.get(subject, 0)
        if collab_score > 0.3:
            factors.append(f"Similar successful students focused on this ({collab_score:.2f})")

        explanation_text = f"**{subject}** (Priority: {priority_score:.2f})\n"
        explanation_text += "Reasons:\n"
        for factor in factors:
            explanation_text += f"  • {factor}\n"

        explanations.append({
            'subject': subject,
            'priority_score': priority_score,
            'explanation': explanation_text,
            'factors': factors
        })

    return explanations


def _explain_module_recommendations(result: Dict, profile: Dict) -> List[Dict]:
    
    explanations = []
    learning_path = result.get('learning_path', [])

    for i, module in enumerate(learning_path):
        module_name = module['module']
        subject = module['subject']
        difficulty = module['difficulty']
        hours = module['estimated_hours']
        reason = module.get('reason', '')

        explanation_parts = []

        # Position in learning path
        if i == 0:
            explanation_parts.append("**Starting point** - Most critical for immediate improvement")
        elif i < 3:
            explanation_parts.append("**Early priority** - Important foundation module")
        else:
            explanation_parts.append("**Later stage** - Builds on earlier modules")

        # Difficulty justification
        current_score = profile['subject_scores'].get(subject, 0)
        if difficulty == 'beginner' and current_score < 70:
            explanation_parts.append(f"Beginner level appropriate given {subject} score of {current_score}%")
        elif difficulty == 'intermediate' and 70 <= current_score < 85:
            explanation_parts.append(f"Intermediate level matches your {subject} proficiency ({current_score}%)")
        elif difficulty == 'advanced' and current_score >= 85:
            explanation_parts.append(f"Advanced level suitable for your strong {subject} skills ({current_score}%)")

        # Time estimate
        daily_hours = profile.get('study_hours_per_day', 4)
        days_estimate = int(hours / daily_hours) if daily_hours > 0 else 0
        explanation_parts.append(f"Estimated {hours} hours (~{days_estimate} days at {daily_hours}hrs/day)")

        # Original reason from recommendation engine
        if reason:
            explanation_parts.append(f"Context: {reason}")

        full_explanation = f"**{module_name}** ({subject} - {difficulty})\n"
        for part in explanation_parts:
            full_explanation += f"  • {part}\n"

        explanations.append({
            'module': module_name,
            'subject': subject,
            'explanation': full_explanation,
            'estimated_hours': hours
        })

    return explanations


def _explain_learning_style_alignment(profile: Dict) -> str:
    
    style = profile.get('learning_style', 'Mixed')

    style_recommendations = {
        'Visual': (
            "Your **Visual** learning style means you learn best through diagrams, charts, and videos. "
            "We recommend: \n"
            "  • Use YouTube tutorials and video courses\n"
            "  • Create mind maps and flowcharts for complex topics\n"
            "  • Watch demonstrations before trying problems\n"
            "  • Use color-coding in notes"
        ),
        'Auditory': (
            "Your **Auditory** learning style means you learn best through listening and discussion. "
            "We recommend: \n"
            "  • Listen to educational podcasts and lectures\n"
            "  • Explain concepts out loud to yourself\n"
            "  • Join study groups for discussion\n"
            "  • Record and replay your own explanations"
        ),
        'Reading/Writing': (
            "Your **Reading/Writing** learning style means you learn best through text. "
            "We recommend: \n"
            "  • Read textbooks and articles thoroughly\n"
            "  • Take detailed written notes\n"
            "  • Write summaries after each study session\n"
            "  • Create written explanations of concepts"
        ),
        'Kinesthetic': (
            "Your **Kinesthetic** learning style means you learn best through hands-on practice. "
            "We recommend: \n"
            "  • Focus on practical exercises and projects\n"
            "  • Build things while learning concepts\n"
            "  • Use physical models when possible\n"
            "  • Take frequent breaks to move around"
        ),
        'Mixed': (
            "Your **Mixed** learning style means you benefit from various approaches. "
            "We recommend: \n"
            "  • Combine videos, reading, and hands-on practice\n"
            "  • Experiment to find what works best for each topic\n"
            "  • Use multiple resources for complex subjects\n"
            "  • Adapt your approach based on the material"
        )
    }

    return style_recommendations.get(style, style_recommendations['Mixed'])


def _explain_time_allocation(result: Dict, profile: Dict) -> str:
    """
    Explain time allocation strategy.

    Args:
        result: Recommendation result
        profile: Student profile

    Returns:
        Time allocation explanation
    """
    daily_hours = profile.get('study_hours_per_day', 4)
    total_hours = result['metadata'].get('total_estimated_hours', 0)
    weeks = result.get('estimated_completion_weeks', 8)

    explanation = f"**Time Allocation Strategy**\n\n"
    explanation += f"Based on your availability of {daily_hours} hours per day:\n"
    explanation += f"  • Total learning time: {total_hours} hours\n"
    explanation += f"  • Estimated completion: {weeks} weeks\n"
    explanation += f"  • Weekly commitment: ~{daily_hours * 5} hours (5 days/week)\n\n"

    if daily_hours < 3:
        explanation += "**Note:** With limited daily hours, focus is crucial. Prioritize the first 2-3 modules.\n"
    elif daily_hours >= 6:
        explanation += "**Note:** Your strong time commitment allows for comprehensive coverage and extra practice.\n"

    explanation += "\n**Recommended schedule:**\n"
    explanation += "  • Use peak energy times for difficult subjects\n"
    explanation += "  • Take 5-10 minute breaks every hour\n"
    explanation += "  • Reserve 20% of time for review and practice\n"
    explanation += "  • Plan 1-2 rest days per week"

    return explanation


def _identify_key_factors(result: Dict, profile: Dict) -> List[Dict]:
    """
    Identify and rank key factors influencing recommendations.

    Args:
        result: Recommendation result
        profile: Student profile

    Returns:
        List of key factors with importance scores
    """
    factors = []

    # Performance factor
    avg_score = profile.get('average_score', 0)
    if avg_score < 70:
        factors.append({
            'factor': 'Performance Level',
            'importance': 'High',
            'description': f'Average score of {avg_score:.1f}% indicates need for foundational strengthening'
        })
    elif avg_score >= 85:
        factors.append({
            'factor': 'Performance Level',
            'importance': 'High',
            'description': f'Strong average score of {avg_score:.1f}% enables advanced topic exploration'
        })

    # Weak subjects factor
    weak_subjects = profile.get('weak_subjects', [])
    if weak_subjects:
        factors.append({
            'factor': 'Weak Subjects',
            'importance': 'Critical',
            'description': f'Identified weak subjects ({", ".join(weak_subjects)}) receive highest priority'
        })

    # Learning style factor
    factors.append({
        'factor': 'Learning Style',
        'importance': 'Medium',
        'description': f'{profile.get("learning_style", "Mixed")} learning style influences resource recommendations'
    })

    # Study time factor
    daily_hours = profile.get('study_hours_per_day', 4)
    if daily_hours >= 6:
        time_impact = 'High time availability enables comprehensive learning path'
    elif daily_hours < 3:
        time_impact = 'Limited time requires focused, prioritized approach'
    else:
        time_impact = 'Moderate time availability suits balanced learning approach'

    factors.append({
        'factor': 'Time Availability',
        'importance': 'High',
        'description': time_impact
    })

    # Goal factor
    goal = profile.get('goal', '')
    if goal:
        factors.append({
            'factor': 'Learning Goal',
            'importance': 'Medium',
            'description': f'Goal alignment: "{goal}"'
        })

    # Collaborative insights factor
    metadata = result.get('metadata', {})
    if metadata.get('collaborative_weight', 0) > 0:
        factors.append({
            'factor': 'Peer Learning Patterns',
            'importance': 'Medium',
            'description': 'Recommendations influenced by successful paths of similar students'
        })

    return factors


def format_explanation_for_display(explanations: Dict) -> str:
    """
    Format explanations into readable text for display.

    Args:
        explanations: Explanation dictionary

    Returns:
        Formatted explanation text
    """
    output = "# 📊 Recommendation Explanation\n\n"

    # Overview
    output += "## Overview\n"
    output += explanations['overview'] + "\n\n"

    # Key Factors
    output += "## 🔑 Key Factors Considered\n\n"
    for factor in explanations['key_factors']:
        output += f"**{factor['factor']}** ({factor['importance']} importance)\n"
        output += f"  {factor['description']}\n\n"

    # Subject priorities
    output += "## 🎯 Why These Subjects?\n\n"
    for subj_exp in explanations['subject_explanations']:
        output += subj_exp['explanation'] + "\n"

    # Learning style
    output += "## 🎨 Learning Style Alignment\n\n"
    output += explanations['learning_style_match'] + "\n\n"

    # Time allocation
    output += "## ⏰ Time Management\n\n"
    output += explanations['time_allocation'] + "\n\n"

    return output
