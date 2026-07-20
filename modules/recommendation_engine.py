
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from typing import Dict, List, Tuple


class RecommendationEngine:
    """
    Hybrid recommendation system for personalized learning paths.
    Uses content-based filtering and collaborative filtering.
    """

    def __init__(self, student_database: pd.DataFrame):
        
        self.student_db = student_database
        self.subject_names = ['Math', 'Physics', 'Chemistry', 'Programming', 'English']
        self.learning_modules = self._define_learning_modules()

    def _define_learning_modules(self) -> Dict:
        
        return {
            'Math': [
                {'name': 'Basic Algebra', 'difficulty': 'beginner', 'prerequisites': [], 'estimated_hours': 20},
                {'name': 'Advanced Algebra', 'difficulty': 'intermediate', 'prerequisites': ['Basic Algebra'], 'estimated_hours': 25},
                {'name': 'Calculus Fundamentals', 'difficulty': 'intermediate', 'prerequisites': ['Advanced Algebra'], 'estimated_hours': 30},
                {'name': 'Advanced Calculus', 'difficulty': 'advanced', 'prerequisites': ['Calculus Fundamentals'], 'estimated_hours': 35},
                {'name': 'Linear Algebra', 'difficulty': 'intermediate', 'prerequisites': ['Advanced Algebra'], 'estimated_hours': 28},
                {'name': 'Probability & Statistics', 'difficulty': 'intermediate', 'prerequisites': ['Basic Algebra'], 'estimated_hours': 25},
            ],
            'Physics': [
                {'name': 'Classical Mechanics Basics', 'difficulty': 'beginner', 'prerequisites': [], 'estimated_hours': 22},
                {'name': 'Advanced Mechanics', 'difficulty': 'intermediate', 'prerequisites': ['Classical Mechanics Basics'], 'estimated_hours': 28},
                {'name': 'Electromagnetism', 'difficulty': 'intermediate', 'prerequisites': ['Classical Mechanics Basics'], 'estimated_hours': 30},
                {'name': 'Quantum Physics', 'difficulty': 'advanced', 'prerequisites': ['Advanced Mechanics'], 'estimated_hours': 40},
                {'name': 'Thermodynamics', 'difficulty': 'intermediate', 'prerequisites': ['Classical Mechanics Basics'], 'estimated_hours': 26},
            ],
            'Chemistry': [
                {'name': 'General Chemistry', 'difficulty': 'beginner', 'prerequisites': [], 'estimated_hours': 20},
                {'name': 'Organic Chemistry', 'difficulty': 'intermediate', 'prerequisites': ['General Chemistry'], 'estimated_hours': 32},
                {'name': 'Inorganic Chemistry', 'difficulty': 'intermediate', 'prerequisites': ['General Chemistry'], 'estimated_hours': 28},
                {'name': 'Physical Chemistry', 'difficulty': 'advanced', 'prerequisites': ['General Chemistry', 'Organic Chemistry'], 'estimated_hours': 35},
                {'name': 'Analytical Chemistry', 'difficulty': 'intermediate', 'prerequisites': ['General Chemistry'], 'estimated_hours': 26},
            ],
            'Programming': [
                {'name': 'Programming Basics', 'difficulty': 'beginner', 'prerequisites': [], 'estimated_hours': 25},
                {'name': 'Data Structures', 'difficulty': 'intermediate', 'prerequisites': ['Programming Basics'], 'estimated_hours': 30},
                {'name': 'Algorithms', 'difficulty': 'intermediate', 'prerequisites': ['Data Structures'], 'estimated_hours': 35},
                {'name': 'Object-Oriented Programming', 'difficulty': 'intermediate', 'prerequisites': ['Programming Basics'], 'estimated_hours': 28},
                {'name': 'Database Systems', 'difficulty': 'intermediate', 'prerequisites': ['Programming Basics'], 'estimated_hours': 26},
                {'name': 'Web Development', 'difficulty': 'intermediate', 'prerequisites': ['Programming Basics'], 'estimated_hours': 32},
                {'name': 'Machine Learning', 'difficulty': 'advanced', 'prerequisites': ['Algorithms', 'Data Structures'], 'estimated_hours': 40},
            ],
            'English': [
                {'name': 'Grammar Fundamentals', 'difficulty': 'beginner', 'prerequisites': [], 'estimated_hours': 18},
                {'name': 'Academic Writing', 'difficulty': 'intermediate', 'prerequisites': ['Grammar Fundamentals'], 'estimated_hours': 25},
                {'name': 'Technical Writing', 'difficulty': 'intermediate', 'prerequisites': ['Academic Writing'], 'estimated_hours': 22},
                {'name': 'Literature Analysis', 'difficulty': 'intermediate', 'prerequisites': ['Grammar Fundamentals'], 'estimated_hours': 24},
                {'name': 'Research Paper Writing', 'difficulty': 'advanced', 'prerequisites': ['Academic Writing'], 'estimated_hours': 28},
            ]
        }

    def run_recommendation_model(self, student_profile: Dict, params: Dict) -> Dict:
        
        content_weight = params.get('content_weight', 0.6)
        collaborative_weight = params.get('collaborative_weight', 0.4)
        weak_subject_focus = params.get('weak_subject_focus', 0.7)
        goal_alignment = params.get('goal_alignment', 0.8)

        
        content_scores = self._content_based_filtering(student_profile, weak_subject_focus)

        
        collaborative_scores = self._collaborative_filtering(student_profile)

        
        combined_scores = {}
        for subject in self.subject_names:
            combined_scores[subject] = (
                content_weight * content_scores.get(subject, 0) +
                collaborative_weight * collaborative_scores.get(subject, 0)
            )

        
        learning_path = self._generate_learning_path(
            student_profile, combined_scores, goal_alignment
        )

        
        metadata = {
            'content_scores': content_scores,
            'collaborative_scores': collaborative_scores,
            'combined_scores': combined_scores,
            'total_estimated_hours': sum(module['estimated_hours'] for module in learning_path),
            'approach': 'hybrid',
            'content_weight': content_weight,
            'collaborative_weight': collaborative_weight
        }

        return {
            'learning_path': learning_path,
            'priority_subjects': self._rank_subjects(combined_scores),
            'daily_schedule': self._create_daily_schedule(learning_path, student_profile),
            'weekly_plan': self._create_weekly_plan(learning_path, student_profile),
            'estimated_completion_weeks': self._estimate_completion_time(learning_path, student_profile),
            'metadata': metadata
        }

    def _content_based_filtering(self, student_profile: Dict, weak_focus: float) -> Dict:
       
        scores = {}
        subject_scores = student_profile['subject_scores']

        # Calculate priority: lower performance = higher priority
        max_score = 100
        for subject, score in subject_scores.items():
            # Inverse score: weak subjects get higher priority
            weakness_score = (max_score - score) / max_score

            # Check if subject is explicitly marked as weak
            is_weak = subject in student_profile.get('weak_subjects', [])
            weak_bonus = 0.3 if is_weak else 0

            # Calculate final priority
            priority = weakness_score * weak_focus + weak_bonus

            # Normalize to 0-1 range
            scores[subject] = min(priority, 1.0)

        return scores

    def _collaborative_filtering(self, student_profile: Dict) -> Dict:
        
        
        current_features = self._create_feature_vector(student_profile)


        db_features = []
        for _, row in self.student_db.iterrows():
            db_profile = {
                'subject_scores': row['subject_scores'],
                'learning_style': row['learning_style'],
                'education_level': row['education_level'],
                'study_hours_per_day': row['study_hours_per_day']
            }
            db_features.append(self._create_feature_vector(db_profile))

        db_features = np.array(db_features)
        current_features = np.array([current_features])

        # Find k nearest neighbors
        k = min(5, len(db_features))
        nbrs = NearestNeighbors(n_neighbors=k, metric='euclidean')
        nbrs.fit(db_features)
        distances, indices = nbrs.kneighbors(current_features)

        # Analyze successful patterns from similar students
        scores = {subject: 0.0 for subject in self.subject_names}

        for idx, distance in zip(indices[0], distances[0]):
            similar_student = self.student_db.iloc[idx]
            weight = 1 / (1 + distance)  # Closer students have higher weight

            # If similar student improved in certain subjects, recommend those
            for subject in self.subject_names:
                subject_col = f"{subject.lower()}_score"
                if subject_col in similar_student:
                    score = similar_student[subject_col]
                    # High-performing similar students suggest good subjects to focus on
                    if score >= 80:
                        scores[subject] += weight * 0.3
                    elif score < 70:
                        # Similar students struggled here, might need extra focus
                        scores[subject] += weight * 0.5

        # Normalize scores
        max_score = max(scores.values()) if scores.values() else 1
        if max_score > 0:
            scores = {k: v / max_score for k, v in scores.items()}

        return scores

    def _create_feature_vector(self, profile: Dict) -> List[float]:
        
        features = []

        
        for subject in self.subject_names:
            score = profile['subject_scores'].get(subject, 0) / 100.0
            features.append(score)

        
        features.append(profile.get('study_hours_per_day', 4) / 24.0)

    
        learning_styles = ['Visual', 'Auditory', 'Reading/Writing', 'Kinesthetic', 'Mixed']
        style = profile.get('learning_style', 'Mixed')
        style_encoding = [1.0 if s == style else 0.0 for s in learning_styles]
        features.extend(style_encoding)

        return features

    def _generate_learning_path(self, profile: Dict, priority_scores: Dict, goal_weight: float) -> List[Dict]:
        
        path = []
        completed_modules = set()

        # Get top 3 priority subjects
        sorted_subjects = sorted(priority_scores.items(), key=lambda x: x[1], reverse=True)[:3]

        for subject, priority in sorted_subjects:
            subject_score = profile['subject_scores'].get(subject, 0)
            modules = self.learning_modules.get(subject, [])

            for module in modules:
                # Check prerequisites
                prereqs_met = all(prereq in completed_modules for prereq in module['prerequisites'])

                if not prereqs_met:
                    continue

                # Determine if module is appropriate for student's level
                if subject_score < 70 and module['difficulty'] == 'advanced':
                    continue  # Skip advanced modules for struggling students

                if subject_score >= 85 and module['difficulty'] == 'beginner':
                    completed_modules.add(module['name'])
                    continue  # Skip basics for strong students

                # Add module to path
                path.append({
                    'subject': subject,
                    'module': module['name'],
                    'difficulty': module['difficulty'],
                    'estimated_hours': module['estimated_hours'],
                    'priority_score': priority,
                    'reason': self._get_module_reason(subject, module, profile)
                })

                completed_modules.add(module['name'])

                # Limit path length
                if len(path) >= 8:
                    break

            if len(path) >= 8:
                break

        return path

    def _get_module_reason(self, subject: str, module: Dict, profile: Dict) -> str:
        
        score = profile['subject_scores'].get(subject, 0)

        if subject in profile.get('weak_subjects', []):
            return f"Identified as weak subject - focusing on {module['difficulty']} level"
        elif score < 70:
            return f"Current score ({score}%) suggests need for strengthening"
        elif score >= 85:
            return f"Strong foundation ({score}%) - ready for {module['difficulty']} concepts"
        else:
            return f"Building on current knowledge ({score}%)"

    def _rank_subjects(self, scores: Dict) -> List[Dict]:
        
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{'subject': subj, 'priority_score': score} for subj, score in ranked]

    def _create_daily_schedule(self, learning_path: List[Dict], profile: Dict) -> List[str]:
        """
        Create daily study schedule.

        Args:
            learning_path: Learning path modules
            profile: Student profile

        Returns:
            List of daily schedule items
        """
        daily_hours = profile.get('study_hours_per_day', 4)
        schedule = []

        if daily_hours >= 6:
            schedule.append(f"Morning (2 hrs): Focus on {learning_path[0]['subject']} - {learning_path[0]['module']}")
            schedule.append(f"Afternoon (2 hrs): {learning_path[1]['subject'] if len(learning_path) > 1 else 'Review'}")
            schedule.append(f"Evening (2 hrs): Practice problems and projects")
        elif daily_hours >= 4:
            schedule.append(f"Session 1 (2 hrs): {learning_path[0]['subject']} - {learning_path[0]['module']}")
            schedule.append(f"Session 2 (2 hrs): {learning_path[1]['subject'] if len(learning_path) > 1 else 'Review and practice'}")
        else:
            schedule.append(f"Study session ({daily_hours} hrs): Focus on {learning_path[0]['subject']}")
            schedule.append("Break sessions into 25-min focused blocks (Pomodoro technique)")

        return schedule

    def _create_weekly_plan(self, learning_path: List[Dict], profile: Dict) -> List[str]:
        """
        Create weekly study plan.

        Args:
            learning_path: Learning path modules
            profile: Student profile

        Returns:
            List of weekly plan items
        """
        plan = []

        if len(learning_path) >= 3:
            plan.append(f"Week 1-2: Master {learning_path[0]['module']} ({learning_path[0]['subject']})")
            plan.append(f"Week 3-4: Complete {learning_path[1]['module']} ({learning_path[1]['subject']})")
            plan.append(f"Week 5-6: Begin {learning_path[2]['module']} ({learning_path[2]['subject']})")
            plan.append("Week 7-8: Practice and project work, review weak areas")
        else:
            for i, module in enumerate(learning_path[:4]):
                weeks = (i * 2) + 1
                plan.append(f"Week {weeks}-{weeks+1}: {module['module']} ({module['subject']})")

        return plan

    def _estimate_completion_time(self, learning_path: List[Dict], profile: Dict) -> int:
        """
        Estimate weeks to complete learning path.

        Args:
            learning_path: Learning path modules
            profile: Student profile

        Returns:
            Estimated weeks
        """
        total_hours = sum(module['estimated_hours'] for module in learning_path)
        daily_hours = profile.get('study_hours_per_day', 4)
        weekly_hours = daily_hours * 5  # Assuming 5 study days per week

        weeks = int(np.ceil(total_hours / weekly_hours))
        return max(weeks, 4)  # Minimum 4 weeks
