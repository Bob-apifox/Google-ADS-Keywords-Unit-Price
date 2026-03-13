@echo off
echo ========================================
echo Google Ads & Metabase 注册单价分析启动程序
echo ========================================
echo 正在执行数据拉取与报表生成...
echo.
py keyword_unit_price/scripts/generate_unit_price_report.py
echo.
echo ========================================
echo ✅ 报表生成完毕！
echo 请查看: keyword_unit_price/reports/final_registration_report.md
echo 历史存档: keyword_unit_price/archive/
echo ========================================
pause
