from uuid import UUID

from sqlalchemy.orm import Session

from app.profile.models import Education, Experience, Profile
from app.profile.schemas import EducationIn, ExperienceIn, ProfileIn, ProfileOut


class ProfileService:
    def get_profile(self, db: Session, user_id: UUID) -> Profile | None:
        return db.query(Profile).filter(Profile.user_id == user_id).first()

    def upsert_profile(self, db: Session, user_id: UUID, profile_in: ProfileIn) -> ProfileOut:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()

        if profile is None:
            profile = Profile(
                user_id=user_id,
                career_goal=profile_in.career_goal.value,
                skills=profile_in.skills,
            )
            db.add(profile)
            db.flush()
        else:
            profile.career_goal = profile_in.career_goal.value
            profile.skills = profile_in.skills
            # Delete existing related records
            db.query(Experience).filter(Experience.profile_id == profile.id).delete()
            db.query(Education).filter(Education.profile_id == profile.id).delete()
            db.flush()

        # Insert new experiences
        for exp_in in profile_in.experiences:
            exp = Experience(
                profile_id=profile.id,
                role=exp_in.role,
                seniority=exp_in.seniority.value,
                company=exp_in.company,
                start_date=exp_in.start_date,
                end_date=exp_in.end_date,
            )
            db.add(exp)

        # Insert new educations
        for edu_in in profile_in.educations:
            edu = Education(
                profile_id=profile.id,
                institution=edu_in.institution,
                level=edu_in.level.value,
                title=edu_in.title,
                study_area=edu_in.study_area,
                start_date=edu_in.start_date,
                end_date=edu_in.end_date,
            )
            db.add(edu)

        db.commit()
        db.refresh(profile)

        return ProfileOut.model_validate(profile)

    def is_profile_complete(self, db: Session, user_id: UUID) -> bool:
        profile = db.query(Profile).filter(Profile.user_id == user_id).first()
        if profile is None:
            return False

        has_experience = (
            db.query(Experience).filter(Experience.profile_id == profile.id).count() >= 1
        )
        has_education = (
            db.query(Education).filter(Education.profile_id == profile.id).count() >= 1
        )
        has_skills = bool(profile.skills)
        has_career_goal = bool(profile.career_goal)

        return has_experience and has_education and has_skills and has_career_goal
