
import numpy as np
from typing import Dict, List, Tuple


def evaluate_recommendation(result: Dict, student_profile: Dict) -> Dict:
    
    metrics = {
        'relevance_score': calculate_relevance_score(result, student_profile),
        'weak_area_coverage': calculate_weak_area_coverage(result, student_profile),
        'estimated_learning_time': calculate_estimated_time(result, student_profile),
        'difficulty_balance': calculate_difficulty_balance(result),
        'prerequisite_coherence': calculate_prerequisite_coherence(result),
        'overall_score': 0.0
    }

    # Calculate 
    metrics['overall_score'] = (
        metrics['relevance_score'] * 0.35 +
        metrics['weak_area_coverage'] * 0.30 +
        (1.0 - min(metrics['estimated_learning_time'] / 1000.0, 1.0)) * 0.15 +
        metrics['difficulty_balance'] * 0.10 +
        metrics['prerequisite_coherence'] * 0.10
    )

    return metrics


def calculate_relevance_score(result: Dict, profile: Dict) -> float:
    
    learning_path = result.get('learning_path', [])
    subject_scores = profile.get('subject_scores', {})
    weak_subjects = profile.get('weak_subjects', [])

    if not learning_path:
        return 0.0

    relevance_points = 0.0
    max_points = len(learning_path)

    for module in learning_path:
        subject = module['subject']
        difficulty = module['difficulty']
        current_score = subject_scores.get(subject, 0)

        
        if current_score < 60 and difficulty == 'beginner':
            relevance_points += 1.0  
        elif 60 <= current_score < 75 and difficulty in ['beginner', 'intermediate']:
            relevance_points += 0.9  
        elif 75 <= current_score < 85 and difficulty == 'intermediate':
            relevance_points += 1.0  
        elif current_score >= 85 and difficulty in ['intermediate', 'advanced']:
            relevance_points += 0.9  
        else:
            relevance_points += 0.5  

        
        if subject in weak_subjects:
            relevance_points += 0.2

    return min(relevance_points / max_points, 1.0)


def calculate_weak_area_coverage(result: Dict, profile: Dict) -> float:
    
    learning_path = result.get('learning_path', [])
    weak_subjects = profile.get('weak_subjects', [])
    subject_scores = profile.get('subject_scores', {})

    if not weak_subjects and not any(score < 70 for score in subject_scores.values()):
    
        return 1.0

    
    all_weak_areas = set(weak_subjects)
    for subject, score in subject_scores.items():
        if score < 70:
            all_weak_areas.add(subject)

    if not all_weak_areas:
        return 1.0

    
    addressed_areas = set(module['subject'] for module in learning_path)
    covered = len(all_weak_areas & addressed_areas)

    
    weak_subject_hours = sum(
        module['estimated_hours']
        for module in learning_path
        if module['subject'] in all_weak_areas
    )
    total_hours = sum(module['estimated_hours'] for module in learning_path)

    if total_hours == 0:
        return 0.0

    
    breadth_score = covered / len(all_weak_areas)
    depth_score = weak_subject_hours / total_hours

    return (breadth_score * 0.6 + depth_score * 0.4)


def calculate_estimated_time(result: Dict, profile: Dict) -> int:

    learning_path = result.get('learning_path', [])
    total_hours = sum(module['estimated_hours'] for module in learning_path)
    return total_hours


def calculate_difficulty_balance(result: Dict) -> float:
    
    learning_path = result.get('learning_path', [])

    if not learning_path:
        return 0.0

    # Count modules by difficulty
    difficulty_counts = {'beginner': 0, 'intermediate': 0, 'advanced': 0}
    for module in learning_path:
        difficulty = module['difficulty']
        if difficulty in difficulty_counts:
            difficulty_counts[difficulty] += 1

    total = len(learning_path)
    proportions = [count / total for count in difficulty_counts.values()]

    ideal_proportions = [0.35, 0.45, 0.20]

    distance = np.sqrt(sum((p - i) ** 2 for p, i in zip(proportions, ideal_proportions)))
    max_distance = np.sqrt(2)  # Maximum possible distance

    
    balance = 1.0 - (distance / max_distance)

    return balance


def calculate_prerequisite_coherence(result: Dict) -> float:
    
    learning_path = result.get('learning_path', [])

    if len(learning_path) <= 1:
        return 1.0  # No prerequisite issues with single module

    # Check prerequisite flow
    coherence_violations = 0
    max_violations = len(learning_path) - 1

    for i in range(len(learning_path) - 1):
        current_module = learning_path[i]
        next_module = learning_path[i + 1]

        current_difficulty = current_module['difficulty']
        next_difficulty = next_module['difficulty']

        # Check for jumps that are too large
        difficulty_order = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
        current_level = difficulty_order.get(current_difficulty, 1)
        next_level = difficulty_order.get(next_difficulty, 1)

        # Jumping from beginner to advanced is a violation
        if next_level - current_level > 1:
            coherence_violations += 0.5

        # Going backward in difficulty for same subject is a violation
        if (current_module['subject'] == next_module['subject'] and
            next_level < current_level):
            coherence_violations += 1.0

    coherence = 1.0 - (coherence_violations / max_violations)
    return max(coherence, 0.0)


