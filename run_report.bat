@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo ========================================
echo Google Ads ^& Metabase Registration Unit Price Analysis
echo ========================================
echo Generating data pull and reports...
echo.
py keyword_unit_price/scripts/generate_unit_price_report.py
echo.
echo Running High CPA Deep Optimization Analysis...
py keyword_unit_price/scripts/analyze_cpa.py
echo.
echo ========================================
echo [DONE] All analysis completed!
echo Basic Report: keyword_unit_price/reports/final_registration_report.md
echo Optimization: keyword_unit_price/reports/optimization_plan_*.md
echo History: keyword_unit_price/archive/
echo ========================================
pause
