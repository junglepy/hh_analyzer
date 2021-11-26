# -*- coding: utf-8 -*-
from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    request,
    render_template_string,
    redirect
)
from app import app
from app.models import *
import json
# import sys
import urllib


@app.route("/")
@app.route("/index")
@app.route("/proffs-list")
def proffs():
    proffs_list = ProffsList.query.all()
    proffs = Proffs.query.with_entities(Proffs.proff).order_by(Proffs.proff).all()
    proffs_list = proff_list_normalize(proffs_list)
    segment = get_segment(request)
    breadcrumb = 'Similarity of professions'

    return render_template(
        "proffs-list.html", segment=segment, proffs_list=proffs_list, proffs=proffs,
        breadcrumb=breadcrumb
    )


@app.route("/proffs-fully", methods=["GET"])
def proffs_fully():
    proff1 = urllib.parse.unquote(request.args.get("proff1"))  # from C%23 to C#
    proff2 = urllib.parse.unquote(request.args.get("proff2"))
    proffs = Proffs.query.with_entities(Proffs.proff).order_by(Proffs.proff).all()
    proffs = [proff[0] for proff in proffs]
    if proff1 in proffs and proff2 in proffs and proff1 != proff2:
        query = f"""WITH t1 AS
              (SELECT p1.proff proff1,
                      p2.proff proff2,
                      pl.similarity,
                      s.skill,
                      pl.skill_score,
                      pl.skill_pid1,
                      pl.skill_pid2
               FROM proff_link AS pl
               JOIN proffs p1 ON pl.proff1_id = p1.id
               JOIN proffs p2 ON pl.proff2_id = p2.id
               JOIN key_skills s ON pl.skill_id = s.id
               WHERE skill_score > 0.001)
            SELECT *
            FROM t1
            WHERE (proff1 = '{proff1}' AND proff2 = '{proff2}') OR (proff2 = '{proff1}' AND proff1 = '{proff2}')
            ORDER BY similarity DESC,
                     skill_score DESC"""
        proff_link = db.engine.execute(query).all()
        segment = get_segment(request)
        breadcrumb = 'Similarity of professions full statistics'
        return render_template(
            "proffs-fully.html", segment=segment, proff_link=proff_link,
            proffs=proffs, proff1=proff1, proff2=proff2, breadcrumb=breadcrumb,
        )
    # print(proff_link, file=sys.stderr)
    return redirect('/proffs-list', code=303)


@app.route("/proff/<proff>")
def proff(proff):
    proffs = Proffs.query.with_entities(Proffs.proff).all()
    proffs = [proff[0] for proff in proffs]
    if proff in proffs:
        query = f"""
            SELECT proffs.proff, key_skills.skill, frequ  FROM proff_stat
            JOIN proffs ON proff_stat.proff_id = proffs.id
            JOIN key_skills ON key_skills.id = proff_stat.skill_id
            WHERE frequ > 0.001 AND proffs.proff = '{proff}'
            ORDER BY proff_id, frequ DESC
            """
        proff_stat = db.engine.execute(query).all()
        segment = 'proff-stat'
        breadcrumb = 'Profession statistics'
        return render_template("proff.html", segment=segment, proff_stat=proff_stat, proff=proff, breadcrumb=breadcrumb)
    return redirect('/proffs-list', code=303)


@app.route("/prof-chooser")
def chooser():
    proffs_list = ProffsList.query.all()
    proffs = Proffs.query.with_entities(Proffs.proff).order_by(Proffs.proff).all()
    proffs_list = proff_list_normalize(proffs_list)
    segment = get_segment(request)
    breadcrumb = 'Professions chooser'
    return render_template("chooser.html", segment=segment, breadcrumb=breadcrumb)


@app.route("/search/", methods=["POST"])
def search():
    proffs = Proffs.query.with_entities(Proffs.proff).all()
    proffs = [el[0] for el in proffs]
    searchWord1 = request.form.get("search1", None)
    searchWord2 = request.form.get("search2", None)

    if searchWord1 in proffs and searchWord2 not in proffs:
        proffs_list = ProffsList.query.filter(
            (ProffsList.proff1 == searchWord1) | (ProffsList.proff2 == searchWord1)
        ).all()
        proffs_list = proff_list_normalize(proffs_list)
    elif searchWord2 in proffs and searchWord1 not in proffs:
        proffs_list = ProffsList.query.filter(
            (ProffsList.proff1 == searchWord2) | (ProffsList.proff2 == searchWord2)
        ).all()
        proffs_list = proff_list_normalize(proffs_list)
    elif searchWord1 in proffs and searchWord2 in proffs:
        proffs_list = ProffsList.query.filter(
            ((ProffsList.proff1 == searchWord1) & (ProffsList.proff2 == searchWord2))
            | ((ProffsList.proff1 == searchWord2) & (ProffsList.proff2 == searchWord1))
        ).all()
        proffs_list = proff_list_normalize(proffs_list)
    elif searchWord1 not in proffs and searchWord2 not in proffs:
        proffs_list = ProffsList.query.all()
        proffs_list = proff_list_normalize(proffs_list)
    return render_template("/includes/proffs-list.html", proffs_list=proffs_list)


def proff_list_normalize(proffs_list):
    for proff in proffs_list:
        proff.skills = json.loads(proff.skills)
        proff.proff1u = urllib.parse.quote(proff.proff1)
        proff.proff2u = urllib.parse.quote(proff.proff2)
    return proffs_list


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split("/")[-1]
        if segment == "":
            segment = "index"
        return segment
    except:
        return None