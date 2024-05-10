import azure.functions as func
from os import environ
from sqlalchemy import create_engine, String, Column, Integer, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from domain.goal import Goal
from datetime import datetime
from datetime import timedelta
from domain.user import User
from domain.assessment import Assessment
import json
from datetime import date
from logging import getLogger

factory = sessionmaker(bind=create_engine(environ.get("DB_CONNECTION_STRING"), echo=True))
session = factory()

app = func.FunctionApp()

MOCK_USER_ID = 1


@app.route(route="goals", methods=["POST"], auth_level="anonymous")
def add_goal(req: func.HttpRequest) -> func.HttpResponse:
    getLogger().info(environ.get("DB_CONNECTION_STRING"))
    request_body = req.get_json()
    user_id = MOCK_USER_ID
    year = date.today().year
    month = date.today().month
    week = date.today().day // 7 + 1

    goal = Goal(user_id=user_id, description=request_body.get("description"), resolved=False,
                year=year, month=month, week=week, created_at=datetime.now(), updated_at=datetime.now())
    session.add(goal)
    session.commit()

    return func.HttpResponse(
        json.dumps(goal.as_dict(), default=str, ensure_ascii=False),
        status_code=200)


@app.route(route="goals", methods=["GET"], auth_level="anonymous")
def get_goals(req: func.HttpRequest) -> func.HttpResponse:
    weekly_offset = req.params.get("weekly_offset") or 0
    target_date = datetime.now() - timedelta(weeks=int(weekly_offset))
    target_month = target_date.month
    target_year = target_date.year
    target_week = target_date.day // 7 + 1

    goals = session.query(Goal).filter(
        Goal.year == target_year and Goal.month == target_month and Goal.week == target_week
    ).order_by(Goal.id.desc())

    return func.HttpResponse(
        json.dumps([goal.as_dict() for goal in goals], default=str, ensure_ascii=False),
        status_code=200)


@app.route(route="goals/stats", methods=["GET"], auth_level="anonymous")
def get_goals_stats(req: func.HttpRequest) -> func.HttpResponse:
    year = req.params.get("year")
    month = req.params.get("month")

    if year is None or month is None:
        return func.HttpResponse(
            "연도와 월을 입력해주세요.",
            status_code=400)

    goals = session.query(Goal).where(Goal.year == year).where(Goal.month == month).order_by(Goal.week.asc())

    assessments = session.query(Assessment).where(Assessment.year == year).where(Assessment.month == month).order_by(
        Assessment.week.asc())
    assessments = {assessment.week: assessment for assessment in assessments}

    result = []
    for goal in goals:
        assessment = assessments.get(goal.week)
        result_of_assessment = {
            "id": assessment.id,
            "content": assessment.content,
            "created_at": assessment.created_at,
            "updated_at": assessment.updated_at
        } if assessment is not None else None

        result.append({
            "week": goal.week,
            "goals": [
                {
                    "id": goal.id,
                    "description": goal.description,
                    "resolved": goal.resolved,
                    "created_at": goal.created_at,
                    "updated_at": goal.updated_at
                }
            ],
            "assessment": result_of_assessment
        })

    return func.HttpResponse(
        json.dumps(result, default=str, ensure_ascii=False),
        status_code=200
    )


@app.route(route="assessments", methods=["POST"], auth_level="anonymous")
def add_assessment(req: func.HttpRequest) -> func.HttpResponse:
    pass


@app.route(route="assessments", methods=["GET"], auth_level="anonymous")
def get_assessment(req: func.HttpRequest) -> func.HttpResponse:
    pass
