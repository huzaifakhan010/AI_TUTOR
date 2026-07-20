

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List


def load_data(file_path: str = 'data/student_profiles.csv') -> pd.DataFrame:
    
    try:
        df = pd.read_csv(file_path)

        # Validate required columns
        required_columns = [
            'student_id', 'name', 'education_level', 'semester', 'age',
            'math_score', 'physics_score', 'chemistry_score', 'programming_score',
            'english_score', 'learning_style', 'study_hours_per_day', 'goal',
            'weak_subjects', 'strong_subjects', 'interests'
        ]

        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at: {file_path}")
    except Exception as e:
        raise ValueError(f"Error loading CSV: {str(e)}")


def preprocess_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    
    df_processed = df.copy()

    # Convert weak_subjects and strong_subjects from string to list
    df_processed['weak_subjects_list'] = df_processed['weak_subjects'].apply(
        lambda x: [s.strip() for s in str(x).split(';')] if pd.notna(x) and str(x).lower() != 'none' else []
    )
    df_processed['strong_subjects_list'] = df_processed['strong_subjects'].apply(
        lambda x: [s.strip() for s in str(x).split(';')] if pd.notna(x) and str(x).lower() != 'none' else []
    )

    # Calculate average score across all subjects
    subject_columns = ['math_score', 'physics_score', 'chemistry_score',
                      'programming_score', 'english_score']
    df_processed['average_score'] = df_processed[subject_columns].mean(axis=1)

    # Calculate performance variance (consistency indicator)
    df_processed['score_variance'] = df_processed[subject_columns].var(axis=1)

    # Create subject performance dictionary for each student
    df_processed['subject_scores'] = df_processed.apply(
        lambda row: {
            'Math': row['math_score'],
            'Physics': row['physics_score'],
            'Chemistry': row['chemistry_score'],
            'Programming': row['programming_score'],
            'English': row['english_score']
        }, axis=1
    )

    # Normalize scores to 0-1 range for ML algorithms
    for col in subject_columns:
        df_processed[f'{col}_normalized'] = df_processed[col] / 100.0

    # Encode learning style as numeric
    learning_style_mapping = {
        'Visual': 0,
        'Auditory': 1,
        'Reading/Writing': 2,
        'Kinesthetic': 3,
        'Mixed': 4
    }
    df_processed['learning_style_encoded'] = df_processed['learning_style'].map(learning_style_mapping)

    # Create metadata
    metadata = {
        'total_students': len(df_processed),
        'avg_overall_score': df_processed['average_score'].mean(),
        'subject_columns': subject_columns,
        'learning_styles': list(learning_style_mapping.keys()),
        'education_levels': df_processed['education_level'].unique().tolist()
    }

    return df_processed, metadata


def validate_student_input(student_data: Dict) -> Tuple[bool, List[str]]:
    
    errors = []

    # Check required fields
    required_fields = ['name', 'age', 'education_level', 'semester', 'learning_style',
                       'study_hours_per_day', 'goal']
    for field in required_fields:
        if field not in student_data or not student_data[field]:
            errors.append(f"'{field}' is required")

    # Validate age
    if 'age' in student_data:
        try:
            age = int(student_data['age'])
            if age < 10 or age > 100:
                errors.append("Age must be between 10 and 100")
        except (ValueError, TypeError):
            errors.append("Age must be a valid number")

    # Validate semester
    if 'semester' in student_data:
        try:
            semester = int(student_data['semester'])
            if semester < 1 or semester > 12:
                errors.append("Semester must be between 1 and 12")
        except (ValueError, TypeError):
            errors.append("Semester must be a valid number")

    # Validate study hours
    if 'study_hours_per_day' in student_data:
        try:
            hours = float(student_data['study_hours_per_day'])
            if hours < 0.5 or hours > 24:
                errors.append("Study hours must be between 0.5 and 24")
        except (ValueError, TypeError):
            errors.append("Study hours must be a valid number")

    # Validate subject scores
    for subject in ['math_score', 'physics_score', 'chemistry_score',
                   'programming_score', 'english_score']:
        if subject in student_data:
            try:
                score = float(student_data[subject])
                if score < 0 or score > 100:
                    errors.append(f"{subject.replace('_', ' ').title()} must be between 0 and 100")
            except (ValueError, TypeError):
                errors.append(f"{subject.replace('_', ' ').title()} must be a valid number")

    return len(errors) == 0, errors


def create_student_profile(input_data: Dict) -> Dict:
    """
    Create a structured student profile from input data.

    Args:
        input_data: Raw input data from form

    Returns:
        Structured student profile dictionary
    """
    # Parse weak and strong subjects
    weak_subjects = []
    strong_subjects = []

    if 'weak_subjects' in input_data and input_data['weak_subjects']:
        weak_subjects = [s.strip() for s in str(input_data['weak_subjects']).split(',')]

    if 'strong_subjects' in input_data and input_data['strong_subjects']:
        strong_subjects = [s.strip() for s in str(input_data['strong_subjects']).split(',')]

    profile = {
        'name': input_data.get('name', ''),
        'age': int(input_data.get('age', 0)),
        'education_level': input_data.get('education_level', ''),
        'semester': int(input_data.get('semester', 0)),
        'learning_style': input_data.get('learning_style', ''),
        'study_hours_per_day': float(input_data.get('study_hours_per_day', 0)),
        'goal': input_data.get('goal', ''),
        'interests': input_data.get('interests', ''),
        'weak_subjects': weak_subjects,
        'strong_subjects': strong_subjects,
        'subject_scores': {
            'Math': float(input_data.get('math_score', 0)),
            'Physics': float(input_data.get('physics_score', 0)),
            'Chemistry': float(input_data.get('chemistry_score', 0)),
            'Programming': float(input_data.get('programming_score', 0)),
            'English': float(input_data.get('english_score', 0))
        }
    }

    # Calculate derived metrics
    scores = list(profile['subject_scores'].values())
    profile['average_score'] = np.mean(scores)
    profile['score_variance'] = np.var(scores)

    return profile
