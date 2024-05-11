import azure.functions as func
from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.goal import Goal
from datetime import datetime
from datetime import timedelta
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
    user_id = get_user_id()
    year = current_datetime().year
    month = current_datetime().month
    week = week_of_this_month()

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
    target_date = current_datetime() - timedelta(weeks=int(weekly_offset))
    target_month = target_date.month
    target_year = target_date.year
    target_week = week_of_this_month(target_date)

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
            json.dumps({"message": "연도와 월을 입력해주세요."}),
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
    request_body = req.get_json()
    content = request_body.get("content")
    year = request_body.get("year")
    month = request_body.get("month")
    week = request_body.get("week")
    resolved_goal_ids = set(request_body.get("resolvedGoalIds"))

    if content is None or year is None or month is None or week is None or resolved_goal_ids is None:
        return func.HttpResponse(
            json.dumps({"message": "필드를 입력해주세요."}, default=str, ensure_ascii=False),
            status_code=400)

    user_id = get_user_id()

    already_wrote_assessment = (session.query(Assessment)
                                .where(Assessment.year == year)
                                .where(Assessment.month == month)
                                .where(Assessment.week == week).first()) is not None

    if already_wrote_assessment:
        return func.HttpResponse(
            json.dumps({"message": "이미 해당 주차의 평가를 작성했습니다."}, default=str, ensure_ascii=False),
            status_code=400)

    is_goal_not_exists = (session.query(Goal)
                          .where(Goal.year == year)
                          .where(Goal.month == month)
                          .where(Goal.week == week).first()) is None
    if is_goal_not_exists:
        return func.HttpResponse(
            json.dumps({"message": "해당하는 주차의 목표가 존재하지 않습니다."}, default=str, ensure_ascii=False),
            status_code=400)

    goals = session.query(Goal).where(Goal.id.in_(resolved_goal_ids)).all()
    if len(goals) != len(resolved_goal_ids):
        return func.HttpResponse(
            json.dumps({"message": "해당하는 목표가 존재하지 않습니다."}, default=str, ensure_ascii=False),
            status_code=400)

    session.query(Goal).where(Goal.id.in_(resolved_goal_ids)).update({"resolved": True})
    assessment = Assessment(user_id=user_id, year=year, month=month, week=week, content=content,
                            created_at=datetime.now(), updated_at=datetime.now())
    session.add(assessment)
    session.commit()

    return func.HttpResponse(
        json.dumps({
            "id": assessment.id,
            "year": assessment.year,
            "month": assessment.month,
            "week": assessment.week,
            "content": assessment.content,
            "created_at": assessment.created_at,
            "updated_at": assessment.updated_at
        }, default=str, ensure_ascii=False),
        status_code=201
    )


@app.route(route="assessment", methods=["GET"], auth_level="anonymous")
def get_assessment(req: func.HttpRequest) -> func.HttpResponse:
    week_offset = req.params.get("week_offset") or 0
    target_date = current_datetime() - timedelta(weeks=int(week_offset))

    assessment = (session.query(Assessment)
                  .where(Assessment.year == target_date.year)
                  .where(Assessment.month == target_date.month)
                  .where(Assessment.week == week_from_datetime(target_date))
                  .first())

    if assessment is None:
        return func.HttpResponse(
            json.dumps({"message": "해당하는 주차의 평가가 존재하지 않습니다."}, default=str, ensure_ascii=False),
            status_code=404)

    return func.HttpResponse(
        json.dumps({
            "id": assessment.id,
            "year": assessment.year,
            "month": assessment.month,
            "week": assessment.week,
            "content": assessment.content,
            "created_at": assessment.created_at,
            "updated_at": assessment.updated_at
        }, default=str, ensure_ascii=False),
        status_code=200
    )


def get_user_id():
    return MOCK_USER_ID


def current_datetime():
    return datetime.now()


def week_of_this_month():
    return week_from_datetime(current_datetime())


def week_from_datetime(ddate: date):
    return ddate.day // 7 + 1
