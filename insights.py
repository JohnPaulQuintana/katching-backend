from fastapi import APIRouter
from sqlalchemy.orm import Session
from collections import defaultdict
from datetime import datetime, timedelta

from database import SessionLocal
import models

router = APIRouter()

@router.get("/insights")
def get_insights():
    db: Session = SessionLocal()
    try:
        expenses = db.query(models.Expense).all()
        setting = db.query(models.Settings).filter_by(id=1).first()
        user_budget = setting.budget if setting else 10000

        if not expenses:
            return {
                "total_spent": 0,
                "top_category": {"name": "N/A", "amount": 0},
                "daily_avg": 0,
                "budget_left": user_budget,
                "warning": "",
                "suggestions": [],
                "upcoming_reminders": [],
                "ai_summary": "",
                "trend_analysis": ""
            }

        # Core values
        total_spent = sum(e.amount for e in expenses)
        unique_days = set(e.date for e in expenses)
        daily_avg = round(total_spent / max(1, len(unique_days)), 2)

        # Top category
        categories = defaultdict(float)
        for e in expenses:
            categories[e.category or "Uncategorized"] += e.amount
        top = max(categories.items(), key=lambda x: x[1]) if categories else ("None", 0)

        budget_left = round(user_budget - total_spent, 2)

        # Warnings
        warning = ""
        if budget_left < user_budget * 0.1:
            warning = "You're almost out of budget!"
        elif top[1] > total_spent * 0.3:
            warning = f"High spending on {top[0]}"

        # Suggestions
        suggestions = []
        if top[1] > total_spent * 0.3:
            suggestions.append(f"Limit spending on {top[0].lower()} to reduce costs.")
        if budget_left < user_budget * 0.2:
            suggestions.append("Review your spending to stay within your monthly budget.")
        if daily_avg > (user_budget / 30):
            suggestions.append("Your daily average is above budget. Spend less each day.")

        # Reminders
        today = datetime.now().date()
        all_reminders = [
            {"title": "Pay Water Bill", "due": "2025-06-20"},
            {"title": "Electricity Bill", "due": "2025-06-22"},
            {"title": "Internet Bill", "due": "2025-06-25"},
        ]
        upcoming_reminders = [
            r for r in all_reminders
            if today <= datetime.strptime(r["due"], "%Y-%m-%d").date() <= today + timedelta(days=5)
        ]

        # Summary
        if total_spent == 0:
            summary = "You haven't spent anything this month. Great start!"
        elif budget_left < 0:
            summary = f"⚠️ You've exceeded your budget. So far you've spent ₱{total_spent:.2f}, mostly on {top[0]} (₱{top[1]:.2f}). Budget left: ₱{budget_left:.2f}."
        elif budget_left < 0.2 * user_budget:
            summary = f"🔻 You're close to exceeding your budget. So far you've spent ₱{total_spent:.2f}, mostly on {top[0]} (₱{top[1]:.2f}). Budget left: ₱{budget_left:.2f}."
        else:
            summary = f"✅ You're managing your budget well. So far you've spent ₱{total_spent:.2f}, mostly on {top[0]} (₱{top[1]:.2f}). Budget left: ₱{budget_left:.2f}."

        # Weekly trend analysis (pure Python)
        weekly_totals = defaultdict(float)
        for e in expenses:
            week_start = e.date - timedelta(days=e.date.weekday())  # Monday
            weekly_totals[week_start] += e.amount

        sorted_weeks = sorted(weekly_totals.items())
        if len(sorted_weeks) >= 2:
            last = sorted_weeks[-1][1]
            prev = sorted_weeks[-2][1]
            if prev > 0:
                trend = (last - prev) / prev
            else:
                trend = 0
            if trend > 0.2:
                trend_note = "🔺 Your spending is increasing rapidly this week."
            elif trend < -0.2:
                trend_note = "🔻 You're spending much less this week. Good job!"
            else:
                trend_note = "➖ Your weekly spending is stable."
        else:
            trend_note = "Not enough data to predict trend."

        return {
            "total_spent": round(total_spent, 2),
            "top_category": {"name": top[0], "amount": round(top[1], 2)},
            "daily_avg": daily_avg,
            "budget_left": budget_left,
            "warning": warning,
            "suggestions": suggestions,
            "upcoming_reminders": upcoming_reminders,
            "ai_summary": summary,
            "trend_analysis": trend_note
        }

    finally:
        db.close()