def compare_approaches(results_list: List[Dict], student_profile: Dict, approach_names: List[str]) -> Dict:
    
    comparison = {
        'approaches': approach_names,
        'metrics': {},
        'winner': None,
        'summary': []
    }

    # Evaluate each approach
    evaluations = []
    for i, result in enumerate(results_list):
        eval_metrics = evaluate_recommendation(result, student_profile)
        eval_metrics['approach_name'] = approach_names[i]
        evaluations.append(eval_metrics)

    # Organize metrics by type
    metric_names = ['relevance_score', 'weak_area_coverage', 'estimated_learning_time',
                   'difficulty_balance', 'prerequisite_coherence', 'overall_score']

    for metric in metric_names:
        comparison['metrics'][metric] = [
            eval_dict[metric] for eval_dict in evaluations
        ]

    # Determine winner based on overall score
    overall_scores = comparison['metrics']['overall_score']
    winner_index = np.argmax(overall_scores)
    comparison['winner'] = approach_names[winner_index]

    # Generate summary
    for i, eval_dict in enumerate(evaluations):
        summary_text = f"**{approach_names[i]}**:\n"
        summary_text += f"  - Overall Score: {eval_dict['overall_score']:.3f}\n"
        summary_text += f"  - Relevance: {eval_dict['relevance_score']:.3f}\n"
        summary_text += f"  - Weak Area Coverage: {eval_dict['weak_area_coverage']:.3f}\n"
        summary_text += f"  - Estimated Time: {eval_dict['estimated_learning_time']} hours\n"
        summary_text += f"  - Difficulty Balance: {eval_dict['difficulty_balance']:.3f}\n"
        summary_text += f"  - Prerequisite Coherence: {eval_dict['prerequisite_coherence']:.3f}\n"

        comparison['summary'].append(summary_text)

    return comparison


def generate_evaluation_report(evaluation: Dict, approach_name: str = "Hybrid") -> str:
    
    report = f"# 📊 Evaluation Report: {approach_name} Approach\n\n"

    report += "## Overall Performance\n"
    overall = evaluation['overall_score']
    report += f"**Overall Score: {overall:.3f}** "

    if overall >= 0.8:
        report += "✅ Excellent\n\n"
    elif overall >= 0.65:
        report += "✓ Good\n\n"
    elif overall >= 0.5:
        report += "⚠️ Fair\n\n"
    else:
        report += "❌ Needs Improvement\n\n"

    report += "## Detailed Metrics\n\n"

    # Relevance
    report += f"### 1. Relevance Score: {evaluation['relevance_score']:.3f}\n"
    report += "Measures how well recommendations match the student's current level and needs.\n"
    if evaluation['relevance_score'] >= 0.8:
        report += "✅ Recommendations are highly relevant to student's needs.\n\n"
    elif evaluation['relevance_score'] >= 0.6:
        report += "✓ Recommendations are reasonably relevant.\n\n"
    else:
        report += "⚠️ Recommendations could be better tailored.\n\n"

    # Weak Area Coverage
    report += f"### 2. Weak Area Coverage: {evaluation['weak_area_coverage']:.3f}\n"
    report += "Measures how comprehensively the plan addresses weak subjects.\n"
    if evaluation['weak_area_coverage'] >= 0.7:
        report += "✅ Weak areas are well covered.\n\n"
    elif evaluation['weak_area_coverage'] >= 0.5:
        report += "✓ Reasonable coverage of weak areas.\n\n"
    else:
        report += "⚠️ Some weak areas may be under-addressed.\n\n"

    # Estimated Time
    report += f"### 3. Estimated Learning Time: {evaluation['estimated_learning_time']} hours\n"
    weeks = evaluation['estimated_learning_time'] / 20  # Assuming 20 hours per week
    report += f"Approximately {weeks:.1f} weeks of study.\n"
    if evaluation['estimated_learning_time'] < 100:
        report += "✓ Reasonable time commitment.\n\n"
    elif evaluation['estimated_learning_time'] < 200:
        report += "⚠️ Significant time commitment required.\n\n"
    else:
        report += "⚠️ Very extensive program - consider breaking into phases.\n\n"

    # Difficulty Balance
    report += f"### 4. Difficulty Balance: {evaluation['difficulty_balance']:.3f}\n"
    report += "Measures the balance of beginner, intermediate, and advanced modules.\n"
    if evaluation['difficulty_balance'] >= 0.7:
        report += "✅ Well-balanced progression through difficulty levels.\n\n"
    else:
        report += "⚠️ Difficulty distribution could be more balanced.\n\n"

    # Prerequisite Coherence
    report += f"### 5. Prerequisite Coherence: {evaluation['prerequisite_coherence']:.3f}\n"
    report += "Measures how well the learning path respects prerequisites and logical progression.\n"
    if evaluation['prerequisite_coherence'] >= 0.8:
        report += "✅ Learning path follows a logical progression.\n\n"
    elif evaluation['prerequisite_coherence'] >= 0.6:
        report += "✓ Generally logical progression.\n\n"
    else:
        report += "⚠️ Some prerequisite or progression issues detected.\n\n"

    return report
